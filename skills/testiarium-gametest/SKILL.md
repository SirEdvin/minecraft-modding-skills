---
name: testiarium-gametest
description: Testiarium GameTest development for Minecraft 1.20.1 on Forge and Fabric. Use when adding or debugging Testiarium testmods, registering GameTest classes, grouping tests, writing server or automated client GameTests, managing SNBT fixtures, producing JUnit reports, or testing CC:Tweaked computers and peripherals.
license: MIT
compatibility: Minecraft 1.20.1, Java 17, Forge 47.x, and Fabric projects using Testiarium.
metadata:
  version: "1.0.0"
---

# Testiarium GameTest

Use this skill for the Testiarium cross-loader GameTest framework. Testiarium supplies loader-neutral test registration, grouping, assertions, client automation, fixture commands, reports, and an optional CC:Tweaked harness for Minecraft 1.20.1.

## First Checks

- Confirm the project targets Minecraft 1.20.1 and Java 17.
- Identify the loader and test source sets before editing Gradle: core/shared tests should remain loader-neutral, while Forge and Fabric bootstrap code belongs in their loader modules.
- Determine which Testiarium layer is actually available. Registration, grouping, generic assertions, and reporting are in the main artifacts. Fixture commands, client helpers, structure mixins, and CC:Tweaked helpers are testmod facilities and require corresponding test-only outputs and dependencies.
- Inspect the project's existing testmod source-set wiring and run configurations. Do not assume adding the production Testiarium artifact exposes testmod or CCT packages.
- Keep Testiarium and all test-only integrations out of published runtime dependencies unless the mod intentionally exposes them.
- Prefer explicit structure names and test groups. Generated names use only `<SimpleClassName>.<methodName>` and can collide across packages.

## Architecture

Testiarium is split into these responsibilities:

| Layer | Responsibility |
|---|---|
| Core main API | `Testiarium`, annotations, groups, sequences, assertions, and reporters |
| Forge adapter | Forge lifecycle and `RegisterGameTestsEvent` integration |
| Fabric adapter | Fabric lifecycle and vanilla `GameTestRegistry` integration |
| Generic testmod tooling | Fixture commands, structure mixins, client runner, screenshots |
| CCT testmod tooling | CC:Tweaked computer actions, Lua markers, assertions, and fixture import |

Keep generic tests in a shared test source set. Put loader entrypoints, event registration, metadata, and client bootstrap in matching Forge or Fabric test source sets.

## Register Tests

Always collect classes before invoking the loader adapter:

```kotlin
Testiarium.register(MyGameTests::class.java)
FabricTestiarium.registerTests()
```

```java
Testiarium.register(MyGameTests.class);
ForgeTestiarium.registerTests();
```

Registration is one-shot per process:

- Fabric scans immediately when `FabricTestiarium.registerTests()` is called. Classes added afterward are not discovered.
- Forge installs a listener and must call `ForgeTestiarium.registerTests()` before `RegisterGameTestsEvent` fires.
- Repeated adapter calls do nothing, so register all classes first.
- Non-static test methods require a public zero-argument constructor. Kotlin classes with no constructor parameters satisfy this by default.
- Keep unrelated helper methods outside registered classes when practical. Testiarium passes enabled, unrecognized declared methods to the loader's fallback GameTest registrar.

Typical Fabric testmod entrypoint:

```kotlin
object ExampleFabricTestMod : ModInitializer {
    override fun onInitialize() {
        Testiarium.register(ExampleGameTests::class.java)
        FabricTestiarium.registerTests()
    }
}
```

Typical Forge testmod entrypoint:

```java
@Mod("example_testmod")
public final class ExampleForgeTestMod {
    public ExampleForgeTestMod() {
        Testiarium.register(ExampleGameTests.class);
        ForgeTestiarium.registerTests();
    }
}
```

## Write Server GameTests

Use vanilla `@GameTest` with Testiarium's sequence and assertion extensions:

```kotlin
@TestGroup("example")
class ExampleGameTests {
    @GameTest(template = "examplegametests.places_block")
    fun placesBlock(helper: GameTestHelper) = helper.sequence {
        thenExecuteFailFast {
            helper.assertBlock(BlockPos(1, 1, 1), { !it.isAir }, "Expected a block")
        }
    }
}
```

`helper.sequence { ... }` creates a sequence and automatically appends `thenSucceed()`. Do not add another terminal success step unless using `helper.startSequence()` directly.

Use `helper.immediate { ... }` for synchronous assertions followed by immediate success:

```kotlin
@GameTest(template = "empty")
fun recipeExists(helper: GameTestHelper) = helper.immediate {
    helper.assertCraftable(inputs, expectedOutput)
}
```

Useful generic helpers include:

- `thenExecuteFailFast { ... }`: converts arbitrary thrown errors into GameTest failures.
- `assertBlock(pos, predicate, message)` and `assertBlockProperty(pos, property, expected)`.
- `getContainer(pos)` and `assertContainer(pos, expectedStacks)`.
- `getBlockEntity(pos, type)` and `getEntity(type)`.
- `assertItemCount(item, expected)` and `assertCraftable(inputs, expected)`.

Be precise with their scopes:

- `getEntity` requires exactly one matching entity within 64 blocks of the test origin.
- `assertItemCount` counts all matching dropped items in that radius.
- `assertContainer` checks actual slots and treats omitted expected slots as empty; it does not detect expected entries beyond the real container size.
- `thenExecuteFailFast` may reduce a non-GameTest exception to its message, so use meaningful assertion messages.

## Groups And Properties

Apply `@TestGroup("name")` to a class or method. A method annotation overrides its class annotation. Ungrouped vanilla tests default to `common`; `@ClientGameTest` defaults to `client`.

Enable groups with an exact comma-separated JVM property:

```text
-Dtestiarium.tags=common,example
```

Tag names are case-sensitive, whitespace is not trimmed, and the property is read once. Use `common,client`, not `common, client`. Enabling `client` does not implicitly enable `common`.

Other properties:

| Property | Purpose |
|---|---|
| `testiarium.structures` | Runtime SNBT structure directory |
| `testiarium.fixture-source` | Editable/source SNBT directory used by fixture commands |
| `testiarium.gametest-report` | JUnit XML output; Testiarium also writes sibling HTML |
| `testiarium.client` | Enables the automated client runner when the property is present |
| `testiarium.screenshots` | Client screenshot output directory |
| `testiarium.cct-fixtures` | CC:Tweaked computer fixture root |

## Structures And Fixtures

Specify `template` explicitly unless the generated `<SimpleClassName>.<methodName>` name is intentional. Keep SNBT resources in the location expected by the project's GameTest setup.

When generic testmod fixture commands are wired, use:

```text
/testiarium import
/testiarium export
/testiarium regen-structures
/testiarium marker
```

- `import` copies source fixtures into the runtime structures directory.
- `export` copies runtime structures back to the source directory.
- `regen-structures` imports, invokes vanilla structure export for registered tests, then exports files back.
- `marker` places or removes a named invisible armor stand used as a position/orientation marker.

Set both `testiarium.fixture-source` and `testiarium.structures` for these workflows. Synchronization overwrites files but does not delete stale destination files, so inspect both directories when a removed fixture still appears.

The testmod structure mixin fills omitted SNBT positions with explicit air. Include the testmod mixin configuration and resources if relying on compact structures; this behavior is not part of the core production artifact.

## Reports And CI

Set a report destination in the run configuration:

```text
-Dtestiarium.gametest-report=build/test-results/gametest.xml
```

Testiarium writes JUnit XML plus an HTML file with the same basename. Required failures are failures; non-required vanilla GameTest failures are reported as skipped. Reports finish during server shutdown or client completion, so a forcibly killed process may not produce one.

GameTest runs are Minecraft `JavaExec` tasks, not JUnit `Test` tasks. `./gradlew test` does not replace running the configured GameTest server/client task. CI must invoke the relevant loader task and preserve its exit status and report files.

## Automated Client Tests

Use `@ClientGameTest` for tests that require a real client:

```kotlin
@ClientGameTest(template = "empty", timeoutTicks = Timeouts.SECOND * 20)
@TestGroup(TestTags.CLIENT)
fun opensScreen(helper: GameTestHelper) = helper.sequence {
    thenOnClient {
        check(minecraft.player != null)
    }
    thenScreenshot("opens-screen")
}
```

Available client sequence helpers include:

- `thenOnClient { ... }`: schedules work on the Minecraft client thread.
- `thenRenderIdle(ticks)`: waits until rendering remains stable.
- `thenScreenshot(name, showGui)`: waits for stable rendering and captures a PNG.
- `positionAt(pos, yRot, xRot)` and `positionAtArmorStand()`: position the player for visual interaction.
- `ClientTestHelper.getOpenMenu(type)`: assert and return the currently open menu.

The automated runner creates or reuses a `testiarium-client` flat world, waits for stable rendering, runs tests around `(0, -60, 0)`, finishes reports, and exits. Exit code 1 means no tests ran; exit code 2 means a required test failed.

Client GameTests require graphics even in automation. In a headless environment always use a virtual X server and an explicit timeout:

```bash
timeout --foreground 180s xvfb-run --auto-servernum \
  ./gradlew :example-forge:runClientGameTest --no-daemon
```

```bash
timeout --foreground 180s xvfb-run --auto-servernum \
  ./gradlew :example-fabric:runClientGameTest --no-daemon
```

