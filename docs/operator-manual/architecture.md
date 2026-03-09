# Architectural Overview

![Argo CD Architecture](../assets/argocd_architecture.png)

* Argo CD
  * == ⭐️Kubernetes controller⭐️ / 
    * CONTINUOUSLY monitors running applications
    * compares the current, live state vs desired target state (== | Git repo)
      * `OutOfSync` == deployed application's status / 's live state != target state
        * if it's `OutOfSync` -> Argo CD reports & visualizes the differences
      * if you modify the target state -> AUTOMATICALLY reflected | specified target environments
  * provide
    * facilities to AUTOMATICALLY OR MANUALLY sync the live state -- & -- desired target state

## Components

* goal
  * functional components
    * ❌!= Kubernetes objects❌

### API Server
* API server
  * == gRPC/REST server / exposes the API
  * responsibilities
    * application management & status reporting
    * invoke application operations
      * _Examples:_ sync, rollback, user-defined actions
    * repository & cluster credential management
      * stored -- as -- K8s secrets
    * authentication & auth delegation -- to -- external identity providers
    * RBAC enforcement
    * listener/forwarder -- for -- Git webhook events

* API
  * consumed by 
    * Web UI
    * CLI
    * CI/CD systems

### Repository Server
* repository server
  * == internal service /
    * maintains a local cache -- about the -- Git repository
    * hold the application manifests
  * responsible for
    * generating & returning the Kubernetes manifests
      * 's inputs
        * repository URL
        * revision (commit, tag, branch)
        * application path
        * template specific settings: parameters, helm values.yaml

### Application Controller
* application controller
  * == Kubernetes controller / 
    * continuously monitors running applications
    * compares the current, live state vs desired target state
      * desired target state 
        * specified | repo
  * detects `OutOfSync` application state
    * if it's out of sync -> OPTIONALLY takes corrective action
  * responsible for
    * invoking any user-defined hooks for lifecycle events (PreSync, Sync, PostSync)
