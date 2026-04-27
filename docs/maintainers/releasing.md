# Releasing agentic

This is the short, practical version.

`agentic` publishes through GitHub Actions using PyPI Trusted Publishing. That means no long-lived PyPI API token needs to live in GitHub secrets.

## What is automated

The release workflow:

- runs tests
- runs `agentic architecture check --project-root .`
- validates the TypeScript and PHP extractors
- builds `sdist` and `wheel`
- checks package metadata with `twine check`
- smoke-installs the built wheel
- attaches the built artifacts to the GitHub release
- publishes to TestPyPI for prereleases
- publishes to PyPI for normal releases

## One-time PyPI setup

Trusted Publishing still needs one manual trust relationship on the package index side.

For PyPI:

1. Open the `agentic-oss` project on PyPI.
2. Go to `Publishing`.
3. Add a trusted publisher with:
   - owner: `9orky`
   - repository: `agentic`
   - workflow name: `release.yml`
   - environment name: `pypi`

For TestPyPI, repeat the same process with environment name `testpypi`.

The relevant workflow file is:

- `.github/workflows/release.yml`

This is the one required manual step. After that, GitHub Actions mints short-lived OIDC credentials automatically during release jobs.

## Release flow

### Stable release

1. Update `CHANGELOG.md`.
2. Create an annotated Git tag in the form `vX.Y.Z`.
3. Create a GitHub release from that tag.
4. Mark it as a normal release.

That triggers:

- GitHub release asset upload
- PyPI publish

### Prerelease

1. Create an annotated prerelease tag in the form `vX.Y.Zrc1`, `vX.Y.Zb1`, or similar.
2. Create a GitHub release from that tag.
3. Mark it as a prerelease.

That triggers:

- GitHub release asset upload
- TestPyPI publish

## Notes

- `workflow_dispatch` is available for dry runs of the release pipeline without publishing.
- If publishing fails before the upload step, GitHub release assets are still preserved for inspection.
- If you change the package name or repository owner, update both `pyproject.toml` metadata and the Trusted Publisher settings on PyPI/TestPyPI.
- Package version is derived from Git tags through `setuptools-scm`, not hardcoded in `pyproject.toml`.

## Common failure: invalid-publisher

If PyPI responds with `invalid-publisher`, check these first:

- the PyPI project name matches the distribution name in `pyproject.toml`
- the trusted publisher points to:
  - owner `9orky`
  - repo `agentic`
  - workflow `release.yml`
  - environment `pypi` or `testpypi`
- the release tag matches the version that `setuptools-scm` derives, for example `v0.1.0`

If PyPI says the project already exists and you do not control it, then the package name is taken.

In that case, Trusted Publishing cannot be fixed on the GitHub side alone. You must either:

- publish under a different distribution name, or
- gain maintainer access to the existing PyPI project

The console command can still remain `agentic` even if the PyPI distribution name changes.
