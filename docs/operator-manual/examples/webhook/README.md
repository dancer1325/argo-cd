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
* [install Argo CD](../../operator-manual/installation.md)
* [deploy](https://github.com/dancer1325/argocd-example-apps/tree/master/apps#how-to-deploy-locally)

# vs Argo CD polling Git repositories
## ❌NO delay❌
TODO:

# webhook handler
## limitation: ❌NO differentiate branchName == tagName❌
TODO:

# steps
## 1. Create the WebHook | Git Provider
* follow the steps
  * set payload URL 
    * ❌https://localhost:8080/api/webhook NOT valid❌
      * Reason:🧠NOT reached -- through -- internet🧠
  * set secret
TODO: NOT POSSIBLE local, UNLESS you expose it
### | "argocd-cm" ConfigMap,
#### specify `data.webhook.maxPayloadSizeMB` -- based on -- your use case
##### == limit the payload size
TODO:
##### by default, 50MB
* `kubectl describe configmap argocd-cm -n argocd | grep maxPayloadSizeMB`
  * 's return: NOTHING
* [source code](/util/settings/settings.go)'s `defaultMaxWebhookPayloadSize = int64(50) * 1024 * 1024`
## 2. Configure the WebHook secret | Argo CD
* follow the steps
  * `kubectl patch secret argocd-secret -n argocd --type merge --patch-file patchWebhookArgoCDSecret.yaml`
  * `kubectl -n argocd rollout restart statefulset argocd-application-controller && kubectl -n argocd rollout status statefulset argocd-application-controller`
  TODO:

# TODO:
TODO: 