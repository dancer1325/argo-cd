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

# Generators
## generate parameters /
* NOT possible to check
  * ONLY, check the generated ApplicationS
### == key/value pairs
* see `spec.generators[].<SOME_FIELD>`
  * [List generator](/applicationset/examples/list-generator/list-example.yaml)
    * `spec.generators.list.elements`
      ```
      cluster: <CLUSTER_VALUE>
      url: <URL_VALUE>
      ```
  * [Cluster generator](/applicationset/examples/cluster)
    * `spec.generators.clusters`
  * Git generator
    * 's [directory type](/applicationset/examples/git-generator-directory)
      * built-in parameters
      * `spec.generators.git.values`
    * 's [files discovery type](/applicationset/examples/git-generator-files-discovery)
      * built-in parameters
      * `spec.generators.git.values`
  * [Matrix generator](/applicationset/examples/matrix)
    * combination of child generator's parameters
  * Merge generator
    * TODO:
  * SCM provider
    * TODO:
  * PR
    * TODO:
  * Plugin
    * TODO:
#### | render the template, they are substituted | ApplicationSet resource's `spec.template` section
* / EACH generator use case
  * `kubectl get applicationset <APPLICATION_NAME> -n argocd -o jsonpath='{.spec.template}' | jq .`
### -- primarily based on -- data sources
* [List generator](../../Generators-List.md)
* [Cluster generator](../../Generators-Cluster.md)
* [Git generator](../../Generators-Git.md)
* [Matrix generator](../../Generators-Matrix.md)
* [Merge generator](../../Generators-Merge.md)
* [SCM Provider generator](../../Generators-SCM-Provider.md)
* [Pull Request generator](../../Generators-Pull-Request.md)
* [Cluster Decision Resource generator](../../Generators-Cluster-Decision-Resource.md)
* [Plugin generator](../../Generators-Plugin.md)
