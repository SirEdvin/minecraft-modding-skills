# Versioned GTCEu implementation notes

## Reviewed template: Forge 1.20.1, GTCEu 7.4.0

Template commit `19cc9032b50b378033f95e1e8e0de1ab4e3bf062` uses
`minecraft_version`, `gtceu_version`, and Legacy ModDevGradle. Its dependency is
`modImplementation("com.gregtechceu.gtceu:gtceu-${minecraft_version}:${gtceu_version}:slim")`
with transitive resolution disabled and explicitly declared LDLib, Registrate,
and Configuration dependencies. Copy the **whole matching dependency contract**,
not a bare `implementation` line; configuration names depend on the build plugin.
The template includes Lombok processors and Spotless, not universal addon mandates.

`ExampleMod.java` owns `GTRegistrate.create(MOD_ID)` and calls
`registerRegistrate()`. Its mod-bus listeners handle:

- `MaterialRegistryEvent`: create the addon namespace's material registry;
- `MaterialEvent`: initialize custom materials;
- `PostMaterialEvent`: modify existing materials;
- generic `GTCEuAPI.RegisterEvent` for recipe types, machines, and sounds.

`ExampleGTAddon.java` is annotated `@GTAddon`, implements `IGTAddon`, returns
its mod ID and registrate instance, and offers `addRecipes(Consumer<FinishedRecipe>)`.
Do not defer registry creation to common setup, which occurs after registration.

## Materials and generated forms

At GTCEu release `v7.4.0-1.20.1`, commit
`07ac5207f6f58ba3a2f9cd8b862b382d24300a17`:

- `Material.Builder(ResourceLocation)` and `buildAndRegister()` exist. Create
  definitions during material registration, not arbitrary eager class loading.
- `color(int)` takes RGB, not an invented `0xAARRGGBB` placeholder.
- Properties (`ingot`, `dust`, `gem`, fluid states, ore, blast/tool properties)
  and generation flags have different responsibilities. Read property checks and
  TagPrefix generation predicates before promising any generated form.
- Use a namespaced addon ID helper. Reference already-created component materials
  and order definitions by actual dependencies, not GTCEu's internal tier class names.
- Do not assume `GTItems.get(TagPrefix, Material)` exists; it is absent in the
  reviewed `GTItems.java`. Find the release's material/unification lookup API.

## Machines, multiblocks, and recipes

Read comparable implementations under `common/data` and the matching `api/machine`
and `api/recipe` packages. A conceptual factory is not a compilable registration
recipe. Verify constructors, registrate builder methods, renderer methods, and
return types before adapting code.

For a single block, choose the base by recipe processing, tier, energy storage,
and traits. Register its recipe type before binding the machine to it. For a
multiblock, check aisle orientation, controller position, shape completion,
minimum/maximum hatch counts, energy/item/fluid abilities, and maintenance or
muffler requirements. Do not use unrestricted `any()` where literal air is required.
Test forming, invalidating, rotating, unloading/reloading, and processing.

Recipe review checklist:

- stable addon-owned recipe ID and the exact type/serializer;
- max item/fluid input/output counts and custom capabilities;
- matching overloads for material forms, item stacks, tags, and fluid amounts;
- positive duration in ticks, intended EU/t, chance scale and tier boost;
- dimensions, cleanroom/research conditions only where supported;
- provider type and save method for the exact Minecraft line;
- generated JSON reload and actual processing, not recipe-viewer visibility alone.

`GTValues.V` is nominal voltage; `VA` is **voltage adjusted for cable loss**, not
voltage multiplied by amps. Use the appropriate tier budget deliberately; lower
recipe EU/t values are valid. `VN` and `VNF` supply plain/formatted tier names.

## KubeJS schema and major-version boundary

The 7.4.0 template documents `registerRecipeKeys(KJSRecipeKeyEvent)` on `IGTAddon`
for custom capability `ContentJS` input/output keys. Without these keys KubeJS may
remove recipes it cannot represent. Verify key component types and capability
mapping from the same GTCEu/KubeJS release. Built-in GTCEu scripting helpers and
startup registries are distinct from writing a compiled KubeJS plugin.

Do not combine that template with current branch-head lifecycle assumptions:
`IGTAddon.java` at `4c30877e75544603615ff8b1647d9beabe03122c` marks
`registerRecipeKeys` deprecated since 8.0.0 in favor of subscribing to the event
itself. It similarly deprecates several old registry hooks. This is evidence of
an API boundary, **not** permission to upgrade a 7.4.0 addon automatically.
