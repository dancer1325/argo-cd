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

# Argo CD
* deploy [some Argo CD Applications](https://github.com/dancer1325/argocd-example-apps/tree/master/apps#how-to-deploy-locally)
* `kubectl port-forward svc/argocd-server -n argocd 8080:443`
  * port-forward "argocd-server" locally
* `kubectl get secret argocd-initial-admin-secret -n argocd -o jsonpath='{.data.password}' | base64 -d`
  * copy the password
* `argocd login localhost:8080 --insecure`
  * user: admin
  * password: previouslyCopied
## is largely stateless
### pods do NOT store anything | anywhere
* TODO:
### data is stored | Kubernetes' etcd
```
kubectl exec -it etcd-kind-control-plane -n kube-system -- \
  etcdctl --endpoints=https://127.0.0.1:2379 \
  --cacert=/etc/kubernetes/pki/etcd/ca.crt \
  --cert=/etc/kubernetes/pki/etcd/server.crt \
  --key=/etc/kubernetes/pki/etcd/server.key \
  get /registry/argoproj.io --prefix --keys-only
```
### | kill a pod, ALL keeps on working fine
* kill some Argo CD pod
  * `kubectl delete pod argocd-application-controller-0 -n argocd`
* `argocd app list`
  * NO down in any Argo CD Application

# Argo CD HA
* [follow steps to install](/manifests/README.md#high-availability)
## runs Redis -- in -- HA mode
* `kubectl get statefulset.apps/argocd-redis-ha-server`
## requirements
### 3 nodes
* if you try to install | cluster / has 1! node
  * `kind create cluster`
  * [follow steps to install](/manifests/README.md#high-availability)
  * `kubectl get deployment` & `kubectl get statefulset`
    * ❌NO meet DESIRED number❌
## ❌NOT support❌
### IPv6 only clusters
* `kind create cluster --config ipv6ClusterConfiguration.yaml`
  * Problems:
    * Problem1: "ERROR: failed to create cluster: could not find a log line that matches "Reached target .*Multi-User System.*|detected cgroup v1""
      * Attempt1: configure docker daemon / enable it
        * if you use Rancher Desktop -> | "/.rd/docker/daemon.json"
          ```json
          {                                                                                        
            "ipv6": true,                                                                          
            "fixed-cidr-v6": "2001:db8:1::/64"                                                     
          }
          ```
      * Solution: TODO:
# TODO: 

