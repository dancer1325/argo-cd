# RBAC Configuration

* RBAC  
  * enables
    * restrictions of access -- to -- Argo CD resources
  * requirements
    * [SSO configuration](user-management/index.md), OR 
    * [>=1 local users setup](user-management/index.md)
  * 👀| configure RBAC, main components 👀
    * ["argocd-rbac-cm" configMap](examples/argocd-rbac-cm.yaml)
      * == global RBAC configMap
      * apply | specified policy rule's resource
    * [AppProject's roles](../user-guide/projects.md#project-roles)
      - apply | SPECIFIC project
  * steps
    * define & apply RBAC roles
    * map SSO groups OR local users -- to -- roles

## RBAC Model

* [here](/assets/model.conf)

* model syntax
  * is -- based on -- [Casbin](https://casbin.org/docs/overview)
  * types of syntax
    * [Policy -- `p` --](https://casbin.apache.org/docs/how-it-works#policy)
      * syntax -- for -- assigning policies
    * [group -- role definition --](https://casbin.apache.org/docs/rbac#role-definition)
      * syntax -- for -- assigning users -- to -- internal roles

* **Policy**
  * allows
    * assign permissions -- to an -- entity
  * `p, <role/user/group>, <resource>, <action>, <object>, <effect>`
    * == syntax
    - `<role/user/group>`
      - == entity | policy will be assigned
      - if you want to distinguish user vs role -> user [`role::` prefix](https://casbin.apache.org/docs/rbac#distinguishing-users-from-roles)
      - group comes -- from -- [SSO provider](user-management/index.md)
    - `<resource>`
      - == type of resource | action is performed
        - [accounts](user-management/index.md)
          - == local users
        - [certificates](tls.md)
        - [gpgkeys](../user-guide/gpg-verification.md)
        - [exec](web_based_terminal.md)
        - [extensions](../developer-guide/extensions/proxy-extensions.md)
    - `<action>`
      - == operation / performed | resource
      - below table
    - `<object>`
      - == object identifier /
        - represent the resource | perform the action
        - 's format -- , depend on the -- resource
    - `<effect>`
      - Whether this policy should grant or restrict the operation | target object
      - ALLOWED values
        - `allow`
        - `deny`

* **Group**
  * allows
    * assign authenticated users/groups -- to -- internal roles
  * `g, <user/group>, <role>`
    * == syntax
    - `<user/group>`
      - == entity | role will be assigned
        - types
          - local user
          - user / authenticated -- via -- SSO
            - `user` is derived -- from the -- token’s `federated_claims.user_id` field
            - `group` is derived -- from the -- values returned by the OIDC provider | configured scopes (e.g., groups, roles)
    - `<role>`
      - == internal role | entity will be assigned

* actions / EACH [resource](/util/rbac/rbac.go)

  | Resource\Action     | get | create | update | delete | sync | action | override | invoke |
  | :------------------ | :-: | :----: | :----: | :----: | :--: | :----: | :------: | :----: |
  | **applications**    | ✅  |   ✅   |   ✅   |   ✅   |  ✅  |   ✅   |    ✅    |   ❌   |
  | **applicationsets** | ✅  |   ✅   |   ✅   |   ✅   |  ❌  |   ❌   |    ❌    |   ❌   |
  | **clusters**        | ✅  |   ✅   |   ✅   |   ✅   |  ❌  |   ❌   |    ❌    |   ❌   |
  | **projects**        | ✅  |   ✅   |   ✅   |   ✅   |  ❌  |   ❌   |    ❌    |   ❌   |
  | **repositories**    | ✅  |   ✅   |   ✅   |   ✅   |  ❌  |   ❌   |    ❌    |   ❌   |
  | **accounts**        | ✅  |   ❌   |   ✅   |   ❌   |  ❌  |   ❌   |    ❌    |   ❌   |
  | **certificates**    | ✅  |   ✅   |   ❌   |   ✅   |  ❌  |   ❌   |    ❌    |   ❌   |
  | **gpgkeys**         | ✅  |   ✅   |   ❌   |   ✅   |  ❌  |   ❌   |    ❌    |   ❌   |
  | **logs**            | ✅  |   ❌   |   ❌   |   ❌   |  ❌  |   ❌   |    ❌    |   ❌   |
  | **exec**            | ❌  |   ✅   |   ❌   |   ❌   |  ❌  |   ❌   |    ❌    |   ❌   |
  | **extensions**      | ❌  |   ❌   |   ❌   |   ❌   |  ❌  |   ❌   |    ❌    |   ✅   |


#### application-specific policy -- `<object>` == `<app-project>/<app-name>` --

* uses
  * | ALLOWED resources
    - `applications`
    - `applicationsets`
    - `logs`
    - `exec`

##### | ANY Namespaces -- `<object>` == `<app-project>/<app-ns>/<app-name>` --

* requirements
  * enable [application | ANY namespace](app-any-namespace.md)

##### Fine-grained Permissions for `update`/`delete` action

The `update` and `delete` actions, when granted on an application, will allow the user to perform the operation on the application itself,
but not on its resources.

To allow an action on the application's resources, specify the action as `<action>/<group>/<kind>/<ns>/<name>`.

For instance, to grant access to `example-user` to only delete Pods in the `prod-app` Application, the policy could be:

```csv
p, example-user, applications, delete/*/Pod/*/*, default/prod-app, allow
```

> [!WARNING]
> **Understand glob pattern behavior**
>
> Argo CD RBAC does not use `/` as a separator when evaluating glob patterns. So the pattern `delete/*/kind/*`
> will match `delete/<group>/kind/<namespace>/<name>` but also `delete/<group>/<kind>/kind/<name>`.
>
> The fact that both of these match will generally not be a problem, because resource kinds generally contain capital
> letters, and namespaces cannot contain capital letters. However, it is possible for a resource kind to be lowercase.
> So it is better to just always include all the parts of the resource in the pattern (in other words, always use four
> slashes).

If we want to grant access to the user to update all resources of an application, but not the application itself:

```csv
p, example-user, applications, update/*, default/prod-app, allow
```

If we want to explicitly deny delete of the application, but allow the user to delete Pods:

```csv
p, example-user, applications, delete, default/prod-app, deny
p, example-user, applications, delete/*/Pod/*/*, default/prod-app, allow
```

If we want to explicitly allow updates to the application, but deny updates to any sub-resources:

```csv
p, example-user, applications, update, default/prod-app, allow
p, example-user, applications, update/*, default/prod-app, deny
```

> [!NOTE]
> **Preserve Application permission Inheritance (Since v3.0.0)**
>
> Prior to v3, `update` and `delete` actions (without a `/*`) were also evaluated
> on sub-resources.
>
> To preserve this behavior, you can set the config value
> `server.rbac.disableApplicationFineGrainedRBACInheritance` to `false` in
> the Argo CD ConfigMap `argocd-cm`.
>
> When disabled, it is not possible to deny fine-grained permissions for a sub-resource
> if the action was **explicitly allowed on the application**.
> For instance, the following policies will **allow** a user to delete the Pod and any
> other resources in the application:
>
> ```csv
> p, example-user, applications, delete, default/prod-app, allow
> p, example-user, applications, delete/*/Pod/*, default/prod-app, deny
> ```

##### The `action` action

The `action` action corresponds to either built-in resource customizations defined
[in the Argo CD repository](https://github.com/argoproj/argo-cd/tree/master/resource_customizations),
or to [custom resource actions](resource_actions.md#custom-resource-actions) defined by you.

See the [resource actions documentation](resource_actions.md#built-in-actions) for a list of built-in actions.

The `<action>` has the `action/<group>/<kind>/<action-name>` format.

For example, a resource customization path `resource_customizations/extensions/DaemonSet/actions/restart/action.lua`
corresponds to the `action` path `action/extensions/DaemonSet/restart`. If the resource is not under a group (for example, Pods or ConfigMaps),
then the path will be `action//Pod/action-name`.

The following policies allows the user to perform any action on the DaemonSet resources, as well as the `maintenance-off` action on a Pod:

```csv
p, example-user, applications, action//Pod/maintenance-off, default/*, allow
p, example-user, applications, action/extensions/DaemonSet/*, default/*, allow
```

To allow the user to perform any actions:

```csv
p, example-user, applications, action/*, default/*, allow
```

##### The `override` action

The `override` action privilege can be used to allow passing arbitrary manifests or different revisions when syncing an `Application`. This can e.g. be used for development or testing purposes.

**Attention:** This allows users to completely change/delete the deployed resources of the application.

While the `sync` action privilege gives the right to synchronize the objects in the cluster to the desired state as defined in the `Application` Object, the `override` action privilege will allow a user to synchronize arbitrary local manifests to the Application. These manifests will be used _instead of_ the configured source, until the next sync is performed. After performing such a override sync, the application will most probably be OutOfSync with the state defined via the `Application` object.
It is not possible to perform an `override` sync when auto-sync is enabled.

New since v3.2:

When `application.sync.requireOverridePrivilegeForRevisionSync: 'true'` is set in the `argcd-cm` configmap,
passing a revision when syncing an `Application` is also considered as an `override`, to prevent synchronizing to arbitrary revisions other than the revision(s) given in the `Application` object. Similar as syncing to an arbitrary yaml manifest, syncing to a different revision/branch/commit will also bring the controlled objects to a state differing, and thus OufOfSync from the state as defined in the `Application`.

The default setting of this flag is 'false', to prevent breaking changes in existing installations. It is recommended to set this setting to 'true' and only grant the `override` privilege per AppProject to the users that actually need this behavior.


#### `applicationsets` resource

* == [Application-Specific policy](#application-specific-policy)

[ApplicationSets](applicationset/index.md) provide a declarative way to automatically create/update/delete Applications.

Allowing the `create` action on the resource effectively grants the ability to create Applications. While it doesn't allow the
user to create Applications directly, they can create Applications via an ApplicationSet.

> [!NOTE]
> In v2.5, it is not possible to create an ApplicationSet with a templated Project field (e.g. `project: {{path.basename}}`)
> via the API (or, by extension, the CLI). Disallowing templated projects makes project restrictions via RBAC safe:

With the resource being application-specific, the `<object>` of the applicationsets policy will have the format `<app-project>/<app-name>`.
However, since an ApplicationSet does belong to any project, the `<app-project>` value represents the projects in which the ApplicationSet will be able to create Applications.

With the following policy, a `dev-group` user will be unable to create an ApplicationSet capable of creating Applications
outside the `dev-project` project.

```csv
p, dev-group, applicationsets, *, dev-project/*, allow
```

#### `logs` resource

* allows
  * seeing pod's logs

* == `kubectl logs`

#### `exec` resource

* requirements
  * | argocd-cm.yaml,
    * `data.exec.enabled: "true"`

* allows
  * | ArgoCD UI, 
    * user can `exec` | Pods

* == `kubectl exec`

* [MORE](web_based_terminal.md)

#### `extensions` resource

With the `extensions` resource, it is possible to configure permissions to invoke [proxy extensions](../developer-guide/extensions/proxy-extensions.md).
The `extensions` RBAC validation works in conjunction with the `applications` resource.
A user **needs to have read permission on the application** where the request is originated from.

Consider the example below, it will allow the `example-user` to invoke the `httpbin` extensions in all
applications under the `default` project.

```csv
p, example-user, applications, get, default/*, allow
p, example-user, extensions, invoke, httpbin, allow
```

### `deny` effect

When `deny` is used as an effect in a policy, it will be effective if the policy matches.
Even if more specific policies with the `allow` effect match as well, the `deny` will have priority.

The order in which the policies appears in the policy file configuration has no impact, and the result is deterministic.

## Built-in 

* [policy](/assets/builtin-policy.csv)
* RBAC Roles
  * `role:readonly`
    * read-only access -- to -- ALL resources
  * `role:admin`
    * unrestricted access -- to -- ALL resources

## default policy

* | "argocd-rbac-cm" ConfigMap,
  * [`data.policy.default`](examples/argocd-rbac-cm.yaml)

## Anonymous Access

* steps
  * | ["argocd-cm" ConfigMap](examples/argocd-cm.yaml),
    * `data.users.anonymous.enabled: "true"`
      * == enable anonymous access

* allows
  * anonymous users can access -- to the -- Argo CD instance /
    * assume the [default role permissions](#default-policy)

## Policies Evaluation and Matching

The evaluation of access is done in two parts: validating against the default policy configuration, then validating against the policies for the current user.

**If an action is allowed or denied by the default policies, then this effect will be effective without further evaluation**.
When the effect is undefined, the evaluation will continue with subject-specific policies.

The access will be evaluated for the user, then for each configured group that the user is part of.

The matching engine, configured in `policy.matchMode`, can use two different match modes to compare the values of tokens:

- `glob`: based on the [`glob` package](https://pkg.go.dev/github.com/gobwas/glob).
- `regex`: based on the [`regexp` package](https://pkg.go.dev/regexp).

When all tokens match during the evaluation, the effect will be returned. The evaluation will continue until all matching policies are evaluated, or until a policy with the `deny` effect matches.
After all policies are evaluated, if there was at least one `allow` effect and no `deny`, access will be granted.

### Glob matching

When `glob` is used, the policy tokens are treated as single terms, without separators.

Consider the following policy:

```
p, example-user, applications, action/extensions/*, default/*, allow
```

When the `example-user` executes the `extensions/DaemonSet/test` action, the following `glob` matches will happen:

1. The current user `example-user` matches the token `example-user`.
2. The value `applications` matches the token `applications`.
3. The value `action/extensions/DaemonSet/test` matches `action/extensions/*`. Note that `/` is not treated as a separator and the use of `**` is not necessary.
4. The value `default/my-app` matches `default/*`.

## -- via -- 

### Local Users/Accounts

* [Local users](user-management/index.md#local-usersaccounts)
  * ways to assign access
    * group them -- with a -- role
    * assign policies DIRECTLY -- to -- them

TODO: 
> [!WARNING]
> **Ambiguous Group Assignments**
>
> If you have [enabled SSO](user-management/index.md#sso), any SSO user with a scope that matches a local user will be
> added to the same roles as the local user
> For example, if local user `sally` is assigned to `role:admin`, and if an
> SSO user has a scope which happens to be named `sally`, that SSO user will also be assigned to `role:admin`.
>
> An example of where this may be a problem is if your SSO provider is an SCM, and org members are automatically
> granted scopes named after the orgs
> If a user can create or add themselves to an org in the SCM, they can gain the
> permissions of the local user with the same name.
>
> To avoid ambiguity, if you are using local users and SSO, it is recommended to assign policies directly to local
> users, and not to assign roles to local users
> In other words, instead of using `g, my-local-user, role:admin`, you
> should explicitly assign policies to `my-local-user`:
>
> ```yaml
> p, my-local-user, *, *, *, allow
> ```

### SSO Users/Groups

The `scopes` field controls which OIDC scopes to examine during RBAC enforcement (in addition to `sub` scope).
If omitted, it defaults to `'[groups]'`. The scope value can be a string, or a list of strings.

For more information on `scopes` please review the [User Management Documentation](user-management/index.md).

The following example shows targeting `email` as well as `groups` from your OIDC provider, and also demonstrates explicit role assignments and role-to-role inheritance:

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: argocd-rbac-cm
  namespace: argocd
  labels:
    app.kubernetes.io/name: argocd-rbac-cm
    app.kubernetes.io/part-of: argocd
data:
  policy.csv: |
    p, my-org:team-alpha, applications, sync, my-project/*, allow
    g, my-org:team-beta, role:admin
    g, user@example.org, role:admin
    g, admin, role:admin
    g, role:admin, role:readonly
  policy.default: role:readonly
  scopes: '[groups, email]'
```

Here:
1. `g, admin, role:admin` explicitly binds the built-in admin user to the admin role.
2. `g, role:admin, role:readonly` shows role inheritance, so anyone granted `role:admin` also automatically has all the permissions of
   `role:readonly`.

This approach can be combined with AppProjects to associate users' emails and groups directly at the project level:
```yaml
apiVersion: argoproj.io/v1alpha1
kind: AppProject
metadata:
  name: team-beta-project
  namespace: argocd
spec:
  roles:
    - name: admin
      description: Admin privileges to team-beta
      policies:
        - p, proj:team-beta-project:admin, applications, *, team-beta-project/*, allow
      groups:
        - user@example.org # Value from the email scope
        - my-org:team-beta # Value from the groups scope
```

## Policy CSV Composition

It is possible to provide additional entries in the `argocd-rbac-cm` configmap to compose the final policy csv.
In this case, the key must follow the pattern `policy.<any string>.csv`.
Argo CD will concatenate all additional policies it finds with this pattern below the main one ('policy.csv').
The order of additional provided policies are determined by the key string.

Example: if two additional policies are provided with keys `policy.A.csv` and `policy.B.csv`,
it will first concatenate `policy.A.csv` and then `policy.B.csv`.

This is useful to allow composing policies in config management tools like Kustomize, Helm, etc.

The example below shows how a Kustomize patch can be provided in an overlay to add additional configuration to an existing RBAC ConfigMap.

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: argocd-rbac-cm
  namespace: argocd
data:
  policy.tester-overlay.csv: |
    p, role:tester, applications, *, */*, allow
    p, role:tester, projects, *, *, allow
    g, my-org:team-qa, role:tester
```

## Validating and testing your RBAC policies

If you want to ensure that your RBAC policies are working as expected, you can
use the [`argocd admin settings rbac` command](../user-guide/commands/argocd_admin_settings_rbac.md) to validate them.
This tool allows you to test whether a certain role or subject can perform the requested action with a policy
that's not live yet in the system, i.e. from a local file or config map.
Additionally, it can be used against the live RBAC configuration in the cluster your Argo CD is running in.

### Validating a policy

To check whether your new policy configuration is valid and understood by Argo CD's RBAC implementation,
you can use the [`argocd admin settings rbac validate` command](../user-guide/commands/argocd_admin_settings_rbac_validate.md).

### Testing a policy

To test whether a role or subject (group or local user) has sufficient
permissions to execute certain actions on certain resources, you can
use the [`argocd admin settings rbac can` command](../user-guide/commands/argocd_admin_settings_rbac_can.md).
