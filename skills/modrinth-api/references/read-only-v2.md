# Modrinth Read-Only API v2

Official sources used for this reference:

- API overview: https://docs.modrinth.com/api/
- Search projects: https://docs.modrinth.com/api/operations/searchprojects/
- Get project: https://docs.modrinth.com/api/operations/getproject/
- List project's versions: https://docs.modrinth.com/api/operations/getprojectversions/
- Get version: https://docs.modrinth.com/api/operations/getversion/
- Get multiple versions: https://docs.modrinth.com/api/operations/getversions/
- Get version from hash: https://docs.modrinth.com/api/operations/versionfromhash/
- Latest version from hash/loaders/game versions: https://docs.modrinth.com/api/operations/getlatestversionfromhash/
- Get versions from hashes: https://docs.modrinth.com/api/operations/versionsfromhashes/
- Tags and game versions: https://docs.modrinth.com/api/operations/versionlist/

## Base Request Rules

- Production base URL: `https://api.modrinth.com/v2`.
- Required header: a uniquely identifying `User-Agent`.
- Most read-only public endpoints do not require authentication.
- Watch `X-Ratelimit-Limit`, `X-Ratelimit-Remaining`, and `X-Ratelimit-Reset`.

## Search

- Endpoint: `GET /search`.
- Documented query parameters include `query`, `facets`, `index`, `offset`, and `limit`.
- Loader filters are commonly category facets such as `categories:fabric` or `categories:forge`.
- Minecraft version filters use `versions:<version>`.
- Project type filters use `project_type:mod`, `project_type:modpack`, and related documented values.

## Project Versions

- Endpoint: `GET /project/{id|slug}/version`.
- Documented query parameters: `loaders`, `game_versions`, `featured`, `include_changelog`.
- The official docs do not document `limit` or `offset` for this endpoint. Do not add them to generated clients or guidance unless the official operation docs change.

## File Lookup And Verification

- Endpoint: `GET /version_file/{hash}` with required `algorithm` (`sha1` or `sha512`).
- Batch endpoints exist for multiple hashes; use them when checking many files.
- Version file metadata includes `url`, `filename`, `primary`, `size`, and `hashes`.
- Download to a temporary/cache path, compute the documented hash over bytes, then move/use the file only after the digest matches.

## Source Lookup

- Store stable project IDs rather than slugs when persisting results; slugs can change.
- To locate source links, read project metadata fields returned by `GET /project/{id|slug}` and verify the repository/link is present for that project.
