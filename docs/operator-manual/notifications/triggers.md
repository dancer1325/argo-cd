* trigger
  * == condition | send the notification
  * == name + condition + notification templates reference
    * condition -- `when:` -- 
      * == predicate expression / if the notification should be sent -> returns true
      * condition evaluation
        * is powered -- by -- [antonmedv/expr](https://github.com/antonmedv/expr)
      * [condition language syntax](https://github.com/antonmedv/expr/blob/master/docs/language-definition.md)
    * notification templateS reference -- `send:` --
      * `send: [template1, template2, ...]`
  * ALLOWED [conditions bundles](#conditions-bundles)
  * how to configure?
    * | "argocd-notifications-cm" ConfigMap
      * add `data.trigger.*: |`
  * audience
    * administrators
  * consumers
    * end users
  * _Example:_ [`data.trigger.*: |`](examples/argocd-notifications-cm.yaml)   

## Conditions Bundles

* == MULTIPLE (conditions + template referenceS) / EACH condition

## Accessing Optional Manifest Sections and Fields

* TODO:
Note that in the trigger example above, the `?.` (optional chaining)
operator is used to access the Application's
`status.operationState` section
* This section is optional; it is not present when an operation has been initiated but has not yet
started by the Application Controller.

If the `?.` operator were not used, `status.operationState` would resolve to `nil`
and the evaluation of the
`app.status.operationState.phase` expression would fail
*  The `app.status?.operationState.phase` expression is equivalent to
`app.status.operationState != nil ?  app.status.operationState.phase : nil`.

## Avoid Sending Same Notification Too Often

* use cases
  * trigger's conditionS (`when`) change
    * quickly
    * intermittently

* `oncePer` field
  * OPTIONAL
  * configures triggers -- to -- avoid generating MULTIPLE notificationS

* | [mono repos](../applicationset/Use-Cases.md#use-case-monorepos)
TODO:
When one repo is used to sync multiple applications, the `oncePer: app.status.sync.revision` field 
will trigger a notification for each commit
* For mono repos, the better approach will be using `oncePer: app.status?.operationState.syncResult.revision`
statement
* This way a notification will be sent only for a particular Application's revision.

## Default Triggers

* how to configure?
  * | "argocd-notifications-cm" ConfigMap
    * add `data.defaultTriggers.(<custom-name>): |`
  * Argo CD application OR ArgoCD project,
    * TODO: add the structure `notifications.argoproj.io/subscribe.on-sync-succeeded.slack` annotation


* TODO: In this example, `slack` sends when `on-sync-status-unknown`, and `mattermost` sends when `on-sync-running` and `on-sync-succeeded`.

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  annotations:
    notifications.argoproj.io/subscribe.slack: my-channel
    notifications.argoproj.io/subscribe.mattermost: my-mattermost-channel
```

## Functions

Triggers have access to the set of built-in functions.

Example:

```yaml
when: time.Now().Sub(time.Parse(app.status?.operationState.startedAt)).Minutes() >= 5
```

* [MORE](functions.md)
