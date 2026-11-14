# Provenance And Sources

This repository's expanded coverage was inspired by reviewing the topic scope of `zerodegress/minecraft-modding-skills` at commit `ab38622536fb07c6b6aef0052ca77d2b059861a8`. That upstream repository did not declare a license at the time of review. No upstream text, examples, or line-by-line paraphrases were copied into this repository; the new material here was independently authored from official documentation, this repository's existing content, and observed project conventions.

## Official Documentation Used

`fabric-modding`:

- https://docs.fabricmc.net/develop/
- https://docs.fabricmc.net/develop/loader/
- https://docs.fabricmc.net/develop/loom/
- https://docs.fabricmc.net/develop/networking
- https://docs.fabricmc.net/develop/data-generation/setup
- https://github.com/FabricMC/fabric-docs/tree/main/reference/latest

`neoforge-modding`:

- https://docs.neoforged.net/docs/gettingstarted/
- https://docs.neoforged.net/docs/1.21.1/gettingstarted/
- https://docs.neoforged.net/docs/concepts/registries/
- https://docs.neoforged.net/docs/networking/
- https://docs.neoforged.net/docs/1.21.1/networking/
- https://docs.neoforged.net/docs/datastorage/attachments/
- https://docs.neoforged.net/docs/items/datacomponents/
- https://docs.neoforged.net/docs/resources/
- https://github.com/neoforged/ModDevGradle

`neoforge-legacy-modding`:

- https://docs.minecraftforge.net/en/1.20.x/
- https://docs.minecraftforge.net/en/1.20.x/concepts/registries/
- https://docs.minecraftforge.net/en/1.20.x/concepts/events/
- https://docs.minecraftforge.net/en/1.20.x/networking/simpleimpl/
- https://docs.minecraftforge.net/en/1.20.x/datastorage/capabilities/
- https://docs.minecraftforge.net/en/1.20.x/advanced/accesstransformers/
- https://docs.minecraftforge.net/en/1.20.x/datagen/
- https://github.com/MinecraftForge/ForgeGradle
- https://github.com/neoforged/ModDevGradle

`kubejs-modding`:

- https://kubejs.com/wiki/
- https://kubejs.com/wiki/folder-structure
- https://kubejs.com/wiki/events
- https://kubejs.com/wiki/addons
- https://kubejs.com/wiki/tooling
- https://github.com/KubeJS-Mods/Rhino
- https://github.com/Prunoideae/ProbeJS

`minecraft-modpack-authoring`:

- https://tweaked.cc/module/pocket.html#v:equipBack
- The stateful gameplay protocol is independently distilled from fixture-isolation and restart-validation failures. The pocket API documentation supports inventory-search semantics only; the protocol is a recommended testing convention, not a claim of runtime coverage or release compatibility.
- https://packwiz.infra.link/
- https://packwiz.infra.link/tutorials/creating/getting-started/
- https://packwiz.infra.link/tutorials/creating/adding-mods/
- https://packwiz.infra.link/tutorials/installing/packwiz-installer/
- https://packwiz.infra.link/reference/commands/packwiz/
- https://github.com/packwiz/packwiz (reviewed at `dfd8b68a4796c763e25bad50265ea1f1233e24f1`)
- https://github.com/packwiz/packwiz-spec
- https://github.com/packwiz/packwiz-example-pack
- https://github.com/packwiz/packwiz-installer
- https://kubejs.com/wiki/
- https://github.com/KubeJS-Mods/KubeJS (reviewed at `84b072de677c2da12e150e34f2f300a669a2dff3`)
- https://docs.minecraftforge.net/en/1.20.x/misc/config/
- https://docs.neoforged.net/docs/misc/config/
- https://docs.neoforged.net/docs/1.21.1/misc/config/
- https://raw.githubusercontent.com/MinecraftForge/MinecraftForge/1.20.x/fmlcore/src/main/java/net/minecraftforge/fml/config/ModConfig.java
- https://raw.githubusercontent.com/MinecraftForge/MinecraftForge/1.20.x/fmlcore/src/main/java/net/minecraftforge/fml/config/ConfigFileTypeHandler.java
- https://raw.githubusercontent.com/neoforged/NeoForge/1.21.x/src/main/java/net/neoforged/neoforge/server/ServerLifecycleHooks.java
- https://raw.githubusercontent.com/neoforged/FancyModLoader/main/loader/src/main/java/net/neoforged/fml/config/ConfigTracker.java
- https://docs.fabricmc.net/develop/data-generation/setup
- https://minecraft.wiki/w/Data_pack
- https://www.minecraft.net/en-us/usage-guidelines
- https://support.curseforge.com/en/support/solutions/articles/9000197913-non-curseforge-mods

`minecraft-26-1-migration`:

- https://docs.fabricmc.net/develop/porting/
- https://docs.fabricmc.net/develop/porting/mappings/
- https://docs.fabricmc.net/develop/porting/fabric-api
- https://fabricmc.net/2026/03/14/261.html
- https://github.com/FabricMC/fabric-example-mod/branches
- https://docs.neoforged.net/docs/gettingstarted/
- https://neoforged.net/news/26.1release/
- https://github.com/neoforged/.github/blob/main/primers/26.1/index.md
- https://github.com/neoforged/ModDevGradle/blob/main/BREAKING_CHANGES.md
- https://github.com/NeoForgeMDKs/MDK-26.1-ModDevGradle
- https://www.minecraft.net/en-us/article/removing-obfuscation-in-java-edition
- https://github.com/cc-tweaked/CC-Tweaked/commit/8be5c2848484562185e300ecdd945d5628c4cfd9
- https://github.com/CaffeineMC/sodium/commit/eeed957a1c900ecfc09d1350eeec291a2fa1585d
- https://github.com/shedaniel/RoughlyEnoughItems/commit/14ba3b6d6825d72986a3984e7f4e7c1b356d750d
- https://github.com/shedaniel/RoughlyEnoughItems/commit/c022719540e9781e52cac85389b8e401d7e836ad
- https://github.com/architectury/architectury-api/commit/52b04952efaf77d11b42ce5fef716cd69120ac33
- https://github.com/Snownee/Jade/commit/7de912d5c29b25bf556d84e2165309dd4e497172

The migration skill was independently authored from official documentation and real-project port evidence. The package's `references/26.1-change-map-and-sources.md` is the authoritative complete provenance index for this skill, including all intervening release primers, Fabric API/Loader/Loom audit indexes, project branches, comparisons, PRs, and reviewed commits. Project ports are architectural examples rather than loader contracts; no project source or prose was copied.

`stonecutter-multiversion`:

- https://stonecutter.kikugie.dev/
- https://stonecutter.kikugie.dev/wiki/index
- https://stonecutter.kikugie.dev/wiki/start/
- https://stonecutter.kikugie.dev/wiki/start/settings
- https://stonecutter.kikugie.dev/wiki/start/builds
- https://stonecutter.kikugie.dev/wiki/start/comments
- https://stonecutter.kikugie.dev/wiki/config/settings
- https://stonecutter.kikugie.dev/wiki/config/controller
- https://stonecutter.kikugie.dev/wiki/config/build
- https://stonecutter.kikugie.dev/wiki/config/params
- https://stonecutter.kikugie.dev/wiki/config/properties
- https://stonecutter.kikugie.dev/wiki/config/handlers
- https://stonecutter.kikugie.dev/wiki/tips/multiloader
- https://stonecutter.kikugie.dev/wiki/tips/resource-processing
- https://stonecutter.kikugie.dev/wiki/tips/interface-injection
- https://stonecutter.kikugie.dev/wiki/faq
- https://stonecutter.kikugie.dev/blog/changes/0.9
- https://plugins.gradle.org/plugin/dev.kikugie.stonecutter
- https://codeberg.org/stonecutter/docs (reviewed at `5b34b7d2761fa1c9e13f776ba55750b3695bc146`)
- https://codeberg.org/stonecutter/stonecutter (reviewed at `fd815381d03457917ed849894b6350e15cc5fc92`)
- https://codeberg.org/stonecutter/template-fabric (reviewed at `c01bd28d4c590e2825924582527a660f2c2e45f6`)
- https://codeberg.org/stonecutter/template-neoforge (reviewed at `e7536b30e8e99cf2f7435d9062ce189c13a719e4`)
- https://codeberg.org/stonecutter/template-multiloader (reviewed at `a3d36a17322aa20e009c175e8ec908b237d7ccab`)

The Stonecutter skill was independently distilled from official documentation, current plugin source, and official template behavior. Documented task names and version-switch/reset semantics were smoke-tested with Stonecutter 0.9.7 and Gradle 9.6.1 in a disposable copy of the official Fabric template; no upstream prose or source was copied.

The 0.2.0 skill update checks Stonecutter 0.9.8 stable and 0.10-beta.1 prerelease against both Maven repositories on 2026-10-16. Release notes were read from `stonecutter/docs` commit `2f685fdf78a83c5453e007177b5e4dc4f14b29e6`, files `changelogs/stonecutter-0.9.md` and `changelogs/stonecutter-0.10.md`; stable source was inspected at `stonecutter/stonecutter` commit `73632f3266a1e81683dedb4a52168ec53c583442` and compared with published source JARs. Stable upgrade/build/switch checks were executed in Minecraft-Modding-Libs and TemplateProject. The 0.10 beta was researched, not adopted or runtime-verified. See the skill's release-and-migration-contracts reference for complete endpoints and limitations.

`modrinth-api`:

- https://docs.modrinth.com/api/
- https://docs.modrinth.com/api/operations/searchprojects/
- https://docs.modrinth.com/api/operations/getproject/
- https://docs.modrinth.com/api/operations/getprojectversions/
- https://docs.modrinth.com/api/operations/getversion/
- https://docs.modrinth.com/api/operations/getversions/
- https://docs.modrinth.com/api/operations/versionfromhash/
- https://docs.modrinth.com/api/operations/getlatestversionfromhash/
- https://docs.modrinth.com/api/operations/versionsfromhashes/
- https://docs.modrinth.com/api/operations/versionlist/

`testiarium-gametest`:

- https://github.com/SirEdvin/Minecraft-Modding-Libs/tree/main/projects/testiarium-core
- https://github.com/SirEdvin/Minecraft-Modding-Libs/tree/main/projects/testiarium-forge
- https://github.com/SirEdvin/Minecraft-Modding-Libs/tree/main/projects/testiarium-fabric

## Stonecutter documentation refresh (2026-09-06)

The 0.9.8 refresh adds independently distilled notes from these official pages:

- https://stonecutter.kikugie.dev/wiki/v2/
- https://stonecutter.kikugie.dev/wiki/v2/reference/gradle-api/structured-properties
- https://stonecutter.kikugie.dev/wiki/v2/reference/gradle-api/data-driven-setup
- https://stonecutter.kikugie.dev/wiki/v2/reference/gradle-api/project-controller
- https://stonecutter.kikugie.dev/wiki/v2/reference/syntax/replacements
- https://stonecutter.kikugie.dev/blog/changes/0.9
- https://plugins.gradle.org/plugin/dev.kikugie.stonecutter

The portal listed 0.9.8 while the live wiki described some 0.10 APIs. The package references explicitly version-gate those APIs and preserve disagreements between wiki and changelog rather than asserting unverified historical availability. Earlier source/template commit observations above remain historical; this refresh does not imply reinspection of those commits.