Keep client hook registration physically client-only. On Forge use `DistExecutor` or an equivalent safe boundary; on Fabric use a `client` entrypoint. Never load client helper classes on a dedicated server.

## Optional CC:Tweaked Harness

CC:Tweaked support is test-only and version-sensitive. Put CCT-dependent code and matching loader dependencies in a dedicated test source set. Do not introduce CC:Tweaked into Testiarium core or ordinary runtime classpaths.

Initialize the CCT harness before CC:Tweaked creates its server context, then reset state and import fixtures on every server start:

```kotlin
CctComputers.initialize()

ServerLifecycleEvents.SERVER_STARTING.register { server ->
    CctComputers.reset()
    CctFixtureCommands.importFiles(server)
}

Testiarium.register(ComputerGameTests::class.java)
FabricTestiarium.registerTests()
```

Use equivalent Forge lifecycle events in a Forge testmod. Initialization globally replaces CC:Tweaked's Lua machine factory for that process, so do it only in the CCT test environment.

Sequence helpers:

- `thenStartComputer(name, action)` starts a Kotlin computer action without waiting.
- `thenOnComputer(name, action)` starts an action, waits, and propagates failure.
- `thenComputerOk(name, marker)` waits for a Lua completion marker.
- `helper.thenLua(label)` waits for the fixture computer to signal the default `DONE` marker.

Example Lua-driven test:

```kotlin
@TestGroup("example-cct")
class ComputerGameTests {
    @GameTest(template = "computergametests.peripheral")
    fun peripheral(helper: GameTestHelper) = helper.thenLua()
}
```

The default `thenLua` label is the structure name. Kotlin action helpers instead derive labels from `<TestClass>.<method>` plus an optional suffix. Label fixture computers deliberately and ensure `tests/<label>.lua` exists beneath `testiarium.cct-fixtures`.

Lua tests communicate through:

```lua
test.log("diagnostic")
test.ok()          -- DONE marker
test.ok("phase-1")
test.fail("reason")
```

CCT fixture commands are:

```text
/testiarium cct import
/testiarium cct export
/testiarium cct give-computer <item>
```

The built-in fixture synchronization targets CC:Tweaked computer directory `1`. Check world state and computer IDs if imported files are ignored.

## Loader Run Patterns

Task names are project-defined, but Testiarium's own modules demonstrate these patterns:

```bash
./gradlew :testiarium-forge:runGameTestServer
./gradlew :testiarium-forge:runGameTestServer -Ptestiarium.cct
./gradlew :testiarium-fabric:runServer
./gradlew :testiarium-fabric:runCctGameTest
```

Forge uses `forge.enabledGameTestNamespaces` and registration events. Fabric requires `fabric-api.gametest=true` and immediate registry integration. Copy the concepts into consumer run configurations rather than hardcoding these module task names.

## Debugging Checklist

- No tests discovered: verify class registration occurs before loader registration, the group is enabled, and the loader's GameTest namespace/property is configured.
- Structure missing: check the explicit template name, namespace, `testiarium.structures`, fixture import, and stale runtime files.
- Reflection failure: make the test method static or give its class a public zero-argument constructor.
- Client run hangs: verify client hooks and mixins are loaded, use `xvfb-run`, inspect rendering logs, and retain an external timeout.
- Client run exits 1: the `client` group probably selected no registered tests.
- Report missing: set `testiarium.gametest-report` and allow orderly server/client shutdown.
- CCT test never completes: verify early `CctComputers.initialize()`, server-start reset/import, computer label, fixture directory, and Lua `test.ok()` call.
- Fabric-only registration issue: ensure every class is registered before the first `FabricTestiarium.registerTests()` call.
- Dedicated server classloading failure: move all client fixture references behind loader-specific physical-client boundaries.

## Validation

- Run the smallest affected server GameTest task first.
- Run both Forge and Fabric GameTest tasks after changing shared registration, annotations, fixtures, or assertions.
- Run CCT tasks when changing computer fixtures, labels, Lua scripts, peripherals, or CCT lifecycle wiring.
- Run client tasks under `xvfb-run` with a timeout after changing screens, menus, rendering, screenshots, or client hooks.
- Inspect generated XML and HTML reports, not only process output.
- Verify test-only dependencies and source-set outputs do not leak into published runtime artifacts.

## Source Reference

- Testiarium source: `https://github.com/SirEdvin/Minecraft-Modding-Libs/tree/main/projects/testiarium-core`
- Forge adapter: `https://github.com/SirEdvin/Minecraft-Modding-Libs/tree/main/projects/testiarium-forge`
- Fabric adapter: `https://github.com/SirEdvin/Minecraft-Modding-Libs/tree/main/projects/testiarium-fabric`
