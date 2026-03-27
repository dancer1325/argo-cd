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

# Quick Start
## 1. Install Argo CD

```bash
# 1.
kubectl create namespace argocd
#   check argocd namespace was created
kubectl get namespace

# 2. 
# ⚠️if you do NOT pass --server-side --force-conflicts -> you get errors⚠️
#     "The CustomResourceDefinition "applicationsets.argoproj.io" is invalid: metadata.annotations: Too long: must have at most 262144 bytes"
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml

# SOLUTION: 
kubectl apply -n argocd --server-side --force-conflicts -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
```

* `--server-side`
  * [here](https://kubernetes.io/docs/reference/using-api/server-side-apply/)
* `last-applied-configuration`
  * ['s size < 256kb](https://github.com/kubernetes/kubernetes/blob/master/staging/src/k8s.io/apimachinery/pkg/api/validation/objectmeta.go#L36)
* `--force-conflicts`
  * [here](https://kubernetes.io/docs/reference/using-api/server-side-apply/)

* ⚠️if you install Argo CD | DIFFERENT namespace -> update `ClusterRoleBinding.subjects.namespace` | [install.yaml](/manifests/install.yaml) ⚠️

* ⚠️if you are NOT interested in UI, SSO & multi-cluster features -> install ONLY the Argo CD [core components](/docs/operator-manual/core.md#installing) ⚠️
  * requirements
    * self-signed certificate
      * Reason:🧠| Argo CD Core installation, there is NO permanent Argo CD API Server / generates certificate🧠
      * | server side,
        * [here](/docs/operator-manual/tls.md)
      * | client side,
        * `.. --insecure`, OR
        * `--server-crt /path/to/cert.pem`
  
    ```
    FULL install                          CORE install
    ─────────────────────────────         ──────────────────────────────────
    argocd-server (permanent)             NO permanent argocd-server
      - manages TLS automatically           │
      - auto-generated cert                 │ argocd login --core
      - serves UI + SSO + API               │
                                            ▼
                                          CLI spawns a LOCAL temporary
                                          API server process
                                            │
                                            │ needs TLS to work
                                            │ NO cert-manager
                                            │ NO ingress
                                            ▼
                                          self-signed certificate required
                                            │
                                            ├── option 1: configure client to trust it
                                            └── option 2: use --insecure flag
    ```

* `kubectl config set-context --current --namespace=argocd`
  * set CURRENT context / namespace=argocd

* `argocd login --core`
  * [configure](../../user-guide/commands/argocd_login.md) CLI access
  * -> | "~/.config/argocd/config", saves `core: true` 
    * subsequent commands flow:
      ```
      argocd <command>
          │
          ▼
      reads ~/.config/argocd/config
          │
          └── core: true?
                │
                ▼  YES
              spawns local temporary API server
                │
                ▼
              Kubernetes API server  ← uses kubeconfig directly
              (❌NO argocd-server needed❌)
      ```

* Redis' default installation
  * -- is using -- password authentication 
    * see it [here](/manifests/install.yaml)'s `kind: Deployment` -- for -- "argocd-server"
    * /
      * password stored | Kubernetes secret `argocd-redis`
      * key `auth` | namespace / Argo CD is installed
        * `kubectl get secret argocd-redis -n argocd -o jsonpath='{.data.auth}' | base64 -d`

## 2. Download Argo CD CLI

* [here](../../cli_installation.md)

## 3. Access Argo CD

* Argo CD
  * ❌by default, NOT exposed outside the cluster❌
    * `kubectl get svc -n argocd` ALL are TYPE == ClusterIP & `kubectl get ingress` is EMPTY

### ways to expose
#### Service Type Load Balancer

* change the argocd-server service's type -- to -- `LoadBalancer`
    ```bash
    kubectl patch svc argocd-server -n argocd -p '{"spec": {"type": "LoadBalancer"}}'
    ```
  * AFTER a while -> your cloud provider will assign an external IP address
    * `kubectl get svc argocd-server -n argocd -o=jsonpath='{.status.loadBalancer.ingress[0].ip}'`

#### Ingress
* [here](operator-manual/ingress.md)

#### Port Forwarding
* allows
  * connecting to the API server / WITHOUT exposing the service

* steps
  * `kubectl port-forward svc/argocd-server -n argocd 8080:443`
  * `kubectl get secret argocd-initial-admin-secret -n argocd -o jsonpath='{.data.password}' | base64 -d`
    * copy the password
  * | browser, opens https://localhost:8080
    * user: admin
    * password: previouslyCopied

## 4. login -- via -- CLI

* `admin` account
  * 's INITIAL password
    * auto-generated
      * ⚠️EACH time the ArgoCD Server pod is rebooted⚠️
    * 💡stored as clear text | secret `argocd-initial-admin-secret`'s field `password` 💡
    * ways to retrieve
      * `argocd admin initial-password -n argocd` OR
        * Problems:
          * Problem1: {"level":"fatal","msg":"secrets \"argocd-initial-admin-secret\" not found"
            * Solution: `argocd login --core`
            * Reason:🧠ArgoCD config file ("$HOME/.config/argocd") was NOT configured properly 🧠
      * `kubectl get secret argocd-initial-admin-secret -n argocd -o jsonpath='{.data.password}' | base64 -d`
    * recommendations
      * change the password -- via -- `argocd account update-password`
        * requirements
          * 's length == [8,32]
        * steps:
          * `argocd login localhost:8080 --insecure`
            * user: admin
            * password: previouslyCopied
          * `argocd account update-password`
            * password: previouslyCopied
            * new password: aaaaaaaa
        * Problem:
          * Problem1: "{"level":"fatal","msg":"configmap \"argocd-cm\" not found" 
            * Solution: `kubectl config set-context --current --namespace=argocd`
              * Reason:🧠NOT specified namespace | current-context -> default one🧠
      * delete `argocd-initial-admin-secret`
        * steps
          * `kubectl delete secret argocd-initial-admin-secret -n argocd`
  * if you loose the admin password ->
    * `htpasswd -bnBC 10 "" nuevaPassword | tr -d ':\n' | sed 's/$2y/$2a/'`
      * generate a NEW hash bcrypt
    * `kubectl -n argocd patch secret argocd-secret -p '{"stringData": {"admin.password":        
  "$2a$10$8/xsS0Bdr95FvZlo4sZh7e660kYJ8LxVQP5xeesgTO8iBOJcArgXK", "admin.passwordMtime":    
  "'$(date +%FT%T%Z)'"}}'`
  * if a NEW admin password MUST be re-generated -> it will be re-created -- by Argo CD, -- on demand

* `argocd login <ARGOCD_SERVER>`
  * enter `admin` & PREVIOUS password
  * if [Argo CD API server is DIRECTLY accessible](/docs/user-guide/commands/argocd_login.md)
  * if [Argo CD API server is ❌NOT❌ DIRECTLY accessible](#ways-to-expose)
    * requirements
      * | "~/.config/argocd/config", `core: false`
    * -> ways to access
      1) add `--port-forward-namespace argocd` flag | EVERY CLI command; OR
         * _Example:_ `argocd cluster list --port-forward-namespace argocd`
         * Problems:
           * Problem1: "{"level":"fatal","msg":"rpc error: code = Unauthenticated desc = no session information""
             * Solution: 
               * `argocd login --port-forward --port-forward-namespace argocd --insecure`
                 * user: admin
                 * password: adminPassword
             * Reason: 🧠token expired 
      2) `export ARGOCD_OPTS='--port-forward-namespace argocd'`

## 5. Register A Cluster -- to -- Deploy Apps

* goal
  * cluster | deploy Argo CD Applications != cluster | Argo CD is installed
    ```
    ┌─────────────────────────────┐       ┌─────────────────────────────┐
    │  Cluster A  (hub)           │       │  Cluster B  (spoke)         │
    │                             │       │                             │
    │  - ArgoCD installed         │       │  - ArgoCD Applications      │
    │  - argocd-manager SA        │──────▶│    deployed here            │
    │    credentials stored       │       │  - argocd-manager SA        │
    │    as Secret                │       │    installed here           │
    └─────────────────────────────┘       └─────────────────────────────┘
    ```

* local recommendations
  * 2 Kind clusters

* 👀OPTIONAL 👀
  * if you deploy INTERNALLY (== SAME cluster | Argo CD runs) ->
    * https://kubernetes.default.svc == application's K8s API server address

* registers a cluster's credentials | Argo CD

* steps
  * create another cluster
    * [requirements](#requirements)
  * `kubectl config get-contexts -o name`
    * list ALL clusters contexts | your CURRENT kubeconfig
  * `argocd cluster add <CONTEXTNAME>`
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

## 6. Create an Application -- from a -- Git Repository

* _Example:_ [sample git repository](https://github.com/dancer1325/argocd-example-apps)

TODO:
> The following example application may only be compatible with AMD64 architecture
> If you are running on a different architecture (such as ARM64 or ARMv7), you may encounter issues with dependencies or container images that are not built for your platform
> Consider verifying the compatibility of the application or building architecture-specific images if necessary.

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
    * -- depend on -- [way of exposing](#ways-to-expose)
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

## 8. how to uninstall Argo CD?

* `kubectl delete -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml`
* `kubectl delete namespace argocd`