Refresh verification used a disposable Java-only fixture with Stonecutter 0.9.8, Gradle 9.6.1, and Java 21. Both nodes (1.20.1 and 1.21.1) compiled; JSON tree loading, merged structured properties, typed integer access, colon-path raw-list access, generated inactive sources, and named reversible string replacement were exercised. Separate refresh/switch/reset invocations succeeded, and the source round trip was byte-identical after initial comment normalization. Combining reset and build in one invocation failed Gradle implicit-dependency validation; separating them passed. Minecraft loader runtimes, publishing services, and forward-looking 0.10 APIs were not exercised.

## Stonecutter 0.10 refresh (2026-11-12)

The 0.3.0 skill update re-validates every version-sensitive statement against the stable 0.10 release and labels each one with its evidence level inside the package.

Published artifacts and upstream revisions read:

- https://plugins.gradle.org/m2/dev/kikugie/stonecutter/maven-metadata.xml and https://maven.kikugie.dev/releases/dev/kikugie/stonecutter/maven-metadata.xml (latest and release `0.10`); https://maven.kikugie.dev/snapshots/dev/kikugie/stonecutter/maven-metadata.xml (ends at `0.10-beta.4`)
- `stonecutter-0.10.module` (built with Gradle 9.8.2, `org.gradle.jvm.version` 25) and `stonecutter-0.10-sources.jar` (SHA-256 `d1c64c784875b8a148440eb1ebec49f53a43ee4ae7b3061a8417feef9e0e3692`); `stonecutter-0.9.8.module` (JVM 21) and its source JAR for the comparison column
- https://codeberg.org/stonecutter/docs at `b3b446df7f5c296202066f9ded738f3b13b7f48e`: `changelogs/stonecutter-0.10.md` and the versioned wiki snippets under `docs/wiki/v2/**/_versions/`
- https://codeberg.org/stonecutter/stonecutter at `8329ec273bcfa121d313613f5a2bd41f4ef34a25` (version bump to 0.10)
- https://codeberg.org/stonecutter/template-fabric at `c6212f2bb97a5382ed4ccb805eddd324bcec1cf7`, template-neoforge at `7ecc883c64f964390e8b026ca4a2d5bef9d547dc`, template-multiloader at `805360f1178e0721bbf062f7df04eeb1a0c689e1` (all pin 0.10 on Gradle 9.9.0)

Probe builds, all in disposable copies with `--no-daemon`:

- A two-node Java-only fixture with structured properties, a per-node `gradle.properties`, a full-file override, `#`-comment and comment-less resources, and a global string replacement. Run with 0.10 on Gradle 9.5.0/Java 21 and Gradle 9.5.0/Java 25 (both rejected with the requirement messages quoted in the package), Gradle 9.7.0/Java 25 and Gradle 9.9.1/Java 25 (passing); and with 0.9.8 on Gradle 9.5.0/Java 21 and Gradle 9.9.1/Java 25 for the comparison column. Exercised: project/task listing, all-node build, switch, refresh, reset, switch-plus-build in one invocation, active-node override collision, property fallback, deprecated accessors, default file formats, and node removal in wrong and right order.
- A two-tree fixture with a root branch and a `fabric` branch per tree (eight nodes), on 0.10 with Gradle 9.9.1/Java 25 and on 0.9.8 with Gradle 9.5.0/Java 21: node paths, branch IDs, cross-branch project dependency, all-node build, qualified versus unqualified switching, and reset.
- A scratch copy of a four-node flat Fabric/Forge/NeoForge template project moved to 0.10 on Gradle 9.9.1 with a Java 25 launcher: configuration, full build of all four nodes, and a switch/reset round trip. It needed one accessor edit and a newer loader-compatibility plugin; nothing was committed to that project.

Not exercised: Groovy DSL, Isolated Projects, custom file handlers, PCRE replacements, file disabling, IDE integration, game runtimes, and publication. Statements about those carry `[changelog]`, `[wiki]`, or `[unverified]` labels in the package.
