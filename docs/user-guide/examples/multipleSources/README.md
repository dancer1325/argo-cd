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
* [install Argo CD cluster-scoped](../installation.md)
* [deploy these Applications](https://github.com/dancer1325/argocd-example-apps/tree/master/apps)

# Argo CD application == link BETWEEN
## 1! source -- & -- 1 Application
* [here](https://github.com/dancer1325/argocd-example-apps/blob/master/apps/templates/applications.yaml) 
## 👀\>1 sourceS -- & -- 1 Application👀
* [here](application.yaml)
* `kubectl apply -f application.yaml`
* `argocd app get multiple-sources-app`
    * 's return: MULTIPLE group resources to deploy
* `argocd app sync multiple-sources-app`
  * MULTIPLE Application are sync
### how does it work?
#### Argo CD compiles ALL the sources == generate SEPARATELY the manifests / EACH source
* `argocd app get multiple-sources-app`
  * 's return: MULTIPLE group resources to deploy
### if you specify `spec.sources` -> Argo CD ignores `spec.source`
* `argocd app get multiple-sources-app`
  * 's return: ONLY `.sources`, NOT `.source`

# if MULTIPLE sources produce the SAME resource (== SAME `group`, `kind`, `name`, and `namespace`) ->
## the last source to produce the resource take precedence
* `kubectl apply -f application.yaml`
* `argocd app get multiple-sources-which-produce-sameresource-app`
  * 's return: ONLY 1! Deployment + 1! Service
## `RepeatedResourceWarning` is produced
* `argocd app get multiple-sources-which-produce-sameresource-app`
  * 's return: CONDITION TRANSITION: "RepeatedResourceWarning ...."

# how to configure the ArgoCD Application?
* `kubectl apply -f applicationHelmSplittedValues.yaml`
* `argocd app get helm-guestbook-valuesfiles-differentrepo`
* `argocd app sync helm-guestbook-valuesfiles-differentrepo`
* `kubectl get svc -n helm-guestbook-valuesfiles-differentrepo`
  * 's return: ClusterIP
    * == value / specified | [values-production.yaml](values-production.yaml)