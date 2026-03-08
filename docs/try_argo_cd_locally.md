# Try Argo CD Locally

* goal
  * install `Kind`
  * set up `Kind` -- with -- Argo CD

* requirements
  * [how to run Argo CD development environment locally](./developer-guide/running-locally.md)

## Install Kind

* follow [Kind quick-start](https://kind.sigs.k8s.io/docs/user/quick-start#installation)

##  Create a Kind Cluster

```bash
# create a local Kubernetes cluster / name = "argocd-cluster" 
kind create cluster --name argocd-cluster
```

## Set Up kubectl / use the Kind Cluster

```bash
kubectl cluster-info --context kind-argocd-cluster
```

## Quick Start

* [here](examples/gettingStarted/README.md#quick-start)
