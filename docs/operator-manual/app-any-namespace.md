# Applications | ANY namespace

* goal
  * manage `Application` resources | namespaces / != control plane's namespace
    * Reason:🧠by default, ONLY ALLOWED | Argo CD's control plane namespace🧠

## Introduction

* requirements
  * Argo CD v2.5+
  * Cluster-scoped Argo CD installation
    * [here](/manifests/README.md)
      * Reason:🧠has permissions -- to -- list & manipulate resources | cluster scope🧠
    * ❌!= Argo CD namespace-scoped installation❌
  * switch the application tracking method -- to -- `annotation` OR `annotation+label`
    * Reason: 🧠application names == namespace's name + `Application`'s name
      * -> 's length can be > 63 characters (==labelS' limit length)
    * ❌NOT technically required❌
      * BUT strongly recommended
    * [how to enable](../user-guide/resource_tracking.md)
  * | `argocd-application-controller` & `argocd-server` workloads,
    * set `--application-namespaces = <NAMESPACE_FIRST>, <NAMESPACE_SECOND>, ...`
    * == globally
  * | `AppProject`,
    * set `.spec.sourceNamespaces= <NAMESPACE_FIRST>, <NAMESPACE_SECOND>, ...`

* control plane's namespace
  * by default,
    * "argocd" 

* 👀enable👀
  * ordinary Argo CD users
    * can manage ArgoCD Applications
      * _Example:_ [declaratively](declarative-setup.md) 
      * 💡WITHOUT risk of privilege escalation💡
        * Reason:🧠restricted to the namespace🧠
    * can configure [notifications / Argo CD application | specific namespace](notifications/index.md#namespace-based-configuration)

* ⚠️take care enabling it⚠️
  * Reason:🧠Misconfiguration -> could lead -- to -- potential security issues🧠

## Implementation details

### Reconfigure Argo CD to allow certain namespaces

#### Change workload startup parameters

In order to enable this feature, the Argo CD administrator must reconfigure the `argocd-server` and `argocd-application-controller` workloads to add the `--application-namespaces` parameter to the container's startup command.

The `--application-namespaces` parameter takes a comma-separated list of namespaces where `Applications` are to be allowed in. Each entry of the list supports:

- shell-style wildcards such as `*`, so for example the entry `app-team-*` would match `app-team-one` and `app-team-two`. To enable all namespaces on the cluster where Argo CD is running on, you can just specify `*`, i.e. `--application-namespaces=*`.
- regex, requires wrapping the string in ```/```, example to allow all namespaces except a particular one: ```/^((?!not-allowed).)*$/```.
  
The startup parameters for both, the `argocd-server` and the `argocd-application-controller` can also be conveniently set up and kept in sync by specifying the `application.namespaces` settings in the `argocd-cmd-params-cm` ConfigMap _instead_ of changing the manifests for the respective workloads. For example:

```yaml
data:
  application.namespaces: app-team-one, app-team-two
```

would allow the `app-team-one` and `app-team-two` namespaces for managing `Application` resources. After a change to the `argocd-cmd-params-cm` namespace, the appropriate workloads need to be restarted:

```bash
kubectl rollout restart -n argocd deployment argocd-server
kubectl rollout restart -n argocd statefulset argocd-application-controller
```

#### Adapt Kubernetes RBAC

We decided to not extend the Kubernetes RBAC for the `argocd-server` workload by default for the time being. If you want `Applications` in other namespaces to be managed by the Argo CD API (i.e. the CLI and UI), you need to extend the Kubernetes permissions for the `argocd-server` ServiceAccount.

We supply a `ClusterRole` and `ClusterRoleBinding` suitable for this purpose in the `examples/k8s-rbac/argocd-server-applications` directory. For a default Argo CD installation (i.e. installed to the `argocd` namespace), you can just apply them as-is:

```shell
kubectl apply -k examples/k8s-rbac/argocd-server-applications/
```

`argocd-notifications-controller-rbac-clusterrole.yaml` and `argocd-notifications-controller-rbac-clusterrolebinding.yaml` are used to support notifications controller to notify apps in all namespaces.

> [!NOTE]
> At some later point in time, we may make this cluster role part of the default installation manifests.

### Allowing ADDITIONAL namespaces | AppProject

* Argo CD admin
  * := user / 
    * Kubernetes access | Argo CD control plane's namespace (`argocd`)
    * permissions -- to -- create OR update `Applications` / declaratively 

* unprivileged Argo CD users
  * if they want to create or manage `Applications` 
    * ❌NOT declaratively ❌ 
    * use the API
      * Reason: 🧠subject -- to -- Argo CD RBAC🧠
        * -> ONLY can create `Applications` | ALLOWED `AppProjects`

* TODO:

In order for an Application to set `.spec.project` to `project-one`, it would have to be created in either namespace `namespace-one` or `argocd`. 
Likewise, in order for an Application to set `.spec.project` to `project-two`, it would have to be created in either namespace `namespace-two` or `argocd`.

If an Application in `namespace-two` would set their `.spec.project` to `project-one` or an Application in `namespace-one` would set their `.spec.project` to `project-two`, Argo CD would consider this as a permission violation and refuse to reconcile the Application.

Also, the Argo CD API will enforce these constraints, regardless of the Argo CD RBAC permissions.

The `.spec.sourceNamespaces` field of the `AppProject` is a list that can contain an arbitrary amount of namespaces, and each entry supports shell-style wildcard, so that you can allow namespaces with patterns like `team-one-*`.

> [!WARNING]
> Do not add user controlled namespaces in the `.spec.sourceNamespaces` field of any privileged AppProject like the `default` project. Always make sure that the AppProject follows the principle of granting least required privileges. Never grant access to the `argocd` namespace within the AppProject.

> [!NOTE]
> For backwards compatibility, Applications in the Argo CD control plane's namespace (`argocd`) are allowed to set their `.spec.project` field to reference any AppProject, regardless of the restrictions placed by the AppProject's `.spec.sourceNamespaces` field.

> [!NOTE]
> Currently it's not possible to have a applicationset in one namespace and have the application
> be generated in another. See [#11104](https://github.com/argoproj/argo-cd/issues/11104) for more info.

### Application names

For the CLI and UI, applications are now referred to and displayed as in the format `<namespace>/<name>`.

For backwards compatibility, if the namespace of the Application is the control plane's namespace (i.e. `argocd`), the `<namespace>` can be omitted from the application name when referring to it. For example, the application names `argocd/someapp` and `someapp` are semantically the same and refer to the same application in the CLI and the UI.

### Application RBAC

The RBAC syntax for Application objects has been changed from `<project>/<application>` to `<project>/<namespace>/<application>` to accommodate the need to restrict access based on the source namespace of the Application to be managed.

For backwards compatibility, Applications in the `argocd` namespace can still be referred to as `<project>/<application>` in the RBAC policy rules.

Wildcards do not make any distinction between project and application namespaces yet. For example, the following RBAC rule would match any application belonging to project `foo`, regardless of the namespace it is created in:

```
p, somerole, applications, get, foo/*, allow
```

If you want to restrict access to be granted only to `Applications` in project `foo` within namespace `bar`, the rule would need to be adapted as follows:

```
p, somerole, applications, get, foo/bar/*, allow
```
  
## how to manage applications | OTHER namespaces?

### Declaratively

* define the Application -- through -- AppProject / 
  * AppProject specifies the `spec.sourceNamespaces`

### -- via -- `argocd` CL

* `argocd [COMMAND] <APPLICATION_NAME>/<NAMESPACE_NAME>`
  * if application live | Argo CD's control plane namespace -> you can omit the `<NAMESPACE_NAME>` 

### -- via -- ArgoCD UI

* | create an application,
  * General
    * name == `<APPLICATION_NAME>`
  * Destination
    * namespace == `<NAMESPACE_NAME>`

### -- via -- ArgoCD  REST API

If you are using the REST API, the namespace for `Application` cannot be specified as the application name, 
and resources need to be specified using the optional `appNamespace` query parameter
* For example, to work with the `Application` resource named `foo` in the namespace `bar`, 
* the request would look like follows:

```bash
GET /api/v1/applications/foo?appNamespace=bar
```

For other operations such as `POST` and `PUT`, the `appNamespace` parameter must be part of the request's payload.

For `Application` resources in the control plane namespace, this parameter can be omitted.
