# Simple Helm plugin

## requirements
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
* [install Kustomize](https://github.com/dancer1325/kubernetes-sigs-cli-experimental/tree/master/site/content/en/installation/kustomize)
## how to install?

* steps
  * | [plugin.yaml](plugin.yaml),
    * adjust the `<path>` -- based on -- where you mount the scripts | sidecar
  * `kustomize build . | kubectl apply -n argocd -f -`
  * check
    * `kubectl get pods -n argocd -l app.kubernetes.io/name=argocd-repo-server`
      * there are 2 container: "argocd-repo-server" container itself + "argocd-repo-server"s sidecar  
    * `kubectl logs -n argocd deployment/argocd-repo-server -c helm-plugin`
      * argocd-repo-server's sidecar logs
  * `kubectl apply -f applicationMatchingPluginDiscovery.yaml`
    * [applicationMatchingPluginDiscovery.yaml](applicationMatchingPluginDiscovery.yaml) match plugin's `spec.discovery`
  * `argocd app get helm-guestbook-match-plugin-discovery`
    * check they are up
  * `kubectl get app helm-guestbook-match-plugin-discovery -n argocd -o jsonpath='{.status.sourceType}'`
    * 's return: "plugin"
  * `kubectl logs -n argocd deployment/argocd-repo-server -c helm-plugin --tail=20`
    * check "Generating manifests"
  * `argocd app manifests helm-guestbook-with-params`
    * check
      * image: gcr.io/google-samples/gb-frontend:v6
      * replicas: 3
