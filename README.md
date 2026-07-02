# Minecraft Modding Skills

Reusable [Agent Skills](https://agentskills.io/specification) for Minecraft Java mod development.

This repository is designed to be installable by Hermes Agent, skills.sh-compatible tooling, and other agents that understand `SKILL.md` directories.

## Skills

| Skill | Purpose |
| --- | --- |
| `minecraft-modding` | Global, public Minecraft modding workflow for Fabric, Forge, NeoForge, Gradle, mappings, mixins, datagen, networking, and common integrations. |
| `siredvin-minecraft-modding` | SirEdvin-specific overlay for local repositories, modding-buildenv, Minecraft-Modding-Libs, CC:Tweaked/peripheral projects, and private Maven/build conventions. |

## Install with Hermes

Install one skill directly:

```bash
hermes skills install SirEdvin/minecraft-modding-skills/skills/minecraft-modding
hermes skills install SirEdvin/minecraft-modding-skills/skills/siredvin-minecraft-modding
```

Or add the repository as a tap:

```bash
hermes skills tap add SirEdvin/minecraft-modding-skills
hermes skills search minecraft
hermes skills install SirEdvin/minecraft-modding-skills/minecraft-modding
hermes skills install SirEdvin/minecraft-modding-skills/siredvin-minecraft-modding
```

## Install with skills.sh-compatible tooling

```bash
npx skills add SirEdvin/minecraft-modding-skills
```

## Recommended usage

For general Minecraft modding work, load only `minecraft-modding`.

For SirEdvin repositories, load both:

```text
/minecraft-modding
/siredvin-minecraft-modding
```

The global skill intentionally avoids local filesystem paths and private repository assumptions. The SirEdvin overlay carries those local conventions so the public skill stays reusable.
