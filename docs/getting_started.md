# Getting Started

* read [understanding the basics](understand_the_basics.md)

## Requirements

* Install [kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl/)
* Have a [kubeconfig](https://kubernetes.io/docs/tasks/access-application-cluster/configure-access-multiple-clusters/) file
  * by default location,
    * `~/.kube/config`
* ways to run a cluster locally
  * -- via -- [kind](https://kind.sigs.k8s.io/) 
    * `kind create cluster`
  * TODO: OTHERS
* CoreDNS
  * | microk8s,
    * if you want to enable -> `microk8s enable dns && microk8s stop && microk8s start`

## 1. Install Argo CD

*
    ```bash
    kubectl create namespace argocd
    kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
    ```
  * ⚠️if you install Argo CD | DIFFERENT namespace -> update the https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml's namespace reference⚠️
    * see `ClusterRoleBinding` resources

  * ⚠️if you are NOT interested in UI, SSO & multi-cluster features -> install ONLY the Argo CD [core components](operator-manual/core.md#installing) ⚠️ 
    * requirements
      * self-signed certificate
        * follow [these instructions](operator-manual/tls.md)
        * configure the client
        * use `--insecure`

* `kubectl config set-context --current --namespace=argocd`
  * set CURRENT namespace
    
* `argocd login --core`
  * [configure](./user-guide/commands/argocd_login.md) CLI access

* Redis' default installation
  * -- is using -- password authentication /
    * password stored | Kubernetes secret `argocd-redis` 
    * key `auth` | namespace / Argo CD is installed

## 2. Download Argo CD CLI

* ways
  * [latest Argo CD version](https://github.com/argoproj/argo-cd/releases/latest)
    * see [CLI installation documentation](cli_installation.md)
  * | Mac, Linux & WSL Homebrew
    ```bash
    brew install argocd
    ```

## 3. Access Argo CD API Server

* Argo CD API server
  * ❌by default, NOT exposed -- with an -- external IP❌

### ways to expose
#### Service Type Load Balancer

* change the argocd-server service's type -- to -- `LoadBalancer`
    ```bash
    kubectl patch svc argocd-server -n argocd -p '{"spec": {"type": "LoadBalancer"}}'
    ```

#### Ingress
* [here](operator-manual/ingress.md)

#### Port Forwarding
* allows
  * connecting to the API server / WITHOUT exposing the service

* steps
  * `kubectl port-forward svc/argocd-server -n argocd 8080:443`
  * | browser, opens https://localhost:8080

## 4. login -- via -- CLI

* `admin` account
  * 's INITIAL password
    * auto-generated
    * 💡stored as clear text | secret `argocd-initial-admin-secret`'s field `password` 💡
      * 👀if you want to retrieve it -> `argocd admin initial-password -n argocd` 👀
    * recommendations
      * change the password -- via -- `argocd account update-password`
      * delete `argocd-initial-admin-secret`
    * if a NEW admin password MUST be re-generated -> it will be re-created -- by Argo CD, -- on demand  

* `argocd login <ARGOCD_SERVER>` 
  * enter `admin` & PREVIOUS password
  * if [Argo CD API server is DIRECTLY accessible](#3-access-the-argo-cd-api-server) -- by --
    * service type LoadBalancer -> TODO: How?
    * Ingress -> TODO: How?
    * Port Forwarding -> `argocd login localhost:8080`
  * if [Argo CD API server is ❌NOT❌ DIRECTLY accessible](#3-access-the-argo-cd-api-server) 
    * -> ways to access 
      1) add `--port-forward-namespace argocd` flag | EVERY CLI command; or 
      2) `export ARGOCD_OPTS='--port-forward-namespace argocd'`
    * Problems:
      * Problem1: "FATA[0000] dial tcp: lookup cd.argoproj.io: no such host"
        * Solution: TODO:

## 5. Register A Cluster -- to -- Deploy Apps 

* 👀OPTIONAL 👀
* registers a cluster's credentials | Argo CD
* use cases
  * deploy | EXTERNAL cluster 
* if you deploy INTERNALLY (== SAME cluster | Argo CD runs) -> 
  * https://kubernetes.default.svc == application's K8s API server address

* steps
  * `kubectl config get-contexts -o name`
    * list ALL clusters contexts | your CURRENT kubeconfig
  * `argocd cluster add CONTEXTNAME`
    * choose a context name -- from the -- list
    * installs a ServiceAccount (`argocd-manager`)
      * | that kubectl context's kube-system namespace
      * bound -- to an -- admin-level ClusterRole
      * uses
        * by Argo CD, -- to -- perform Argo CD's management tasks (_Example:_ deploy/monitoring)

* `argocd-manager-role` role
  * `create`, `update`, `patch`, `delete` privileges -- can be -- modified | limited set of namespaces, groups, kinds
  * required to work Argo CD,
    * | cluster-scope,
      * `get`, `list`, `watch` privileges  

## 6. Create An Application -- from A -- Git Repository

* _Example:_ [sample git repository](https://github.com/argoproj/argocd-example-apps.git)

### Creating Apps -- via -- CLI

* `kubectl config set-context --current --namespace=argocd`
  * set "argocd" -- as -- CURRENT namespace

* `argocd app create guestbook --repo https://github.com/dancer1325/argocd-example-apps.git --path guestbook --dest-server https://kubernetes.default.svc --dest-namespace default`
  * create the example guestbook application
  * Problems:
    * Problem1: "FATA[0000] Argo CD server address unspecified"
      * Solution: ⚠️[log PREVIOUSLY](#3-access-argo-cd-api-server)⚠️ 

### Creating Apps -- via -- UI

* | browser,
  * "argocd-server'sIP:argocd-server'sport"
    * if you [exposed it](#3-access-argo-cd-api-server) -- by --
      * service type LoadBalancer -> TODO: How?
      * Ingress -> TODO: How?
      * Port Forwarding -> "localhost:8080"
  * [pass admin credentials](#4-login----via----cli)
  * | Applications, click **+ New App** button
    
    ![+ new app button](assets/new-app.png)
  * | NEW panel opened
    * 's general

      ![app information](assets/app-ui-information.png)
    * 's source

      ![connect repo](assets/connect-repo.png)

    * 's destination

      ![destination](assets/destination.png)

## 7. Sync (Deploy) The Application

### Syncing via CLI

```bash
$ argocd app get guestbook
Name:               guestbook
Server:             https://kubernetes.default.svc
Namespace:          default
URL:                https://10.97.164.88/applications/guestbook
Repo:               https://github.com/argoproj/argocd-example-apps.git
Target:
Path:               guestbook
Sync Policy:        <none>
Sync Status:        OutOfSync from  (1ff8a67)
Health Status:      Missing

GROUP  KIND        NAMESPACE  NAME          STATUS     HEALTH
apps   Deployment  default    guestbook-ui  OutOfSync  Missing
       Service     default    guestbook-ui  OutOfSync  Missing
```

* application status
  * ⚠️INITIALLY, `OutOfSync` ⚠️
    * Reason: 🧠 
      * application has to be deployed
      * NO Kubernetes resources have been created 🧠

* `argocd app sync [APPNAME... | -l selector | --project project-name]` 
    ```bash
    argocd app sync guestbook
    ```
  * how does it work?
    * from the repository -- retrieves the -- manifests 
    * performs a `kubectl apply` of the manifests

### Syncing -- via -- UI

* steps
  * | Applications page, click "Sync" of the guestbook application
      ![guestbook app](assets/guestbook-app.png)
  * | panel opened, click on "Synchronize"

