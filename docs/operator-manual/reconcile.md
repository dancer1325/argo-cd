# Reconcile Optimization

* reconcile
  * == process / 
    * 💡desired state == cluster state💡

```
╔═════════════════════════════════════════════════════════════════╗
║                 RECONCILE PROCESS                               ║
╠═════════════════════════════════════════════════════════════════╣
║           ┌──────────────────────────────────┐                  ║
║           │  Refresh                         │                  ║
║           │  ┌────────────────────────────┐  │                  ║
║           │  │ • Get desired state:       │  │                  ║
║           │  │   - From cache OR          │  │                  ║
║           │  │   - Fetch from Git         │  │                  ║
║           │  │   (== hard refresh)        │  │                  ║
║           │  │                            │  │                  ║
║           │  │ • Get live state           │  │                  ║
║           │  │   (via Kube API)           │  │                  ║
║           │  │                            │  │                  ║
║           │  │ • Diffing (==              │  │                  ║
║           │  │   Compare both with        │  │                  ║
║           │  │   ignoreDifferences):      │  │                  ║
║           │  │   - System-level           │  │                  ║
║           │  │   - Per-app config         │  │                  ║
║           │  └────────────────────────────┘  │                  ║
║           └──────────────┬───────────────────┘                  ║
║                          ↓                                      ║
║           ┌──────────────────────────────────┐                  ║
║           │  Update Sync Status              │                  ║
║           │  (based on comparison)           │                  ║
║           └──────────┬─────────┬─────────────┘                  ║
║                      │         │                                ║
║               Synced │         │ OutOfSync                      ║
║                      ↓         ↓                                ║
║            ┌────────┐   ┌──────────────────────┐                ║
║            │  END   │   │ Auto-Sync OR         │                ║
║            └────────┘   │    MANUAL sync       │                ║
║                         └──────────────────────┘                ║
║                                   ↓                             ║
║                                 END                             ║
╚═════════════════════════════════════════════════════════════════╝
```

## ⭐️ways to trigger it ⭐️

* [live state changes](#live-state-changes-)
* [Argo CD poll configuration](#polling)
* [webhooks](#git-webhook)
* [MANUAL refresh](#manual-refresh-cli--ui)
  * -- via -- CLI
    * `--refresh`
      * `argocd app get APPNAME --refresh`
  * -- via -- Argo CD UI

### live state changes 

```
┌─────────────────────────────────────────────────────────────────┐
│                    Kubernetes Cluster                           │
│  Resource changes (Pod restart, HPA scaling, etc.)              │
└────────────────────────────┬────────────────────────────────────┘
                             ↓
╔═════════════════════════════════════════════════════════════════╗
║           Application Controller                                ║
╠═════════════════════════════════════════════════════════════════╣
║           ┌─────────────────────┐                               ║
║           │  Watch  Resources   │                               ║
║           │(tracked & untracked)│                               ║
║           │  (Kubernetes API)   │                               ║
║           └────────┬────────────┘                               ║
║                    ↓                                            ║
║           ┌────────────────────┐                                ║
║           │  Detect Change     │                                ║
║           │  (Watch event)     │                                ║
║           └────────┬───────────┘                                ║
║                    ↓                                            ║
║       ┌──────────────────────────────┐                          ║
║       │  ignoreResourceUpdates?      │                          ║
║       │  • System-level config       │                          ║
║       │  • Resource annotation       │                          ║
║       └──────┬───────────────┬───────┘                          ║
║              │               │                                  ║
║          YES │               │ NO                               ║
║              ↓               │                                  ║
║  ┌─────────────────────┐    │                                   ║
║  │ Health status       │    │                                   ║
║  │     changed?        │    │                                   ║
║  └───┬──────────┬──────┘    │                                   ║
║      │          │           │                                   ║
║   NO │       YES│           │                                   ║
║      ↓          │           │                                   ║
║ ┌────────┐      │           │                                   ║
║ │  STOP  │      │           │                                   ║
║ └────────┘      ↓           ↓                                   ║
║       ┌─────────────────────────────┐                           ║
║       │    Enqueue Application      │                           ║
║       └────────────┬────────────────┘                           ║
║                    ↓                                            ║
║                     RECONCILE                                   ║
╚═════════════════════════════════════════════════════════════════╝
```

* 👀| specific fields, ignore resource updates 👀
  * -- for -- [tracked resources](../user-guide/resource_tracking.md)
  * -- for -- [untracked resources](#-untracked-resources-how-to-ignore-updates)

#### how to check that resource updates are ignored?

* steps
  * configure the application-controller's log level == `debug`
  * look for | application-controller's logs: "Ignoring change of object because none of the watched resource fields have changed"

#### untracked resources

* untracked resources
  * == resources / NOT exist | Git & exist | cluster
    * types 
      * tracked resources' dependant
        * _Example:_ `Deployment` | Git,
          * creates DEPENDENT `ReplicaSet` & `Pod` | Cluster
          * DEPENDENT `ReplicaSet` & `Pod` do NOT exist | Git
      * MANUALLY created
  * Argo CD
    * ❌do NOT reconcile them ❌
      * Reason:🧠it does NOT exist | Git🧠
    * 💡monitors them💡
      * _Example:_ if DEPENDENT `ReplicaSet` & `Pod` | Cluster change -> trigger a reconcile of whole Application

#### how to ignore resource updates?

* ways
  * | "argocd-cm" ConfigMap
  * | OWN resources, annotate with `argocd.argoproj.io/ignore-resource-updates=true`

##### | "argocd-cm" ConfigMap

* | "argocd-cm" ConfigMap,
  * `resource.ignoreResourceUpdatesEnabled`
    * 👀enable OR disable👀
      * Argo CD can ignore resource updates
    * by default, `true`
      * -> reduce unnecessary reconcile operations
    * ALLOWED values
      * `'true'`
      * `'false'`
  * `resource.customizations.ignoreResourceUpdates.all`

      ```yaml
      data:
        resource.customizations.ignoreResourceUpdates.all: |                                                                                                                                                                                
          # ways to specify the resource updates / ignore
          jsonPointers:              # [JSON Pointer]                                                                                                                                                                   
          - /path/to/field                                                                                                                                                                                                                     
          jqPathExpressions:         # [JQPathExpressions]                                                                                                                                                                      
          - .path.to.field  
      ```
    * [JSON pointers](https://tools.ietf.org/html/rfc6902)
    * [JQ path expressions](https://stedolan.github.io/jq/manual/#path(path_expression))
  * `resource.customizations.ignoreResourceUpdates.<group>_<kind>`
    * ⚠️override `resource.customizations.ignoreResourceUpdates.all`⚠️

      ```yaml
      data:
        resource.customizations.ignoreResourceUpdates.<group>_<kind>: |                                                                                                                                                                                
          # ways to specify the resource updates / ignore
          jsonPointers:              # [JSON Pointer]                                                                                                                                                                   
          - /path/to/field                                                                                                                                                                                                                     
          jqPathExpressions:         # [JQPathExpressions]                                                                                                                                                                      
          - .path.to.field  
      ```
    * [JSON pointers](https://tools.ietf.org/html/rfc6902)
    * [JQ path expressions](https://stedolan.github.io/jq/manual/#path(path_expression))

##### | OWN resources, annotate with `argocd.argoproj.io/ignore-resource-updates=true`

* requirements  
  * | "argocd-cm" ConfigMap,
  * `resource.ignoreResourceUpdatesEnabled: 'true'`

* `argocd.argoproj.io/ignore-resource-updates` annotations
  * ⚠️ONLY apply | k8s resource ⚠️
  * |
    * tracked resources,
      * ❌does NOT apply | tracked DEPENDENT resources❌
        * _Example:_ `Deployment` | GIT -> `Deployment`'s DEPENDENT `ReplicaSet` & `Pod` are NOT ignored
    * untracked resources,
      * you MUST MANUALLY add

### Polling

```
╔═════════════════════════════════════════════════════════════════╗
║           Application Controller                                ║
╠═════════════════════════════════════════════════════════════════╣
║           ┌────────────────────────────────┐                    ║
║           │  ⏱️ timeout.reconciliation     │                    ║ 
║           │             +                  │                    ║
║           │     timeout.reconciliation     │                    ║
║           │        (default 3m) expires    │                    ║
║           └────────────┬───────────────────┘                    ║
║                        ↓                                        ║
║           ┌─────────────────────────────┐                       ║
║           │ Enqueue Application         │                       ║
║           └────────────┬────────────────┘                       ║
║                        ↓                                        ║
║                     RECONCILE                                   ║
╚═════════════════════════════════════════════════════════════════╝
```

* [`data.timeout.reconciliation`, `data.timeout.reconciliation` + `data.timeout.reconciliation.jitter`]
  * == frequency / Argo CD poll changes -- from -- Git OR helm repository
    * ❌NOT ALWAYS SAME❌
      * Reason:🧠`data.timeout.reconciliation.jitter` is arbitrary🧠
  * by default, EACH 3' (== 2 + 1)
  * specified | "argocd-cm" ConfigMap,
  * `data.timeout.reconciliation`
    * ⚠️if you set 0 -> disables AUTOMATIC polling⚠️
      * requirements
        * configure `ARGOCD_DEFAULT_CACHE_EXPIRATION`
          * by default, 24h
          * Reason:🧠OTHERWISE, argocd-repo-server does NOT expire🧠
      * -> use ANOTHER reconciliation trigger
      * ❌NOT recommended❌
        * Reason: 🧠
          * ArgoCD would trust in OTHER approaches / have MORE dependencies
          * misconfiguration🧠
  * [MORE](/docs/operator-manual/examples/argocd-cm.yaml)

* recommendations
  * if you set Argo CD poll + Git webhook -> set `timeout.reconciliation` = medium values (_Example:_ `15m`, `1h`)
    * Reason:🧠OTHERWISE it's redundant -- by -- Git webhooks / are ALMOST IMMEDIATLEY🧠

### Git Webhook

```
┌─────────────────────────────────────────────────────────────────┐
│  Git Repository (GitHub, GitLab, Bitbucket)                     │
│  Push event → webhook → Argo CD API Server                      │
└────────────────────────────┬────────────────────────────────────┘
                             ↓
╔═════════════════════════════════════════════════════════════════╗
║           Application Controller                                ║
╠═════════════════════════════════════════════════════════════════╣
║           ┌─────────────────────────────┐                       ║
║           │ Enqueue Application         │                       ║
║           └────────────┬────────────────┘                       ║
║                        ↓                                        ║
║                     RECONCILE                                   ║
╚═════════════════════════════════════════════════════════════════╝
```

* [MORE](webhook.md)

### Manual Refresh (CLI / UI)

```
┌─────────────────────────────────────────────────────────────────┐
│  User action:                                                   │
│  • argocd app get APPNAME --refresh                             │
│  • argocd app get APPNAME --hard-refresh                        │
│  • UI: Refresh / Hard Refresh button                            │
└────────────────────────────┬────────────────────────────────────┘
                             ↓
╔═════════════════════════════════════════════════════════════════╗
║           Application Controller                                ║
╠═════════════════════════════════════════════════════════════════╣
║           ┌─────────────────────────────┐                       ║
║           │ Enqueue Application         │                       ║
║           └────────────┬────────────────┘                       ║
║                        ↓                                        ║
║                     RECONCILE                                   ║
╚═════════════════════════════════════════════════════════════════╝
```

## System-Level Configuration

### -- via -- `ignoreDifferences`

* `ignoreDifferences` 
  * allows
    * | calculate sync status, ignore certain fields
  * by default, 
    * 👀`ignoreDifferences` customizations -> apply | `ignoreResourceUpdates`👀
      * Reason:🧠reduce config management -- by -- preventing you to copy duplicated🧠
      * if you want to disable it `ignoreDifferencesOnResourceUpdates: false`
  * [source code](/pkg/apis/application/v1alpha1/types.go)'s `ResourceIgnoreDifferences`

* -- based on -- scope
  * global: | "argocd-cm" ConfigMap,
    * `resource.customizations.ignoreDifferences.all`

        ```yaml
        data:
          resource.customizations.ignoreDifferences.all: |                                                                                                                                                                                
            # ways to specify the resource updates / ignore
            jsonPointers:              # [JSON Pointer]                                                                                                                                                                   
            - /path/to/field                                                                                                                                                                                                                     
            jqPathExpressions:         # [JQPathExpressions]                                                                                                                                                                      
            - .path.to.field  
            managedFieldsManagers:
            - someManagedFieldManager
        ```
    * `resource.customizations.ignoreDifferences.<group>_<kind>`
      * ⚠️override `resource.customizations.ignoreDifferences.all`⚠️

        ```yaml
        data:
          resource.customizations.ignoreDifferences.<group>_<kind>: |                                                                                                                                                                                
            # ways to specify the resource updates / ignore
            jsonPointers:              # [JSON Pointer]                                                                                                                                                                   
            - /path/to/field                                                                                                                                                                                                                     
            jqPathExpressions:         # [JQPathExpressions]                                                                                                                                                                      
            - .path.to.field  
            managedFieldsManagers:
            - someManagedFieldManager
          ```
  * Argo CD Application,

    ```yaml
    apiVersion: argoproj.io/v1alpha1
    kind: Application
    spec:
  
      ignoreDifferences:
        - group: "API_GROUP"
          kind: "API_KIND"
          jsonPointers:
            - /path/to/field
    ```

## default Configuration

* metadata fields / ALWAYS ignored | ALL resources -- via -- `ignoreResourceUpdates` & `ignoreDifferences`
  * `metadata.generation`
  * `metadata.resourceVersion`
  * `metadata.managedFields`

## how to find high-churn resources?

* high-churn resources
  * == resources / CONTINUOUSLY change
    * -> CONTINUOUSLY trigger reconcile
      * COMMON PROBLEMS: ⚠️HIGH CPU usage | "argocd-application-controller"⚠️

* steps
  * configure the application-controller's log level == `debug`
  * look for | application-controller's logs: `"Requesting app refresh caused by object update"`
    * return `api-version` & `kind` fields 
    * hit | refresh step
  * identify the 
    * high-churn resource kinds
      * == count NUMBER of `"Requesting app refresh caused by object update"` / EACH `kind`
    * fields / are changing

      ```shell
      kubectl get <resource> -o yaml > /tmp/before.yaml
        # Wait a minute or two.
      kubectl get <resource> -o yaml > /tmp/after.yaml
      diff /tmp/before.yaml /tmp/after.yaml
      ```
