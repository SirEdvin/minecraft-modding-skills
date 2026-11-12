# Minecraft Modding Skills

Reusable agent skills for Minecraft Java mods, loader APIs, version ports, native UI, addon development, GameTests, modpack authoring, and distribution metadata.

## Skills

- `fabric-modding` — Fabric source projects, loader entrypoints, mappings, networking, resources, and side safety.
- `gtceu-addon` — Java GTCEu addons; match the game, loader, and GTCEu release before using registry or recipe APIs.
- `kubejs-modding` — Version-matched script lifecycle, recipes, tags, registries, integrations, and debugging.
- `minecraft-26-1-migration` — Decision-gated migration from 1.21.x to 26.1.x, grounded in release primers and real ports.
- `minecraft-modpack-authoring` — Reproducible Packwiz packs, dependency/side classification, configuration, exports, and testing.
- `minecraft-native-ui` — Native Minecraft screens, widgets, menus, input, layout, and UI verification.
- `modrinth-api` — Modrinth discovery, version/file selection, hashes, dependencies, and API response handling.
- `neoforge-legacy-modding` — MinecraftForge-era projects using legacy tooling, including ModDevGradle's legacy Forge plugin; not modern NeoForge by name alone.
- `neoforge-modding` — Modern NeoForge source projects and version-specific loader APIs.
- `stonecutter-multiversion` — Multi-version source processing, flat and branched builds, switching, testing, and release hygiene.
- `testiarium-gametest` — Testiarium-backed Minecraft GameTests, fixture registration, server/client runs, and evidence checks.

## Use in a project

Start with the target project's checked-in build scripts, wrapper, metadata, source roots, and CI. Install only the packages needed for the task; selecting a skill does not authorize porting, changing the loader, installing dependencies, or publishing artifacts.

- Ordinary mod change: choose the loader skill for the exact target; add native UI or Testiarium only when those features are involved.
- Shared-source multi-version change: combine the applicable loader skill(s) with Stonecutter; discover exact node paths instead of assuming flat root tasks.
- Version port: add the migration skill only for its documented source/target range.
- Java GTCEu addon: use GTCEu plus the matching loader skill. KubeJS is not a replacement for Java addon registration.
- Pack scripting or dependency discovery: use KubeJS, modpack authoring, or Modrinth as needed; do not load all three for every Java source edit.

See [project usage](docs/project-usage.md) for a task-to-skill matrix, a reusable project brief, and pinned flat/multi-module examples. See [audit results](docs/skill-audit.md) for coverage, validation evidence, and explicit limits of the repository-wide audit.

## Install

List packages without installing:

```bash
npx -y skills@1.5.15 add SirEdvin/minecraft-modding-skills --list --full-depth
```

Install one package with skills.sh (select an agent/scope deliberately):

```bash
npx -y skills@1.5.15 add SirEdvin/minecraft-modding-skills \
  --skill stonecutter-multiversion --agent '*' --yes
```

`--agent '*'` selects all supported agent targets; it is not required for normal use. Consult the CLI's help to choose a narrower target. Installation changes the agent's skill files; listing does not.

Inspect or install one package with Hermes:

```bash
hermes skills inspect SirEdvin/minecraft-modding-skills/skills/stonecutter-multiversion
hermes skills install SirEdvin/minecraft-modding-skills/skills/stonecutter-multiversion
```

Optional Hermes tap discovery:

```bash
hermes skills tap add SirEdvin/minecraft-modding-skills
hermes skills search stonecutter
```

Install multi-file skills from the repository path, not a raw `SKILL.md` URL, so `references/`, `templates/`, and `scripts/` are included. Packages can be installed individually: companion skills named in prose are optional task-specific guidance, not filesystem dependencies. Do not assume repository-level `docs/` is copied into an individual skill installation.

In Hermes, use `skill_view` to load the selected skill and its referenced files on demand. In other agents, use their skill loader or file-reading tools; the Gradle/API contracts do not require Hermes.

## Validate

Run from the repository root through the agent's terminal tool. Python 3.12 and `uv` avoid modifying system Python; Node/npm are needed for the discovery check.

```bash
uv run --with-requirements requirements-dev.txt python -m unittest discover -s scripts -p 'test_*.py'
uv run --with-requirements requirements-dev.txt python scripts/validate-skills.py
for d in skills/*; do uvx --from skills-ref==0.1.1 agentskills validate "$d"; done
npx -y skills@1.5.15 add . --list --full-depth
git diff --check
```

The shell loop shown is POSIX; on other shells invoke `agentskills validate` once per package. The validator and unit tests are portable Python. CI runs the same validation layers.

Repository policy is deliberately stricter than the Agent Skills specification: descriptions must be single-line, at most 60 characters, and end in a period for compact discovery. Metadata must use the specification's string-to-string map; portable author/version/tag fields belong there. Package validation proves structure and discovery, not that every documented Minecraft version or runtime was exercised.

See `PROVENANCE.md` for source and attribution notes, [contribution guidance](CONTRIBUTING.md) for package maintenance, and the [all-package audit](docs/skill-audit.md) for findings, evidence, and verification limits.
