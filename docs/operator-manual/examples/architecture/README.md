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

# UI
* [demo](https://cd.apps.argoproj.io/applications?proj=&sync=&autoSync=&health=&namespace=&cluster=&labels=&annotations=&operation=)

# CLI
* [CLI installation](../../../cli_installation.md)
* `argocd version`

# gRPC REST
* install grpcurl
  * _Example:_ | Mac, 
    * `brew install grpcurl`
* get user (localhost:8080)'s auth-token
  * `cat $HOME/.config/argocd/config` > users: name: localhost:8080 > copy auth-token
* `grpcurl -insecure -H "Authorization: Bearer <PREVIOUS_TOKEN>" localhost:8080 list`
  * 's return
    * EXISTING gRPC services

# Argo CD API Server 
* `kubectl get all -n argocd | grep "argocd-server"`
## == gRPC/REST server / exposes the API
* "*.proto" | [server](/server)
  * _Examples:_ 
    * [cluster.proto](/server/cluster/cluster.proto)
    * [certificate.proto](/server/certificate/certificate.proto)
    * ...
* [here](#grpc-rest)
## responsibilities
### application management & status reporting
* `argocd app --help`
  * check AVAILABLE commands
    * _Examples:_ create, delete, list, sync, rollback, ...
### repository & cluster credential management
* `argocd cluster --help` & `argocd repo --help` & `argocd repocreds list`
  * check AVAILABLE commands
#### stored -- as -- K8s secrets
* [private repositories](../../../user-guide/private-repositories.md)
* [cluster](../../cluster-management.md) 
### delegate authentication & auth -- to -- external identity providers
* [here](../../user-management/index.md) 
### RBAC enforcement
* `argocd proj role --help`
  * see help RBAC-related
### listener/forwarder -- for -- Git webhook events
* [here](/server/server.go)'s  `mux.HandleFunc("/api/webhook", acdWebhookHandler.Handler)`
## API
* https://localhost:8080/swagger-ui
  * Swagger UI
### consumed by
#### ArgoCD UI
* | browser,
  * open developer settings
  * https://localhost:8080/applications
    * user: admin
    * password: copiedFrom `argocd admin initial-password -n argocd`
  * | developer settings > network,
    * check URL
#### CLI
* `argocd version`
  * check `argocd-server` output
#### CI/CD systems
* can be call -- through -- [gRPC REST](#grpc-rest)

# Repository Server 
* `kubectl get all -n argocd | grep "argocd-repo-server"`
## internal service
* `kubectl get svc -n argocd | grep "argocd-repo-server"`
  * check it's `ClusterIP` 
### maintains a local cache -- about the -- Git repository
* `kubectl logs -n argocd deploy/argocd-repo-server | grep -i "cache\|clone\|fetch" | head -20`
### hold the application manifests
TODO: 
## responsible for
### internal service

# Application Controller 
## == Kubernetes controller
TODO:

# Sync hooks
TODO:

# App actions
TODO:
