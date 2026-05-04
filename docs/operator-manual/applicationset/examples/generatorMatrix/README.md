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

# 💡combines ALL POSSIBLE 2 child generators' parameters 💡
## == / EACH 1@ child generator's parameters, run the 2@ child generator
* [here](/applicationset/examples/matrix/README.md#list-generator--list-generator)
* `argocd app list | grep list-and-list`
  * return 4 ApplicationS
## -> 👀gain BOTH generators' intrinsic properties 👀
* [here](/applicationset/examples/matrix/list-and-list.yaml)
  * | `spec.template`, check it's using generator parameters coming -- from -- BOTH child generatorS
## ⚠️if matrix generator use 2 child Git generators -> 1 OR BOTH MUST use the `pathParamPrefix` option⚠️
* [here](/applicationset/examples/matrix/git-and-git.yaml)
  * see `path` parameters using to distinguish them
    * `app.path`
    * `target.path`

# child generator's parameters
## can be used | POST child generatorS
* [here](/applicationset/examples/matrix/README.md#git-file-generator--cluster-generator)
## / ⚠️SAME name, FIRST child generator take priority⚠️
* `kubectl apply -f applicationSetParameterOverride.yaml`
  * if you want to check what failed -> `kubectl logs -n argocd deployment/argocd-applicationset-controller --tail=200 | grep -i "matrix-parameter\|error\|err"`
* `argocd app get matrix-parameter-override -o yaml`
  * check `metadata.annotations.servicetype: ClusterIP`

# Restrictions 
TODO: