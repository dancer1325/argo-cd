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

# Refresh
## compare the desired state vs live state
* `kubectl apply -f argoCDCMDParamsCMPatch.yaml`
  * Reason: 🧠see controller debug level logs🧠
* `kubectl -n argocd rollout restart statefulset argocd-application-controller`
* `kubectl apply -f application.yaml`
* [steps to trigger refresh](https://github.com/dancer1325/argocd-example-apps/tree/master/guestbook#refresh)
* `kubectl logs -n argocd argocd-application-controller-0 | grep "example.guestbook"`
  * look for "refresh" & latest log about that time and you can see
    * "Comparing app state"
    * "Ignoring change of object because none of the watched resource fields have changed"
### desired state, FIRSTLY, checked | repo-server
* `kubectl logs -n argocd argocd-application-controller-0 | grep "example.guestbook"`
  * look for "refresh" & latest log about that time and you can see
    * NO message about fetching Git
* `kubectl logs -n argocd deployment/argocd-repo-server | grep "git "`
  * there are NO recent logs

# Hard Refresh
## invalidate EXISTING desired state | repo-server
* `kubectl apply -f argoCDCMDParamsCMPatch.yaml`
  * Reason: 🧠see controller debug level logs🧠
* `kubectl -n argocd rollout restart statefulset argocd-application-controller`
* [steps to trigger hard refresh](https://github.com/dancer1325/argocd-example-apps/tree/master/guestbook#hard-refresh)
* `kubectl logs -n argocd argocd-application-controller-0 | grep "example.guestbook"`
  * look for "refresh" & latest log about that time and you can see
    * "noCache is true"
    * "useDiffCache":"false"
## fetch Git
* `kubectl logs -n argocd deployment/argocd-repo-server | grep "git "`
  * look for latest ones and you can see
    * "git checkout --force"

# Sync
## == process / application is moved -- to -- its target state
* PREVIOUS application's sync status: outOfSync
* [here](https://github.com/dancer1325/argocd-example-apps/blob/master/guestbook/README.md#sync-status--sync-live-state-vs-target-state)

# Sync Status
## | sync, live state vs target state
* [here](https://github.com/dancer1325/argocd-example-apps/blob/master/guestbook/README.md#sync-status--sync-live-state-vs-target-state)

# Sync Operation Status
## ALLOWED values: syncing, sync ok, sync error, sync failed, unknown 
* [here](https://github.com/dancer1325/argocd-example-apps/tree/master/guestbook#sync-operation-status-allowed-values-syncing-sync-ok-sync-error-sync-failed-unknown)

# Health
## == application's health
* [here](https://github.com/dancer1325/argocd-example-apps/tree/master/guestbook#health--applications-health)

# Tool
* [here](#application-source-type)