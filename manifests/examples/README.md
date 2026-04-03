# requirements
* download software / enable you to run local Kubernetes clusters
    * [Docker desktop](https://docs.docker.com/get-started/introduction/get-docker-desktop/)
    * [kind](https://kind.sigs.k8s.io/) + [install Kubectl](https://kubernetes.io/docs/tasks/tools/#kubectl)
    * [minikube](https://minikube.sigs.k8s.io/docs/)
        * `kubectl` commands are wrapped -- via -- `minikube kubectl`
    * [microk8s](https://canonical.com/microk8s)
        * `kubectl` commands are wrapped -- via -- `microk8s kubectl`
* run ⚠️2⚠️ local Kubernetes cluster
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
* [install Argo CD](../README.md)
  * ⚠️depending on EACH use case⚠️
* `kubectl port-forward svc/argocd-server -n argocd 8080:443`
  * port-forward "argocd-server" locally
* login
  * get initial admin password
    * `kubectl get secret argocd-initial-admin-secret -n argocd -o jsonpath='{.data.password}' | base64 -d` OR
    * `argocd admin initial-password -n argocd`
  * `argocd login localhost:8080 --insecure`
    * user: admin
    * password: pasteInitialAdminPassword

# Multi-Tenant
* install [Non-High Availability -- via -- 1! step](../README.md#---via----1-step)
  * steps
    * [here](../)
      * `kubectl create namespace argocd`
      * `kubectl apply --server-side --force-conflicts -f install.yaml -n argocd` 

## use cases: >1 application developer teams
### enables you configure (== set the pillars, != PRE configured)
#### RBAC model
* `kubectl get configmap argocd-rbac-cm -n argocd -o yaml`
  * exist
    * ALTHOUGH data is `{}`
#### OIDC authentication
* `kubectl get configmap argocd-cm -n argocd -o yaml`
  * exist
    * ALTHOUGH NO preconfiguration about OIDC -- `kubectl get configmap argocd-cm -n argocd -o jsonpath='{.data.oidc\.config}'` -- 
### can access Argo CD's API server -- via --
#### Web UI OR
* https://localhost:8080/applications
#### `argocd` CLI
* `argocd app list`

## Non-High Availability
### -- via -- 1! step
#### deploy applications |
##### SAME cluster / Argo CD runs
* follow [here](https://github.com/dancer1325/argocd-example-apps?tab=readme-ov-file#how-to-run-locally)
##### external clusters
* [here](/docs/operator-manual/cluster-management.md)
### -- via -- 2 steps
#### deploy applications |
##### SAME cluster / Argo CD runs
* follow [here](https://github.com/dancer1325/argocd-example-apps?tab=readme-ov-file#how-to-run-locally)
  * `helm install apps . --namespace randomname`
###### ❌NOT deployed DIRECTLY❌
* ways to check
  * `argocd app list`
    * check ALL Argo CD Applications' status == UNKNOWN
  * https://localhost:8080/applications 
    * 's left pannel's sync status == UNKNOWN
    * \> click | ANY 
      * 's sync status == UNKNOWN
      * app conditions == ERROR
###### requirements: specify inputted credentials
* TODO:
##### external clusters
TODO:

## High Availability
TODO:

# Core
* TODO: 