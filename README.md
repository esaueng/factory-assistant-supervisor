# Factory Assistant Supervisor

Factory Assistant Supervisor is a container-based system for managing the
Factory Assistant Core installation and related applications. It communicates
with the rest of the appliance and provides an API to manage the installation —
including changing network settings or installing and updating software.

Factory Assistant is based on Home Assistant.

## Installation

Factory Assistant Supervisor ships as part of Factory Assistant OS. See the
[Factory Assistant OS](https://github.com/esaueng/FactoryAssistantOS) repository
for build and installation instructions.

## Development

For small changes and bugfixes you can just follow this, but for significant
changes open an RFC first. This fork tracks the upstream Home Assistant
Supervisor, so the upstream [development instructions][development] apply to the
codebase.

## Release

Releases are done in 3 stages (channels) with this structure:

1. Pull requests are merged to the `main` branch.
2. A new build is pushed to the `dev` stage.
3. Releases are published.
4. A new build is pushed to the `beta` stage.
5. The [channel file][stable] is updated.
6. The build that was pushed to `beta` will now be pushed to `stable`.

[development]: https://developers.home-assistant.io/docs/supervisor/development
[stable]: https://esaueng.github.io/FactoryAssistantOS/stable.json
