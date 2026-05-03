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

# Git generator / `spec.template.spec.project` specified
## ❌does NOT support Signature Verification❌
TODO:
## use "non-scoped" repositories
TODO: 

# generates parameters -- based on -- specified repository's directory structure
* [here](/applicationset/examples/git-generator-directory)
## built-in parameters
### `{{.path.path}}`
* [here](/applicationset/examples/git-generator-directory)
* `argocd app get argo-workflows -o yaml`
  * check `spec.source.path`
### `{{index .path.segments n}}`
* [here](/applicationset/examples/git-generator-directory)
* `argocd app get argo-workflows -o yaml`
  * check `metadata.labels`
### `{{.path.basename}}`
* [here](/applicationset/examples/git-generator-directory)
* `argocd app get argo-workflows -o yaml`
  * check `spec.destination.namespace`
* `argocd app sync argo-workflows`
* `kubectl get namespaces | grep argo-workflows`
  * namespace created
### `{{.path.basenameNormalized}}`
* [here](/applicationset/examples/git-generator-directory)
* `argocd app get argo-workflows -o yaml`
  * check `metadata.labels`


TODO:


## ⚠️if you specify `.git.pathParamPrefix` -> `<.git.pathParamPrefix_VALUE>.path.<path_parameter>`⚠️
* `kubectl apply -f applicationSetGitDirectoryPathParamPrefix.yaml`
* `argocd app list | grep pathparamprefix`
  * 's return: 2 ApplicationS
* `argocd app get argo-workflows-pathparamprefix -o yaml`
  * check work & parameters are interpolated
## | add a NEW Helm chart/Kustomize YAML/Application/plain subdirectory | Git repository, ApplicationSet controller
* 
### detect this change
TODO:
### AUTOMATICALLY deploy the resulting manifests | NEW `Application` resources
TODO:

