# NeoForge 1.21 merge/porting notes from Minecraft-Modding-Libs

Use when merging a 1.20.x maintenance branch into a 1.21.x NeoForge migration branch while preserving history.

## Durable patterns

- If the user asks to preserve history, perform a real merge from the source branch, e.g. `git merge --no-ff origin/1.20`, and resolve conflicts in that merge state. Do not cherry-pick or squash the source commits.
- For pushed merge branches, avoid amending/force-pushing unless the user explicitly approves rewriting history. A small follow-up commit is safer and still preserves the real merge commit.
- Verify the merge commit shape with `git log --oneline --graph --parents`; the merge commit should show both the destination branch parent and the source branch head as parents.

## Buildenv/plugin resolution

- Clean GitHub runners may fail to resolve `site.siredvin.*` Gradle plugins even if local caches or plugin marker paths work locally.
- For SirEdvin custom build plugins, add explicit plugin resolution mapping in `settings.gradle.kts`:

```kotlin
resolutionStrategy {
    eachPlugin {
        if (requested.id.id == "org.spongepowered.mixin") {
            useModule("org.spongepowered:mixingradle:${requested.version}")
        }
        if (requested.id.id.startsWith("site.siredvin.")) {
            useModule("site.siredvin:<custom-build-artifact>:${requested.version}")
        }
    }
}
```

- Verify clean-ish resolution with `./gradlew --no-daemon --refresh-dependencies help` before relying on CI.

## 1.20 Forge -> 1.21 NeoForge conflict adaptations

- Keep 1.21/NeoForge imports, not old `net.minecraftforge.*` imports:
  - `net.neoforged.neoforge.items.IItemHandler`
  - `net.neoforged.neoforge.fluids.capability.IFluidHandler`
  - `net.neoforged.neoforge.energy.IEnergyStorage`
  - `net.neoforged.neoforge.capabilities.Capabilities`
- NeoForge capability lookup calls can trigger Kotlin Java-type warnings under `-Werror` if nullable context values are passed. Use concrete context placeholders such as `direction ?: Direction.UP` or the API-required `null as Void` for entity item handlers.
- Preserve 1.21 data component handling for saved block data (`DataComponents.CUSTOM_DATA`, `CustomData`, `DataComponents.BLOCK_STATE`) rather than reintroducing old item NBT/tag hooks.
- When old 1.20 classes exist only to override a now-removed NBT tag key, collapse them to plain subclasses of the 1.21 data-component-based base class.
- Fabric/1.21 `ItemStack` no longer uses old `tag`/`hasTag` access in the same way; compare item/component equality with `ItemStack.isSameItemSameComponents` or existing helpers such as `ItemStorageUtils.canStack`.
- Use `item.defaultMaxStackSize` where `item.maxStackSize` no longer exists.

## Test/CI gotchas

- Under Fabric test classloaders, generic `kotlin.test.assertEquals` may fail through `kotlin.test.AsserterContributor` service loading. Shared test fixtures can use JUnit Jupiter assertions directly instead:

```kotlin
import org.junit.jupiter.api.Assertions.assertEquals
import org.junit.jupiter.api.Assertions.assertTrue
```

- Local validation that proved useful:

```bash
./gradlew --no-daemon :broccolium-core:compileKotlin :tweakium-core:compileKotlin
./gradlew --no-daemon :broccolium-fabric:compileKotlin :tweakium-fabric:compileKotlin
./gradlew --no-daemon :broccolium-forge:compileKotlin :tweakium-forge:compileKotlin
./gradlew --no-daemon :broccolium-fabric:test
./gradlew --no-daemon check
./gradlew --no-daemon :broccolium-forge:publishToMavenLocal :tweakium-forge:publishToMavenLocal :peripheralium-forge:publishToMavenLocal
```

## Review notes

- Treat old Forge-vs-NeoForge conflicts as semantic ports, not simple choose-ours/choose-theirs resolutions.
- After opening the PR, watch both PR-event and push-event CI runs if the workflow triggers both. Rerun failed stale runs only after confirming the head commit has a passing clean run.
