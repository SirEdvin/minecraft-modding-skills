#!/usr/bin/env python3
from collections import Counter
import json
from pathlib import Path
import re
import sys
import unicodedata
from urllib.parse import unquote

from jsonschema import Draft202012Validator, FormatChecker
import yaml


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
MARKDOWN_LINK = re.compile(r"!?\[[^\]\n]*\]\(\s*(<[^)\n]*>|[^)\n]*?)\s*\)")
BACKTICKED_LOCAL = re.compile(
    r"`((?:references|templates|scripts|assets)/[^`\s]+|"
    r"(?:(?:\.\.?/)?[^`/\s]+/)+[^`\s]+\.md)`"
)
URI_SCHEME = re.compile(r"^[a-z][a-z0-9+.-]*:", re.IGNORECASE)
CATALOG_ENTRY = re.compile(r"^- `([a-z0-9]+(?:-[a-z0-9]+)*)` — (.+)$")
SUPPORT_DIRECTORIES = ("references", "templates", "scripts")


class UniqueKeyLoader(yaml.SafeLoader):
    pass


def construct_unique_mapping(loader, node, deep=False):
    mapping = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        try:
            duplicate = key in mapping
        except TypeError as exc:
            raise yaml.constructor.ConstructorError(
                "while constructing a mapping",
                node.start_mark,
                "found an unhashable YAML key",
                key_node.start_mark,
            ) from exc
        if duplicate:
            raise yaml.constructor.ConstructorError(
                "while constructing a mapping",
                node.start_mark,
                f"duplicate YAML key {key!r}",
                key_node.start_mark,
            )
        mapping[key] = loader.construct_object(value_node, deep=deep)
    return mapping


UniqueKeyLoader.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, construct_unique_mapping
)


def read_text(path, errors):
    try:
        return path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        errors.append(f"{path}: cannot read UTF-8 text: {exc}")
        return None


def parse_frontmatter(path, text, errors):
    if not text.startswith("---\n"):
        errors.append(f"{path}: frontmatter must start at byte 0")
        return None
    match = re.search(r"\n---\s*\n", text[4:])
    if not match:
        errors.append(f"{path}: missing closing frontmatter")
        return None
    end = match.start() + 4
    try:
        frontmatter = yaml.load(text[4:end], Loader=UniqueKeyLoader)
    except yaml.YAMLError as exc:
        errors.append(f"{path}: invalid YAML: {exc}")
        return None
    if not isinstance(frontmatter, dict):
        errors.append(f"{path}: frontmatter is not a mapping")
        return None
    return frontmatter


def reference_targets(markdown_path, skill_root, text, errors):
    raw_targets = [match.group(1) for match in MARKDOWN_LINK.finditer(text)]
    raw_targets.extend(BACKTICKED_LOCAL.findall(text))
    targets = set()
    package = skill_root.resolve()
    for raw_target in raw_targets:
        target = raw_target.strip()
        if target.startswith("<") and target.endswith(">"):
            target = target[1:-1].strip()
        elif target:
            target = target.split(maxsplit=1)[0]
        if (
            not target
            or target.startswith(("#", "//"))
            or URI_SCHEME.match(target)
            or re.search(r"<[^>]+>", target)
        ):
            continue
        clean = unquote(target.split("#", 1)[0].split("?", 1)[0])
        if not clean:
            continue
        candidate = (markdown_path.parent / clean).resolve()
        try:
            candidate.relative_to(package)
        except ValueError:
            errors.append(
                f"{markdown_path}: local reference escapes skill package: {raw_target}"
            )
            continue
        if not candidate.exists():
            errors.append(f"{markdown_path}: missing local reference {raw_target}")
            continue
        targets.add(candidate)
    return targets


def validate_skill(skill, errors):
    path = skill / "SKILL.md"
    if not path.exists():
        errors.append(f"{skill}: missing SKILL.md")
        return
    text = read_text(path, errors)
    if text is None:
        return
    frontmatter = parse_frontmatter(path, text, errors)
    if frontmatter is None:
        return

    invalid_keys = [key for key in frontmatter if not isinstance(key, str)]
    if invalid_keys:
        errors.append(
            f"{path}: frontmatter keys must be strings: "
            + ", ".join(repr(key) for key in invalid_keys)
        )
        return

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
    if not isinstance(name, str) or len(name) > 64 or not SKILL_NAME.fullmatch(name):
        errors.append(f"{path}: invalid skill name {name!r}")
    if (
        not isinstance(description, str)
        or not description.strip()
        or "\n" in description
        or "\r" in description
        or len(description) > 60
        or not description.endswith(".")
    ):
        errors.append(
            f"{path}: description must be one line, at most 60 characters, and end with a period"
        )
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
        or not all(isinstance(key, str) and isinstance(value, str) for key, value in metadata.items())
    ):
        errors.append(f"{path}: metadata must map string keys to string values")
    if not isinstance(version, str) or not SEMVER.fullmatch(version):
        errors.append(f"{path}: metadata.version must be clean SemVer")
    if "allowed-tools" in frontmatter and not isinstance(frontmatter["allowed-tools"], str):
        errors.append(f"{path}: allowed-tools must be a space-separated string")
    if len(text) > 100_000:
        errors.append(f"{path}: SKILL.md too large ({len(text)})")

    graph = {}
    for markdown_path in sorted(skill.glob("**/*.md")):
        markdown = read_text(markdown_path, errors)
        if markdown is not None:
            graph[markdown_path.resolve()] = reference_targets(
                markdown_path, skill, markdown, errors
            )
    reachable = {path.resolve()}
    pending = [path.resolve()]
    package = skill.resolve()
    while pending:
        for target in graph.get(pending.pop(), set()):
            relative = target.relative_to(package)
            if relative.parts and relative.parts[0] in SUPPORT_DIRECTORIES and target not in reachable:
                reachable.add(target)
                pending.append(target)
    for directory in SUPPORT_DIRECTORIES:
        support_root = skill / directory
        if not support_root.exists():
            continue
        for support_file in sorted(
            path for path in support_root.rglob("*") if path.is_file()
        ):
            try:
                support_file.resolve().relative_to(skill.resolve())
            except ValueError:
                errors.append(f"{support_file}: support file escapes skill package")
                continue
            if support_file.resolve() not in reachable:
                errors.append(
                    f"{path}: support file is not reachable from SKILL.md: "
                    f"{support_file.relative_to(skill)}"
                )


def validate_manifest(root, skill_names, errors):
    manifest_path = root / "skills.sh.json"
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        errors.append(f"{manifest_path}: invalid JSON: {exc}")
        manifest = None

    schema_path = root / "schemas" / "skills.sh.schema.json"
    try:
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        errors.append(f"{schema_path}: invalid JSON schema: {exc}")
        schema = None

    if manifest is not None and schema is not None:
        validator = Draft202012Validator(schema, format_checker=FormatChecker())
        for error in sorted(
            validator.iter_errors(manifest), key=lambda item: tuple(map(str, item.path))
        ):
            location = ".".join(str(part) for part in error.path) or "<root>"
            errors.append(f"{manifest_path}: schema error at {location}: {error.message}")

    listed = []
    if isinstance(manifest, dict) and isinstance(manifest.get("groupings"), list):
        for grouping in manifest["groupings"]:
            if isinstance(grouping, dict) and isinstance(grouping.get("skills"), list):
                listed.extend(name for name in grouping["skills"] if isinstance(name, str))
    counts = Counter(listed)
    for name, count in sorted(counts.items()):
        if count > 1:
            errors.append(f"{manifest_path}: duplicate skill entry {name!r}")
    for name in sorted(set(listed) - set(skill_names)):
        errors.append(f"{manifest_path}: lists missing skill {name!r}")
    for name in sorted(set(skill_names) - set(listed)):
        errors.append(f"{manifest_path}: missing skill entry {name!r}")


def validate_readme(root, skill_names, errors):
    path = root / "README.md"
    text = read_text(path, errors)
    if text is None:
        return
    lines = text.splitlines()
    try:
        start = lines.index("## Skills") + 1
    except ValueError:
        errors.append(f"{path}: missing ## Skills catalog")
        return
    end = next(
        (
            index
            for index in range(start, len(lines))
            if lines[index].startswith("## ")
        ),
        len(lines),
    )
    listed = []
    for number, line in enumerate(lines[start:end], start + 1):
        if not line:
            continue
        match = CATALOG_ENTRY.fullmatch(line)
        if not match:
            errors.append(f"{path}:{number}: invalid Skills catalog entry")
            continue
        listed.append(match.group(1))
    counts = Counter(listed)
    for name, count in sorted(counts.items()):
        if count > 1:
            errors.append(f"{path}: README Skills catalog has duplicate entry {name!r}")
    for name in sorted(set(listed) - set(skill_names)):
        errors.append(f"{path}: README Skills catalog lists missing skill {name!r}")
    for name in sorted(set(skill_names) - set(listed)):
        errors.append(f"{path}: README Skills catalog missing entry {name!r}")


def validate_unicode(root, errors):
    paths = {
        path
        for name in ("README.md", "PROVENANCE.md", "CONTRIBUTING.md")
        if (path := root / name).is_file()
    }
    for directory in (root / "docs", root / "skills"):
        if directory.is_dir():
            paths.update(directory.rglob("*.md"))
    for path in sorted(paths):
        text = read_text(path, errors)
        if text is None:
            continue
        for line_number, line in enumerate(text.splitlines(), 1):
            for character in line:
                if unicodedata.category(character) == "Cf":
                    errors.append(
                        f"{path}:{line_number}: Unicode format control U+{ord(character):04X} is not allowed"
                    )


def validate_repository(root):
    root = Path(root)
    errors = []
    skills_dir = root / "skills"
    try:
        skills = sorted(
            skill
            for skill in skills_dir.iterdir()
            if skill.is_dir() and not skill.name.startswith((".", "_"))
        )
    except OSError as exc:
        errors.append(f"{skills_dir}: cannot list skills: {exc}")
        skills = []
    for skill in skills:
        validate_skill(skill, errors)
    skill_names = [skill.name for skill in skills]
    validate_manifest(root, skill_names, errors)
    validate_readme(root, skill_names, errors)
    validate_unicode(root, errors)
    return errors


def main(root=None):
    root = Path(root) if root is not None else Path(__file__).resolve().parents[1]
    errors = validate_repository(root)
    if errors:
        print("Skill validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print(
        "OK: skills, package-local references, README catalog, "
        "and skills.sh.json validated"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
