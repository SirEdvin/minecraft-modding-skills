#!/usr/bin/env python3
import json
from pathlib import Path
import re
import sys

from jsonschema import Draft202012Validator, FormatChecker
import yaml

ROOT = Path(__file__).resolve().parents[1]
errors = []

ALLOWED_FIELDS = {
    "name",
    "description",
    "license",
    "compatibility",
    "metadata",
    "allowed-tools",
}
SKILL_NAME = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
SEMVER_IDENTIFIER = r"(?:0|[1-9]\d*|\d*[A-Za-z-][0-9A-Za-z-]*)"
SEMVER = re.compile(
    rf"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)"
    rf"(?:-{SEMVER_IDENTIFIER}(?:\.{SEMVER_IDENTIFIER})*)?"
    r"(?:\+[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?$"
)
LOCAL_LINK = re.compile(r"\[[^\]]+\]\((?![a-z]+:|#)([^)]+)\)", re.IGNORECASE)
BACKTICKED_LOCAL = re.compile(
    r"`((?:(?:\.\.?/)?[^`\s]+/)+[^`\s]+\.md|(?:references|templates|scripts|assets)/[^`\s]+)`"
)


def parse_frontmatter(path):
    text = path.read_text()
    if not text.startswith("---\n"):
        errors.append(f"{path}: frontmatter must start at byte 0")
        return text, None
    match = re.search(r"\n---\s*\n", text[4:])
    if not match:
        errors.append(f"{path}: missing closing frontmatter")
        return text, None
    end = match.start() + 4
    try:
        frontmatter = yaml.safe_load(text[4:end])
    except yaml.YAMLError as exc:
        errors.append(f"{path}: invalid YAML: {exc}")
        return text, None
    if not isinstance(frontmatter, dict):
        errors.append(f"{path}: frontmatter is not a mapping")
        return text, None
    return text, frontmatter


def check_local_path(markdown_path, skill_root, target):
    clean = target.split("#", 1)[0].split("?", 1)[0].strip()
    if not clean:
        return
    candidate = (markdown_path.parent / clean).resolve()
    try:
        candidate.relative_to(skill_root.resolve())
    except ValueError:
        errors.append(f"{markdown_path}: local reference escapes skill package: {target}")
        return
    if not candidate.exists():
        errors.append(f"{markdown_path}: missing local reference {target}")


skills_dir = ROOT / "skills"
skill_names = []

for skill in sorted(skills_dir.iterdir()):
    if not skill.is_dir() or skill.name.startswith((".", "_")):
        continue
    skill_names.append(skill.name)
    path = skill / "SKILL.md"
    if not path.exists():
        errors.append(f"{skill}: missing SKILL.md")
        continue
    text, frontmatter = parse_frontmatter(path)
    if frontmatter is None:
        continue
    unknown_fields = sorted(set(frontmatter) - ALLOWED_FIELDS)
    if unknown_fields:
        errors.append(f"{path}: unsupported frontmatter fields: {', '.join(unknown_fields)}")
    name = frontmatter.get("name")
    description = frontmatter.get("description")
    compatibility = frontmatter.get("compatibility")
    metadata = frontmatter.get("metadata")
    version = metadata.get("version") if isinstance(metadata, dict) else None
    if name != skill.name:
        errors.append(f"{path}: name {name!r} must match directory {skill.name!r}")
    if (
        not isinstance(name, str)
        or len(name) > 64
        or not SKILL_NAME.fullmatch(name)
    ):
        errors.append(f"{path}: invalid skill name {name!r}")
    if not isinstance(description, str) or not description.strip():
        errors.append(f"{path}: missing description")
    elif len(description) > 1024:
        errors.append(f"{path}: description too long ({len(description)})")
    if frontmatter.get("license") != "MIT":
        errors.append(f"{path}: license must be MIT")
    if "compatibility" in frontmatter and (
        not isinstance(compatibility, str)
        or not compatibility.strip()
        or len(compatibility) > 500
    ):
        errors.append(f"{path}: compatibility must contain 1..500 characters")
    if metadata is not None and (
        not isinstance(metadata, dict)
        or any(not isinstance(key, str) or not isinstance(value, str) for key, value in metadata.items())
    ):
        errors.append(f"{path}: metadata must map strings to strings")
    if not isinstance(version, str) or not SEMVER.fullmatch(version):
        errors.append(f"{path}: metadata.version must be clean SemVer")
    if "allowed-tools" in frontmatter and not isinstance(frontmatter["allowed-tools"], str):
        errors.append(f"{path}: allowed-tools must be a space-separated string")
    if len(text) > 100_000:
        errors.append(f"{path}: SKILL.md too large ({len(text)})")

    for markdown_path in sorted(skill.glob("**/*.md")):
        markdown = markdown_path.read_text()
        for target in LOCAL_LINK.findall(markdown):
            check_local_path(markdown_path, skill, target)
        for target in BACKTICKED_LOCAL.findall(markdown):
            check_local_path(markdown_path, skill, target)

manifest_path = ROOT / "skills.sh.json"
try:
    manifest = json.loads(manifest_path.read_text())
except (OSError, json.JSONDecodeError) as exc:
    errors.append(f"{manifest_path}: invalid JSON: {exc}")
    manifest = None

schema_path = ROOT / "schemas" / "skills.sh.schema.json"
try:
    schema = json.loads(schema_path.read_text())
except (OSError, json.JSONDecodeError) as exc:
    errors.append(f"{schema_path}: invalid JSON schema: {exc}")
    schema = None

if manifest is not None and schema is not None:
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    for error in sorted(validator.iter_errors(manifest), key=lambda item: tuple(map(str, item.path))):
        location = ".".join(str(part) for part in error.path) or "<root>"
        errors.append(f"{manifest_path}: schema error at {location}: {error.message}")

if isinstance(manifest, dict) and isinstance(manifest.get("groupings"), list):
    listed = []
    for grouping in manifest["groupings"]:
        if isinstance(grouping, dict) and isinstance(grouping.get("skills"), list):
            listed.extend(name for name in grouping["skills"] if isinstance(name, str))
    for name in listed:
        if name not in skill_names:
            errors.append(f"{manifest_path}: lists missing skill {name!r}")
    for name in skill_names:
        if name not in listed:
            errors.append(f"{manifest_path}: missing skill entry {name!r}")

if errors:
    print("Skill validation failed:")
    for error in errors:
        print(f"- {error}")
    sys.exit(1)
print("OK: skills, package-local references, and schema-valid skills.sh.json validated")
