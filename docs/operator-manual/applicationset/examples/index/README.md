# requirements
* download software / enable you to run local Kubernetes clusters
  * [Docker desktop](https://docs.docker.com/get-started/introduction/get-docker-desktop/)
  * [kind](https://kind.sigs.k8s.io/) + [install Kubectl](https://kubernetes.io/docs/tasks/tools/#kubectl)
  * [minikube](https://minikube.sigs.k8s.io/docs/)
    * `kubectl` commands are wrapped -- via -- `minikube kubectl`
  * [microk8s](https://canonical.com/microk8s)
    * `kubectl` commands are wrapped -- via -- `microk8s kubectl`
* run local Kubernetes cluster
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
* [install Argo CD](../../../installation.md)
* login
  * `kubectl get secret argocd-initial-admin-secret -n argocd -o jsonpath='{.data.password}' | base64 -d`
    * get initial admin password
  * `argocd login localhost:8080 --insecure`
    * user: admin
    * password: pasteInitialAdminPassword

# ApplicationSet controller
## == Kubernetes controller / support -- for -- `ApplicationSet` CRD 
* [create BEFORE an ApplicationSet](#parameter-substitution--applicationsets-spectemplate)
* `kubectl logs -n argocd -l app.kubernetes.io/name=argocd-application-controller | grep -i "reconcil"`
  * run reconciliation loop -> done -- by -- controller
## | Argo CD v2.3, ApplicationSet controller is bundled | Argo CD (== installed INDEPENDENTLY)
TODO:
## allows: | 1! Kubernetes manifest,
### target MULTIPLE Kubernetes clusters
* [applicationsetWhatAllow.yaml](applicationsetWhatAllow.yaml)
### 💡manage MULTIPLE Argo CD Applications 💡-- as a -- 1! unit
* [applicationsetWhatAllow.yaml](applicationsetWhatAllow.yaml)
### deploy MULTIPLE applications -- from -- >=1 Git repositories
* [applicationsetWhatAllow.yaml](applicationsetWhatAllow.yaml)

# Parameter substitution | ApplicationSet's `spec.template`
## use cases
### | ANY generator
TODO:
## allows: parameters / generated -- by a -- generator, can be substituted | `spec.template` -- via -- `{{parameter_name}}`
* `kubectl create namespace dev`
* `kubectl create namespace staging`
* `kubectl apply -n argocd -f applicationset.yaml`
  * `kubectl get applications -n argocd | grep guestbook`
    * 's return: ALL Applications'
    * `kubectl get all -n dev` && `kubectl get all -n staging`
      * 's return: 'No resources found ...'
      * Reason:🧠ArgoCD Application are OutOfSync🧠
        TODO:
  * `argocd app sync guestbook-dev` & `argocd app sync guestbook-staging`
    * `kubectl get all -n dev` && `kubectl get all -n staging`
      * 's return: deployment & services

## steps to processing it
TODO:
