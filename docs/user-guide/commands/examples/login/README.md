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

# `argocd login SERVER [flags]`
## how to get `SERVER`? 
* `kubectl get svc -n argocd` & identify "argocd-server" OR `kubectl get svc -n argocd | grep argocd-server`
  * if TYPE ==
    * ClusterIP & local ->
      * `kubectl port-forward svc/my-release-argocd-server -n argocd 8080:443`
      * SERVER == localhost:8080
    * LoadBalancer ->
      * SERVER == EXTERNAL-IP column
    * NodePort ->
      * SERVER == <NODE-IP>:<NODE-PORT>
      * `kubectl get nodes -o wide` -- to get -- NODE-IP
* if Ingress ->
  * ❌NOT a Service type❌ -> `kubectl get ingress -n argocd`
  * SERVER == ADDRESS column

## `argocd login SERVER`
* `kubectl get secret argocd-initial-admin-secret -o jsonpath='{.data.password}' | base64 -d`
  * get secret
* `kubectl port-forward svc/my-release-argocd-server 8080:443`
* `argocd login localhost:8080`
  * username: admin
  * password: passPreviouslyGot

# `--sso`

TODO:

# `--core`
## login | Argo CD -- via -- Kubernetes API server
* [install Argo CD core](/docs/operator-manual/core.md#installing)
  * == NO contain Argo CD API Server
* `argocd login --core`
  * work
* `cat ~/.config/argocd/config`
  * check servers[*].server == kubernetes != IP

## ❌NO request username NOR password❌
* `argocd login --core`
  * NO request username & password
