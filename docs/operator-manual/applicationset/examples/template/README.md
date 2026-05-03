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

# allows: 👀generating Argo CD `Application` resources👀
## generation -- thanks to --
### RIGHT NOW: fasttemplate
* [here](list-example-fasttemplate.yaml)
* `kubectl apply -f list-example-gotemplate.yaml`
### FUTURE: Go Template
* [here](list-example-gotemplate.yaml)
* `kubectl apply -f list-example-fasttemplate.yaml`

# 's fields
## `spec.template.spec` == 💡Application's `spec`💡/
* [here](list-example-gotemplate.yaml)
### can use generator's parameters
* [here](list-example-gotemplate.yaml)
## `spec.template.metadata`
* [here](list-example-gotemplate.yaml)
### set Application's metadata
* `kubectl apply -f list-example-gotemplate.yaml`
* `argocd app get engineering-dev-guestbook-template-gotemplate`
  * find Application -- by -- `metadata.name`
## | Deploy ApplicationSet resources, as part of a Helm chart
* [here](helm-string-literal-chart)
### ⚠️if you use Helm to deploy your ApplicationSet resources -> write the template -- as a -- Helm string literal⚠️
* [here](helm-string-literal-chart)
* `helm install applicationsetviahelm ./helm-string-literal-chart -n argocd`
  * `helm list -n argocd`
    * 's return: installed ApplicationSet
* `helm upgrade --install applicationsetviahelm ./helm-string-literal-chart -n argocd`
  * allow
    * upgrading the helm chart
* `argocd appset list | grep parth-of-helm`
  * 's return: EXISTING ApplicationSet
#### OTHERWISE, throw errorS
TODO: 

# Generator templates
TODO:

# Template Patch
TODO:
