# Automated Sync Policy

* ⚠️sync != trigger Argo CD detection⚠️
  * ways of sync
    * automatic sync policy
      * recommended one
    * [`argocd app sync APPNAME`](ci_automation.md)
  * [ways of trigger Argo CD detection](../faq.md#how-often-does-argo-cd-check-for-changes--git-or-helm-repository-)

* Argo CD sync policy
  * allows
    * 👀if it detects DIFFERENCES BETWEEN the desired manifests | Git vs live state | cluster -> AUTOMATICALLY sync an application👀 
      * -> CI/CD pipelines can perform the deployment
        * ❌WITHOUT direct access to the Argo CD API server❌
        * -- via -- `git commit` & `git push` | Git repository
  * ways to configure
    * `argocd app set <APPNAME> --sync-policy automated`
    * | Argo CD's Application

      ```yaml
      spec:
        syncPolicy:
          automated: {}
            # ==
            # enabled: null     == true
      ```
      * if you want to explicitly set -> specify `spec.syncPolicy.automated.enabled`
        * ALLOWED values: true OR false
        * if you set `false` -> skip `prune`, `self-heal` & `allowEmpty` configurations

## Temporarily toggling auto-sync for applications managed by ApplicationSets

TODO: 
For a standalone application, toggling auto-sync is performed by changing the application's `spec.syncPolicy.automated` field
* For an ApplicationSet managed application, changing the application's `spec.syncPolicy.automated` field will, however, have no effect.
[Controlling Resource Modification](../operator-manual/applicationset/Controlling-Resource-Modification.md) has more details about how to perform the toggling for applications managed by ApplicationSets.


## Automatic Pruning

By default (and as a safety mechanism), automated sync will not delete resources when Argo CD detects
the resource is no longer defined in Git
* To prune the resources, a manual sync can always be
performed (with pruning checked)
* Pruning can also be enabled to happen automatically as part of the
automated sync by running:

```bash
argocd app set <APPNAME> --auto-prune
```

Or by setting the prune option to true in the automated sync policy:

```yaml
spec:
  syncPolicy:
    automated:
      prune: true
```

## Automatic Pruning with Allow-Empty (v1.8)

By default (and as a safety mechanism), automated sync with prune have a protection from any automation/human errors 
when there are no target resources
* It prevents application from having empty resources
* To allow applications have empty resources, run:

```bash
argocd app set <APPNAME> --allow-empty
```

Or by setting the allow empty option to true in the automated sync policy:

```yaml
spec:
  syncPolicy:
    automated:
      prune: true
      allowEmpty: true
```

## Automatic Self-Healing
By default, changes that are made to the live cluster will not trigger automated sync
* To enable automatic sync 
when the live cluster's state deviates from the state defined in Git, run:

```bash
argocd app set <APPNAME> --self-heal
```

Or by setting the self-heal option to true in the automated sync policy:

```yaml
spec:
  syncPolicy:
    automated:
      selfHeal: true
```

> [!NOTE]
> Disabling self-heal does not guarantee that live cluster changes in multi-source applications will persist
* Although one of the resource's sources remains unchanged, changes in another can trigger `autosync`
* To handle such cases, consider disabling `autosync`.

## Automatic Retry Refresh on new revisions

This feature allows users to configure their applications to refresh on new revisions when the current sync is retrying
* To enable automatic refresh during sync retries, run:

```bash
argocd app set <APPNAME> --sync-retry-refresh
```

Or by setting the `retry.refresh` option to `true` in the sync policy:

```yaml
spec:
  syncPolicy:
    retry:
      refresh: true
```

## Automated Sync Semantics

* automated sync
  * ⚠️requirements⚠️
    * application is OutOfSync
      * if application's status != OutOfSync (_Examples:_ Synced, Error, ...) -> NO try automated sync
  * ⚠️ONLY try 1 AUTOMATIC synchronization / EACH UNIQUE combination of commit SHA1 + application parameters⚠️
    * EXCEPTION: 
      * if PREVIOUS automatic sync succeed + `selfHeal: true` + drift -- due to -- MANUAL adjustment | cluster -> retry automatic sync AFTER `--self-heal-timeout-seconds` 
    * ❌ALTHOUGH PREVIOUS automatic sync failed, NOT retry❌
  * ❌if it's enabled -> NOT possible to perform a Rollback❌
  * automatic sync interval
    * determined -- by -- [`timeout.reconciliation` value | `argocd-cm` ConfigMap](../faq.md#how-often-does-argo-cd-check-for-changes--git-or-helm-repository-)
