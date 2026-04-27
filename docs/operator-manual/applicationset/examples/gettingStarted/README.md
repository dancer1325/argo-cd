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

# ways to install ApplicationSet controller
## | Argo CD v2.3+, ALREADY part of Argo CD
* follow the steps
* `kubectl get crd`
  * check ALSO returns "applicationsets.argoproj.io"

## | Argo CD v2.3-, install ApplicationSet
* TODO:
### Kubernetes manifests / require the ApplicationSet controller
#### | [manifests/install.yaml](/manifests/install.yaml)
* see the Kubernetes resources / depend on it

# how to enable high availability mode?
## Reason:🧠[HA](/manifests/ha/install.yaml) do NOT configure ApplicationSet as HA🧠
* check | [HA](/manifests/ha/install.yaml) / "argocd-applicationset-controller" deployment has replicas: 1
## steps
* `kubectl get deployment/argocd-applicationset-controller -n argocd`
  * 's return: 1! deployment
* `kubectl patch deployment argocd-applicationset-controller -n argocd --type json --patch-file patchEnableApplicationSetAsHA.yaml`
  * `kubectl get deployment/argocd-applicationset-controller -n argocd`
    * 's return: 2 deploymentS
  * `kubectl get deployment argocd-applicationset-controller -n argocd -o jsonpath='{.spec.template.spec.containers[0].args}'`
    * 's return: --enable-leader-election=true

# TODO:
* TODO: