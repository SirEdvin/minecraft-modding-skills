#!/usr/bin/env python3
import json
from pathlib import Path
import re
import sys
import yaml

ROOT = Path(__file__).resolve().parents[1]
errors = []

SKILL_NAME = re.compile(r"^[a-z0-9][a-z0-9-]{0,63}$")
SEMVER = re.compile(r"^\d+\.\d+\.\d+(?:[-+][0-9A-Za-z.-]+)?$")
LOCAL_LINK = re.compile(r"\[[^\]]+\]\((?![a-z]+:|#)([^)]+)\)")
BACKTICKED_LOCAL = re.compile(r"`((?:\.\./)?(?:references|templates)/[^`]+)`")


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
    frontmatter = yaml.safe_load(text[4:end])
    if not isinstance(frontmatter, dict):
        errors.append(f"{path}: frontmatter is not a mapping")
        return text, None
    return text, frontmatter


def check_local_path(markdown_path, target):
    clean = target.split("#", 1)[0].strip()
    if not clean:
        return
    if clean.startswith("/"):
        candidate = ROOT / clean.lstrip("/")
    else:
        candidate = (markdown_path.parent / clean).resolve()
    try:
        candidate.relative_to(ROOT)
    except ValueError:
        errors.append(f"{markdown_path}: local link escapes repository: {target}")
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
    name = frontmatter.get("name")
    description = frontmatter.get("description")
    version = frontmatter.get("version")
    if name != skill.name:
        errors.append(f"{path}: name {name!r} must match directory {skill.name!r}")
    if not isinstance(name, str) or not SKILL_NAME.fullmatch(name):
        errors.append(f"{path}: invalid skill name {name!r}")
    if not isinstance(description, str) or not description.strip():
        errors.append(f"{path}: missing description")
    elif len(description) > 1024:
        errors.append(f"{path}: description too long ({len(description)})")
    if frontmatter.get("license") != "MIT":
        errors.append(f"{path}: license must be MIT")
    if not isinstance(version, str) or not SEMVER.fullmatch(version):
        errors.append(f"{path}: version must be clean SemVer")
    if len(text) > 100_000:
        errors.append(f"{path}: SKILL.md too large ({len(text)})")
    for target in LOCAL_LINK.findall(text):
        check_local_path(path, target)
    for target in BACKTICKED_LOCAL.findall(text):
        check_local_path(path, target)

for markdown_path in sorted((ROOT / "skills").glob("**/*.md")):
    text = markdown_path.read_text()
    for target in LOCAL_LINK.findall(text):
        check_local_path(markdown_path, target)

manifest_path = ROOT / "skills.sh.json"
try:
    manifest = json.loads(manifest_path.read_text())
except json.JSONDecodeError as exc:
    errors.append(f"{manifest_path}: invalid JSON: {exc}")
    manifest = None

if manifest is not None:
    listed = []
    for grouping in manifest.get("groupings", []):
        listed.extend(grouping.get("skills", []))
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
print("OK: skills, local references, and skills.sh.json validated")
