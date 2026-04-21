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
* [install Argo CD](../../installation.md)

# Introduction
## control plane's namespace, by default, "argocd"
* `kubectl get all -n argocd`
  * check ArgoCD is installed here
* `kubectl get applications -n argocd`
  * check ArgoCD Applications are installed here
## enable
### ordinary Argo CD users
#### can manage ArgoCD Applications
TODO:
#### can configure notifications / Argo CD application | specific namespace
TODO: 

# requirements
TODO:



# TODO:

# how to manage applications | OTHER namespaces?
## declaratively
TODO: 
## -- via -- `argocd` CL
```bash
# Create an application "foo" | "bar" namespace
argocd app create foo/bartwo ...

# Sync the application "foo" | "bar" namespace
argocd app sync foo/bar

# Retrieve application's manifest  "foo" | "bar" namespace
argocd app manifests foo/bar

# Delete the application "foo" | "bar" namespace
argocd app delete foo/bar
```
* Problems:
  * Problem1: "{"level":"fatal","msg":"rpc error: code = InvalidArgument desc = app is not allowed in project \"\", or the project does not exist""
    * Solution: TODO:

## -- via -- ArgoCD UI
* | browser,
  * https://localhost:8080,
    * user: admin
    * pass:
    * \> NEW APP,
      * General
        * app name: foo
        * Auto-Create Namespace: true
      * Source
        * Repository URL: https://github.com/dancer1325/argocd-example-apps
        * Path: guestbook
      * Destination
        * Cluster URL: https://kubernetes.default.svc
        * Namespace: bar
      * Create

