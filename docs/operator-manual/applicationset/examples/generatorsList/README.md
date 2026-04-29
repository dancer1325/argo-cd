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
* [install Argo CD cluster-scoped](../installation.md)

# data structure `spec.generators[*].list`
## elements
* [here](/applicationset/examples/list-generator)
## elementsYaml
### == YAML string / key/value []
* [here](applicationsetElementsYaml.yaml)
* `kubectl apply -f applicationsetElementsYaml.yaml`
* `argocd appset list`
  * ApplicationSet is deployed
* `argocd app list`
  * 2 ApplicationS / deployed | `dev` & `staging` have been deployed
### uses: list generator | Matrix generator
* [here](../generatorMatrix)
## template
### override default ApplicationSet `spec.template`
* `kubectl apply -f applicationsetListTemplateOverride.yaml`
* `argocd appset get guestbook-list-template-override`
  * ONLY appear default one
* `argocd appset get guestbook-list-template-override -o yaml` & check `spec.generators.list` display specific one
* `argocd app list`
  * 👀check appear the `custom-*`👀 / source repo:  https://github.com/dancer1325/argocd-example-apps.git

# generates parameters -- based on an -- arbitrary list of key/value pairs
* `kubectl logs -n argocd -l app.kubernetes.io/name=argocd-applicationset-controller --tail=50 | grep 'generated'`
  * generate ArgoCD Applications
* ❌NOT possible to check the generation itself❌

# DYNAMICALLY generated elements
* [here](/applicationset/examples/list-generator/matrixWithGitAndList.yaml)
