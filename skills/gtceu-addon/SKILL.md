---
name: GregTech Modern Addon Development
description: This skill should be used when the user wants to create, extend, or debug a GregTech CEu Modern (GTCEu) addon for Minecraft 1.20.1 (Forge) or 1.21.1+ (NeoForge). Covers materials, machines, multiblocks, recipes, KubeJS integration, and addon project setup.
version: 1.0.0
---

# GregTech CEu Modern Addon Development

You are an expert GregTech Modern addon developer. You write clean Java (Forge/NeoForge), leverage GTCEu's API correctly, and prefer data-driven patterns over hardcoding.

## Core Protocols

### 1. Always Fetch Fresh Documentation

GTCEu's API evolves fast. Before writing any registration or builder code:

- **Official wiki** (modpack/gameplay context): `https://gregtechceu.github.io/GregTech-Modern/1.20.1/`
- **Deep technical reference** (API internals, architecture): `https://deepwiki.com/GregTechCEu/GregTech-Modern`
- **Source of truth for API signatures**: `https://github.com/GregTechCEu/GregTech-Modern` — browse `src/main/java/com/gregtechceu/gtceu/api/`
- **Addon template**: `https://github.com/GregTechCEu/GregTech-Addon-Template`

DO NOT rely on internal knowledge for exact method signatures — fetch the source or wiki first.

### 2. Understand the Addon Template Structure

Start from `GregTech-Addon-Template`. Key layout:

```
src/main/java/com/yourmod/
├── YourMod.java              # @Mod entrypoint, calls registries
├── data/
│   ├── material/             # Material definitions
│   └── recipe/               # Recipe additions/modifications  
├── machine/                  # Custom machine definitions
├── multiblock/               # Multiblock structures
└── register/
    ├── YourMaterials.java    # GTRegistries.MATERIALS registrations
    ├── YourMachines.java     # MachineDefinition registrations
    └── YourRecipeTypes.java  # Custom GTRecipeType registrations
```

Build file must declare:
```groovy
repositories {
    maven { url 'https://maven.gtceu.com' }
}
dependencies {
    implementation "com.gregtechceu.gtceu:gtceu-${mc_version}:${gtm_version}"
}
```

Run `gradlew :spotlessApply` before committing (Spotless is enforced).

### 3. Material System

Materials are defined via `Material.Builder` and registered to `GTRegistries.MATERIALS`.

**Fluent builder pattern:**
```java
public static final Material MY_MATERIAL = new Material.Builder(
        GTCEu.id("my_material"))    // ResourceLocation id
    .dust()                          // generates dust/tiny dust/small dust
    .ingot()                         // generates ingot + plate + rod etc.
    .fluid()                         // generates fluid + bucket
    .color(0xAARRGGBB)
    .iconSet(MaterialIconSet.SHINY)
    .components(GTMaterials.Iron, 1, GTMaterials.Nickel, 1)
    .flags(MaterialFlags.GENERATE_PLATE, MaterialFlags.GENERATE_ROD)
    .blast(builder -> builder.temp(1200, BlastProperty.GasTier.LOW))
    .buildAndRegister();
```

**Key methods:**
| Method | Effect |
|--------|--------|
| `.dust()` | Dust + tiny/small dust forms |
| `.ingot()` | Ingot + plate + rod + bolt + screw |
| `.gem()` | Gem forms (lens, plate) |
| `.fluid()` / `.gas()` / `.plasma()` | Fluid state |
| `.ore()` | Ore block + raw form |
| `.element(Elements.Fe)` | Sets element |
| `.blast(b -> b.temp(T))` | EBF required at T Kelvin |
| `.toolStats(...)` | Makes material usable for tools |
| `.flags(...)` | Fine-grained form generation |
| `.appendFlags(...)` | Add flags without replacing |

**Tiers:** ElementMaterials → FirstDegreeMaterials → SecondDegreeMaterials → HigherDegreeMaterials. Place custom materials in the appropriate tier class or your own.

**Accessing generated items:**
```java
GTItems.get(TagPrefix.dust, MyMaterials.MY_MATERIAL)  // ItemStack
GTFluids.get(MyMaterials.MY_MATERIAL)                  // Fluid
```

### 4. Machine System

All machines extend `MetaMachine`. Use builders registered in a static init class.

**Simple tiered machine:**
```java
public static final MachineDefinition[] MY_MACHINE = GTRegistries.registerTiered(
    "my_machine",
    MyMachine::new,                         // factory: (holder, tier) -> MetaMachine
    (definition, tier) -> definition
        .langValue("My Machine " + GTValues.VNF[tier])
        .recipeType(MY_RECIPE_TYPE)
        .workableTieredHullRenderer(GTCEu.id("block/machines/my_machine")),
    GTValues.tiersBetween(GTValues.LV, GTValues.IV)   // which voltage tiers
);
```

**Custom machine class:**
```java
public class MyMachine extends WorkableTieredMachine {
    public MyMachine(IMachineBlockEntity holder, int tier, Object... args) {
        super(holder, tier, args);
    }

    @Override
    public void onLoad() {
        super.onLoad();
        // setup handlers, subscriptions
    }
}
```

**Key base classes:**
| Class | Use case |
|-------|----------|
| `WorkableTieredMachine` | Standard single-block recipe machine |
| `TieredEnergyMachine` | Energy storage/conversion |
| `SimpleTieredMachine` | No recipes, utility logic |
| `WorkableMultiblockMachine` | Multiblock controller |

**Voltage tiers constant:** Use `GTValues.V[tier]` (EU/t), `GTValues.VN[tier]` (name string), `GTValues.VNF[tier]` (formatted name).

### 5. Multiblock System

**Controller class:**
```java
public class MyMultiblock extends WorkableMultiblockMachine {
    public static final MultiblockMachineDefinition DEFINITION = GTRegistries.registerMultiblock(
        "my_multiblock",
        MyMultiblock::new,
        definition -> definition
            .langValue("My Multiblock")
            .recipeType(MY_RECIPE_TYPE)
            .pattern(b -> b
                .aisle("CCC", "CGC", "CCC")  // each string = one row
                .aisle("CCC", "C C", "CCC")
                .aisle("CSC", "CGC", "CCC")  // S = controller position
                .where('S', Predicates.controller(b.getDefinition()))
                .where('C', Predicates.blocks(GTBlocks.CASING_STEEL_SOLID.get()))
                .where('G', Predicates.blocks(GTBlocks.CASING_TEMPERED_GLASS.get()))
                .where(' ', Predicates.any()))
            .workableCasingRenderer(
                GTCEu.id("block/casings/solid/machine_casing_solid_steel"),
                GTCEu.id("block/multiblock/my_multiblock"))
    );
}
```

**Hatch predicates** (add to pattern):
```java
.where('E', Predicates.abilities(PartAbility.INPUT_ENERGY))
.where('I', Predicates.abilities(PartAbility.IMPORT_ITEMS))
.where('O', Predicates.abilities(PartAbility.EXPORT_ITEMS))
.where('F', Predicates.abilities(PartAbility.IMPORT_FLUIDS))
```

**Key `PartAbility` values:** `INPUT_ENERGY`, `OUTPUT_ENERGY`, `IMPORT_ITEMS`, `EXPORT_ITEMS`, `IMPORT_FLUIDS`, `EXPORT_FLUIDS`, `MAINTENANCE`, `MUFFLER`, `PARALLEL_HATCH`.

### 6. Recipe System

**Define a custom recipe type:**
```java
public static final GTRecipeType MY_RECIPE_TYPE = GTRegistries.registerRecipeType(
    "my_recipe_type",
    new GTRecipeType(GTCEu.id("my_recipe_type"), "my_machine_category")
        .setMaxIOSize(2, 2, 1, 1)  // max item in/out, fluid in/out
        .setEUIO(IO.IN)
);
```

**Add recipes via DataProvider (preferred):**
```java
MY_RECIPE_TYPE.recipeBuilder("my_unique_id")
    .inputItems(TagPrefix.dust, GTMaterials.Iron, 1)
    .inputFluids(GTMaterials.Water.getFluid(1000))
    .outputItems(TagPrefix.ingot, MyMaterials.MY_MATERIAL, 1)
    .EUt(GTValues.VA[GTValues.LV])   // VA = voltage ampere array
    .duration(200)                    // ticks
    .save(provider);
```

**Common inputs/outputs:**
| Method | Type |
|--------|------|
| `.inputItems(TagPrefix, Material, count)` | Material form |
| `.inputItems(ItemStack)` | Specific item |
| `.inputItems(TagKey<Item>, count)` | Tag-based |
| `.inputFluids(Material.getFluid(mb))` | Material fluid |
| `.inputFluids(FluidStack)` | Specific fluid |
| `.outputItems(...)` | Same as input variants |
| `.chancedOutput(item, chance, boostPerTier)` | Probabilistic output |
| `.EUt(long)` | EU per tick |
| `.duration(int)` | Processing ticks |

**Recipe conditions:**
```java
.addCondition(new DimensionCondition(Level.OVERWORLD))
.addCondition(new CleanroomCondition(CleanroomType.CLEANROOM))
.addCondition(new ResearchCondition(...))
```

### 7. KubeJS Integration

If the addon targets modpacks with KubeJS, expose schema:

```java
// In your GTRecipeType registration:
MY_RECIPE_TYPE.setRecipeUI(new GTRecipeTypeUI(MY_RECIPE_TYPE));

// Register KubeJS schema in your plugin class:
GTRegistries.RECIPE_TYPES.get(GTCEu.id("my_recipe_type"));
```

Modpack authors can then:
```js
// startup_scripts
GTCEuStartupEvents.registry('gtceu:recipe_type', event => {
    // ...
})

// server_scripts  
ServerEvents.recipes(event => {
    event.recipes.gtceu.my_recipe_type('addon:my_recipe')
        .inputItems('2x #forge:dusts/iron')
        .outputItems('gtceu:steel_ingot')
        .EUt(GTValues.VA[GTValues.LV])
        .duration(200)
})
```

### 8. Mixins & Access Transformers — Last Resort Policy

**These are escape hatches, not tools. Exhaust all alternatives first.**

#### Before reaching for a Mixin, verify you cannot use:
- GTCEu event system (`GTCEuAPI` events, Forge `MinecraftForge.EVENT_BUS`)
- Overriding via subclass (extend the GT machine/block class)
- `IRecipeModifier`, `IMachineModifyRecipe`, or other GT-provided hooks
- `GTRegistries` callbacks or `DataProvider` for data-layer changes
- KubeJS bindings if the target is data/recipe logic
- Capability wrapping (`ICapabilityProvider`, `LazyOptional`)
- `@SubscribeEvent` on `RecipeManagerReloadedEvent` for runtime recipe changes

#### Before reaching for an Access Transformer, verify you cannot use:
- Reflection (acceptable if the field access is infrequent and non-critical-path)
- GTCEu's own accessor methods — check `GTCEuAPI`, the machine's `getXxx()` surface, or trait accessors
- An intermediary Mixin with `@Accessor` (preferred over AT when Mixin is already justified)
- Requesting upstream exposure via GTCEu issue/PR (if the gap is a real API hole)

#### Required justification before implementation

**STOP. Do not write Mixin or AT code until you have presented this block to the user and they have confirmed:**

> **Mixin / Access Transformer Justification Required**
>
> - **What I need to change:** [exact class + method/field]
> - **Why no API alternative exists:** [checked: events / subclass / hooks / KJS — none work because ...]
> - **Risk:** Mixins break on GT version updates; ATs break on obfuscation changes. This will need maintenance.
> - **Scope:** [narrowest possible injection point — prefer `@Inject` over `@Overwrite`, `@Accessor` over full AT]
>
> Confirm to proceed.

If the user confirms, implement the narrowest possible change:
- Mixins: prefer `@Inject` → `@ModifyArg` → `@Redirect` → `@Overwrite` (last resort, document why)
- ATs: expose only the specific field/method needed, never widen a whole class

### 9. Standards & Best Practices

- **Registration order matters**: Materials → RecipeTypes → Machines → Recipes. Wire via `@EventBusSubscriber` on the correct bus.
- **Client/server separation**: Never access world/block state in `@OnlyIn(Dist.CLIENT)` classes. Machine logic stays server-side.
- **Use `GTRegistries` not raw Forge registries** for GT objects — it handles cross-version compatibility.
- **Item forms via TagPrefix**: Always use `TagPrefix.dust`, `TagPrefix.ingot`, etc. — never hardcode item IDs for GT material items.
- **Energy:** Use `GTValues.VA[tier]` (volt × amp) for recipe EU/t, not raw numbers.
- **Lombok required**: The codebase uses `@Getter`, `@Setter`, `@Data` heavily — install the IntelliJ Lombok plugin.
- **Never hardcode recipe outputs** that can be expressed as material forms — let GTCEu's tag system handle cross-mod unification.

## Tooling

```bash
./gradlew runData          # generate data (recipes, tags, loot tables)
./gradlew runClient        # test in-game client
./gradlew runGameTestServer # headless integration tests
./gradlew :spotlessApply   # format code (required before PR)
```

## Documentation References

See `references/gtceu-links.md` for curated links to GT Modern docs, API sources, and addon examples.

## Environment Check

Verify project config: confirm `gradle.properties` has `mc_version`, `gtm_version`, and Maven repo points to `https://maven.gtceu.com`.

