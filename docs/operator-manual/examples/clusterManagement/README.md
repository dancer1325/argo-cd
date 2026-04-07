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

# how to add a cluster?
## ways
### `argocd cluster add contextName`

* `kind create cluster --name kind2`
* `argocd cluster add kind-kind2`
  * Problems:
    * Problem1: "error getting server version: failed to get server version: Get \"https://127.0.0.1:50545/version?timeout=32s"
      * Reason:🧠clusters locally are handled -- as -- Docker containers -> container's bridges problems🧠
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
      * Solution: 💡add ANOTHER pod / has argocd-cli & add -- from -- there💡
        * Reason: 🧠| macOs & Windows, you can NOT access -- DIRECTLY to -- container's IPs🧠
        * `kubectl config use-context kind-kind`
        * `ARGOCD_PASSWORD=$(kubectl get secret argocd-initial-admin-secret -n argocd -o jsonpath='{.data.password}' | base64 -d)`
          * export Argo CD password
        * create configMap / has cluster configurations
          * `kind get kubeconfig --name kind2 > /tmp/kind2-kubeconfig`
            * copy Kube config file 
          * `KIND2_IP=$(docker inspect kind2-control-plane --format '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}')`
            * export a kind2's internal IP
          * `sed -i '' "s|server: https://.*:.*|server: https://$KIND2_IP:6443|g" /tmp/kind2-kubeconfig`
            * | the copied kube config file, 
              * update the kind2's server  
          * `kubectl create configmap kind2-kubeconfig --from-file=config=/tmp/kind2-kubeconfig -n argocd`
        * `kubectl apply -f podWithArgoCD.yaml`
        * `kubectl -n argocd exec -it argocd-cli -- sh`
          * `argocd login argocd-server.argocd.svc.cluster.local --insecure --username admin --password <PREVIOUS_EXPORTED_PASSWORD>`
          * `argocd cluster add kind-kind2 --insecure`
            * 's return suceed
          * `exit`
* `argocd login localhost:8080 --insecure  --username admin --password <PREVIOUS_EXPORTED_PASSWORD>`
* `argocd cluster list`
  * check BOTH are configured

### declaratively
* [here](../declarativeSetUp)

## allows: Argo CD can deploy Applications | MULTIPLE clusters (EVEN != cluster | Argo CD is installed)
* `kubectl apply -f applicationInCluster2.yaml`
* | browser,
  * https://localhost:8080/applications/argocd/guestbook?view=tree&resource=
    * \> Details > Cluster
      * check it's == kind-kind2

## what does Argo CD under the hood?
### | target cluster, creates
* `kubectl config use-context kind-kind2`
#### SA "argocd-manager"  / FULL cluster RBAC
* `kubectl get sa -n kube-system | grep "argocd-manager"`
* `kubectl describe clusterrole argocd-manager-role -n kube-system`
  * 's return *
    * == FULL rights

#### secret -- with -- bearer token
* `kubectl get secret -n kube-system | grep "argocd-manager"`

### | source cluster's "argocd" namespace,
#### stores -- as a -- Secret, token + server URL + TLS  
* `kubectl config use-context kind-kind`
* `CLUSTER_SECRET=$(kubectl get secret -n argocd -l argocd.argoproj.io/secret-type=cluster -o jsonpath='{.items[0].metadata.name}')`
* server URL
  * `kubectl get secret $CLUSTER_SECRET -n argocd -o jsonpath='{.data.server}' | base64 -d`
* token
  * `kubectl get secret $CLUSTER_SECRET -n argocd -o jsonpath='{.data.config}' | base64 -d | jq -r '.bearerToken'`
* TLS
  * `kubectl get secret $CLUSTER_SECRET -n argocd -o jsonpath='{.data.config}' | base64 -d | jq -r '.tlsClientConfig.caData'`

### | sync an `Application` / `destination.server: https://...`, Application Controller connect -- , via that Secret, to -- that cluster
TODO:

# Skipping cluster reconciliation

TODO: 

# Removing a cluster

TODO:
