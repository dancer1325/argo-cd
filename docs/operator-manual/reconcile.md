# Reconcile Optimization

* reconcile
  * == action / 
    * desired state == cluster state

* Argo CD Application
  * if a resource changes -> it's refreshed
    * COMMON PROBLEMS: ⚠️HIGH CPU usage | "argocd-application-controller"⚠️
      * Reason: 🧠Kubernetes controllers OFTEN update the resources / they watch periodically -> CONTINUOUSLY reconcile🧠
      * SOLUTION: 👀ignore resource updates | specific fields👀
        * -- for -- [tracked resources](../user-guide/resource_tracking.md)
        * -- for -- [untracked resources](#ignoring-updates-for-untracked-resources)

TODO: 
When a resource update is ignored, if the resource's [health status](./health.md) does not change, 
the Application that this resource belongs to will not be reconciled.

## System-Level Configuration

* `resource.ignoreResourceUpdatesEnabled`
  * enable OR disable
    * Argo CD can ignore resource updates
  * by default, `true`
    * -> reduce unnecessary reconcile operations
  * ways to configure
    * GENERAL
      * | "argocd-cm" ConfigMap,
        * set `resource.ignoreResourceUpdatesEnabled`
    * | ALL tracked resources
      * | "argocd-cm" ConfigMap,
        * set `resource.ignoreResourceUpdatesEnabled.all`

TODO: 

Argo CD allows ignoring resource updates at a specific JSON path, 
using [RFC6902 JSON patches](https://tools.ietf.org/html/rfc6902) and
[JQ path expressions](https://stedolan.github.io/jq/manual/#path(path_expression))
* It can be configured for a specified group and kind
in `resource.customizations` key of the `argocd-cm` ConfigMap.

Following is an example of a customization which ignores the `refreshTime` status field
of an [`ExternalSecret`](https://external-secrets.io/main/api/externalsecret/) resource:

```yaml
data:
  resource.customizations.ignoreResourceUpdates.external-secrets.io_ExternalSecret:
    |
    jsonPointers:
    - /status/refreshTime
    # JQ equivalent of the above:
    # jqPathExpressions:
    # - .status.refreshTime
```

### Using ignoreDifferences to ignore reconcile

By default, the existing system-level `ignoreDifferences` customizations will be added to ignore resource updates as well
* This helps reduce config management by preventing you to copy all existing ignore differences configurations.

To disable this behavior, the `ignoreDifferencesOnResourceUpdates` setting can be disabled:

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: argocd-cm
data:
  resource.compareoptions: |
    ignoreDifferencesOnResourceUpdates: false
```

## Default Configuration

* metadata fields / ALWAYS ignored | ALL resources
  * `metadata.generation`
  * `metadata.resourceVersion`
  * `metadata.managedFields`

## Finding Resources to Ignore

TODO: 
The application controller logs when a resource change triggers a refresh
* You can use these logs to find
high-churn resource kinds and then inspect those resources to find which fields to ignore.

To find these logs, search for `"Requesting app refresh caused by object update"`
* The logs include structured
fields for `api-version` and `kind`
* Counting the number of refreshes triggered, by api-version/kind should
reveal the high-churn resource kinds.

> [!NOTE]
> These logs are at the `debug` level
* Configure the application-controller's log level to `debug`.

Once you have identified some resources which change often, you can try to determine which fields are changing
* Here is
one approach:

```shell
kubectl get <resource> -o yaml > /tmp/before.yaml
# Wait a minute or two.
kubectl get <resource> -o yaml > /tmp/after.yaml
diff /tmp/before.yaml /tmp/after.yaml
```

The diff can give you a sense for which fields are changing and should perhaps be ignored.

## Checking Whether Resource Updates are Ignored

Whenever Argo CD skips a refresh due to an ignored resource update, the controller logs the following line:
"Ignoring change of object because none of the watched resource fields have changed".

Search the application-controller logs for this line to confirm that your resource ignore rules are being applied.

> [!NOTE]
> These logs are at the `debug` level
* Configure the application-controller's log level to `debug`.

## Ignoring updates for untracked resources

use the argocd.argoproj.io/ignore-resource-updates annotations

ArgoCD will only apply `ignoreResourceUpdates` configuration to tracked resources of an application
* This means dependent resources, such as a `ReplicaSet` and `Pod` created by a `Deployment`, will not ignore any updates and trigger a reconcile of the application for any changes.

If you want to apply the `ignoreResourceUpdates` configuration to an untracked resource, you can add the
`argocd.argoproj.io/ignore-resource-updates=true` annotation in the dependent resources manifest.
