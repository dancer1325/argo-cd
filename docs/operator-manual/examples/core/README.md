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

# Introduction
## == runs Argo CD / headless mode (== WITHOUT UI)
* [install](#how-to-install)
* `kubectl get pod -n argocd | grep "argocd-server"`
  * ❌NO "argocd-server"❌
    * -> NO UI
## features
### AVAILABLE GitOps functionality
* [here](https://github.com/dancer1325/argocd-example-apps/blob/master/guestbook/README.md#how-to-check-its-tracked)
### ❌NOT AVAILABLE❌
#### Argo CD RBAC model
##### == ANY command / require RBAC, does NOT work
* `argocd proj list --core` fails
#### Argo CD API 
* `kubectl get pods -n argocd | grep argocd-server`
  * NOTHING is returned
#### Argo CD Notification Controller
* `kubectl get pods -n argocd | grep controller`
  * NO notification controller appears
#### OIDC based authentication
* `argocd login localhost:8080 --sso` fails
#### TODO:
TODO:
### partially available
* [here](#how-to-use-)
## use cases
### ONLY rely on
#### Kubernetes RBAC
* `kubectl create serviceaccount test-user -n argocd`
* `kubectl auth can-i list applications.argoproj.io --as=system:serviceaccount:argocd:test-user -n argocd`
  * 's return == No
* `kubectl create clusterrolebinding test-user-binding --clusterrole=argocd-application-controller --serviceaccount=argocd:test-user`
  * ClusterRoleBinding 
    * == Kubernetes' built-in object
* `kubectl auth can-i list applications.argoproj.io --as=system:serviceaccount:argocd:test-user -n argocd`
  * 's return == yes
    * Reason:🧠thanks -- to -- ClusterRoleBinding🧠 
#### Kubernetes API
* `kubectl get pods -n argocd | grep argocd-server` fails

# Architecture
## install fewer components
* TODO: 

# how to install?
* | [this path](../../../../),
  * follow [the steps](../../core.md)
  * [install apps](https://github.com/dancer1325/argocd-example-apps?tab=readme-ov-file#steps)
    * Problems:
      * Problem1: ALL application's status "UNKNOWN"
        * Reason: "Application referencing project default which does not exist" -- `kubectl describe applications/example.guestbook -n argocd` --
        * Solution: 🧠NOT forget to create MANUALLY the default project
          * `kubectl apply -f defaultProjectManually.yaml`🧠

# how to use? 
TODO:
