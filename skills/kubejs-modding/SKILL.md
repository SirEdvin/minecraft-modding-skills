---
name: kubejs-modding
description: Use when working on KubeJS, Rhino, ProbeJS, Minecraft pack scripts, startup/server/client script folders, recipes, tags, custom schemas, KubeJS logs and reload behavior, or boundaries between KubeJS scripts and compiled Java addons.
version: 1.0.0
author: SirEdvin
license: MIT
compatibility: Independently authored for KubeJS/Rhino/ProbeJS work, with Minecraft 1.20.1 focus; verify exact KubeJS, Rhino, ProbeJS, loader, and addon versions from the pack or mod repository before applying API details.
metadata:
  hermes:
    tags: [minecraft, kubejs, rhino, probejs, scripts, modpacks]
---

# KubeJS Modding

Use this specialist for KubeJS pack scripting and for Java mods that expose or consume KubeJS integration. KubeJS APIs are version-sensitive; check the installed mod versions and generated ProbeJS typings before writing scripts.

References:

- `references/kubejs-workflows.md`
- `../minecraft-modding/references/integration-surfaces.md`

## Workflow

1. Identify Minecraft, loader, KubeJS, Rhino, ProbeJS, and addon versions from `mods/`, manifests, Gradle files, or lockfiles. For this skill, assume `1.20.1` only after files prove it.
2. Read the active `kubejs/` tree: `startup_scripts`, `server_scripts`, `client_scripts`, config, generated typings, and logs.
3. Put registry and schema changes in startup scope, datapack/server logic in server scope, and screens/render/client-only hooks in client scope.
4. Prefer ProbeJS-generated types and official KubeJS docs over memory for event names and methods.
5. Keep Java addon boundaries explicit: compiled mods define events/types/integration surfaces; pack scripts consume them. Do not fake a Java API in script if the addon does not expose it.

## Common Work

- Recipes, removals, replacements, and custom recipe JSON/schema handling.
- Tags, loot, item/block registry data, startup registrations, and server reloadable data.
- Script reload/debug loops using KubeJS logs and in-game/server reload behavior.
- Rhino Java interop only where the installed KubeJS/Rhino version supports it.

## Validation

- Run the pack or dev server and inspect `kubejs/logs/` plus the normal Minecraft log.
- Use `/reload` only for reloadable server scripts/data; restart for startup scripts, registry changes, or Java addon changes.
- Regenerate ProbeJS typings when the pack uses ProbeJS and script APIs changed.
