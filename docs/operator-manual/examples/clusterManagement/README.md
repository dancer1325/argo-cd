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
* [install Argo CD](/docs/operator-manual/installation.md) | Kind cluster
  * [expose it ALSO](../../../examples/gettingStarted/README.md#ways-to-expose)
  * [login](../../../examples/gettingStarted/README.md#4-login----via----cli)
* [install Argo CD CLI](../../../cli_installation.md)

# Adding a cluster

* `kind create cluster --name kind-kind2`
* `argocd cluster add kind-kind2`
  * Problems:
    * Problem1: "error getting server version: failed to get server version: Get \"https://127.0.0.1:50545/version?timeout=32s"
      * Attempt1: `argocd cluster add kind-kind2 --kubeconfig ~/.kube/config`
      * Attempt2: 
        * `docker inspect kind2-control-plane | grep IPAddress`
          * get kind-kind2's IP 
        * `kubectl config set-cluster kind-kind2 --server=https://172.18.0.3:6443`
          * adjust kind-kind2's server URL cluster
        * `argocd cluster add kind-kind2`
      * Attempt3:
        * `kubectl -n argocd get pods -l app.kubernetes.io/name=argocd-server`
          * get argocd-server's pod Name
        * `kubectl -n argocd cp ~/.kube/config argocd-server-<POD_ID>:/tmp/kube.conf`
          * copy the local Kube configuration file | Kind's pod
        * `kubectl -n argocd exec -it argocd-server-<POD_ID> -- \                                             
          argocd login localhost:8080 --insecure --username admin --password <ADMIN_PASSWORD>`
        * kubectl -n argocd exec -it argocd-server-<POD_ID> -- \                                             
          argocd cluster add kind-kind2
      * Attempt4:
        * `kind create cluster --name kind2 --config kind2ClusterConfig.yaml`
        * `kubectl config set-cluster kind-kind2 --server=https://127.0.0.1:7443`
        * `argocd cluster set kind-kind2 --SERVER https://127.0.0.1:6443`
      * Solution: add ANOTHER pod / has argocd-cli & add -- from -- there
        * `kubectl apply -f podWithArgoCD.yaml`
        * `kubectl -n argocd exec -it argocd-cli -- sh`
          * `argocd login argocd-server.argocd.svc.cluster.local --insecure --username admin --password aaaaaaaa`
          * `argocd cluster add kind-kind2 --insecure`

## allows: Argo CD can deploy Applications | MULTIPLE clusters (EVEN != cluster | Argo CD is installed)
* `kubectl apply -f applicationInCluster2.yaml`
* | browser,
  * https://localhost:8080/applications/argocd/guestbook?view=tree&resource=
    * \> Details > Cluster
      * check it's == kind-kind2

## what does Argo CD under the hood?
### creates SA "argocd-manager" | target cluster / FULL cluster RBAC
TODO:

### TODO: 

# Skipping cluster reconciliation

TODO: 

# Removing a cluster

TODO:
