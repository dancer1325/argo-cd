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

## -- via -- Client authentication

* steps
  * Problem:
    * Problem1: ArgoCD server | cluster can NOT reach Keycloak
      * Reason: 🧠
        * Keycloak's `KC_HOSTNAME` (== `http://keycloak.localhost:32770`) resolves to `127.0.0.1` | pod 
        * port `32770` ONLY exists -- as a -- Docker mapping | outside the cluster🧠
      * SOLUTION
        * `kubectl apply -f serviceInternalKeycloack.yaml`
        * | argocd-server deployment, add a `hostAlias` / `keycloak.localhost` resolves -- to the -- NEW service's ClusterIP 
          * `CLUSTER_IP=$(kubectl get svc keycloak-internal -o jsonpath='{.spec.clusterIP}')`
          * `kubectl patch deployment argocd-server -n argocd --type='json' -p="[{\"op\": \"add\", \"path\": \"/spec/template/spec/hostAliases\", \"value\": [{\"ip\": \"$CLUSTER_IP\", \"hostnames\": [\"keycloak.localhost\"]}]}]"`
  * follow [guide](../../keycloak.md#how-to-configure-argocd-oidc)
    * ==
      * `kubectl -n argocd patch secret argocd-secret --patch='{"stringData": { "oidc.keycloak.clientSecret": "<REPLACE_WITH_CLIENT_SECRET>" }}'`
      * `kubectl patch configmap argocd-cm -n argocd --type merge --patch-file patchForClientAuthentication.yaml`

## -- via -- PKCE
TODO:


## how to configure the `groups` claim?
TODO:

## how to configure the ArgoCD Policy?
TODO:

## Login
TODO:

