# GTCEu authoritative sources and audit scope

Prefer matching released source over a moving wiki. DeepWiki/community examples
can help navigation but are not authoritative signatures.

- [Official addon template, reviewed commit](https://github.com/GregTechCEu/GregTech-Addon-Template/tree/19cc9032b50b378033f95e1e8e0de1ab4e3bf062): `gradle.properties`, `build.gradle`, `src/main/java/com/example/examplemod/ExampleMod.java`, `ExampleGTAddon.java`.
- [GTCEu 7.4.0 release source](https://github.com/GregTechCEu/GregTech-Modern/tree/07ac5207f6f58ba3a2f9cd8b862b382d24300a17): `src/main/java/com/gregtechceu/gtceu/api/data/chemical/material/Material.java`, `api/addon/IGTAddon.java`, `common/data/GTItems.java`, `common/data/GTRecipeTypes.java` beneath the same Java package root.
- [Later 1.20.1 source snapshot](https://github.com/GregTechCEu/GregTech-Modern/tree/4c30877e75544603615ff8b1647d9beabe03122c): `src/main/java/com/gregtechceu/gtceu/api/addon/IGTAddon.java`, `api/GTValues.java` beneath the same package root.
- [Official 1.20.1 wiki](https://gregtechceu.github.io/GregTech-Modern/1.20.1/).
- [GTCEu Maven](https://maven.gtceu.com).

The representative public Java repositories
[TemplateProject](https://github.com/SirEdvin/TemplateProject/tree/042d296e255d6a9e75e1d2f40da9937810e92004)
and [Minecraft-Modding-Libs](https://github.com/SirEdvin/Minecraft-Modding-Libs/tree/86bfe0b75d0dceb26e713a6c3bdcc91ec74eac2c)
were inspected through tracked paths and tracked-content searches for GTCEu,
GregTech, KubeJS, Packwiz, and Modrinth. Neither contains tracked GTCEu addon
integration at those commits. Their Java build layouts are not GTCEu usage proof;
the official addon template above is the applicable example. No game launch or
addon compilation was performed for this documentation audit.

## Retained community navigation (not signature evidence)

These original discovery links are retained, but were not independently audited
for compatibility or current availability. Match their target versions before
using examples; use pinned official source for signatures.

- DeepWiki navigation: https://deepwiki.com/GregTechCEu/GregTech-Modern
- GT Community Additions: https://github.com/mordgren/GTCA
- GregTech OreMiners: https://github.com/jimmybobjim/GregTech-OreMiners
- Community Discord: https://discord.gg/bWSWuYvURP
- CurseForge: https://www.curseforge.com/minecraft/mc-mods/gregtech-modern
- Modrinth: https://modrinth.com/mod/gregtechceu-modern
