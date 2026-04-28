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
* `kubectl create namespace integrationfirst` && `kubectl create namespace integrationtwo` 

# ApplicationSet controller
## 's responsibility: ensure that the `Application`S remain consistent -- with -- the defined declarative `ApplicationSet` resource
* `kubectl apply -f applicationset.yaml`
* `argocd app sync guestbook-integrationfirst` && `argocd app sync guestbook-integrationtwo`
  * sync BOTH
* `kubectl logs -n argocd -l app.kubernetes.io/name=argocd-applicationset-controller --tail=50`
  * check logs talk ONLY about Application
* `kubectl patch application guestbook-integrationfirst -n argocd --type merge -p '{"spec":{"source":{"path":"helm-guestbook"}}}'`
  * `kubectl logs -n argocd -l app.kubernetes.io/name=argocd-applicationset-controller --tail=50`
    * check last RECENT logs talk about generation of Application
* `kubectl patch application guestbook-integrationtwo -n argocd --type merge -p '{"spec":{"source":{"path":"helm-guestbook"}}}'`
  * `kubectl logs -n argocd -l app.kubernetes.io/name=argocd-applicationset-controller --tail=50`
    * check last RECENT logs talk about generation of Application
## ⚠️limitations⚠️
### ONLY connect -- to the -- cluster | Argo CD is deployed to
TODO:
### ONLY interact -- with -- namespace | Argo CD is deployed
TODO:

# Argo CD itself
## 's responsibility: deploy -- , based on the Git repository, -- the generated child `Application` resources
TODO: 

