# requirements
* download software / enable you to run local Kubernetes clusters
  * [Docker desktop](https://docs.docker.com/get-started/introduction/get-docker-desktop/)
  * [kind](https://kind.sigs.k8s.io/) + [install Kubectl](https://kubernetes.io/docs/tasks/tools/#kubectl)
  * [minikube](https://minikube.sigs.k8s.io/docs/)
    * `kubectl` commands are wrapped -- via -- `minikube kubectl`
  * [microk8s](https://canonical.com/microk8s)
    * `kubectl` commands are wrapped -- via -- `microk8s kubectl`
* run ⚠️2⚠️ local Kubernetes cluster
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
* [install Argo CD](../../../installation.md)
* login
  * `kubectl get secret argocd-initial-admin-secret -n argocd -o jsonpath='{.data.password}' | base64 -d`
    * get initial admin password
  * `argocd login localhost:8080 --insecure`
    * user: admin
    * password: pasteInitialAdminPassword
* configure 2 clusterS | Argo CD
  * Docker Desktop + Minikube
    * `argocd cluster add minikube --server localhost:8080 --insecure`
      * Problems:
        * Problem1: "failed to get server version: Get \"https://127.0.0.1:55552/version?timeout=32s"
          * Solution: `kubectl config set-cluster minikube --server=https://192.168.49.2:8443 --insecure-skip-tls-verify=true`
            * Reason: 🧠set right minikube IP
              * got -- through -- `docker ps | grep minikube`🧠
        * Problem2: "failed to create service account \"argocd-manager\" in namespace \"kube-system"
          * Solution: TODO:
  * Kind1 + Kind2
    * TODO: 

# FROM 1! Argo CD Application template, generate -- , via generators, -- MULTIPLE Applications
* _Example:_ `ApplicationSet` resource / Argo CD Application -- targeted, via list generator, to -- MULTIPLE clusters
* TODO:
* 