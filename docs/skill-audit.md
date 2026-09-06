# All-package audit

## Scope and evidence

All 11 installable packages were reviewed against their applicable source contracts and representative project usage. A package being in the catalog does not imply it is used by either example project.

## fabric-modding

- Fabric was incorrectly treated as Yarn-only; Loom remap and 26.1 contracts were conflated.
- Prior edits referenced a missing support file.

## gtceu-addon

- Unpinned examples mixed GTCEu API generations, wrong namespace ownership, invented registry helpers, unconditional generated forms, ARGB color and incorrect VA meaning.
- Template dependencies, material events, addon hooks, recipe capabilities and 8.0 deprecations require separate versioned contracts.
- Original support link inventory reviewed; community navigation retained with explicit unverified status.

## kubejs-modding

- Claim that script reload cannot replace listeners contradicted pinned 2001 ScriptType/ScriptManager source.
- Java.type was not exposed on the reviewed Java wrapper; command error arguments and Forge tag example needed version labels.
- Retained all original lifecycle, recipe, registry, tags, client, interop, addon and porting coverage.

## minecraft-26-1-migration

- Whole-build MDK replacement risks maintained multiversion nodes.
- Source restoration and observed verification gaps were absent from the brief.

## minecraft-modpack-authoring

- Nested ZIP export could be indexed into subsequent exports; move output outside pack root.
- Source export failures can return without nonzero exit: require fresh valid archive, not exit code alone.
- Loader migration only updates selected loader; bootstrap pin alone does not pin installer/hosted pack.
- Both original support files reviewed; content/testing retained unchanged, long main body preserved in authoring-workflow with targeted corrections.

## minecraft-native-ui

- Fabric factory was incorrectly named ExtendedMenuType; actual import is ExtendedScreenHandlerType.
- Fabric 1.21.1 opening is codec-backed, unlike 1.20.1 buffer constructor.
- Broad 1.21 rendering guidance needed exact 1.20.1/1.21.1 scope; 26.1 remains source-discovery guidance, not this audit verification.
- Client screenshots default to hidden GUI; opening/menu assertions do not prove server validation or dedicated-server safety.

## modrinth-api

- Project-version pagination claim was false; source URLs require full project, dependencies require version records.
- Illustrative response data and invented files[].id, universal tag-name fields and unsafe raw-JSON curl/download examples were replaced.
- Retained endpoint map, selected fields, facets, batch discovery, staging distinction and safe downloads in linked reference.

## neoforge-legacy-modding

- GameTest run name was confused with its Gradle task; reobfJar existence was assumed.
- Legacy dependencies and Forge 47.x channel signatures need explicit contracts.

## neoforge-modding

- Current NeoForge APIs were incorrectly universalized to 1.21.1.
- Run availability and physical-side API syntax need target checks.

## stonecutter-multiversion

- Flat root tree and multi-library monorepo require different task qualification; libs has four independent trees and a non-Stonecutter typed API module.
- Ordinary monorepo root applies java legitimately; controller-root ban must not apply to every repository root.
- forge branch is Forge 1.20.1 and NeoForge 1.21.1; active source and vcsVersion differ deliberately.
- Both real projects pin 0.9.7; preserved existing PR9 0.9.8 fixture results and 0.10 API conflict warnings.
- Captured task parser omitted names with spaces; raw task log confirms qualified Set/Reset/Refresh names.

## testiarium-gametest

- Old testiarium-core/-forge/-fabric source links and tasks no longer match multiversion topology.
- Current Forge 1.20.1 build uses ModDevGradle LegacyForge, not ForgeGradle.
- thenLua returns unfinished sequence: original skill example omitted thenSucceed, unlike the actual Tweakium consumer.
- Testiarium source version is 2.0.0; main/testMod/cctTestMod classes and loader metadata are distinct requirements.
- NeoForge CCT project-property mode adds implementation dependency: publication under that flag risks test dependency leakage.
- Core CI builds only; task discovery and compilation are not runtime GameTest coverage.
- External timeout, graphics driver, game versus Gradle exit status, stale report and screenshot GUI scope required explicit guidance.

## Repository verification

- Official skills-ref 0.1.1 validation: all 11 packages pass.
- Repository schema, package-local references, support reachability, README catalog: pass.
- Validator regression suite: 18 tests pass, including independent review regressions for malformed YAML dates, fenced examples, and intermediate asset links.
- skills 1.5.15 local discovery: exactly 11 packages.
- TemplateProject at `042d296e255d6a9e75e1d2f40da9937810e92004`: task discovery and root build succeeded in a disposable checkout; four release JARs checked for correct loader descriptors and unresolved metadata placeholders.
- Minecraft-Modding-Libs at `86bfe0b75d0dceb26e713a6c3bdcc91ec74eac2c`: task discovery and root build succeeded in a disposable checkout covering 24 versioned nodes and the separate API module; JUnit reports contain 1,060 test executions with no failures, errors, or skips.

## Limits

No client launch, dedicated-server launch, GameTest execution, GTCEu addon compilation, Rhino runtime, Packwiz CLI export, or 26.1 port build is claimed. Modrinth Maven dependency usage is not REST API usage. Public API and Packwiz hash checks in the package reviews are narrower evidence, not game compatibility tests. Original project checkouts were not modified.
