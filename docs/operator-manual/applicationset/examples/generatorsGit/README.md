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

# Git Generator: Directories -- `.git.directories` --
## generates parameters -- based on -- specified repository's directory structure
* [here](/applicationset/examples/git-generator-directory)
### == 👀generate 1 Application / EACH specified repository's directory structure👀
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
## ⚠️if you specify `.git.pathParamPrefix` -> `<.git.pathParamPrefix_VALUE>.path.<path_parameter>`⚠️
* `kubectl apply -f applicationSetGitDirectoryPathParamPrefix.yaml`
* `argocd app list | grep pathparamprefix`
  * 's return: 2 ApplicationS
* `argocd app get argo-workflows-pathparamprefix -o yaml`
  * check work & parameters are interpolated
## | add a NEW Helm chart/Kustomize YAML/Application/plain subdirectory | Git repository, ApplicationSet controller
* added [cert-manager](/applicationset/examples/git-generator-directory/cluster-addons/cert-manager)
* `kubectl apply -f git-directories-example.yaml`
### detect this change
* wait 3' -- for -- polling
* `argocd app list | grep cert-manager`
### AUTOMATICALLY deploy the resulting manifests | NEW `Application` resources
* wait 3' -- for -- polling
* `argocd app list | grep cert-manager`
  * 's status: OutOfSync
    * Problem: it's truth AUTOMATICALLY deploy? 
      * Solution: TODO
## `generators[git].directories[].path`
### if you want to specify -> you can use [path.Match](https://golang.org/pkg/path/#Match)
TODO: 
## Exclude directories
* [here](/applicationset/examples/git-generator-directory/excludes)
### by default, exclude directories / begin with `.`
* [here](/applicationset/examples/git-generator-directory/excludes)
* `argocd app list | grep cluster-addons-exclude`
  * 's return ONLY 2
### `generators[git].directories[].exclude:true`
* [here](/applicationset/examples/git-generator-directory/excludes)
* `argocd app list | grep cluster-addons-exclude`
  * 's return NOT include -- for -- exclude-helm-guestbook
### 's priority > include rules
* `argocd app list | grep cluster-addons-exclude`
  * 's return NOT include -- for -- exclude-helm-guestbook
    * Reason:🧠exclude takes priority🧠
### order |  `generators[git].directories[]`, ❌NOT matter❌
* `argocd app list | grep cluster-addons-exclude`
  * 's return NOT include -- for -- exclude-helm-guestbook
## Root Of Git Repo -- `spec.generators[git].directories[*].path: '*'` --
* `kubectl apply -f applicationSetGitGeneratorDirectoryRootRepo.yaml`
* `argocd app list | grep generator-git-directory-rootrepo`
  * check it creates 1 application / EACH directory
## `values`
### allows: passing ADDITIONAL string key-value pairs
* `kubectl apply -f applicationSetGitGeneratorDirectory.yaml`
* `argocd app get "cluster-addons-general-argo-workflows" -o yaml`
  * check labels
### how to use? `values.(DEFINED_VALUES_KEY)`
* [here](applicationSetGitGeneratorDirectory.yaml)

# Git Generator: Files
## generates parameters -- based on -- specified repository's directory structure
* [here](/applicationset/examples/git-generator-files-discovery)
### == 👀generate 1 Application / EACH JSON/YAML file | specified repository👀
* [here](/applicationset/examples/git-generator-files-discovery)
## built-in parameters
### `{{.path.path}}`
* [here](/applicationset/examples/git-generator-files-discovery)
* `argocd app get engineering-dev-guestbook -o yaml`
  * check labels 
### `{{index .path.segments n}}`
* [here](/applicationset/examples/git-generator-files-discovery)
* `argocd app get engineering-dev-guestbook -o yaml`
  * check `metadata.labels`
### `{{.path.basename}}`
* [here](/applicationset/examples/git-generator-files-discovery)
* `argocd app get engineering-dev-guestbook -o yaml`
  * check labels
### `{{.path.basenameNormalized}}`
* [here](/applicationset/examples/git-generator-files-discovery)
* `argocd app get engineering-dev-guestbook -o yaml`
  * check `metadata.labels`
### `{{.path.filename}}`
* [here](/applicationset/examples/git-generator-files-discovery)
* `argocd app get engineering-dev-guestbook -o yaml`
  * check `metadata.labels`
## ⚠️if you specify `.git.pathParamPrefix` -> `<.git.pathParamPrefix_VALUE>.path.<path_parameter>`⚠️
* [here](applicationSetGitFilesPathParamPrefix.yaml)
* `kubectl apply -f applicationSetGitFilesPathParamPrefix.yaml`
* `argocd app get engineering-dev-guestbook-pathparamprefix -o yaml`
  * check labels
## Exclude files
* [here](/applicationset/examples/git-generator-files-discovery/excludes)
* `argocd app list | grep files-discovery-exclude`
  * return 1! Application
## `values`
### allows: passing ADDITIONAL string key-value pairs
* `kubectl apply -f applicationSetGitGeneratorFile.yaml`
* `argocd app get "engineering-dev-guestbook-gitgenerator-files" -o yaml`
  * check annotations
### how to use? `values.(DEFINED_VALUES_KEY)`
* [here](applicationSetGitGeneratorDirectory.yaml)

# Git Polling Interval
## ways to configure
### `ARGOCD_APPLICATIONSET_CONTROLLER_REQUEUE_AFTER` environment variable
#### got -- from -- `applicationsetcontroller.requeue.after` | "argocd-cmd-params-cm" ConfigMap
* `kubectl patch configmap argocd-cmd-params-cm -n argocd --type merge --patch-file patchArgoCdCmdParams.yaml`
* `kubectl rollout restart deployment argocd-applicationset-controller -n argocd`
* `kubectl exec -n argocd deployment/argocd-applicationset-controller -- env | grep -i requeue`
  * 's return: configured value
#### -> ALL ApplicationSet
TODO:
### `spec.generators[git].requeueAfterSeconds` / EACH ApplicationSet
* `kubectl apply -f applicationSetGitDirectoryRequeAfterSeconds.yaml`
* `argocd appset get git-directory-reque-afterseconds -o yaml`
  * 's return: requeueAfterSeconds: 45
#### 's priority > `ARGOCD_APPLICATIONSET_CONTROLLER_REQUEUE_AFTER`'s priority
* `kubectl logs -n argocd deployment/argocd-applicationset-controller --since=10m | grep "Reconciling\|reconcil" | grep "git-directory-reque-afterseconds"`
  * check there are 45" BETWEEN EACH line
## Git generator ⚠️depends on the ArgoCD Repo Server's Revision Cache Expiration setting⚠️
### `--revision-cache-expiration` flag
#### got it -- from -- `ARGOCD_RECONCILIATION_TIMEOUT` environment variable
##### by default, 3m
* `kubectl logs -n argocd argocd-application-controller-0 | grep -i "resync\|reconciliation" | head -5`
  * BETWEEN lines, there are 3'
##### == `timeout.reconciliation` | ["argocd-cm.yaml"](../examples/argocd-cm.yaml)
* `kubectl patch configmap argocd-cm -n argocd --type merge --patch-file patchArgoCdCM.yaml`
* `kubectl rollout restart deployment argocd-repo-server -n argocd`
  * restart
* `kubectl exec -n argocd deploy/argocd-repo-server -- env | grep ARGOCD_RECONCILIATION_TIMEOUT`
  * 's return: ARGOCD_RECONCILIATION_TIMEOUT=180
### ❌if Revision Cache Expiration > ApplicationSet Controller Polling Interval -> Git generator does NOT see NEW commits | files OR directories❌
TODO:

# `argocd.argoproj.io/application-set-refresh: true` annotation
## triggers an ApplicationSet refresh
TODO:
## AFTER reconciliation, the ApplicationSet controller removes this annotation
TODO:

# TODO:
TODO:

# Repository credentials
## if your ApplicationSets need credentials & the ApplicationSet project field is templated (`{{.}}`) -> you need to add the repository -- as a -- "non project scoped" repository
TODO:
### ways
#### -- via -- UI, set this == **blank**
TODO:
#### -- via -- CLI, | `argocd repo add`, ❌NOT pass `--project`❌
TODO:
#### -- via -- declaratively, | repository's secrets' `.stringData`, ❌NOT define `project:`❌
TODO: