# Git Generator

* [data structure](/manifests/crds/applicationset-crd.yaml)'s `spec.generators[*].git`

* 👀's subtypes👀
  * [Git generator: directory](#git-generator-directories)
  * [Git generator: file](#git-generator-files)

* the MOST flexible/powerful of the generators

TODO: 
> [!WARNING]
> If the `project` field in your ApplicationSet is templated, developers may be able to create Applications under Projects with excessive permissions.
> For ApplicationSets with a templated `project` field, [the source of truth _must_ be controlled by admins](./Security.md#templated-project-field)
> - in the case of git generators, PRs must require admin approval.
> - Git generator does not support Signature Verification For ApplicationSets with a templated `project` field.
> - You must only use "non-scoped" repositories for ApplicationSets with a templated `project` field (see ["Repository Credentials for Applicationsets" below](#repository-credentials-for-applicationsets)).

## Git Generator: Directories

* generates parameters -- based on -- specified repository's directory structure

* _Example:_ [here](/applicationset/examples/git-generator-directory)

* built-in parameters
  * `{{.path.path}}`
    * == directory path / match | Git repository
      * _Example:_ cluster-addons/argo-workflows, cluster-addons/prometheus-operator 
  * `{{index .path.segments n}}`
    * == directory path | Git repository / split | array elements
  * `{{.path.basename}}`
    * == TODO: For any directory path within the Git repository that matches the `path` wildcard,
    * == `path`'s right-most path
      * _Example:_ if `.path` == /one/two/three/four ->  `.path.basename` == four
  * `{{.path.basenameNormalized}}`
    * == `.path.basename` / unsupported characters are replaced -- with -- `-`
      * _Example:_
        * if `path` == `/directory/directory_2` -> would produce `directory-2`
        * if `.path.basename` == `directory_2` -> would produce `directory-2`


> [!NOTE]
> If the `pathParamPrefix` option is specified, all `path`-related parameter names above will be prefixed with the specified value and a dot separator. 
> E.g., if `pathParamPrefix` is `myRepo`, then the generated parameter name would be `.myRepo.path` instead of `.path`. Using this option is necessary 
> in a Matrix generator where both child generators are Git generators (to avoid conflicts when merging the child generators’ items).

Whenever a new Helm chart/Kustomize YAML/Application/plain subdirectory is added to the Git repository, 
the ApplicationSet controller will detect this change and automatically deploy the resulting manifests within new `Application` resources.

As with other generators, clusters *must* already be defined within Argo CD, in order to generate Applications for them.

### Exclude directories

The Git directory generator will automatically exclude directories that begin with `.` (such as `.git`).

The Git directory generator also supports an `exclude` option in order to exclude directories in the repository
from being scanned by the ApplicationSet controller:

```yaml
apiVersion: argoproj.io/v1alpha1
kind: ApplicationSet
metadata:
  name: cluster-addons
  namespace: argocd
spec:
  goTemplate: true
  goTemplateOptions: ["missingkey=error"]
  generators:
  - git:
      repoURL: https://github.com/argoproj/argo-cd.git
      revision: HEAD
      directories:
      - path: applicationset/examples/git-generator-directory/excludes/cluster-addons/*
      - path: applicationset/examples/git-generator-directory/excludes/cluster-addons/exclude-helm-guestbook
        exclude: true
  template:
    metadata:
      name: '{{.path.basename}}'
    spec:
      project: "my-project"
      source:
        repoURL: https://github.com/argoproj/argo-cd.git
        targetRevision: HEAD
        path: '{{.path.path}}'
      destination:
        server: https://kubernetes.default.svc
        namespace: '{{.path.basename}}'
```
(*The [full example](https://github.com/argoproj/argo-cd/tree/master/applicationset/examples/git-generator-directory/excludes).*)

This example excludes the `exclude-helm-guestbook` directory from the list of directories scanned for this `ApplicationSet` resource.

> [!NOTE]
> **Exclude rules have higher priority than include rules**
>
> If a directory matches at least one `exclude` pattern, it will be excluded. Or, said another way,
> *exclude rules take precedence over include rules.*
>
> As a corollary, which directories are included/excluded is not affected by the order of `path`s in the `directories`
> field list (because, as above, exclude rules always take precedence over include rules). 

For example, with these directories:

```
.
└── d
    ├── e
    ├── f
    └── g
```
Say you want to include `/d/e`, but exclude `/d/f` and `/d/g`
* This will *not* work:

```yaml
- path: /d/e
  exclude: false
- path: /d/*
  exclude: true
```
Why? Because the exclude `/d/*` exclude rule will take precedence over the `/d/e` include rule
* When the `/d/e` path in the Git repository is processed by the ApplicationSet controller, the controller detects that at least one exclude rule is matched, and thus that directory should not be scanned.

You would instead need to do:

```yaml
- path: /d/*
- path: /d/f
  exclude: true
- path: /d/g
  exclude: true
```

Or, a shorter way (using [path.Match](https://golang.org/pkg/path/#Match) syntax) would be:

```yaml
- path: /d/*
- path: /d/[fg]
  exclude: true
```

### Root Of Git Repo

The Git directory generator can be configured to deploy from the root of the git repository by providing `'*'` as the `path`.

To exclude directories, you only need to put the name/[path.Match](https://golang.org/pkg/path/#Match) of the directory you do not want to deploy.

```yaml
apiVersion: argoproj.io/v1alpha1
kind: ApplicationSet
metadata:
  name: cluster-addons
  namespace: argocd
spec:
  goTemplate: true
  goTemplateOptions: ["missingkey=error"]
  generators:
  - git:
      repoURL: https://github.com/example/example-repo.git
      revision: HEAD
      directories:
      - path: '*'
      - path: donotdeploy
        exclude: true
  template:
    metadata:
      name: '{{.path.basename}}'
    spec:
      project: "my-project"
      source:
        repoURL: https://github.com/example/example-repo.git
        targetRevision: HEAD
        path: '{{.path.path}}'
      destination:
        server: https://kubernetes.default.svc
        namespace: '{{.path.basename}}'
```

### Pass additional key-value pairs via `values` field

You may pass additional, arbitrary string key-value pairs via the `values` field of the git directory generator
* Values added via the `values` field are added as `values.(field)`.

In this example, a `cluster` parameter value is passed
* It is interpolated from the `path` variable, to then be used to determine the destination namespace.
```yaml
apiVersion: argoproj.io/v1alpha1
kind: ApplicationSet
metadata:
  name: cluster-addons
  namespace: argocd
spec:
  goTemplate: true
  goTemplateOptions: ["missingkey=error"]
  generators:
  - git:
      repoURL: https://github.com/example/example-repo.git
      revision: HEAD
      directories:
      - path: '*'
      values:
        cluster: '{{.path.basename}}'
  template:
    metadata:
      name: '{{.path.basename}}'
    spec:
      project: "my-project"
      source:
        repoURL: https://github.com/example/example-repo.git
        targetRevision: HEAD
        path: '{{.path.path}}'
      destination:
        server: https://kubernetes.default.svc
        namespace: '{{.values.cluster}}'
```

> [!NOTE]
> The `values.` prefix is always prepended to values provided via `generators.git.values` field
* Ensure you include this prefix in the parameter name within the `template` when using it.

In `values` we can also interpolate all fields set by the git directory generator as mentioned above.

## Git Generator: Files

* built-in parameters
  * `{{.path.path}}`
    * == path -- to the -- directory / contain matching configuration file | Git repository
      * _Example:_ if the config file == `/clusters/clusterA/config.json` -> `/clusters/clusterA` 
  * `{{index .path.segments n}}`
    * == path -- to the -- matching configuration file | Git repositor / split | array elements
      * _Example:_ 
        * `index .path.segments 0: clusters`
        * `index .path.segments 1: clusterA`
  * `{{.path.basename}}`
    * == basename of the path to the directory / contain the configuration file
      * _Example:_ `clusterA`
  * `{{.path.basenameNormalized}}`
    * == `.path.basename` / unsupported characters are replaced -- with -- `-`
      * _Example:_ 
        * if `path` == `/directory/directory_2` -> would produce `directory-2`
        * if `.path.basename` == `directory_2` -> would produce `directory-2`
  * `{{.path.filename}}`
    * == matched filename
      * _Example:_ `config.json`
  * `{{.path.filenameNormalized}}`
    * == matched filename / unsupported characters are replaced -- with -- `-`

* generates parameters -- based on -- contents of JSON/YAML files | specified repository

* _Example:_ [here](/applicationset/examples/git-generator-files-discovery)

TODO: 
> [!NOTE]
> The right-most *directory* name always becomes `{{.path.basename}}`
* For example, from `- path: /one/two/three/four/config.json`, `{{.path.basename}}` 
> will be `four`. The filename can always be accessed using `{{.path.filename}}`. 

> [!NOTE]
> If the `pathParamPrefix` option is specified, all `path`-related parameter names above will be prefixed with the specified value and a dot separator. 
> E.g., if `pathParamPrefix` is `myRepo`, then the generated parameter name would be `myRepo.path` instead of `path`
> Using this option is necessary in a Matrix generator where both child generators are Git generators (to avoid conflicts when merging the child generators’ items).

> [!NOTE]
> The default behavior of the Git file generator is very greedy. 
> Please see [Git File Generator Globbing](./Generators-Git-File-Globbing.md) for more information.

### Exclude files

The Git file generator also supports an `exclude` option in order to exclude files in the repository from being scanned by the ApplicationSet controller:

```yaml
apiVersion: argoproj.io/v1alpha1
kind: ApplicationSet
metadata:
  name: guestbook
spec:
  goTemplate: true
  goTemplateOptions: ["missingkey=error"]
  generators:
    - git:
        repoURL: https://github.com/argoproj/argo-cd.git
        revision: HEAD
        files:
          - path: "applicationset/examples/git-generator-files-discovery/cluster-config/**/config.json"
          - path: "applicationset/examples/git-generator-files-discovery/cluster-config/*/dev/config.json"
            exclude: true
  template:
    metadata:
      name: '{{.cluster.name}}-guestbook'
    spec:
      project: default
      source:
        repoURL: https://github.com/argoproj/argo-cd.git
        targetRevision: HEAD
        path: "applicationset/examples/git-generator-files-discovery/apps/guestbook"
      destination:
        server: https://kubernetes.default.svc
        #server: '{{.cluster.address}}'
        namespace: guestbook
```

This example excludes the `config.json` file in the `dev` directory from the list of files scanned for this `ApplicationSet` resource.

(*The [full example](https://github.com/argoproj/argo-cd/tree/master/applicationset/examples/git-generator-files-discovery/excludes).*)

### Pass additional key-value pairs via `values` field

You may pass additional, arbitrary string key-value pairs via the `values` field of the git files generator. Values added via the `values` field are added as `values.(field)`.

In this example, a `base_dir` parameter value is passed. It is interpolated from `path` segments, to then be used to determine the source path.
```yaml
apiVersion: argoproj.io/v1alpha1
kind: ApplicationSet
metadata:
  name: guestbook
  namespace: argocd
spec:
  goTemplate: true
  goTemplateOptions: ["missingkey=error"]
  generators:
  - git:
      repoURL: https://github.com/argoproj/argo-cd.git
      revision: HEAD
      files:
      - path: "applicationset/examples/git-generator-files-discovery/cluster-config/**/config.json"
      values:
        base_dir: "{{index .path.segments 0}}/{{index .path.segments 1}}/{{index .path.segments 2}}"
  template:
    metadata:
      name: '{{.cluster.name}}-guestbook'
    spec:
      project: default
      source:
        repoURL: https://github.com/argoproj/argo-cd.git
        targetRevision: HEAD
        path: "{{.values.base_dir}}/apps/guestbook"
      destination:
        server: '{{.cluster.address}}'
        namespace: guestbook
```

> [!NOTE]
> The `values.` prefix is always prepended to values provided via `generators.git.values` field. Ensure you include this prefix in the parameter name within the `template` when using it.

In `values` we can also interpolate all fields set by the git files generator as mentioned above.

## Git Polling Interval

When using a Git generator, the ApplicationSet controller polls Git
repositories, by default, every 3 minutes to detect changes, unless
different default value is set by the
`ARGOCD_APPLICATIONSET_CONTROLLER_REQUEUE_AFTER` environment variable.
You can customize this interval per ApplicationSet using
`requeueAfterSeconds`.

> [!NOTE]
> The Git generator uses the ArgoCD Repo Server to retrieve file
> and directory lists from Git. Therefore, the Git generator is
> affected by the Repo Server's Revision Cache Expiration setting
> (see the description of the `timeout.reconciliation` parameter in
> [argocd-cm.yaml](../examples/argocd-cm.yaml/#:~:text=timeout.reconciliation%3A)).
> If this value exceeds the configured Git Polling Interval, the
> Git generator might not see files or directories from new commits
> until the previous cache entry expires.
> 
## The `argocd.argoproj.io/application-set-refresh` Annotation

Setting the `argocd.argoproj.io/application-set-refresh` annotation
(to any value) triggers an ApplicationSet refresh. This annotation
forces the Git provider to resolve Git references directly, bypassing
the Revision Cache. The ApplicationSet controller removes this
annotation after reconciliation.

## Webhook Configuration

To eliminate the polling delay, the ApplicationSet webhook
server can be configured to receive webhook events. ApplicationSet
supports Git webhook notifications from GitHub and GitLab. The
following explains how to configure a Git webhook for GitHub, but the
same process should be applicable to other providers.

```yaml
apiVersion: argoproj.io/v1alpha1
kind: ApplicationSet
metadata:
  name: guestbook
  namespace: argocd
spec:
  goTemplate: true
  goTemplateOptions: ["missingkey=error"]
  generators:
  - git:
      # When using a Git generator, the ApplicationSet controller polls every `requeueAfterSeconds` interval (defaulting to every 3 minutes) to detect changes.
      requeueAfterSeconds: 180
      repoURL: https://github.com/argoproj/argo-cd.git
      revision: HEAD
      # ...
```

> [!NOTE]
> The ApplicationSet controller webhook does not use the same [API server webhook](../webhook.md). ApplicationSet exposes a webhook server as a service of type ClusterIP. An ApplicationSet specific Ingress resource needs to be created to expose this service to the webhook source.

### 1. Create the webhook in the Git provider

In your Git provider, navigate to the settings page where webhooks can be configured. The payload
URL configured in the Git provider should use the `/api/webhook` endpoint of your ApplicationSet instance
(e.g. `https://applicationset.example.com/api/webhook`). If you wish to use a shared secret, input an
arbitrary value in the secret. This value will be used when configuring the webhook in the next step.

![Add Webhook](../../assets/applicationset/webhook-config.png "Add Webhook")

> [!NOTE]
> When creating the webhook in GitHub, the "Content type" needs to be set to "application/json". The default value "application/x-www-form-urlencoded" is not supported by the library used to handle the hooks

### 2. Configure ApplicationSet with the webhook secret (Optional)

Configuring a webhook shared secret is optional, since ApplicationSet will still refresh applications
generated by Git generators, even with unauthenticated webhook events. This is safe to do since
the contents of webhook payloads are considered untrusted, and will only result in a refresh of the
application (a process which already occurs at three-minute intervals). If ApplicationSet is publicly
accessible, then configuring a webhook secret is recommended to prevent a DDoS attack.

In the `argocd-secret` Kubernetes secret, include the Git provider's webhook secret configured in step 1.

Edit the Argo CD Kubernetes secret:

```bash
kubectl edit secret argocd-secret -n argocd
```

TIP: for ease of entering secrets, Kubernetes supports inputting secrets in the `stringData` field,
which saves you the trouble of base64 encoding the values and copying it to the `data` field.
Simply copy the shared webhook secret created in step 1, to the corresponding
GitHub/GitLab/BitBucket key under the `stringData` field:

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: argocd-secret
  namespace: argocd
type: Opaque
data:
...

stringData:
  # github webhook secret
  webhook.github.secret: shhhh! it's a github secret

  # gitlab webhook secret
  webhook.gitlab.secret: shhhh! it's a gitlab secret
```

After saving, please restart the ApplicationSet pod for the changes to take effect.

## Repository credentials for ApplicationSets
If your [ApplicationSets](index.md) uses a repository where you need credentials to be able to access it _and_ if the
ApplicationSet project field is templated (i.e. the `project` field of the ApplicationSet contains `{{ ... }}`), you need to add the repository as a "non project scoped" repository.  
- When doing that through the UI, set this to a **blank** value in the dropdown menu.
- When doing that through the CLI, make sure you **DO NOT** supply the parameter `--project` ([argocd repo add docs](../../user-guide/commands/argocd_repo_add.md))
- When doing that declaratively, make sure you **DO NOT** have `project:` defined under `stringData:` ([complete yaml example](../examples/argocd-repositories.yaml))
