# Fabric version contracts and project evidence

## Version boundary

Read the exact target documentation and generated sources before copying names. Fabric ≤1.21.11 can use Yarn or Mojang mappings with remapping Loom. Fabric ≥26.1 uses official unobfuscated names, the non-remapping plugin, ordinary dependency configurations, normal `jar`, and `official` access-file namespaces. The compatibility wrapper used by an existing project is not evidence of misconfiguration.

Official sources reviewed for this audit:

- https://docs.fabricmc.net/develop/loom/ — plugin IDs and remapping versus non-remapping contracts.
- https://docs.fabricmc.net/26.1.2/develop/porting/ — pinned 26.1-line porting guide.
- https://docs.fabricmc.net/26.1.2/develop/porting/fabric-api — source-incompatible Fabric API changes beyond mappings.

The corresponding `/26.1/` documentation paths returned 404; use the observed patch-pinned paths above rather than constructing URLs from a Minecraft version.

## Inspected implementation

[TemplateProject at 042d296e255d6a9e75e1d2f40da9937810e92004](https://github.com/SirEdvin/TemplateProject/tree/042d296e255d6a9e75e1d2f40da9937810e92004):

- `settings.gradle.kts` declares flat 1.20.1/1.21.1 loader nodes and the `1.21.1-fabric` VCS source state.
- `build.fabric.gradle.kts` applies `dev.kikugie.loom-back-compat`, calls `loomx.applyMojangMappings()`, chooses Java 17/21 by target, and expands `fabric.mod.json` while excluding both Forge descriptors.
- This is a concrete counterexample to “Fabric always uses Yarn” and “all versions must live in gradle.properties.” Preserve the structured properties and source-generation ownership.

[Minecraft-Modding-Libs at 86bfe0b75d0dceb26e713a6c3bdcc91ec74eac2c](https://github.com/SirEdvin/Minecraft-Modding-Libs/tree/86bfe0b75d0dceb26e713a6c3bdcc91ec74eac2c): `settings.gradle.kts` declares four common library modules with Fabric/forge branches for 1.20.1 and 1.21.1, plus `typed-peripheral-api`. Resolve convention plugins rather than flattening this graph into an example mod.

## Verification and limits

The audit coordinator built all four TemplateProject nodes in a disposable clone. Both Fabric production JARs contained only `fabric.mod.json` as loader metadata, with no unexpanded metadata placeholders. Task discovery exposed node-qualified `runClient`/`runServer` but no Fabric datagen run in this minimal template. Discover tasks before invoking them.

The coordinator also built all 24 versioned library nodes plus the typed API; 50 JUnit XML reports recorded 1060 test executions with zero failures, errors, or skips. These are aggregate build/unit-test results, not Fabric GameTest or client/server startup evidence. No 26.1 build or runtime was exercised. After generating another node, restore the declared canonical/VCS source state and inspect the diff.
