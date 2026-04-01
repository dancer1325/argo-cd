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
* TODO: 
crea un usuario de solo lectura:

  # 1. Añadir usuario readonly en argocd-cm
  kubectl patch configmap argocd-cm -n argocd --type merge -p '{"data":{"accounts.readonly":"login"}}'

  # 2. Establecer su password
  argocd account update-password --account readonly --new-password readonly123 --server localhost:8080
  --insecure

  # 3. Añadir política RBAC de solo lectura en argocd-rbac-cm
  kubectl patch configmap argocd-rbac-cm -n argocd --type merge -p '{"data":{"policy.csv":"p,          
  role:readonly, applications, get, */*, allow\ng, readonly, role:readonly"}}'

  # 4. Login como readonly
  argocd login localhost:8080 --insecure --username readonly --password readonly123

  # 5. Intenta borrar una app → debería fallar con PermissionDenied
  argocd app delete example.guestbook --server localhost:8080 --insecure
argocd CLI → gRPC → API Server → PermissionDenied
### TODO: 

# Repository Server 
* TODO: 

# Application Controller 
## == Kubernetes controller
TODO:

# Sync hooks
TODO:

# App actions
TODO:
