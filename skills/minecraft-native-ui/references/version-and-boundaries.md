# Version scope and menu/network boundaries

## Pinned project evidence

This audit inspected [Minecraft-Modding-Libs at 86bfe0b75d0dceb26e713a6c3bdcc91ec74eac2c](https://github.com/SirEdvin/Minecraft-Modding-Libs/tree/86bfe0b75d0dceb26e713a6c3bdcc91ec74eac2c), not a live UI session. Its Broccolium library provides a real common menu factory and loader opening adapters; Testiarium provides client automation. It does not prove a complete screen's rendering, accessibility, or malicious-payload handling.

The shared [MenuBuilder.kt](https://github.com/SirEdvin/Minecraft-Modding-Libs/blob/86bfe0b75d0dceb26e713a6c3bdcc91ec74eac2c/projects/broccolium/src/main/kotlin/site/siredvin/broccolium/modules/platform/api/MenuBuilder.kt) takes `(id, Inventory, FriendlyByteBuf)` and returns an `AbstractContainerMenu`. This is **menu construction**, not screen registration and not continuous networking.

| Target | Observed adapter | Porting consequence |
| --- | --- | --- |
| Fabric 1.20.1 | `ExtendedScreenHandlerType(builder::build)` plus `ExtendedScreenHandlerFactory.writeScreenOpeningData` | Match the server writer to the client buffer reader. `ExtendedMenuType` is not the imported Fabric API class. |
| Fabric 1.21.1 | `ExtendedScreenHandlerType(factory, MENU_OPENING_DATA_CODEC)` plus `getScreenOpeningData` | Opening data is codec-backed. This library bridges to its older buffer abstraction; do not copy the old constructor unmodified. |
| Forge 1.20.1 | `IForgeMenuType.create` and `NetworkHooks.openScreen` | Opening must occur for a server player; the library casts accordingly. |
| NeoForge 1.21.1 | `IMenuTypeExtension.create` | Use the target's NeoForge API/imports even though the project branch is named `forge`. |

Source files under `projects/broccolium`:

- [Fabric 1.20.1 registration](https://github.com/SirEdvin/Minecraft-Modding-Libs/blob/86bfe0b75d0dceb26e713a6c3bdcc91ec74eac2c/projects/broccolium/fabric/src/main/kotlin/site/siredvin/broccolium/modules/platform/FabricInnerBasePlatform.kt) and [opening](https://github.com/SirEdvin/Minecraft-Modding-Libs/blob/86bfe0b75d0dceb26e713a6c3bdcc91ec74eac2c/projects/broccolium/fabric/src/main/kotlin/site/siredvin/broccolium/modules/platform/FabricPlatformToolkit.kt).
- [Fabric 1.21.1 registration override](https://github.com/SirEdvin/Minecraft-Modding-Libs/blob/86bfe0b75d0dceb26e713a6c3bdcc91ec74eac2c/projects/broccolium/fabric/versions/1.21.1/src/main/kotlin/site/siredvin/broccolium/modules/platform/FabricInnerBasePlatform.kt) and [opening override](https://github.com/SirEdvin/Minecraft-Modding-Libs/blob/86bfe0b75d0dceb26e713a6c3bdcc91ec74eac2c/projects/broccolium/fabric/versions/1.21.1/src/main/kotlin/site/siredvin/broccolium/modules/platform/FabricPlatformToolkit.kt).
- [Forge 1.20.1 registration](https://github.com/SirEdvin/Minecraft-Modding-Libs/blob/86bfe0b75d0dceb26e713a6c3bdcc91ec74eac2c/projects/broccolium/forge/src/main/kotlin/site/siredvin/broccolium/modules/platform/ForgeInnerBasePlatform.kt) and [opening](https://github.com/SirEdvin/Minecraft-Modding-Libs/blob/86bfe0b75d0dceb26e713a6c3bdcc91ec74eac2c/projects/broccolium/forge/src/main/kotlin/site/siredvin/broccolium/modules/platform/ForgeInnerPlatformToolkit.kt).
- [NeoForge 1.21.1 registration override](https://github.com/SirEdvin/Minecraft-Modding-Libs/blob/86bfe0b75d0dceb26e713a6c3bdcc91ec74eac2c/projects/broccolium/forge/versions/1.21.1/src/main/kotlin/site/siredvin/broccolium/modules/platform/ForgeInnerBasePlatform.kt).

## Separate four contracts

1. **Open context:** bounded host locator or initial snapshot sent once. Ensure writer/reader or codec order, sizes, and version match. Do not interpret this as authority to mutate any later host at that position.
2. **Menu synchronization:** matching slot order and vanilla carried-stack behavior on both sides; suitable integer fields through menu data synchronization. Check the exact protocol's integer width before synchronizing large counters; do not assume a Java `int` means a lossless 32-bit transport on every target.
3. **Custom actions:** serverbound requests express intent, not trusted final state. Resolve the sender's current menu/item, validate container identity, host existence, distance, permissions, sizes/indices, and allowed operation on the proper server thread. Recheck at application time, not only when opening.
4. **Client view:** screen/widget state, focus, rendering, drafts, navigation, and narration. Register and reference client classes only behind physical-client boundaries. An integrated-server test shares a JVM and cannot prove dedicated-server classloading safety.

A standalone `Screen` can send gameplay requests without becoming a container menu, but it still needs the same server validation. Conversely, a loader menu factory cannot replace packet validation or guarantee that a registered client screen exists. Use the existing project abstraction rather than creating a second incompatible open path.

## Exact-version rendering, not a blanket 1.21 recipe

The core's Mojmap names describe architectural roles, not universal imports. `GuiGraphics` is useful guidance for **1.20.1 and 1.21.1**, while later 1.21 releases and 26.1 require renewed inspection of render extraction, input-event signatures, texture/pipeline overloads, and mappings. The two pinned projects do not target 26.1; the core's 26.1 repository branches are discovery leads, not validated code samples.

Before implementing a port, record the target game version, mappings, loader/API version, source branch/commit, method signature, and source set. Verify overrides in a Stonecutter node before editing shared code. For rendering migrations, keep mutations and packet sends in lifecycle/input logic; extraction should submit render state without changing authoritative state.

## Prove UI behavior, not just a screenshot

The pinned [Testiarium client helpers](https://github.com/SirEdvin/Minecraft-Modding-Libs/blob/86bfe0b75d0dceb26e713a6c3bdcc91ec74eac2c/projects/testiarium/src/testMod/kotlin/site/siredvin/testiarium/fixture/client/ClientTestExtensions.kt) schedule `thenOnClient` on the client thread and provide `getOpenMenu(type)` for container screens. They are **testMod** facilities, not automatically exposed by the production dependency.

- For a plain `Screen`, assert its actual type/state on the client thread; `getOpenMenu` specifically requires `MenuAccess` and a matching menu type.
- Open through the actual block/item/server path and wait for the expected screen/menu before asserting. Directly constructing a screen bypasses registration, opening-data decoding, and synchronization.
- Capture with `thenScreenshot("screen-name", showGui = true)`; the helper defaults to hiding GUI and does not compare pixels to a baseline.
- Verify save/reopen and server state independently; exercise stale-menu actions, invalid bounds, removed hosts, and concurrent viewers. A valid screenshot is not proof of any of these.
- Headless client runs still need a display and working OpenGL, client hooks/mixins, an external timeout, and fresh reports. Test tick timeouts cannot bound startup or waiting for a stable frame. Read the Testiarium skill's client reference when that package is installed, or inspect the project's actual run setup.
- Keep interactive keyboard/narration checks and dedicated-server startup as explicit remaining checks when automation does not cover them.
