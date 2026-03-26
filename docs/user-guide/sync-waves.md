# Sync Phases & Sync Waves

* Sync 
  * == 💡process AFTER [reconciliation](../operator-manual/reconcile.md)💡
  * [sync phases](#sync-phases)
  * [sync hook](#sync-hook)
  * [how to clean up sync hook?](#cleanup-sync-hooks)
  * [sync waves](#sync-waves)
  * 💡sync order execution is -- based on --💡
    1. sync phase
    2. sync wave
    3. kind
       * order: namespaces, other Kubernetes resources, Kubernetes CR
    4. name

```
┌────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                            SYNC PROCESS: PHASES & WAVES                                                                    │
│                                  (Left to Right: Sequential Phases  |  Top to Bottom: Waves within each phase)                            │
└────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘

TIME →

┌──────────────────┬──────────────────┬──────────────────┬──────────────────┬──────────────────┬──────────────────┐
│    PRESYNC       │      SYNC        │    POSTSYNC      │    SYNCFAIL      │   PREDELETE      │   POSTDELETE     │
│   (hooks only)   │ (hooks+resources)│   (hooks only)   │   (hooks only)   │   (hooks only)   │   (hooks only)   │
├──────────────────┼──────────────────┼──────────────────┼──────────────────┼──────────────────┼──────────────────┤
│                  │                  │                  │                  │                  │                  │
│ Wave -2          │ Wave -5          │ Wave -1          │ Wave 0           │ Wave -1          │ Wave 0           │
│ ┌──────────────┐ │ ┌──────────────┐ │ ┌──────────────┐ │ ┌──────────────┐ │ ┌──────────────┐ │ ┌──────────────┐ │
│ │  🔧 Hook A   │ │ │  📦 Namespace│ │ │  🔧 Hook P   │ │ │  🔧 Hook X   │ │ │  🔧 Hook M   │ │ │  🔧 Hook Z   │ │
│ │  [execute]   │ │ │  [apply]     │ │ │  [execute]   │ │ │  [execute]   │ │ │  [execute]   │ │ │  [execute]   │ │
│ │  [cleanup]   │ │ │  [keep]      │ │ │  [cleanup]   │ │ │  [cleanup]   │ │ │  [cleanup]   │ │ │  [cleanup]   │ │
│ └──────────────┘ │ └──────────────┘ │ └──────────────┘ │ └──────────────┘ │ └──────────────┘ │ └──────────────┘ │
│        ↓         │        ↓         │        ↓         │        ↓         │        ↓         │        ↓         │
│     ⏱️ 2s        │     ⏱️ 2s        │     ⏱️ 2s        │     ⏱️ 2s        │     ⏱️ 2s        │     ⏱️ 2s        │
│        ↓         │        ↓         │        ↓         │        ↓         │        ↓         │        ↓         │
│                  │                  │                  │                  │                  │                  │
│ Wave 0           │ Wave -1          │ Wave 0           │ Wave 1           │ Wave 0           │ Wave 5           │
│ ┌──────────────┐ │ ┌──────────────┐ │ ┌──────────────┐ │ ┌──────────────┐ │ ┌──────────────┐ │ ┌──────────────┐ │
│ │  🔧 Hook B   │ │ │  📦 ConfigMap│ │ │  🔧 Hook Q   │ │ │  🔧 Hook Y   │ │ │  🔧 Hook N   │ │ │  🔧 Hook W   │ │
│ │  [execute]   │ │ │  [apply]     │ │ │  [execute]   │ │ │  [execute]   │ │ │  [execute]   │ │ │  [execute]   │ │
│ │  [cleanup]   │ │ │  [keep]      │ │ │  [cleanup]   │ │ │  [cleanup]   │ │ │  [cleanup]   │ │ │  [cleanup]   │ │
│ └──────────────┘ │ └──────────────┘ │ └──────────────┘ │ └──────────────┘ │ └──────────────┘ │ └──────────────┘ │
│   (default)      │ ┌──────────────┐ │   (default)      │                  │   (default)      │                  │
│                  │ │  📦 Secret   │ │                  │                  │                  │                  │
│                  │ │  [apply]     │ │                  │                  │                  │                  │
│                  │ │  [keep]      │ │                  │                  │                  │                  │
│                  │ └──────────────┘ │                  │                  │                  │                  │
│        ↓         │        ↓         │        ↓         │        ↓         │        ↓         │        ↓         │
│     ⏱️ 2s        │     ⏱️ 2s        │     ⏱️ 2s        │     ⏱️ 2s        │     ⏱️ 2s        │                  │
│        ↓         │        ↓         │        ↓         │        ↓         │        ↓         │                  │
│                  │                  │                  │                  │                  │                  │
│ Wave 3           │ Wave 0           │ Wave 10          │                  │                  │                  │
│ ┌──────────────┐ │ ┌──────────────┐ │ ┌──────────────┐ │                  │                  │                  │
│ │  🔧 Hook C   │ │ │  🔧 Hook E   │ │ │  🔧 Hook R   │ │                  │                  │                  │
│ │  [execute]   │ │ │  [execute]   │ │ │  [execute]   │ │                  │                  │                  │
│ │  [cleanup]   │ │ │  [cleanup]   │ │ │  [cleanup]   │ │                  │                  │                  │
│ └──────────────┘ │ └──────────────┘ │ └──────────────┘ │                  │                  │                  │
│        ↓         │ ┌──────────────┐ │        ↓         │                  │                  │                  │
│     ⏱️ 2s        │ │  📦 Rsrc D   │ │                  │                  │                  │                  │
│        ↓         │ │  [apply]     │ │                  │                  │                  │                  │
│                  │ │  [keep]      │ │                  │                  │                  │                  │
│                  │ └──────────────┘ │                  │                  │                  │                  │
│                  │        ↓         │                  │                  │                  │                  │
│                  │     ⏱️ 2s        │                  │                  │                  │                  │
│                  │        ↓         │                  │                  │                  │                  │
│                  │                  │                  │                  │                  │                  │
│                  │ Wave 1           │                  │                  │                  │                  │
│                  │ ┌──────────────┐ │                  │                  │                  │                  │
│                  │ │  📦 Deploy   │ │                  │                  │                  │                  │
│                  │ │  [apply]     │ │                  │                  │                  │                  │
│                  │ │  [wait       │ │                  │                  │                  │                  │
│                  │ │   healthy]   │ │                  │                  │                  │                  │
│                  │ └──────────────┘ │                  │                  │                  │                  │
│                  │        ↓         │                  │                  │                  │                  │
│                  │     ⏱️ 2s        │                  │                  │                  │                  │
│                  │        ↓         │                  │                  │                  │                  │
│                  │                  │                  │                  │                  │                  │
│                  │ Wave 2           │                  │                  │                  │                  │
│                  │ ┌──────────────┐ │                  │                  │                  │                  │
│                  │ │  📦 Service  │ │                  │                  │                  │                  │
│                  │ │  [apply]     │ │                  │                  │                  │                  │
│                  │ │  [keep]      │ │                  │                  │                  │                  │
│                  │ └──────────────┘ │                  │                  │                  │                  │
│                  │        ↓         │                  │                  │                  │                  │
│                  │     ⏱️ 2s        │                  │                  │                  │                  │
│                  │        ↓         │                  │                  │                  │                  │
│                  │                  │                  │                  │                  │                  │
│                  │ Wave 10          │                  │                  │                  │                  │
│                  │ ┌──────────────┐ │                  │                  │                  │                  │
│                  │ │  📦 Ingress  │ │                  │                  │                  │                  │
│                  │ │  [apply]     │ │                  │                  │                  │                  │
│                  │ │  [keep]      │ │                  │                  │                  │                  │
│                  │ └──────────────┘ │                  │                  │                  │                  │
│                  │                  │                  │                  │                  │                  │
└──────────────────┴──────────────────┴──────────────────┴──────────────────┴──────────────────┴──────────────────┘
        ↓                  ↓                  ↓             (only if            (only on          (only on
   Phase ends        Phase ends        Phase ends        sync fails)         app delete)       app delete)
        ↓                  ↓                  ↓                  ↓                  ↓                  ↓
        └──────────────────┴──────────────────┴──────────────────┴──────────────────┴──────────────────┘
                                                    ↓
                                        SYNC OPERATION COMPLETE

════════════════════════════════════════════════════════════════════════════════════════════════════════════════════

                                         ┌────────────────────────────────────────┐
                                         │  SKIP (excluded from temporal flow)    │
                                         ├────────────────────────────────────────┤
                                         │  Resources marked with:                │
                                         │  argocd.argoproj.io/hook: Skip         │
                                         │                                        │
                                         │  Are NOT executed in any phase         │
                                         │  Remain in Git but not applied         │
                                         │  Can be hooks or normal resources      │
                                         └────────────────────────────────────────┘

════════════════════════════════════════════════════════════════════════════════════════════════════════════════════

LEGEND:
───────
🔧 = Sync Hook (ephemeral)
   [execute] = Dry-run valiation + Hook executes (Job/Pod runs)
   [cleanup] = -- based on -- hook-delete-policy

📦 = Normal Resource (permanent)
   [apply] = Dry-run valiation + Apply | cluster
   [keep]  = Remains in cluster (no cleanup)
   [wait healthy] = Wait for healthy before next wave

⏱️ = Delay between waves (ARGOCD_SYNC_WAVE_DELAY, default: 2 seconds)

KEY POINTS:
───────────
• LEFT TO RIGHT: Phases execute sequentially
• TOP TO BOTTOM: Waves execute sequentially | EACH phase
• Wave numbers are INDEPENDENT / phase
• Skip is NOT part of the temporal execution flow
• SyncFail only executes if sync operation fails
• PreDelete/PostDelete only execute during application deletion
```

## sync phases

* sync phases
  * == 💡sync process' steps💡/
    * executed ⚠️sequentially⚠️
      * == WAIT BEFORE switching to NEXT one
  * == WHEN creating & executing the sync hook

| Argo CD's built-in sync phases | Description                                                                                                                                                                                                                                                                                                                                                                                                |
|--------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `PreSync`                      | executes PREVIOUS -- to -- sync OutOfSync Kubernetes objects <br/> &nbsp;&nbsp; ⚠️ONLY execute sync hooks ⚠️ <br/> if it fails -> WHOLE sync process <br/> &nbsp;&nbsp; stop <br/> &nbsp;&nbsp; marked -- as -- failed <br/> use cases: validations                                                                                                                                                        |
| `Sync`                         | executes <br/> &nbsp;&nbsp; ⚠️sync hooks + normal Kubernetes resources ⚠️ <br/> &nbsp;&nbsp; AFTER ALL `PreSync` hooks were completed & successful <br/> &nbsp;&nbsp; SAME time -- as -- sync OutOfSync Kubernetes objects                                                                                                                                                                                 |
| `Skip`                         | == skip synchronizing OutOfSync Kubernetes object <br/> &nbsp;&nbsp; ⚠️ALLOWED \| sync hooks & normal Kubernetes resources ⚠️                                                                                                                                                                                                                                                                              |
| `PostSync`                     | executes AFTER ALL `Sync` hooks completed & successful + successful application + ALL resources' state == `Healthy` <br/> &nbsp;&nbsp; ⚠️ONLY execute sync hooks ⚠️ <br/> if it fails -> WHOLE sync process <br/> &nbsp;&nbsp; stop <br/> &nbsp;&nbsp; marked -- as -- failed  <br/> use case: smoke tests                                                                                                 |
| `SyncFail`                     | executes <br/> &nbsp;&nbsp;  \| (ONLY) sync operation fails <br/> &nbsp;&nbsp; ⚠️ONLY execute sync hooks ⚠️ <br/> uses: <br/> &nbsp;&nbsp; cleanup actions <br/> &nbsp;&nbsp; &nbsp;&nbsp; _Example:_ revert partial changes, backups <br/> &nbsp;&nbsp; other housekeeping tasks <br/> &nbsp;&nbsp; &nbsp;&nbsp; _Example:_ send notifications  <br/> if it fails -> Argo CD does NOT do anything special |
| `PreDelete`                    | executes BEFORE deleting ALL Application resources <br/> &nbsp;&nbsp; ⚠️ONLY execute sync hooks ⚠️ <br/> &nbsp;&nbsp;  _Example:_ `kubectl delete application` OR `argocd app delete` <br/> != \| normal sync operations (EVEN pruning enabled ) <br/> [MORE](#predelete)                                                                                                                                  |
| `PostDelete`                   | executes AFTER deleting ALL Application resources <br/> &nbsp;&nbsp; ⚠️ONLY execute sync hooks ⚠️  <br/> requirements: v2.10+  <br/> use cases: cleanup, notifications, remove external resources  <br/> [MORE](#postdelete)                                                                                                                                                                               |

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
  * == 💡Kubernetes resource /
    * contain `metadata.annotations.argocd.argoproj.io/hook`💡
  * == WHICH
  * _ExampleS:_ Pod, Job or Argo Workflows
  * [MORE](resource_hooks.md)

* sync phases & sync hooks
  * == 👀ManyToMany relation👀
    * == MANY sync phases can be related -- to -- MANY sync hooks
    * 💡execution order of sync hooks -- depend on -- sync wave💡

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

## sync waves

* sync waves
  * == 💡Integer (ALSO <0)💡 / 
    * by default, 
      * 0
    * 👀specify the execution order of sync hooks (TODO: OR ALL?) | EACH sync phase👀
      * Reason:🧠sync phases & sync hooks == ManyToMany relation🧠
      * execute OR deploy FIRST sync hooks / LOWEST -- to -- HIGHEST
      * BETWEEN EACH execution,
        * there is a delay
          * Reason: 🧠other controllers can react -- to the -- spec change / applied | PREVIOUS wave🧠
          * by default,
            * 2"
          * if you want to configure -> set `ARGOCD_SYNC_WAVE_DELAY` environment variable
  * ⚠️ONCE ALL Kubernetes resources | waveX are sync & healthy -> execute waveX+1⚠️
    * ❌TILL ALL Kubernetes resources | waveX are NOT sync & healthy -> NOT execute waveX+1❌
      * -> retry | NEXT reconciliation
  * how to configure?
    * | sync hook,

      ```yaml
      metadata:
        annotations:
          argocd.argoproj.io/sync-wave: "SOMEINTEGER"
      ```

* sync phases vs sync waves
  * sync phases
    * enable
      * configure macro-ordering
  * sync waves
    * enable
      * configure micro-ordering

![waves](how_waves_work.png)
