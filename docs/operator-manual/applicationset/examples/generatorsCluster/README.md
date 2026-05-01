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
* recommendations
  * `kind create cluster` & `kind create cluster --name kind2`
* add cluster | ArgoCD, [declaratively](../../../declarative-setup.md#cluster-credentials)
  * `KIND2_IP=$(docker inspect kind2-control-plane --format '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}')`
  * `CA_DATA=$(kubectl config view --raw -o jsonpath='{.clusters[?(@.name=="kind-kind2")].cluster.certificate-authority-data}')`
  * `CERT_DATA=$(kubectl config view --raw -o jsonpath='{.users[?(@.name=="kind-kind2")].user.client-certificate-data}')`
  * `KEY_DATA=$(kubectl config view --raw -o jsonpath='{.users[?(@.name=="kind-kind2")].user.client-key-data }')`
  * `kubectl apply -f clusterSecret.yaml`

# [data structure](/manifests/crds/applicationset-crd.yaml)'s `spec.generators[*].cluster`
## NO property set
* [here](/applicationset/examples/cluster)

## `.flatList`
###  ⚠️deploy 1! ApplicationSet⚠️
* `kubectl apply -f applicationSetWithClusterGenerator.yaml`
* `argocd app manifests all-clusters-guestbook`
  * 's return: ConfigMap with ALL data
### generator parameter: `.clusters`
* [here](applicationSetWithClusterGenerator.yaml)

## `.selector`
### `.matchLabels`
* `kind create cluster --name kind3`
  * Problems:
    * Problem1: 
      * Solution: 
        * | Rancher Desktop UI, > Preferences > VM > 
          * Memory: 9
          * CPU: 4
        * `rdctl shell`
          * `sudo sysctl -w fs.inotify.max_user_watches=1048576`
          * `sudo sysctl -w fs.inotify.max_user_instances=8192`
          * `exit`

TODO:
### `.matchExpressions`

## `.template`
TODO:

## `.value`
TODO:

# generate parameters / EACH registered cluster | Argo CD
## == Cluster credential secrets
TODO:

# built-in parameters
## == cluster credential secrets
### `name` 
TODO:
### `nameNormalized`
TODO:
### `server`
TODO:
### `project`
TODO:
### `metadata.labels.<key>`
TODO:
### `metadata.annotations.<key>`
TODO:
## \| template it, they are decoded
TODO:

