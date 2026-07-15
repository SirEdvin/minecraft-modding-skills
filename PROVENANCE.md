# Provenance And Sources

This repository's expanded coverage was inspired by reviewing the topic scope of `zerodegress/minecraft-modding-skills` at commit `ab38622536fb07c6b6aef0052ca77d2b059861a8`. That upstream repository did not declare a license at the time of review. No upstream text, examples, or line-by-line paraphrases were copied into this repository; the new material here was independently authored from official documentation, this repository's existing content, and observed project conventions.

## Official Documentation Used

`minecraft-fabric-modding`:

- https://docs.fabricmc.net/develop/
- https://docs.fabricmc.net/develop/loader/
- https://docs.fabricmc.net/develop/loom/
- https://docs.fabricmc.net/develop/networking
- https://docs.fabricmc.net/develop/data-generation/setup
- https://github.com/FabricMC/fabric-docs/tree/main/reference/latest

`minecraft-neoforge-modding`:

- https://docs.neoforged.net/docs/gettingstarted/
- https://docs.neoforged.net/docs/1.21.1/gettingstarted/
- https://docs.neoforged.net/docs/concepts/registries/
- https://docs.neoforged.net/docs/networking/
- https://docs.neoforged.net/docs/1.21.1/networking/
- https://docs.neoforged.net/docs/datastorage/attachments/
- https://docs.neoforged.net/docs/items/datacomponents/
- https://docs.neoforged.net/docs/resources/
- https://github.com/neoforged/ModDevGradle

`minecraft-legacy-forge-modding`:

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
