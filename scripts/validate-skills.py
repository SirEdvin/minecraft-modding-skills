#!/usr/bin/env python3
from pathlib import Path
import re
import sys
import yaml

ROOT = Path(__file__).resolve().parents[1]
errors = []
for skill in sorted((ROOT / "skills").iterdir()):
    if not skill.is_dir() or skill.name.startswith((".", "_")):
        continue
    path = skill / "SKILL.md"
    if not path.exists():
        errors.append(f"{skill}: missing SKILL.md")
        continue
    text = path.read_text()
    if not text.startswith("---\n"):
        errors.append(f"{path}: frontmatter must start at byte 0")
        continue
    match = re.search(r"\n---\s*\n", text[4:])
    if not match:
        errors.append(f"{path}: missing closing frontmatter")
        continue
    end = match.start() + 4
    frontmatter = yaml.safe_load(text[4:end])
    if not isinstance(frontmatter, dict):
        errors.append(f"{path}: frontmatter is not a mapping")
        continue
    name = frontmatter.get("name")
    description = frontmatter.get("description")
    if name != skill.name:
        errors.append(f"{path}: name {name!r} must match directory {skill.name!r}")
    if not isinstance(description, str) or not description.strip():
        errors.append(f"{path}: missing description")
    elif len(description) > 1024:
        errors.append(f"{path}: description too long ({len(description)})")
    if len(text) > 100_000:
        errors.append(f"{path}: SKILL.md too large ({len(text)})")

if errors:
    print("Skill validation failed:")
    for error in errors:
        print(f"- {error}")
    sys.exit(1)
print("OK: skill frontmatter validated")
