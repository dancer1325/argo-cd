# Controlling if/when the ApplicationSet controller modifies `Application` resources

* goal
  * avoid unexpected post-upgrade behaviors

* ApplicationSet controller 
  * supports 
    * 👀settings 👀/ 
      * limit the ability of the controller -- to -- make changes | generated Applications
        * _Example:_ prevent the controller can delete child Applications
      * specify when & how, changes are made | your Applications & 's corresponding cluster resources

## ApplicationSet / `dry-run` mode

* == "read only" mode
  * prevent 
    * ApplicationSet can create/modify/delete Applications
      * == NO resource is modified
  * allows
    * controller Reconcile loop will run

* [ways to enable | ApplicationSet Deployment's container launch parameters](#how-to-modify-applicationset-container-launch-parameters)

## policies / manage the ALLOWED operations / ApplicationSet apply | 's managed Applications

* ways to configure
  * | ApplicationSet controller's parameter `--policy`
    * == specified | controller Deployment container
    * ⚠️'s priority > / EACH ApplicationSet's priority⚠️
      * if you want that / EACH ApplicationSet's priority takes priority -> ways
        * | ApplicationSet controller's parameter, `--enable-policy-override: true`
        * | ApplicationSet Deployment, set the the environment variable `ARGOCD_APPLICATIONSET_CONTROLLER_ENABLE_POLICY_OVERRIDE: true`
        * | "argocd-cmd-params-cm" ConfigMap, set `applicationsetcontroller.enable.policy.override: true`
  * / EACH ApplicationSet 
    * `spec.syncPolicy.applicationsSync`

* restricts the types of modifications / made -- to -- managed Argo CD `Application` resources

* ALLOWED values: 
  * `sync`
    * default one
    * == ApplicationSet controller can create/update/delete Applications
  * [`create-only`](#create-only)
  * `create-delete`
    * == ❌ApplicationSet controller can NOT update Applications❌
  * [`create-update`](#create-update)

### `create-only`

* == ApplicationSet controller can NOT
  * modify Applications
  * delete Applications
    * NOT prevent: if you delete ApplicationSet  -> delete -- [due to cascade deletion](Application-Deletion.md) -- Application

### `create-update`

* == ❌ApplicationSet controller can NOT delete Applications❌
  * NOT prevent: if you delete ApplicationSet -> delete -- [due to cascade deletion](Application-Deletion.md) -- Application

### How to prevent Application controller can delete Applications when deleting ApplicationSet

TODO: 
By default, `create-only` and `create-update` policy isn't effective against preventing deletion of Applications 
when deleting ApplicationSet.
You must set the finalizer to ApplicationSet to prevent deletion in such case, and use background cascading deletion.
If you use foreground cascading deletion, there's no guarantee to preserve applications.

```yaml
apiVersion: argoproj.io/v1alpha1
kind: ApplicationSet
metadata:
  finalizers:
  - resources-finalizer.argocd.argoproj.io
spec:
  # (...)
```

## Ignore certain changes to Applications

The ApplicationSet spec includes an `ignoreApplicationDifferences` field, which allows you to specify which fields of 
the ApplicationSet should be ignored when comparing Applications.

The field supports multiple ignore rules
* Each ignore rule may specify a list of either `jsonPointers` or 
`jqPathExpressions` to ignore.

You may optionally also specify a `name` to apply the ignore rule to a specific Application, or omit the `name` to apply
the ignore rule to all Applications.

```yaml
apiVersion: argoproj.io/v1alpha1
kind: ApplicationSet
spec:
  ignoreApplicationDifferences:
    - jsonPointers:
        - /spec/source/targetRevision
    - name: some-app
      jqPathExpressions:
        - .spec.source.helm.values
```

### Allow temporarily toggling auto-sync

One of the most common use cases for ignoring differences is to allow temporarily toggling auto-sync for an Application.

For example, if you have an ApplicationSet that is configured to automatically sync Applications, you may want to temporarily
disable auto-sync for a specific Application
* You can do this by adding an ignore rule for the `spec.syncPolicy.automated` field.

```yaml
apiVersion: argoproj.io/v1alpha1
kind: ApplicationSet
spec:
  ignoreApplicationDifferences:
    - jsonPointers:
        - /spec/syncPolicy
```

### Limitations of `ignoreApplicationDifferences`

When an ApplicationSet is reconciled, the controller will compare the ApplicationSet spec with the spec of each Application
that it manages
* If there are any differences, the controller will generate a patch to update the Application to match the
ApplicationSet spec.

The generated patch is a MergePatch
* According to the MergePatch documentation, "existing lists will be completely 
replaced by new lists" when there is a change to the list.

This limits the effectiveness of `ignoreApplicationDifferences` when the ignored field is in a list
* For example, if you
have an application with multiple sources, and you want to ignore changes to the `targetRevision` of one of the sources,
changes in other fields or in other sources will cause the entire `sources` list to be replaced, and the `targetRevision`
field will be reset to the value defined in the ApplicationSet.

For example, consider this ApplicationSet:

```yaml
apiVersion: argoproj.io/v1alpha1
kind: ApplicationSet
spec:
  ignoreApplicationDifferences:
    - jqPathExpressions:
        - .spec.sources[] | select(.repoURL == "https://git.example.com/org/repo1").targetRevision
  template:
    spec:
      sources:
      - repoURL: https://git.example.com/org/repo1
        targetRevision: main
      - repoURL: https://git.example.com/org/repo2
        targetRevision: main
```

You can freely change the `targetRevision` of the `repo1` source, and the ApplicationSet controller will not overwrite
your change.

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
spec:
  sources:
  - repoURL: https://git.example.com/org/repo1
    targetRevision: fix/bug-123
  - repoURL: https://git.example.com/org/repo2
    targetRevision: main
```

However, if you change the `targetRevision` of the `repo2` source, the ApplicationSet controller will overwrite the entire
`sources` field.

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
spec:
  sources:
  - repoURL: https://git.example.com/org/repo1
    targetRevision: main
  - repoURL: https://git.example.com/org/repo2
    targetRevision: main
```

> [!NOTE]
> [Future improvements](https://github.com/argoproj/argo-cd/issues/15975) to the ApplicationSet controller may 
> eliminate this problem
* For example, the `ref` field might be made a merge key, allowing the ApplicationSet 
> controller to generate and use a StrategicMergePatch instead of a MergePatch
* You could then target a specific 
> source by `ref`, ignore changes to a field in that source, and changes to other sources would not cause the ignored 
> field to be overwritten.

## ALTHOUGH `Application` is deleted, prevent the `Application`'s child resources are deleted 

* [here](Application-Deletion.md)

## how to prevent that Application's child resources are modified?

* [Argo CD Integration](Argo-CD-Integration.md)
* [Application automated sync settings](../../user-guide/auto_sync.md)

## How to modify ApplicationSet container launch parameters?

* ways
  * [`kubectl edit`](#kubectl-edit--modify-the-deployment--cluster)
  * [edit the "install.yaml" manifest -- for the -- ApplicationSet installation](#edit-the-installyaml-manifest----for-the----applicationset-installation)

### `kubectl edit` / modify the deployment | cluster

Edit the applicationset-controller `Deployment` resource on the cluster:
```
kubectl edit deployment/argocd-applicationset-controller -n argocd
```

Locate the `.spec.template.spec.containers[0].command` field, and add the required parameter(s):
```yaml
spec:
    # (...)
  template:
    # (...)
    spec:
      containers:
      - command:
        - entrypoint.sh
        - argocd-applicationset-controller
        # Insert new parameters here, for example:
        # --policy create-only
    # (...)
```

Save and exit the editor
* Wait for a new `Pod` to start containing the updated parameters.

### edit the "install.yaml" manifest -- for the -- ApplicationSet installation

Rather than directly editing the cluster resource, you may instead choose to modify 
the installation YAML that is used to install the ApplicationSet controller:

Applicable for applicationset versions less than 0.4.0. 
```bash
# Clone the repository

git clone https://github.com/argoproj/applicationset

# Checkout the version that corresponds to the one you have installed.
git checkout "(version of applicationset)"
# example: git checkout "0.1.0"

cd applicationset/manifests

# open 'install.yaml' in a text editor, make the same modifications to Deployment 
# as described in the previous section.

# Apply the change to the cluster
kubectl apply -n argocd --server-side --force-conflicts -f install.yaml
```

## Preserving changes made to an Applications annotations and labels

> [!NOTE]
> The same behavior can be achieved on a per-app basis using the [`ignoreApplicationDifferences`](#ignore-certain-changes-to-applications) 
> feature described above
* However, preserved fields may be configured globally, a feature that is not yet available
> for `ignoreApplicationDifferences`.

It is common practice in Kubernetes to store state in annotations, operators will often make use of this
* To allow for this, it is possible to configure a list of annotations that the ApplicationSet should preserve when reconciling.

For example, imagine that we have an Application created from an ApplicationSet, but a custom annotation and label has since been added (to the Application) that does not exist in the `ApplicationSet` resource:
```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  # This annotation and label exists only on this Application, and not in 
  # the parent ApplicationSet template:
  annotations: 
    my-custom-annotation: some-value
  labels:
    my-custom-label: some-value
spec:
  # (...)
```

To preserve this annotation and label we can use the `preservedFields` property of the `ApplicationSet` like so:
```yaml
apiVersion: argoproj.io/v1alpha1
kind: ApplicationSet
spec:
  # (...)
  preservedFields:
    annotations: ["my-custom-annotation"]
    labels: ["my-custom-label"]
```

The ApplicationSet controller will leave this annotation and label as-is when reconciling, even though it is not defined in the metadata of the ApplicationSet itself.

By default, the Argo CD notifications and the Argo CD refresh type annotations are also preserved.

> [!NOTE]
> One can also set global preserved fields for the controller by passing a comma separated list of annotations and labels to 
> `ARGOCD_APPLICATIONSET_CONTROLLER_GLOBAL_PRESERVED_ANNOTATIONS` and `ARGOCD_APPLICATIONSET_CONTROLLER_GLOBAL_PRESERVED_LABELS` respectively.

## how to debug unexpected changes | Applications?

* if the ApplicationSet controller makes a change | an application -> it logs the patch | debug level
  * steps to modify the log level 
    * | "argocd-cmd-params-cm" ConfigMap | `argocd` namespace,
      * `data.applicationsetcontroller.log.level: debug`

## how to preview changes?

* `argocd appset create --dry-run <PATH_TO_APPLICATIONSET>`
  * _Example:_ `argocd appset create --dry-run ./appset.yaml -o json | jq -r '.status.resources[].name'`

* allows
  * preview changes / ApplicationSet controller would make | Applications 

* ❌NOT require❌
  * AppSet ALREADY exist
