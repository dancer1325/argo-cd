# requirements
* download software / enable you to run local Kubernetes clusters
  * [Docker desktop](https://docs.docker.com/get-started/introduction/get-docker-desktop/)
  * [kind](https://kind.sigs.k8s.io/) + [install Kubectl](https://kubernetes.io/docs/tasks/tools/#kubectl)
  * [minikube](https://minikube.sigs.k8s.io/docs/)
    * `kubectl` commands are wrapped -- via -- `minikube kubectl`
  * [microk8s](https://canonical.com/microk8s)
    * `kubectl` commands are wrapped -- via -- `microk8s kubectl`
* run a local Kubernetes cluster
  * -- via --
    * [Docker Desktop](https://docs.docker.com/desktop/use-desktop/kubernetes/#enable-kubernetes)
      * | Docker Desktop
        * Kubernetes > Create cluster > choose any cluster type
    * [Kind](https://kind.sigs.k8s.io/#installation-and-usage)
      * `kind create cluster`
    * minikube
      * `minikube start`
    * microk8s
  * `kubectl config current-context`
    * check Kubectl points to a context
* [install Argo CD](../../operator-manual/installation.md)

# Application
## == CRD 
* PREVIOUS to install Argo CD
  * `kubectl get crd`
    * NO resources found
  * `kubectl get application`
    * "error: the server doesn't have a resource type "application"
* [install Argo CD](../../operator-manual/installation.md)
  * `kubectl get crd` 
    * return installed Argo CD CRD
  * `kubectl get application`
    * "No resources found in default namespace."

### == group Kubernetes resources / defined -- by a -- manifest
* [demo](https://cd.apps.argoproj.io/applications/argocd/example.guestbook?view=tree&resource=)

# Application Source Type
## == tool / used -- to -- build the application
* [here](../../user-guide/examples/applicationSources)

# ApplicationSet
## == CRD
* PREVIOUS to install Argo CD
  * `kubectl get crd`
    * NO resources found
  * `kubectl get applicationset`
    * "error: the server doesn't have a resource type "application"
* [install Argo CD](../../operator-manual/installation.md)
  * `kubectl get crd`
    * return installed Argo CD CRD
  * `kubectl get application`
    * "No resources found in default namespace."
### FROM 1! Argo CD Application template, generate -- , via generators, -- MULTIPLE Applications
* [here](../../operator-manual/applicationset/examples/index)

# Project
## == CRD
* PREVIOUS to install Argo CD
  * `kubectl get crd`
    * NO resources found
  * `kubectl get appproject`
    * "error: the server doesn't have a resource type " appproject"
* [install Argo CD](../../operator-manual/installation.md)
  * `kubectl get crd`
    * return installed Argo CD CRD
  * `kubectl get application`
    * "default" one
### group Argo CD ApplicationS
* [demo / default project](https://cd.apps.argoproj.io/applications?proj=default&sync=&autoSync=&health=&namespace=&cluster=&labels=&annotations=&operation=)
* [demo / sync project](https://cd.apps.argoproj.io/applications?proj=sync&sync=&autoSync=&health=&namespace=&cluster=&labels=&annotations=&operation=)

# Target State
## == files | Git repository
* [ANY folder / EXCEPT TO apps](https://github.com/dancer1325/argocd-example-apps)

# Live State
## application's state | cluster
* [here](https://github.com/dancer1325/argocd-example-apps/tree/master/guestbook#applications-state--cluster)

# Sync
## == process / application is moved -- to -- its target state
* TODO: 

# Sync Status
## | sync, live state vs target state
* [here](https://github.com/dancer1325/argocd-example-apps/blob/master/guestbook/README.md#sync-status--sync-live-state-vs-target-state)

# Sync Operation Status
## ALLOWED values: syncing, sync ok, sync error, sync failed, unknown 
* [here](https://github.com/dancer1325/argocd-example-apps/tree/master/guestbook#sync-operation-status-allowed-values-syncing-sync-ok-sync-error-sync-failed-unknown)

# Refresh
## compare the latest code | Git vs live state
* TODO:

# Health
## == application's health
* [here](https://github.com/dancer1325/argocd-example-apps/tree/master/guestbook#health--applications-health)

# Tool
* [here](#application-source-type)