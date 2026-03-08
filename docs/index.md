# Overview

## How it works

* Application deployments
  * can track updates |
    * branches,
    * tags,
    * specific version of manifests | Git commit
* [tracking strategies](user-guide/tracking_strategies.md)

* [demo video](https://youtu.be/aWDIQMbp1cc?t=1m4s)

## Architecture

![Argo CD Architecture](assets/argocd_architecture.png)
TODO:

Argo CD is implemented as a Kubernetes controller which continuously monitors running applications
and compares the current, live state against the desired target state (as specified in the Git repo).
A deployed application whose live state deviates from the target state is considered `OutOfSync`.
Argo CD reports & visualizes the differences, while providing facilities to automatically or
manually sync the live state back to the desired target state
* Any modifications made to the desired
target state in the Git repo can be automatically applied and reflected in the specified target
environments.

For additional details, see [architecture overview](operator-manual/architecture.md).

## Features

* AUTOMATED deployment of applications -- to -- specified target environments
* Support for multiple config management/templating tools (Kustomize, Helm, Jsonnet, plain-YAML)
* Ability to manage and deploy to multiple clusters
* SSO Integration (OIDC, OAuth2, LDAP, SAML 2.0, GitHub, GitLab, Microsoft, LinkedIn)
* Multi-tenancy and RBAC policies for authorization
* Rollback/Roll-anywhere to any application configuration committed in Git repository
* Health status analysis of application resources
* Automated configuration drift detection and visualization
* Automated or manual syncing of applications to its desired state
* Web UI which provides real-time view of application activity
* CLI for automation and CI integration
* Webhook integration (GitHub, BitBucket, GitLab)
* Access tokens for automation
* PreSync, Sync, PostSync hooks to support complex application rollouts (e.g. blue/green & canary upgrades)
* Audit trails for application events and API calls
* Prometheus metrics
* Parameter overrides for overriding helm parameters in Git
