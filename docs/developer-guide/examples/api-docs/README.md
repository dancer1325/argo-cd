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
* [expose it](../../../getting_started.md)

# Authorization
* `kubectl get secret argocd-initial-admin-secret -n argocd -o jsonpath='{.data.password}' | base64 -d`
  * get initial admin password
## steps
### get a token
#### if you use HTTPS
* `curl -k -H "Content-Type: application/json" https://localhost:8080/api/v1/session -d '{"username":"admin","password":"<INITIAL_ADMIN_PASSWORD>"}'`
#### if you use HTTP
* TODO:
### | ANY AFTER call, use this JWT
#### if you use HTTPS
* `curl -k $ARGOCD_SERVER/api/v1/applications -H "Authorization: Bearer <JWT>"`
#### if you use HTTP
* `curl $ARGOCD_SERVER/api/v1/applications -H "Authorization: Bearer <JWT>"`

# Services
## Applications API -- "/api/v1/applications/*" --
### | ALL endpoints, `project` == OPTIONAL query string parameter
* WITH query string parameter
  * `curl -k "$ARGOCD_SERVER/api/v1/applications?project=default" -H "Authorization: Bearer <JWT>"`
    * ⚠️if you add query parameters -> you need to wrap with ""⚠️
* WITHOUT query string parameter
  * `curl -k $ARGOCD_SERVER/api/v1/applications -H "Authorization: Bearer <JWT>"`
#### if the applications do NOT exist 
##### the API returns a `404` error
* TODO:
##### | that `project` -> the API returns a `403` error
* TODO:
