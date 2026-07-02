# modding-buildenv Conventions

`modding-buildenv` is SirEdvin's custom Gradle convention plugin repository. It currently publishes version `0.9.0` and wraps common Minecraft mod build concerns.

## Plugin IDs Seen in Consumers

- `site.siredvin.root`
- `site.siredvin.release`
- `site.siredvin.vanilla`
- `site.siredvin.fabric`
- `site.siredvin.forge`
- `site.siredvin.neoforge`
- `site.siredvin.publishing`
- `site.siredvin.mod-publishing`

## Convention Blocks

Preserve these blocks unless the task explicitly touches the buildenv itself:

- `baseShaking`
- `vanillaShaking`
- `fabricShaking`
- `forgeShaking`
- `neoforgeShaking`
- `publishingShaking`
- `modPublishing`

They carry loader flags, mappings, dependency buckets, generated metadata, publishing behavior, and mod distribution behavior.

## Repository and Plugin Resolution

Consumer repositories often use SirEdvin Maven:

```kotlin
maven("https://mvn.siredvin.site/minecraft") {
    name = "SirEdvin's Minecraft repository"
}
```

For NeoForge and ModDevGradle support, repository filters should include:

```kotlin
includeGroup("net.neoforged")
includeGroup("net.neoforged.moddev")
```

If CI cannot resolve custom plugin markers, use a plugin management resolution strategy:

```kotlin
resolutionStrategy {
    eachPlugin {
        if (requested.id.id.startsWith("site.siredvin.")) {
            useModule("site.siredvin:modding-buildenv:${requested.version}")
        }
    }
}
```

After buildenv 0.9.0, plugin markers may resolve directly, but the resolution strategy remains a useful CI fallback in consumers.

## Validation

For buildenv changes:

```bash
./gradlew --no-daemon check
./gradlew --no-daemon publishToMavenLocal
```

For consumer resolution changes:

```bash
./gradlew --no-daemon --refresh-dependencies help
./gradlew build --no-daemon
```

Publishing to the private Maven repository requires GitHub or local credentials. Do not publish or deploy unless the user explicitly asks.

GitHub repository secrets required for automated Maven publishing in `SirEdvin/modding-buildenv`:

- `SIR_EDVIN_MAVEN_USERNAME`
- `SIR_EDVIN_MAVEN_PASSWORD`
