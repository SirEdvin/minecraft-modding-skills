# Version scope and menu/network boundaries

## Versioned opening APIs

Menu construction, client screen registration, opening data, and ongoing networking are separate responsibilities. Match the exact target loader API rather than copying a cross-loader adapter from another mod.

| Target | API boundary |
| --- | --- |
| Fabric 1.20.1 | `ExtendedScreenHandlerType` and `ExtendedScreenHandlerFactory.writeScreenOpeningData`; match the server writer to the client buffer reader. |
| Fabric 1.21.1 | Codec-backed `ExtendedScreenHandlerType` and `getScreenOpeningData`; do not copy the older buffer constructor unmodified. |
| Forge 1.20.1 | `IForgeMenuType.create` and `NetworkHooks.openScreen`; opening requires a server player. |
| NeoForge 1.21.1 | `IMenuTypeExtension.create`; verify matching imports and opening APIs in the target source. |

## Separate four contracts

1. **Open context:** bounded host locator or initial snapshot sent once. Ensure writer/reader or codec order, sizes, and version match. Do not interpret this as authority to mutate any later host at that position.
2. **Menu synchronization:** matching slot order and vanilla carried-stack behavior on both sides; suitable integer fields through menu data synchronization. Check the exact protocol's integer width before synchronizing large counters; do not assume a Java `int` means a lossless 32-bit transport on every target.
3. **Custom actions:** serverbound requests express intent, not trusted final state. Resolve the sender's current menu/item, validate container identity, host existence, distance, permissions, sizes/indices, and allowed operation on the proper server thread. Recheck at application time, not only when opening.
4. **Client view:** screen/widget state, focus, rendering, drafts, navigation, and narration. Register and reference client classes only behind physical-client boundaries. An integrated-server test shares a JVM and cannot prove dedicated-server classloading safety.

A standalone `Screen` can send gameplay requests without becoming a container menu, but it still needs the same server validation. Conversely, a loader menu factory cannot replace packet validation or guarantee that a registered client screen exists. Use the existing project abstraction rather than creating a second incompatible open path.

## Exact-version rendering, not a blanket 1.21 recipe

The core's Mojmap names describe architectural roles, not universal imports. `GuiGraphics` is useful guidance for **1.20.1 and 1.21.1**, while later 1.21 releases and 26.1 require renewed inspection of render extraction, input-event signatures, texture/pipeline overloads, and mappings. The core's 26.1 repository branches are discovery leads, not validated code samples.

Before implementing a port, record the target game version, mappings, loader/API version, source branch/commit, method signature, and source set. Verify overrides in a Stonecutter node before editing shared code. For rendering migrations, keep mutations and packet sends in lifecycle/input logic; extraction should submit render state without changing authoritative state.

## Prove UI behavior, not just a screenshot

- Assert the actual screen type and state on the client thread. A container-menu assertion does not cover a standalone screen.
- Open through the actual block/item/server path and wait for the expected screen/menu. Direct construction bypasses registration, opening-data decoding, and synchronization.
- Ensure screenshots include the GUI. Capturing an image is not pixel comparison or an interaction test.
- Verify save/reopen and server state independently; exercise stale-menu actions, invalid bounds, removed hosts, and concurrent viewers.
- Headless clients need a display, working OpenGL, an external timeout, and fresh reports. Test tick timeouts do not bound startup or frame waits.
- Keep keyboard/narration checks and dedicated-server startup explicit when automation does not cover them.
