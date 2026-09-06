# KubeJS lifecycle, schema, and usage evidence

## Source baseline

The reviewed **2001 (Minecraft 1.20.1)** source commit is
[`ba142541dcc1d230383f4a55e38dd92ff10d1029`](https://github.com/KubeJS-Mods/KubeJS/tree/ba142541dcc1d230383f4a55e38dd92ff10d1029).
Read these files under `common/src/main/java/dev/latvian/mods/kubejs/`:

- `command/KubeJSCommands.java`: `reloadServer` calls the script manager then
  explicitly instructs the user to run `/reload` for datapack content;
  `reloadClient` distinguishes script loading from F3+T assets.
- `script/ScriptManager.java`: reload unloads the script type and then loads scripts.
- `script/ScriptType.java`: unload clears registered event handlers for that type.
- `bindings/JavaWrapper.java`: exposes `loadClass` and `tryLoadClass`, not `Java.type`.

Thus “script reload never replaces listeners” is false on this line. Re-registering
listeners still does not re-fire one-shot registry events or replay recipes/tags.
The safe pack workflow remains restart for registries, `/reload` for server data,
and the matching client script/resource lifecycle for client changes. Do not
extrapolate these implementation details to 2101 or 2601 without checking source.

## Recipe API boundaries

The [official recipe tutorial](https://kubejs.com/wiki/tutorials/recipes) explicitly
separates these syntax families:

| Target | Contract to check |
|---|---|
| 1.18.2 | `onEvent('recipes', ...)`, not modern `ServerEvents.recipes` |
| 1.19.2+ | `ServerEvents.recipes(...)`; exact helper overloads remain versioned |
| 1.19.2 and older smithing | output, base, addition |
| 1.20+ smithing | output, template, base, addition |
| 1.21.1 replace-input example | wrap replacement tags using `Ingredient.of(...)` |

For `event.custom`, inspect generated JSON or serializers in the **installed mod
release**, not the tutorial's 1.18.2 Farmer's Delight/Tinkers examples. Minecraft
recipe folders, item-stack data (NBT versus components), ingredients and result
objects changed across lines. Keep serializer `type`, units, IDs, and required
fields exact. ProbeJS helps discover bindings but cannot prove resource reload,
serializer acceptance, or actual machine processing; regenerate stale typings.

Tag conventions are version/loader specific: the main example is 1.20.1 Forge
`forge:ingots/iron`, not a promise that newer `c:ingots/iron` exists in that pack.
Resource IDs permit more than snake_case; snake_case is a naming convention,
not the complete registry ID grammar.

## Pack script versus compiled plugin

A pack's scripts normally live under the instance `kubejs/`; a Java plugin has a
Gradle build and loader metadata plus the matching KubeJS plugin registration
mechanism. Java source inspection or a successful Node parser does not exercise
Rhino or a plugin registration hook. Consult the pinned source's plugin API for
compiled addons; do not place Java addon code in `startup_scripts`.

## Representative project scope

Tracked-tree and tracked-content searches in
[TemplateProject at 042d296](https://github.com/SirEdvin/TemplateProject/tree/042d296e255d6a9e75e1d2f40da9937810e92004)
and [Minecraft-Modding-Libs at 86bfe0b](https://github.com/SirEdvin/Minecraft-Modding-Libs/tree/86bfe0b75d0dceb26e713a6c3bdcc91ec74eac2c)
found no tracked KubeJS pack scripts or integration references. The official 2001
implementation above and version-labelled wiki examples are the applicable
examples; neither Java project is claimed to validate KubeJS runtime behavior.
No Rhino/game runtime was launched during this audit.

Additional official navigation: [folder structure](https://kubejs.com/wiki/folder-structure),
[recipe tutorial](https://kubejs.com/wiki/tutorials/recipes).
