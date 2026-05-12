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

# repositories & repository credentials
## are stored | secrets
* [here](#configure----via----argo-cd-cli)
## recommendations: 👀-- via -- declaratively, use secret management👀
* [here](#declaratively)

# Credentials methods
## Protocol-based
### HTTPS
#### Username & Password
TODO: check one of the supported ones (GitLab self-hosted, Bitbucket Server on-premise, Azure DevOps)
#### Access Token
##### configure -- via -- Argo CD CLI
* `argocd repo add https://github.com/dancer1325/argocd-example-apps-private.git --username "anything" --password <ACCESS_TOKEN>`
* [deploy ArgoCD Applications](https://github.com/dancer1325/argocd-example-apps-private/tree/master/apps#steps)
* `argocd app list`
* `argocd app sync example.guestbook`
* `kubectl get all -n guestbook`
  * 's return: deployment & service is running
* check that they are stored -- as -- secrets
  * `kubectl get secrets -n argocd -l argocd.argoproj.io/secret-type=repository`
    * 's return: EXISTING repository resources
  * `kubectl get secrets <REPO_NAME> -n argocd -o yaml`
    * `kubectl get secrets repo-4050197233 -n argocd -o yaml`
      * 's return: repo + repo credentials
##### -- via -- UI
* follow the steps
##### declaratively
* [here](httpsRepoCredentials.yaml)
* `kubectl apply -f httpsUsernamePassword.yaml`
* `argocd repo list`
  * 's return: https://github.com/dancer1325/argocd-example-apps-private.git repo -- as -- successful
#### TLS Client Certificates -- for -- HTTPS repositories
##### configure -- via -- Argo CD CLI
TODO: 
##### -- via -- UI
* follow the steps
##### declaratively
* [here](httpsRepoCredentials.yaml)
* `kubectl apply -f httpsUsernamePassword.yaml`
### SSH
#### ⚠️requirements⚠️
##### Git repo
TODO:
###### ❌NOT valid | helm repos OR OCI repos❌
TODO:
##### URL regex
TODO:
#### ways to configure
##### configure -- via -- Argo CD CLI
TODO:
##### -- via -- UI
TODO:
##### declaratively
* [here](httpsRepoCredentials.yaml)
* `kubectl apply -f httpsUsernamePassword.yaml`

## TODO: 


# TODO:
TODO: