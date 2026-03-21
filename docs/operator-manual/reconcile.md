# Reconcile Optimization

* reconcile
  * == process / 
    * desired state == cluster state
    * 💡when it's triggered💡
      * if resource changes & 
        * NOT ignored -> ALWAYS reconcile 
        * ignored & resource's [health status](./health.md) changes -> reconcile

```
┌─────────────────────────────────────────────────────────────────┐
│                    Kubernetes Cluster                            │
│                                                                  │
│  Resource changes (Pod restart, HPA scaling, etc.)              │
└────────────────────────────┬─────────────────────────────────────┘
                             ↓
╔═════════════════════════════════════════════════════════════════╗
║              Application Controller (watches & processes)       ║
╠═════════════════════════════════════════════════════════════════╣
║                    ┌────────────────────┐                       ║
║                    │  1. Watch Resources │                      ║
║                    │  (Kubernetes API)   │                      ║
║                    └────────┬────────────┘                      ║
║                             ↓                                   ║
║                    ┌────────────────────┐                       ║
║                    │  2. Detect Change  │                       ║
║                    │  (Watch event)      │                      ║
║                    └────────┬────────────┘                      ║
║                             ↓                                   ║
║              ┌──────────────────────────────┐                   ║
║              │  3. ignoreResourceUpdates?   │                   ║
║              │  • System-level config       │                   ║
║              │  • Resource annotation       │                   ║
║              └──────┬───────────────┬───────┘                   ║
║                     │               │                            ║
║                 YES │               │ NO                         ║
║                     ↓               ↓                            ║
║              ┌──────────┐   ┌─────────────────────────┐          ║
║              │   STOP   │   │ 4. Enqueue Application  │           ║
║              │          |   │    (== added to queue)  │          ║
║              └──────────┘   └────────┬────────────────┘          ║
║                                      ↓                           ║
║                             ⏱️  Wait until:                       ║
║                             • timeout.reconciliation (default 3m)║
║                             • Manual refresh                     ║
║                             • Webhook event                      ║
║                                      ↓                           ║
║                 ╔═══════════════════════════════╗                ║
║                 ║  RECONCILE PROCESS (5-7)      ║                ║
║                 ╚═══════════════════════════════╝                ║
║                                      ↓                           ║
║                    ┌──────────────────────────────┐              ║
║                    │  5. Refresh                  │              ║
║                    │  ┌────────────────────────┐  │              ║
║                    │  │ • Get desired state:   │  │              ║
║                    │  │   - From cache OR      │  │              ║
║                    │  │   - Fetch from Git     │  │              ║
║                    │  │   (via Repo Server)    │  │              ║
║                    │  │                        │  │              ║
║                    │  │ • Get live state       │  │              ║
║                    │  │   (via Kube API)       │  │              ║
║                    │  │                        │  │              ║
║                    │  │ • Compare both with    │  │              ║
║                    │  │   ignoreDifferences:   │  │              ║
║                    │  │   - System-level       │  │              ║
║                    │  │   - Per-app config     │  │              ║
║                    │  └────────────────────────┘  │              ║
║                    └──────────┬───────────────────┘              ║
║                               ↓                                  ║
║                    ┌──────────────────────────────┐              ║
║                    │  6. Update Sync Status       │              ║
║                    │  (based on comparison)       │              ║
║                    └──────┬─────────┬─────────────┘              ║
║                           │         │                            ║
║                    Synced │         │ OutOfSync                  ║
║                           ↓         ↓                            ║
║                      ┌────────┐  ┌──────────────────────┐        ║
║                      │  END   │  │ 7. Auto-Sync         │        ║
║                      └────────┘  │    (if enabled)      │        ║
║                                  └──────────────────────┘        ║
║                                            ↓                     ║
║                                          END                     ║
╚═════════════════════════════════════════════════════════════════╝
```

* Argo CD Application
  * if a resource (tracked OR untracked) changes -> it's refreshed
    * COMMON PROBLEMS: ⚠️HIGH CPU usage | "argocd-application-controller"⚠️
      * Reason: 🧠Kubernetes controllers OFTEN update the resources / they watch periodically -> CONTINUOUSLY reconcile🧠
      * SOLUTION: 👀ignore resource updates | specific fields👀
        * -- for -- [tracked resources](../user-guide/resource_tracking.md)
        * -- for -- [untracked resources](#ignoring-updates-for-untracked-resources)

## System-Level Configuration

* | "argocd-cm" ConfigMap,
  * `resource.ignoreResourceUpdatesEnabled`
    * enable OR disable
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

### Using ignoreDifferences to ignore reconcile

* `ignoreDifferences` 
  * allows
    * | calculate sync status, ignore certain fields
  * by default, 
    * 👀`ignoreDifferences` customizations -> apply | `ignoreResourceUpdates`👀
      * Reason:🧠reduce config management -- by -- preventing you to copy duplicated🧠
      * if you want to disable it `ignoreDifferencesOnResourceUpdates: false`

* | "argocd-cm" ConfigMap,
  * `resource.customizations.ignoreDifferences.all`

      ```yaml
      data:
        resource.customizations.ignoreDifferences.all: |                                                                                                                                                                                
          # ways to specify the resource updates / ignore
          jsonPointers:              # [JSON Pointer]                                                                                                                                                                   
          - /path/to/field                                                                                                                                                                                                                     
          jqPathExpressions:         # [JQPathExpressions]                                                                                                                                                                      
          - .path.to.field  
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
      ```

## Default Configuration

* metadata fields / ALWAYS ignored | ALL resources
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

## how to check that resource updates are ignored?

* steps
  * configure the application-controller's log level == `debug`
  * look for | application-controller's logs: `"Ignoring change of object because none of the watched resource fields have changed"`

## Ignoring updates for untracked resources

* untracked resources
  * == resources / NOT exist | Git & exist | cluster
    * _Example:_ `Deployment` | Git, 
      * creates DEPENDENT `ReplicaSet` & `Pod` | Cluster
      * DEPENDENT `ReplicaSet` & `Pod` do NOT exist | Git
  * Argo CD 
    * ❌do NOT reconcile them ❌
      * Reason:🧠it does NOT exist | Git🧠
    * 💡monitors them💡
      * _Example:_ if DEPENDENT `ReplicaSet` & `Pod` | Cluster change -> trigger a reconcile of whole Application
      * COMMON PROBLEMS: ⚠️HIGH CPU usage | "argocd-application-controller"⚠️
  * ⭐️ways to ignore untracked resources updates⭐️
    * | untracked resources,
      * you must add `argocd.argoproj.io/ignore-resource-updates=true`

* `argocd.argoproj.io/ignore-resource-updates` annotations
  * ArgoCD 
    * ⚠️ONLY apply | application's tracked resources ⚠️
    * ❌does NOT apply them | tracked' DEPENDENT resources❌
      * _Example:_ `Deployment` | GIT -> `Deployment`'s DEPENDENT `ReplicaSet` & `Pod` are NOT ignored
