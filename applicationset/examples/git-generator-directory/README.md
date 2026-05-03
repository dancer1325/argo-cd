* notice this path's structure

```
├── cluster-addons
│   ├── argo-workflows
│   │   └── kustomization.yaml
│   └── prometheus-operator
│   |   ├── Chart.yaml
│   |   ├── requirements.yaml
│   |   └── values.yaml
│   └── cert-manager
│       ├── Chart.yaml
│       ├── requirements.yaml
│       └── values.yaml
├── excludes
│   ├── cluster-addons
│   │   ├── argo-workflows
│   │   │   └── kustomization.yaml
│   │   ├── exclude-helm-guestbook
│   │   │   ├── Chart.yaml
│   │   │   ├── templates/
│   │   │   ├── values-production.yaml
│   │   │   └── values.yaml
│   │   └── prometheus-operator
│   │       ├── Chart.yaml
│   │       ├── requirements.yaml
│   │       └── values.yaml
│   ├── git-directories-exclude-example-fasttemplate.yaml
│   └── git-directories-exclude-example.yaml
├── git-directories-example-fasttemplate.yaml
└── git-directories-example.yaml
```
  * 1 directory / EACH workload -- to -- deploy
    * [Argo Workflow controller](cluster-addons/argo-workflows)
    * [Prometheus Operator Helm chart](cluster-addons/prometheus-operator)
  * [cert-manager](cluster-addons/cert-manager/)
    * added to test, ApplicationSet controller detection

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

# how to run locally?
* `kubectl apply -f git-directories-example.yaml`
* `argocd app list`
  * 1 Application / EACH folder | `generators[git].directories.path`