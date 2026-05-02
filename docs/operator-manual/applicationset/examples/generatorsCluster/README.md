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
### allows: narrow the scope of targeted clusters
* NEXT sections
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
* `kubectl apply -f applicationSetWithClusterGenerator.yaml`
* `argocd app list | grep guestbook-selector-label`
  * 's return: ONLY 1! Application | kind2
### `.matchExpressions`
* `kubectl apply -f applicationSetWithClusterGenerator.yaml`
* `argocd app list | grep guestbook-selector-expression`
  * 's return: ONLY 1! Application | kind2

## `.template`
### override default ApplicationSet `spec.template`
* `kubectl apply -f applicationSetWithClusterGenerator.yaml`
* `argocd appset get guestbook-clustergenerator-template-override`
  * ONLY appear default one
* `argocd app list | grep clustergenerator`
  * check source == https://github.com/dancer1325/argocd-example-apps.git

## `.values`
* [here](applicationSetWithClusterGenerator.yaml)'s "cluster-values"
* `kubectl apply -f applicationSetWithClusterGenerator.yaml`
* `argocd app list | grep values`
  * check existing Applications / related to this ApplicationSet
* `argocd app get in-cluster-guestbook-values`
  * check `source.target` & `namespace`

# built-in parameters
## == cluster credential secrets
### `name` 
* [here](applicationSetWithClusterGenerator.yaml)
  * see `{{.name}}`
### `nameNormalized`
* [here](applicationSetWithClusterGenerator.yaml)
  * see `{{.nameNormalized}}`
### `server`
* [here](applicationSetWithClusterGenerator.yaml)
  * see `{{.server}}`
### `project`
* [here](applicationSetWithClusterGenerator.yaml)
  * see `{{.project}}`
### `metadata.labels.<key>`
* [definition | Cluster credentials](clusterSecret.yaml)'s `metadata.labels`
* [here](applicationSetWithClusterGenerator.yaml)
  * see `{{index .metadata.labels`
* `kubectl apply -f applicationSetWithClusterGenerator.yaml`
* `argocd app list | grep builtin-metadata`
  * 's return: ONLY -- for -- filtered clusters
* `argocd app get clustergenerator-guestbook-builtin-metadata-kind2 -o yaml`
  * check `metadata.annotations`
### `metadata.annotations.<key>`
* [definition | Cluster credentials](clusterSecret.yaml)'s `metadata.annotations`
* [here](applicationSetWithClusterGenerator.yaml)
    * see `{{index .metadata.annotations`
* `kubectl apply -f applicationSetWithClusterGenerator.yaml`
* `argocd app list | grep builtin-metadata`
    * 's return: ONLY -- for -- filtered clusters
* `argocd app get clustergenerator-guestbook-builtin-metadata-kind2 -o yaml`
    * check `metadata.annotations`

## \| template it, they are decoded
* see final output | [PREVIOUS subsection](#-cluster-credential-secrets)



# filter clusters -- based on -- their K8s version
* `kind create cluster --config clusterWithKubernetesVersionConfig.yaml`
* get ALL TLS configuration / register kind4 | cluster 
  * see [clusterSecret.yaml](clusterSecret.yaml)
* `kubectl apply -f clusterSecret.yaml`
  * `argocd cluster list`   
    * check that it returns: "clusterwithspecifiedversion" 
    * Problems:
      * Problem1: NO identifies the version, because it's NOT monitor by Controller, since it has NO Application 
* `kubectl apply -f applicationSetWithClusterGenerator.yaml`
* `argocd app list | grep previous-filtered`
  * create Application | ALL
* `kubectl apply -f applicationSetWithClusterGenerator.yaml`
* `argocd app list | grep filtered`
    * create 1! Application / filtered -- by -- k8s version
