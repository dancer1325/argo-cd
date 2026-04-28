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
* `kubectl create namespace notpreserve` && `kubectl create namespace preserve` 

# if Application is created -- via -- an `ApplicationSet` -> ALL `Application` contain
## `.metadata.ownerReferences`
* `kubectl apply -f applicationsetPreserveResources.yaml`
* login with the admin
  * `argocd login localhost:8080 --insecure`
    * username: admin
    * password: <GOT_IT_FROM_kubectl get secret argocd-initial-admin-secret -n argocd -o jsonpath='{.data.password}' | base64 -d>
* sync Application
  * `argocd app sync guestbook-preserve` && `argocd app sync guestbook-notpreserve`
* check Application contain the ApplicationSet reference
  * `kubectl get application guestbook-preserve -n argocd -o jsonpath='{.metadata.ownerReferences}'` &
    * 's return
      * parent ApplicationSet
  * `kubectl get application guestbook-notpreserve -n argocd -o jsonpath='{.metadata.ownerReferences}'`
    * 's return
      * parent ApplicationSet
## & if `.syncPolicy.preserveResourcesOnDeletion` = `false` -> `.metadata.finalizers` == `resources-finalizer.argocd.argoproj.io`
* "guestbook-notpreserve-resources" ApplicationSet
  * has `.spec.syncPolicy.preserveResourcesOnDeletion: false`
  * `kubectl get application guestbook-notpreserve -n argocd -o jsonpath='{.metadata.finalizers}'`
    * 's return
      * `["resources-finalizer.argocd.argoproj.io"]`
* "guestbook-preserve-resources" ApplicationSet
  * has `.spec.syncPolicy.preserveResourcesOnDeletion: true`
  * `kubectl get application guestbook-preserve -n argocd -o jsonpath='{.metadata.finalizers}'`
    * 's return
      * NOTHING

# if you delete an ApplicationSet ->
* `argocd appset delete guestbook-notpreserve-resources`
## `ApplicationSet` resource itself is deleted
* `argocd appset delete guestbook-notpreserve-resources`
  * `argocd appset get guestbook-notpreserve-resources` returns "not found"
## `Application` resources / were created -- from -- this `ApplicationSet` -> will be deleted
* `argocd app get guestbook-notpreserve` && `argocd app get guestbook-preserve` 
  * 's return: PermissionDenied
    * TODO: why?
* `kubectl get application -n argocd | grep guestbook-notpreserve` && `kubectl get application -n argocd | grep guestbook-preserve` 
  * 's return: NOTHING
## ⚠️ANY deployed resources  | managed cluster / were created -- from -- that `Application` resource -> will be deleted⚠️
* `kubectl get all -n notpreserve`
  * 's return: NOTHING
### 💡if you want to preserve them -> | ApplicationSet, set `.syncPolicy.preserveResourcesOnDeletion` == true 💡
* `kubectl get all  -n preserve`
  * 's return: resources
