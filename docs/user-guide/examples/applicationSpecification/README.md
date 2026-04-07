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
* [install Argo CD](/docs/examples/gettingStarted/README.md)

# check Argo CD Application Specification
## source - git repo -- [this Argo CD Application](/docs/operator-manual/examples/application.yaml)
* | [this path](/docs/operator-manual/examples),
  * `kubectl apply -f application.yaml`
    * Notes: "Warning: metadata.finalizers: "resources-finalizer.argocd.argoproj.io":"
      * Reason:🧠# 1. OFFICIAL value, ALTHOUGH NOT follow strictly Kubernetes conventions: domain/name🧠
* TODO: 

## TODO: 