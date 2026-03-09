# Overview

* audience
  * people / want to build third-party integrations OR contribute | Argo CD 
    * != Argo CD user

## Preface
* [Code Contribution Guide](code-contributions.md)
* [Code Contribution Preface](submit-your-pr.md#preface)

## Contributing to Argo CD documentation 

* steps
  * Fork & clone Argo CD repository
  * [Submit your PR](submit-your-pr.md) | this repo

## Contributing to Argo CD Notifications documentation

* steps
  * Fork & clone Argo CD repository
  * [Submit your PR](submit-your-pr.md) | ["notifications-engine" repo](https://github.com/argoproj/notifications-engine)
  * [Install Go](development-environment.md#install-go)
  * [Submit your PR](submit-your-pr.md) | this repo

## Contributing to Argo CD backend and frontend 

* [set up your development environment](development-environment.md)

TODO:
### Set up a development toolchain (local or virtualized)
- [Understand the differences between the toolchains](toolchain-guide.md#local-vs-virtualized-toolchain)
- Choose a development toolchain

    - Either [set up a local toolchain](toolchain-guide.md#setting-up-a-local-toolchain)
    - Or [set up a virtualized toolchain](toolchain-guide.md#setting-up-a-virtualized-toolchain)

### Perform the development cycle 
- [Set kubectl context to argocd namespace](development-cycle.md#set-kubectl-context-to-argocd-namespace)
- [Pull in all build dependencies](development-cycle.md#pull-in-all-build-dependencies)
- [Generate API glue code and other assets](development-cycle.md#generate-api-glue-code-and-other-assets)
- [Build your code and run unit tests](development-cycle.md#build-your-code-and-run-unit-tests)
- [Lint your code base](development-cycle.md#lint-your-code-base)
- [Run e2e tests](development-cycle.md#run-end-to-end-tests)
- How to contribute to documentation: [build and run documentation site](docs-site.md) on your machine for manual testing

- [Run Argo CD | your machine](running-locally.md)
- [Debug Argo CD | your machine](debugging-locally.md)
  
* [Submit your PR](submit-your-pr.md)

## Contributing to Argo CD dependencies
- [Contributing to argo-ui](dependencies.md#argo-ui-components-githubcomargoprojargo-ui)
- [Contributing to notifications-engine](dependencies.md#notifications-engine-githubcomargoprojnotifications-engine)

## Extensions and Third-Party Applications
* [UI Extensions](extensions/ui-extensions.md)
* [Proxy Extensions](extensions/proxy-extensions.md)
* [Config Management Plugins](../operator-manual/config-management-plugins.md)

## Contributing to Argo Website
The Argo website is maintained in the [argo-site](https://github.com/argoproj/argo-site) repository.
