# Overview

* [index](/mkdocs.yml)'s `nav`

TODO: check if to refactor

## how does it work?

* Application deployments
  * can track updates |
    * branches,
    * tags,
    * specific version of manifests | Git commit
* [tracking strategies](user-guide/tracking_strategies.md)

* [demo video](https://youtu.be/aWDIQMbp1cc?t=1m4s)
  * TODO:

## Features

* allows
  * manage & deploy AUTOMATICALLY applications -- to -- specified MULTIPLE clusters
  * Rollback/Roll-anywhere -- to -- any application configuration / committed | Git repository
* support
  * MULTIPLE config management/templating tools
    * Kustomize, Helm, Jsonnet, plain-YAML
  * about authentication
    * SSO Integration 
      * OIDC, OAuth2, LDAP, SAML 2.0, GitHub, GitLab, Microsoft, LinkedIn
  * about authorization
    * Multi-tenancy 
    * RBAC policies
  * TODO: extensible   -- NO duplicated with some PREVIOUS one ? -- 
* provide
  * application resources' health status analysis 
  * AUTOMATED configuration drift detection and visualization
  * AUTOMATED or MANUAL syncing of applications -- to -- its desired state
  * Web UI 
    * real-time view of application activity
  * CLI 
    * uses
      * automation
      * CI integration
  * Webhook integration
    * GitHub, BitBucket, GitLab
  * Access tokens 
    * for automation
  * PreSync, Sync, PostSync hooks 
    * -- to -- support complex application rollouts (e.g. blue/green & canary upgrades)
  * Audit trails
    * -- for -- application events & API calls
  * [Prometheus metrics](operator-manual/metrics.md)
  * Parameter overrides
    * -- for -- overriding helm parameters | Git
