# Architectural Overview

![Argo CD Architecture](../assets/argocd_architecture.png)

## Components

* goal
  * functional components
    * ❌!= Kubernetes objects❌

### API Server
* API server
  * == gRPC/REST server / exposes the API
  * responsibilities
    * application management & status reporting
      * _Examples of management:_ create, delete, sync, rollback, user-defined actions
    * repository & cluster credential management
      * stored -- as -- K8s secrets
    * delegate authentication & auth -- to -- external identity providers
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
    * CONTINUOUSLY monitors running applications
    * compares the current, live state vs desired target state (== | Git repo)
  * detects `OutOfSync` application state
    * OPTIONALLY takes corrective action
    * == deployed application's status / 's live state != target state
  * responsible for
    * invoking any user-defined hooks for lifecycle events (PreSync, Sync, PostSync)
