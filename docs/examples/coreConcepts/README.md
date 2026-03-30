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

### == group of Kubernetes resources / defined -- by a -- manifest
* ways to check
  * [here](/manifests/crds/application-crd.yaml)
    * group
      * Reason: 🧠define `spec.group`🧠
  * AFTER installing Argo CD
    * `kubectl get crd`
      * check ALL CRDs / SAME group
        * Reason: 🧠NAME == `specName.groupName`🧠

# Application Source Type
## == tool / used -- to -- build the application
* [here](../../user-guide/examples/applicationSources)

# Target State

The desired state of an application, represented as files in a Git repository.

# Live State

The current live state of the application running in the cluster.

# Sync Status

The comparison between the live state and the target state, indicating whether they match.

# Sync

The process of moving an application to its target state, ensuring the live state matches the desired state.

# Sync Operation Status

The result of a sync operation. Allowed values:
- succeeded
- failed

# Refresh

The process of comparing the latest code in Git against the live state in the cluster.

# Health

The health status of an application, indicating:
- Is it running correctly?
- Can it serve requests?

# Tool
* [here](#application-source-type)