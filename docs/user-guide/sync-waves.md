# Sync Phases & Sync Waves

* Sync 
  * == 💡process AFTER [reconciliation](../operator-manual/reconcile.md)💡
  * [sync phases](#sync-phases)
  * [sync hook](#sync-hook)
  * [how to clean up sync hook?](#cleanup-sync-hooks)

```
┌──────────────────────────────────────────────────────────────┐
│            COMPLETE SYNC HOOK LIFECYCLE                      │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  1. SYNC PHASE (argocd.argoproj.io/hook)                     │
│     ↓                                                        │
│     Determines: WHEN the hook is CREATED & EXECUTED          │
│     Values: PreSync, Sync, Skip, PostSync, SyncFail,         │
│             PreDelete, PostDelete                            │
│                                                              │
│  2. EXECUTION                                                │
│     ↓                                                        │
│     The hook runs (Job executes, Pod runs, etc.)             │
│                                                              │
│  3. CLEANUP (argocd.argoproj.io/hook-delete-policy)          │
│     ↓                                                        │
│     Determines: WHEN the hook is DELETED                     │
│     Values: HookSucceeded, HookFailed, BeforeHookCreation    │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

## sync phases

* sync phases
  * == 💡sync process' steps💡/
    * executed ⚠️sequentially⚠️
      * == WAIT BEFORE switching to NEXT one
  * == WHEN creating & executing the sync hook

| Argo CD's built-in sync phases | Description                                                                                                                                                                                                                                                                                                                             |
|--------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `PreSync`                      | executes PREVIOUS -- to -- sync OutOfSync Kubernetes objects <br/> if it fails -> WHOLE sync process <br/> &nbsp;&nbsp; stop <br/> &nbsp;&nbsp; marked -- as -- failed <br/> use cases: validations                                                                                                                                     |
| `Sync`                         | executes <br/> &nbsp;&nbsp; AFTER ALL `PreSync` hooks were completed & successful <br/> &nbsp;&nbsp; SAME time -- as -- sync OutOfSync Kubernetes objects                                                                                                                                                                               |
| `Skip`                         | == skip synchronizing OutOfSync Kubernetes object                                                                                                                                                                                                                                                                                       |
| `PostSync`                     | executes AFTER ALL `Sync` hooks completed & successful + successful application + ALL resources' state == `Healthy` <br/> if it fails -> WHOLE sync process <br/> &nbsp;&nbsp; stop <br/> &nbsp;&nbsp; marked -- as -- failed  <br/> use case: smoke tests                                                                              |
| `SyncFail`                     | executes \| (ONLY) sync operation fails  <br/> uses: <br/> &nbsp;&nbsp; cleanup actions <br/> &nbsp;&nbsp; &nbsp;&nbsp; _Example:_ revert partial changes, backups <br/> &nbsp;&nbsp; other housekeeping tasks <br/> &nbsp;&nbsp; &nbsp;&nbsp; _Example:_ send notifications  <br/> if it fails -> Argo CD does NOT do anything special |
| `PreDelete`                    | executes BEFORE deleting ALL Application resources <br/> &nbsp;&nbsp;  _Example:_ `kubectl delete application` OR `argocd app delete` <br/> != \| normal sync operations (EVEN pruning enabled ) <br/> [MORE](#predelete)                                                                                                               |
| `PostDelete`                   | executes AFTER deleting ALL Application resources <br/> requirements: v2.10+  <br/> use cases: cleanup, notifications, remove external resources  <br/> [MORE](#postdelete)                                                                                                                                                             |

![sync phases](how_phases_work.png)

### `PreDelete`

* if SOME hook | `PreDelete` phase fails -> 
  * ❌Application resources NOT start being deleted❌
  * Application's state == deleting / `DeletionError` condition
  * ways to fix the failing hook
    * user fix -- , by updating the manifest | Git repository, -- the failing hook
    * user MANUALLY delete the failing hook
  * ONCE user fix the failing hook -> Argo CD AUTOMATICALLY retry the deletion | NEXT reconciliation

### `PostDelete`

* if SOME hook | `PostDelete` phase fails ->
  * ⚠️Application resources ALREADY deleted⚠️
  * Application's state == deleting / `DeletionError` condition
  * ways to fix the failing hook
    * user fix -- , by updating the manifest | Git repository, -- the failing hook
    * user MANUALLY delete the failing hook
  * ONCE user fix the failing hook -> Argo CD AUTOMATICALLY retry | NEXT reconciliation

## sync hook

* sync hooks
  * == 💡Kubernetes resource💡 /
    * contain `metadata.annotations.argocd.argoproj.io/hook`
  * == WHICH
  * _ExampleS:_ Pod, Job or Argo Workflows

* sync phases & sync hooks
  * == 👀ManyToMany relation👀
    * == MANY sync phases can be related -- to -- MANY sync hooks

## cleanup sync hooks

* cleanup 
  * -- based on -- policies
  * | sync hook,
    * `metadata.annotations.argocd.argoproj.io/hook-delete-policy: SOME_ALLOWED_POLICY`

| ALLOWED policies     | Description                                                                                                                                                                                                                                                   |
|----------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `HookSucceeded`      | AFTER succeeding the hook (_Example:_ Job/Workflow completed successfully) -> delete the hook resource                                                                                                                                                        |
| `HookFailed`         | AFTER failing the hook -> delete the hook resource                                                                                                                                                                                                            |
| `BeforeHookCreation` | requirements: ⚠️v1.3⚠️ <br/> BEFORE creating the NEW one, the EXISTING hook resource is deleted <br/> &nbsp;&nbsp; identify the EXISTING one -- based on -- `/metadata/name` <br/> default one <br/> &nbsp;&nbsp; == if NONE is specified -> this one is used |

## How sync waves work?

* Argo CD 
  * sync order execution
    * 👀defined -- by -- `argocd.argoproj.io/sync-wave` annotation👀
      * Hooks & resources,
        * 👀by default, 0👀
  * sync operation
    1. order ALL resources -- based on -- their wave
       * lowest -- to -- highest
    2. Apply the resources -- based on -- sync order execution 

* `argocd.argoproj.io/sync-wave`
  * == integer /
    * start deploying FROM the lowest -- to -- the highest number
    * ⚠️ALLOWED ALSO <0⚠️

* TODO: 
There is currently a delay between each sync wave in order to give other controllers a chance to react to the spec change that was just applied
* This also prevents Argo CD from assessing resource health too quickly (against the stale object), causing hooks to fire prematurely
* The current delay between each sync wave is 2 seconds and can be configured via the environment variable ARGOCD_SYNC_WAVE_DELAY.

## Combining Sync waves and hooks

While you can use sync waves on their own, for maximum flexibility you can combine them with hooks
* This way you can use sync phases for coarse grained ordering and sync waves for defining the exact order of a resource within an individual phase.

![waves](how_waves_work.png)

When Argo CD starts a sync, it orders the resources in the following precedence:

1. The phase
2. The wave they are in (lower values first)
3. By kind (e.g. namespaces first and then other Kubernetes resources, followed by custom resources)
4. By name

Once the order is defined:

1. First Argo CD determines the number of the first wave to apply
   * This is the first number where any resource is out-of-sync or unhealthy.
2. It applies resources in that wave.
3. It repeats this process until all phases and waves are in-sync and healthy.

Because an application can have resources that are unhealthy in the first wave, it may be that the app can never get to healthy.

## How Do I Configure Phases?

Pre-sync and post-sync can only contain hooks
* Apply the hook annotation:

```yaml
metadata:
  annotations:
    argocd.argoproj.io/hook: PreSync
```

[Read more about hooks](resource_hooks.md).

## How Do I Configure Waves?

Specify the wave using the following annotation:

```yaml
metadata:
  annotations:
    argocd.argoproj.io/sync-wave: "5"
```

Hooks and resources are assigned to wave zero by default
* The wave can be negative, so you can create a wave that runs before all other resources.

## Examples

### Work around ArgoCD sync failure
TODO: 

* use case
  * | upgrade ingress-nginx controller (/ managed by helm) -- via -- ArgoCD 2.x,
    * SOMETIMES fails

| .         | .                                                                       |
|-----------|-------------------------------------------------------------------------|
| OPERATION | Sync                                                                    |
| PHASE     | Running                                                                 |
| MESSAGE   | waiting for completion of hook batch/Job/ingress-nginx-admission-create |

| .         | .                              |
|-----------|--------------------------------|
| KIND      | batch/v1/Job                   |
| NAMESPACE | ingress-nginx                  |
| NAME      | ingress-nginx-admission-create |
| STATUS    | Running                        |
| HOOK      | PreSync                        |
| MESSAGE   | Pending deletion               |

* SOLUTION:
  * TODO: helm user can add:

```yaml
ingress-nginx:
  controller:
    admissionWebhooks:
      annotations:
        argocd.argoproj.io/hook: Skip
```

Which results in a successful sync.
