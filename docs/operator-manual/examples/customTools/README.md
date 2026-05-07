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

# ArgoCD
## about supported templating tools (helm, kustomize, ks, jsonnet)
### bundled PREFERRED versions
* `argocd version`
  * 's return: templating tools version
* [source code](/hack/tool-versions.sh)

# adding tools -- via -- volume mounts
* `kubectl patch deployment argocd-repo-server -n argocd --patch-file patchRepoServerDeploymentAddingToolsViaVolumeMounts.yaml`
* `kubectl --context kind-kind -n argocd exec deployment/argocd-repo-server -- helm version --short`
  * 's return: v2.12.3 == configured 
    * != `argocd version --server`

# BYOI (Build Your Own Image)
* `docker build -t dancer13/argocd-custom:v2.5.4 .`
* `docker push dancer13/argocd-custom:v2.5.4` 
* `kubectl set image deployment/argocd-repo-server argocd-repo-server=dancer13/argocd-custom:v2.5.4 -n argocd`
* `kubectl get deployment argocd-repo-server -o jsonpath='{.spec.template.spec.containers[0].image}' -n argocd`
  * 's return: dancer13/argocd-custom:v2.5.4
