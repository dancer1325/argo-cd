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

# TODO:


# Repositories

# Clusters

# TODO:

* TODO:

# "self-managed" Argo CD
## == 💡Argo CD is managed -- by -- Argo CD 💡
* prepare stack / deploy SAME Argo CD / you are going to track
  * `kubectl create namespace argocd`
  * `kubectl apply -n argocd --server-side --force-conflicts -k https://github.com/dancer1325/argo-cd/manifests/cluster-install`
* `kubectl apply -f applicationToMonitorArgoCD.yaml`
* `kubectl port-forward svc/argocd-server -n argocd 8080:443`
  * port-forward "argocd-server" locally
* `kubectl get secret argocd-initial-admin-secret -n argocd -o jsonpath='{.data.password}' | base64 -d`
  * copy the password
* https://localhost:8080/
  * login
    * user: admin
    * password: previouslyCopiedPassword
  * \> Applications > argocd
