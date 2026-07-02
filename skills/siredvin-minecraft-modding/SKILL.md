---
name: siredvin-minecraft-modding
description: Use when working on SirEdvin Minecraft modding repositories, including Turtlematic, DigitalItems, Minecraft-Modding-Libs, UnlimitedPeripheralWorks, GregTech True Age of Steam, CloudSolutions, SmartHome-Appliances, and modding-buildenv. Adds local paths, buildenv conventions, private Maven coordinates, branch/version inventory, and repository-specific validation guidance on top of the generic minecraft-modding skill.
version: 1.0.0
author: SirEdvin
license: MIT
compatibility: Intended for SirEdvin's local development environment and repositories under /home/siredvin/projects; load after the generic minecraft-modding skill.
metadata:
  hermes:
    tags: [minecraft, siredvin, modding-buildenv, cc-tweaked, neoforge, forge, fabric]
---

# SirEdvin Minecraft Modding Overlay

## Overview

Load this skill after `minecraft-modding` when working on SirEdvin Minecraft repositories. The generic skill carries reusable Fabric/Forge/NeoForge practice; this overlay carries local repository paths, observed branches, build plugin conventions, Maven coordinates, and SirEdvin-specific pitfalls.

Supporting references:

- `references/siredvin-repository-map.md` — local repo inventory and current versions.
- `references/modding-buildenv-conventions.md` — custom Gradle convention plugins and migration traps.
- `references/neoforge-121-merge-porting.md` — preserving 1.20 branch history while porting into 1.21/NeoForge.

## When to Use

- The task touches any repository under `/home/siredvin/projects` related to SirEdvin Minecraft mods.
- The user mentions Turtlematic, DigitalItems, Minecraft-Modding-Libs, UnlimitedPeripheralWorks, GregTech True Age of Steam, CloudSolutions, SmartHome-Appliances, modding-buildenv, Broccolium, Tweakium, Peripheralium, CC:Tweaked peripherals, or SirEdvin Maven.
- A change involves custom Gradle plugins under `site.siredvin.*`, `modding-buildenv`, `baseShaking`, `fabricShaking`, `forgeShaking`, `neoforgeShaking`, `publishingShaking`, or `modPublishing`.
- Work may affect Forge 1.20.1, NeoForge 1.21.1, Java 17/21/25 requirements, private Maven publishing, or GitHub Actions publishing.

## Local Repository Roots

Primary source root:

```text
/home/siredvin/projects/
```

Known repositories:

- `/home/siredvin/projects/Turtlematic`
- `/home/siredvin/projects/DigitalItems`
- `/home/siredvin/projects/Minecraft-Modding-Libs`
- `/home/siredvin/projects/UnlimitedPeripheralWorks`
- `/home/siredvin/projects/GregTech-True-Age-of-Steam`
- `/home/siredvin/projects/CloudSolutions`
- `/home/siredvin/projects/SmartHome-Appliances`
- `/home/siredvin/projects/modding-buildenv`

Use `git status --short --branch` before assuming branch state; several repos have active version branches rather than `main`.

## SirEdvin Build Patterns

Multi-loader app repos commonly use:

- `settings.gradle.kts` with `include(":core")`, `include(":forge")`, `include(":fabric")`, and `project.projectDir = file("projects/${project.name}")`.
- `projects/core` for common code.
- `projects/fabric` for Fabric-specific resources and entrypoints.
- `projects/forge` for Forge or NeoForge-specific code depending on branch/version.

Minecraft-Modding-Libs uses module names such as:

- `broccolium-core`, `broccolium-fabric`, `broccolium-forge`
- `tweakium-core`, `tweakium-fabric`, `tweakium-forge`
- `peripheralium-core`, `peripheralium-fabric`, `peripheralium-forge`

Custom buildenv plugins/conventions seen in repos include:

- `site.siredvin.root`
- `site.siredvin.release`
- `site.siredvin.vanilla`
- `site.siredvin.fabric`
- `site.siredvin.forge`
- `site.siredvin.neoforge`
- `site.siredvin.publishing`
- `site.siredvin.mod-publishing`

Keep `baseShaking`, `vanillaShaking`, `fabricShaking`, `forgeShaking`, `neoforgeShaking`, `publishingShaking`, and `modPublishing` structure intact unless the task is explicitly build-plugin maintenance.

## Repository and Version Inventory

Observed local inventory during skill refresh:

- Turtlematic: branch `1.20`, Minecraft `1.20.1`, Forge/Fabric, buildenv `0.8.18`, CC:Tweaked `1.116.1`.
- DigitalItems: branch `1.20`, Minecraft `1.20.1`, Forge/Fabric, buildenv `0.8.18`, CC:Tweaked `1.113.0`.
- UnlimitedPeripheralWorks: branch `1.20`, Minecraft `1.20.1`, Forge/Fabric, buildenv `0.8.26`, many optional integration mods, CC:Tweaked `1.116.1`.
- CloudSolutions: branch `1.20`, Minecraft `1.20.1`, Forge/Fabric, buildenv `0.8.18`, Forge `47.4.10`.
- Minecraft-Modding-Libs: active local branch `feat/merge-1.20-into-1.21`, Minecraft `1.21.1`, buildenv `0.9.0`, Fabric and NeoForge-style modules, plugin resolution maps `site.siredvin.*` to `site.siredvin:modding-buildenv:${requested.version}`.
- SmartHome-Appliances: branch `1.21`, Minecraft `1.21.1`, Fabric active, Forge module commented in settings, buildenv `0.8.14`.
- GregTech True Age of Steam: branch `buildenv-migration`, Minecraft/Forge `1.20.1` / `47.4.10`, buildenv `0.9.0`, single-loader Forge/GregTech project with Java 17 guidance in its AGENTS.md.
- modding-buildenv: branch `main`, projectVersion `0.9.0`, publishes custom convention plugins and includes NeoForge ModDevGradle plugin dependency.

This inventory is a starting point only. Always re-read files before changing code.

## Maven and Repository Conventions

Known Maven endpoints and repositories:

- SirEdvin Maven: `https://mvn.siredvin.site/minecraft`
- JEI Maven: `https://maven.blamejared.com/`
- ModMenu/Terraformers Maven: `https://maven.terraformersmc.com/releases`
- Kotlin for Forge Maven: `https://thedarkcolour.github.io/KotlinForForge/`
- GTCEu Maven: `https://maven.gtceu.com`

For clean CI resolution of custom buildenv plugins, do not trust local Gradle caches alone. If plugin markers fail on GitHub runners, map `site.siredvin.*` plugin IDs to `site.siredvin:modding-buildenv:${requested.version}` in `pluginManagement.resolutionStrategy` and verify with:

```bash
./gradlew --no-daemon --refresh-dependencies help
```

For NeoForge support, repository filters should include `net.neoforged` and `net.neoforged.moddev` where ModDevGradle/plugin markers are resolved.

## Validation Preferences

Use Gradle wrapper commands from the affected repo root. The user prefers Gradle with `--no-daemon`.

Canonical checks:

```bash
./gradlew build --no-daemon
```

For dependency/plugin resolution changes:

```bash
./gradlew --no-daemon --refresh-dependencies help
```

For modding-buildenv convention work:

```bash
./gradlew --no-daemon check
./gradlew --no-daemon publishToMavenLocal
```

For GregTech True Age of Steam, follow the repo AGENTS.md: `./gradlew build`, `spotlessCheck`, `spotlessApply`, `runClient`, `runServer`, and `runData` are the relevant commands; prefer adding `--no-daemon` for this user.

## Pitfalls

1. **Do not treat every `forge` module as legacy Forge.** MML's 1.21 work uses NeoForge-style forge modules and `META-INF/neoforge.mods.toml`; older 1.20 repos use Forge 47.x and `mods.toml`.
2. **Do not flatten buildenv convention blocks.** The shaking blocks encode publishing, loader, mappings, and generated metadata behavior.
3. **Preserve dependency mappings.** `extraVersionMappings` / `extraRawVersionMappings` may map project names to distribution slugs such as `computercraft` -> `cc-tweaked`.
4. **Check JDK before blaming Gradle.** Minecraft 1.21.1 work may require JDK 21+; older Forge 1.20.1 projects commonly use Java 17. Newer NeoForge 26.x docs may recommend newer JDKs.
5. **Metadata placeholders are build-expanded.** Preserve placeholders such as `${version}`, `${file.jarVersion}`, `${computercraftVersion}`, `${forgeVersion}`, `${neoforge_version}`, `broccoliumVersion`, and `tweakiumVersion`.
6. **Fabric test classloaders can expose Kotlin test service-loader issues.** For shared JUnit 5 fixtures, prefer direct `org.junit.jupiter.api.Assertions` imports when assertion service loading fails.
7. **Do not manually publish or deploy without explicit request.** Build/publish workflows may touch private Maven or GitHub Actions releases.

## Verification Checklist

- [ ] Loaded generic `minecraft-modding` first, then this overlay.
- [ ] Re-read the target repo's branch, `gradle.properties`, `settings.gradle.kts`, build files, and metadata.
- [ ] Confirmed whether `forge` means Forge 1.20.1, NeoForge 1.21.1, or migration state.
- [ ] Preserved custom `site.siredvin.*` buildenv conventions and dependency scope buckets.
- [ ] Used `--no-daemon` Gradle commands unless the repo's tooling forbids it.
- [ ] Reported exact validation output or a precise environment blocker.
