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
    * ❌NOT technically required❌
      * BUT strongly recommended
    * Reason: 🧠application names == namespace's name + `Application`'s name
      * -> 's length can be > 63 characters (==labelS' limit length)
    * [how to enable](../user-guide/resource_tracking.md)
  * | "argocd-application-controller" & "argocd-server" workloads,
    * set `--application-namespaces = <NAMESPACE_FIRST>, <NAMESPACE_SECOND>, ...` / 
      * ways to specify
        * modifying the manifests -- for the -- respective workloads
        * | `argocd-cmd-params-cm` ConfigMap,
          * specify the `application.namespaces` settings
      * EACH `<NAMESPACE_*>` supports 
        * `*`
          * _Example:_ `app-team-*`
            * -> would match `app-team-one` & `app-team-two`
        * regex pattern / MUST be wrapped with ```/```
          * _Example:_  ```/^((?!not-allowed).)*$/```
    * == globally
  * adapt Kubernetes RBAC /
    * enable `Applications` | OTHER namespaces, can be managed -- by the -- Argo CD API (i.e. the CLI and UI)
    * _Example:_ [here](/examples/k8s-rbac/argocd-server-applications)
  * | "AppProject",
    * set `.spec.sourceNamespaces= <NAMESPACE_FIRST>, <NAMESPACE_SECOND>, ...`
      * recommendations
        * ❌NOT specify `argocd`❌
        * ❌| privileged project (_Example:_ `default`),
          * NOT specify user controlled namespaces❌
        * follow the least required privileges principle

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

* ⚠️restrictions⚠️
  * namespace | Applicationset lives != namespace | Application lives
    * [issue raised up](https://github.com/argoproj/argo-cd/issues/11104)

### Application names

* | CLI & UI,
  * `<namespace>/<name>`
    * == format -- to -- refer & display applications
    * if namespace == control plane's namespace (by default, `argocd`) -> you can use `<name>`
      * Reason:🧠backwards compatibility🧠
      * _Example:_ application name `argocd/someapp` == application name `someapp`

### Application RBAC

* [here](rbac.md)
  
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

* | GET,
  * `?appNamespace`
    * == query parameter
    * OPTIONAL

* | POST & PUT
  * | request's payload,
    * add `appNamespace` 

* for `Application` resources | control plane namespace,
  * `appNamespace` can be omitted
