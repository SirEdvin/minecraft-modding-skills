---
name: gtceu-addon
description: Develop version-pinned GregTech CEu Modern addons.
license: MIT
metadata:
  author: "SirEdvin"
  version: "1.1.0"
---

# GregTech CEu Modern Addons

Use for compiled GTCEu addons, not ordinary pack recipes. For pack-only changes,
use KubeJS or datapack APIs supported by the installed GTCEu version instead of
introducing a Java addon unnecessarily.

## Establish the target

- Read Minecraft, loader, Java, GTCEu, build plugin, LDLib, and Registrate versions.
- Inspect the matching official addon template and GTCEu release source. A branch
  named `1.20.1` can span incompatible GTCEu majors; it is not an API version pin.
- The audited template targets **Minecraft 1.20.1 / Forge / GTCEu 7.4.0 / Java 17**.
  It is not evidence for a NeoForge 1.21.1+ recipe or registration API.
- Check the worktree and existing architecture before changing dependencies.
  Do not impose template property names or a new build plugin on an existing mod.

## Implement at the correct lifecycle

1. Use an addon-owned namespace and `GTRegistrate`; never put new addon materials
   under `GTCEu.id(...)` unless deliberately modifying GTCEu-owned content.
2. In the reviewed 7.4.0 template, the `@Mod` entrypoint wires material registry,
   material creation/modification, recipe-type and machine events to the mod bus.
   The separate `@GTAddon` implementation supplies `IGTAddon` hooks.
3. Create the addon's material registry before material definitions. Match form
   flags and property requirements to the release; `.ingot()` is not a promise
   to generate every plate, rod, bolt, and screw.
4. Choose machine base classes and registration builders from a comparable
   upstream implementation at the target commit. Do not invent convenience
   methods on `GTRegistries` from a conceptual example.
5. Wire recipes through the matching provider/addon hook; preserve explicit IDs,
   capability input/output limits, EU/t, duration, and conditions.
6. For KubeJS interoperability, verify recipe capabilities and their schema keys.
   A UI setter or a registry lookup does not register a KubeJS recipe schema.

Read [versioned implementation notes](references/gtceu-development.md) before
writing material, machine, multiblock, recipe, or KubeJS integration code.
[Sources and scope](references/gtceu-links.md) identify the reviewed commits.

## Verification and escape hatches

- Discover Gradle tasks before running them. The reviewed template declares
  client, server, data runs and Spotless; it does not declare a GameTest run.
- Compile, inspect generated recipes/tags, then test client and dedicated server
  with the exact dependency set when execution is authorized. A source audit
  alone is not a compilation or gameplay test.
- Keep client-only classes out of dedicated-server execution paths. Client
  renderers may legitimately access client world state; authoritative machine
  simulation and mutations belong on the server.
- Prefer public events, subclasses, traits, and recipe modifiers. Before mixins
  or access transformers, present the exact target, unavailable alternatives,
  smallest change, and update risk for approval. Reflection is not inherently
  safer than a narrow supported access mechanism. Avoid broad overwrites.
