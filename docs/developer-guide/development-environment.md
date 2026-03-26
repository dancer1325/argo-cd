# Setting Up the Development Environment

## install required tools

* [Git v2.0.0+](https://github.com/git-guides/install-git)   
* [Go](https://go.dev/doc/install/)
  * ways to check the version
    * see | [go.mod](/go.mod)
    * `go version`
* container runtime engine
  * [Docker v20.10.0+](https://docs.docker.com/engine/install/) OR 
  * [Podman v3.0.0+](https://podman.io/docs/installation)
* local k8s cluster
  * [Kind v0.11.0+](https://kind.sigs.k8s.io/docs/user/quick-start) OR
  * [Minikube v1.23.0+](https://minikube.sigs.k8s.io/docs/start) OR
  * [K3d v5.7.3+](https://k3d.io/stable/#quick-start)
* Kubernete client
  * [`kubectl`](https://kubernetes.io/docs/tasks/tools/#kubectl)


## install ADDITIONAL required development tools

```shell
make install-go-tools-local
make install-codegen-tools-local
```

## install latest Argo CD | your local cluster

```shell
kubectl create namespace argocd &&
kubectl apply -n argocd --server-side --force-conflicts -f https://raw.githubusercontent.com/argoproj/argo-cd/master/manifests/install.yaml

# set `kubectl` / points -- to -- `namespace=argocd`
#   Reason:🧠avoid specifying the namespace / every `kubectl` command🧠
kubectl config set-context --current --namespace=argocd
```
