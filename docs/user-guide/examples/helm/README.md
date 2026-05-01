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
* [deploy these Applications](https://github.com/dancer1325/argocd-example-apps/tree/master/apps)

# ArgoCD ONLY uses Helm -- , through `helm template`, to -- inflate charts
* `kubectl apply -f applicationHelmBased.yaml`
* `argocd app list`
  * check they are displayed
* `helm list` OR `helm list -n argocd`
  * 's return: NOTHING

# Values Files
## | Application, `spec.source.helm.valueFiles`
* [here](applicationHelmBased.yaml)
### | Argo CD v2.6+, git repository | values files (can be) != git repository | Helm chart
* [here](../helm)
### ⚠️requirements: ⚠️| Argo CD v2.6-, git repository | values files (MUST be) == git repository | Helm chart
TODO:
## ways to specify
### declaratively
* [here](applicationHelmBased.yaml)'s "helm-guestbook-valuesfiles"
* `kubectl apply -f applicationHelmBased.yaml`
* `argocd app get helm-guestbook-valuesfiles`
  * 's return: source.HelmValues ALREADY specified
* `argocd app sync helm-guestbook-valuesfiles`
* `kubectl get svc -n helm-guestbook-valuesfiles`
  * 's return: TYPE LoadBalancer
### `argocd <SOME_COMMAND> --values <RELATIVE_PATH_TO_SOURECE_REPO>`
* `kubectl get service helm-guestbook -n helm-guestbook`
  * 's return: TYPE: ClusterIP
* `argocd app get example.helm-guestbook`
  * 's return: NOT specified
* `argocd app set example.helm-guestbook --values values-production.yaml`
* `kubectl get service helm-guestbook -n helm-guestbook`
  * 's return: TYPE: LoadBalancer
## if you specify a value file / NO exist -> | template expansion, it errors "Missing"
* `kubectl apply -f applicationHelmBased.yaml`
* `argocd app get helm-guestbook-valuesfiles-missing`
  * 's return: ComparisonError
### | template expansion, it errors "Missing"
TODO: 
* `kubectl logs -n argocd -l app.kubernetes.io/name=argocd-application-controller | grep -i "missing"`
  * NOT display it
### if you want to skip this error -> set `--ignore-missing-value-files: true`
* `kubectl apply -f applicationHelmBased.yaml`
* `argocd app get helm-guestbook-valuesfiles-ignoremissing`
  * 's return: k8s resources compiled fine

# Values
## `spec.source.helm.valuesObject`
### == Helm values / passed -- to -- Helm template
* `kubectl apply -f applicationHelmBased.yaml`
* `argocd app manifests helm-guestbook-valuesobject`
  * check service type == ClusterIP
#### defined -- as a -- map
* [here](applicationHelmBased.yaml)'s see "helm-guestbook-valuesobject" Application
### ways to specify
#### declaratively
* [here](applicationHelmBased.yaml)'s see "helm-guestbook-valuesobject" Application
### 's priority > `spec.source.helm.values`'s priority
* `kubectl apply -f applicationHelmBased.yaml`
* `argocd app manifests helm-guestbook-valuesobject-priority`
  * check service type == ClusterIP == valuesObject specified
## `spec.source.helm.values`
### == Helm values / passed -- to -- Helm template
* `kubectl apply -f applicationHelmBased.yaml`
* `argocd app manifests helm-guestbook-values`
  * check service type == ClusterIP
#### defined -- as a -- string
* [here](applicationHelmBased.yaml)'s see "helm-guestbook-values" Application
### ways to specify
#### declaratively
* [here](applicationHelmBased.yaml)'s see "helm-guestbook-values" Application

# Parameters
## uses: | manifest generation, -- by -- `helm template`
* `kubectl apply -f applicationHelmBased.yaml`
* `argocd app manifests helm-guestbook-parameters`
  * check service type == LoadBalancer
## ways to specify
### declaratively
* [here](applicationHelmBased.yaml)'s "helm-guestbook-parameters" Application
### `argocd app set <ARGO_CD_APPLICATION_NAME> -p <PARAMETER_KEY>=<PARAMETER_VALUE>`
* `argocd app set helm-guestbook-parameters -p service.type=LoadBalancer`
* `argocd app manifests helm-guestbook-parameters`
  * check service type == LoadBalancer

# TODO:
TODO:

# Helm Release Name
## by default, == Application name / it belongs
* `kubectl apply -f applicationHelmBased.yaml`
* `argocd app manifests helm-guestbook-releasename-default`
  * check `labels.release`
## ways to specify
### declaratively
* `kubectl apply -f applicationHelmBased.yaml`
* `argocd app manifests helm-guestbook-releasename-specified`
  * check `labels.release`
### `argocd app set <ARGO_CD_APPLICATION_NAME> --release-name <SPECIFY_RELEASE_NAME>`
* `argocd app set helm-guestbook-releasename-specified --release-name helm-guestbook-releasename-specified-cli`
* `argocd app manifests helm-guestbook-releasename-specified`

# TODO:
TODO:
