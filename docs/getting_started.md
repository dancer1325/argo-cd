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
    # TODO: check why it's recommended NOW
    # kubectl apply -n argocd --server-side --force-conflicts -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
    ```
  * ⚠️if you install Argo CD | DIFFERENT namespace -> update the https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml's namespace reference⚠️
    * see `ClusterRoleBinding` resources


> [!NOTE]
> **Why `--server-side --force-conflicts`?**
>
> The `--server-side` flag is required because some Argo CD CRDs (like ApplicationSet) exceed the 262KB annotation size limit imposed by client-side `kubectl apply`. Server-side apply avoids this limitation by not storing the `last-applied-configuration` annotation.
>
> The `--force-conflicts` flag allows the apply operation to take ownership of fields that may have been previously managed by other tools (such as Helm or a previous `kubectl apply`). This is safe for fresh installs and necessary for upgrades. Note that any custom modifications you've made to fields that are defined in the Argo CD manifests (like `affinity`, `env`, or `probes`) will be overwritten. However, fields not specified in the manifests (like `resources` limits/requests or `tolerations`) will be preserved.

> [!WARNING]
> The installation manifests include `ClusterRoleBinding` resources that reference `argocd` namespace. If you are installing Argo CD into a different
> namespace then make sure to update the namespace reference.

  * ⚠️if you are NOT interested in UI, SSO & multi-cluster features -> install ONLY the Argo CD [core components](operator-manual/core.md#installing) ⚠️ 
    * requirements
      * self-signed certificate
        * follow [these instructions](operator-manual/tls.md)
        * configure the client
        * use `--insecure`

This default installation will have a self-signed certificate and cannot be accessed without a bit of extra work.
Do one of:

* Follow the [instructions to configure a certificate](operator-manual/tls.md) (and ensure that the client OS trusts it).
* Configure the client OS to trust the self signed certificate.
* Use the --insecure flag on all Argo CD CLI operations in this guide.

* `kubectl config set-context --current --namespace=argocd`
  * set CURRENT namespace
    
* `argocd login --core`
  * [configure](./user-guide/commands/argocd_login.md) CLI access

* Redis' default installation
  * -- is using -- password authentication /
    * password stored | Kubernetes secret `argocd-redis` 
    * key `auth` | namespace / Argo CD is installed

* TODO: 
> If you are running Argo CD on Docker Desktop or another local Kubernetes environment, refer to the [Running Argo CD Locally](developer-guide/running-locally.md) guide for the full setup instructions and configuration steps tailored for local clusters.

## 2. Download Argo CD CLI

* ways
  * [latest Argo CD version](https://github.com/argoproj/argo-cd/releases/latest)
    * see [CLI installation documentation](cli_installation.md)
  * | Mac, Linux & WSL Homebrew
    ```bash
    brew install argocd
    ```

## 3. Access Argo CD

* Argo CD
  * ❌by default, NOT exposed outside the cluster❌

### ways to expose
#### Service Type Load Balancer

* change the argocd-server service's type -- to -- `LoadBalancer`
    ```bash
    kubectl patch svc argocd-server -n argocd -p '{"spec": {"type": "LoadBalancer"}}'
    ```
After a short wait, your cloud provider will assign an external IP address to the service. You can retrieve this IP with:

```bash
kubectl get svc argocd-server -n argocd -o=jsonpath='{.status.loadBalancer.ingress[0].ip}'
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

TODO:
> [!WARNING]
> You should delete the `argocd-initial-admin-secret` from the Argo CD
> namespace once you changed the password. The secret serves no other
> purpose than to store the initially generated password in clear and can
> safely be deleted at any time. It will be re-created on demand by Argo CD
> if a new admin password must be re-generated.


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

TODO:
> The following example application may only be compatible with AMD64 architecture. If you are running on a different architecture (such as ARM64 or ARMv7), you may encounter issues with dependencies or container images that are not built for your platform. Consider verifying the compatibility of the application or building architecture-specific images if necessary.

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

