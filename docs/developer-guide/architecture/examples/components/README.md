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

# separate the responsibility
## benefits
### Modularity
#### == pretty flexible
##### == components can be replaced & omit
* [core installation](/manifests/core-install.yaml)
  * == omit some components
* TODO: prove how to replace
###### requirements: fit the contract interface
* Argo CD Repo Server
  * 's contract interface == gRPC API ([`RepoServerService`](/reposerver/repository/repository.proto))
* Argo CD API Server
  * 's contract interface == gRPC + REST API
    * == "*.proto" | [API Server](/server)
      * _Examples:_
        * [manage applications](/server/application/application.proto)
        * [manage clusters](/server/cluster/cluster.proto)
        * ...
* Argo CD Redis
  * 's contract interface == used [DIRECTLY](/util/cache/cache.go)'s "github.com/redis/go-redis/v9" dependency
#### components interact -- , via an interface, with -- each other
* `kubectl get service -n argocd`
  * services are TYPE == ClusterIP
    * == internal

### 1! responsibility / EACH component
* `kubectl get service -n argocd`
  * check there are 1 OR 2 ports / EACH one
    * -- related to -- 1 OR 2 functionalities
      * _Examples:_ 
        * argocd-server's ports
          *  80/443/ -- API
            * 8080 -- UI
        * argocd-repo-server's ports
          * 8081 -- Git manifests
        * argocd-redis
          * 6379 - Cache
### Reusability
* TODO:

# Responsibility
## UI
### allows: managing applications / deployed | Kubernetes cluster
* | browser,
  * https://localhost:8080/applications
    * user: admin
    * password: paste the password / got -- via -- `argocd admin initial-password`
  * you can, about Argo CD applications, 
    * create 
    * sync
    * refresh

## Argo CD CLI
### allows: interacting -- with -- Argo CD API
* [here](../../../../operator-manual/architecture.md)

## API Server
* [here](../../../../operator-manual/architecture.md)

## Application Controller
* [here](../../../../operator-manual/architecture.md)

## ApplicationSet Controller
### responsible for: reconciling the ApplicationSet resource
* `kubectl logs -n argocd -lapp.kubernetes.io/name=argocd-applicationset-controller --tail=-1 | head -20`
  * look up "Starting Controller" == reconciliation process

## Repository Server
* [here](../../../../operator-manual/architecture.md)

## Redis
### responsible for:
#### reducing requests to: Kube API & Git provider
* `kubectl get pod -n argocd | grep "redis"`
  * copy Redis podName
* `kubectl get secret argocd-redis -n argocd -o jsonpath='{.data.auth}' | base64 -d`
  * copy Redis secret
* `kubectl exec -n argocd PASTE_REDIS_POD_NAME -- redis-cli -a REDIS_SECRET KEYS "*"`
  * _Example:_ `kubectl exec -n argocd argocd-redis-547cf77b6b-jj24x -- redis-cli -a Dql5sxnc5pY3TOFx KEYS "*"`
  * look up
    * "mfst"
      * == manifests
      * == cache manifests == Git-provider
#### few UI operations
* [source code](/util/session/state.go)'s `statestorage`

## Kube API
### responsible for: run the reconciliation loop
* it has "watch" verbs | Kubernetes
  * `kubectl get clusterrole argocd-application-controller -o yaml | grep -A3 "verbs"`
  * [manifest](/manifests/install.yaml)'s `clusterrole`
  * Reason: 🧠needed -- for the -- refresh🧠

## Git
### provide: Kubernetes object's desired state
* [Argo CD Application manifest](/manifests/crds/application-crd.yaml)'s `spec.source.repoURL`
### ALLOWED values
#### git repo
* [ALL here](https://github.com/dancer1325/argocd-example-apps/blob/master/apps/values.yaml#L6)
#### helm repo
* `argocd repo add https://prometheus-community.github.io/helm-charts --type helm --name prometheus --insecure-skip-server-verification`
  * Reason:🧠configure the connection🧠
* `kubectl apply -f helmRepoApplication.yaml`
  * Problem:
    * Problem1: "Error: failed to start container "node-exporter": Error response from daemon: path / is mounted on / but it is not a shared or slave mount"
      * Solution: TODO:
* https://localhost:8080/applications/argocd/prometheus?resource=
  * ALL prometheus helm chart-related objects are deployed
* `kubectl get all -n prometheus`
  * check clearly ALL Kubernetes objects
#### OCI artifact repo
* [here](../../../../user-guide/oci.md)

## Dex

* [exist | COMMON installation](/manifests/install.yaml)'s `argocd-dex-server`
* `kubectl get all -n argocd`
  * deployed | cluster
