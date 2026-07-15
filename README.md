# Minecraft Modding Skills

Reusable agent skills for Minecraft Java mod development, modpack authoring, loader APIs, KubeJS, platform metadata, and GameTest automation.

## Skills

- `minecraft-modpack-authoring` — reproducible Packwiz packs, configuration, KubeJS integration, datapacks, quests, exports, and client/server validation.
- `kubejs-modding` — detailed KubeJS script lifecycle, recipes, registries, tags, integrations, and debugging.
- `fabric-modding` — Fabric mod development.
- `neoforge-modding` — current NeoForge mod development.
- `neoforge-legacy-modding` — legacy Forge/NeoForge version guidance.
- `gtceu-addon` — GTCEu addon development.
- `modrinth-api` — Modrinth API workflows.
- `testiarium-gametest` — cross-loader Testiarium GameTest development.

## Install

List all skills with skills.sh:

```bash
npx -y skills add SirEdvin/minecraft-modding-skills --list --full-depth
```

Install one skill with skills.sh:

```bash
npx -y skills add SirEdvin/minecraft-modding-skills \
  --skill minecraft-modpack-authoring --agent '*' --yes
```

Inspect or install with Hermes:

```bash
hermes skills inspect SirEdvin/minecraft-modding-skills/skills/minecraft-modpack-authoring
hermes skills install SirEdvin/minecraft-modding-skills/skills/minecraft-modpack-authoring
```

Multi-file skills should be installed from the repository path so their `references/` files remain available.

## Validate

```bash
python -m pip install -r requirements-dev.txt
python scripts/validate-skills.py
for d in skills/*; do uvx --from skills-ref==0.1.1 agentskills validate "$d"; done
npx -y skills@1.5.15 add . --list --full-depth
```

See `PROVENANCE.md` for source and attribution notes.
