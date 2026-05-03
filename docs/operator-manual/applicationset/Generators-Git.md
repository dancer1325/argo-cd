# Git Generator

* [data structure](/manifests/crds/applicationset-crd.yaml)'s `spec.generators[*].git`

* 👀's subtypes👀
  * [Git generator: directory](#git-generator-directories----gitdirectories---)
  * [Git generator: file](#git-generator-files)

* the MOST flexible/powerful of the generators

* Git generator / `spec.template.spec.project` specified
  * ❌does NOT support [Signature Verification](../../user-guide/gpg-verification.md)❌
  * use ["non-scoped" repositories](#repository-credentials)

## Git Generator: Directories -- `.git.directories` --

* generates parameters -- based on -- specified repository's directory structure
  * built-in parameters
    * `{{.path.path}}`
      * == directory path / match | Git repository
    * `{{index .path.segments n}}`
      * == directory path | Git repository / split | array elements
    * `{{.path.basename}}`
      * == `path`'s right-most path
        * _Example:_ if `.path` == /one/two/three/four ->  `.path.basename` == four
    * `{{.path.basenameNormalized}}`
      * == `.path.basename` / unsupported characters are replaced -- with -- `-`
        * _Example:_
          * if `path` == `/directory/directory_2` -> would produce `directory-2`
          * if `.path.basename` == `directory_2` -> would produce `directory-2`

* ⚠️if you specify `.git.pathParamPrefix` -> `<.git.pathParamPrefix_VALUE>.path.<path_parameter>`⚠️
  * == 
    * `path.path` -> `<.git.pathParamPrefix_VALUE>.path.path`
    * `path.basename` -> `<.git.pathParamPrefix_VALUE>.path.basename`
    * `path.basenameNormalized` -> `<.git.pathParamPrefix_VALUE>.path.basenameNormalized`
  * uses
    * | Matrix generator
      * Reason:🧠BOTH child generators are Git generators -> | merge child generators’ items, you can avoid conflicts🧠 

* | add a NEW Helm chart/Kustomize YAML/Application/plain subdirectory | Git repository, ApplicationSet controller 
  * detect this change
  * AUTOMATICALLY deploy the resulting manifests | NEW `Application` resources

* `generators[git].directories[].path`
  * if you want to specify -> you can use [path.Match](https://golang.org/pkg/path/#Match)

### Exclude directories -- `generators[git].directories[].exclude:true` --
 
* by default, exclude directories / begin with `.`

* 's priority > include rules

* order |  `generators[git].directories[]`
  * ❌NOT matter❌

### Root Of Git Repo 

* `spec.generators[git].directories[*].path: '*'`

### `values`

* allows
  * passing ADDITIONAL string key-value pairs
* how to use?
  * `values.(DEFINED_VALUES_KEY)`

## Git Generator: Files

* generates parameters -- based on -- contents of JSON/YAML files | specified repository
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

### `values`

* allows
  * passing ADDITIONAL string key-value pairs
* how to use?
  * `values.(DEFINED_VALUES_KEY)`

## Git Polling Interval

* polling interval -- by -- ApplicationSet Controller
  * == 💡poll generators💡
    * ❌!= [poll Applications](/docs/faq.md#how-often-does-argo-cd-check-for-changes--git-or-helm-repository-)❌
  * ways to configure
    * `ARGOCD_APPLICATIONSET_CONTROLLER_REQUEUE_AFTER` environment variable
      * [source code](/manifests/base/applicationset-controller/argocd-applicationset-controller-deployment.yaml)
      * -> ALL ApplicationSet
      * got -- from -- `applicationsetcontroller.requeue.after` | "argocd-cmd-params-cm" ConfigMap
    * `spec.generators[git].requeueAfterSeconds` / EACH ApplicationSet
      * 's priority > `ARGOCD_APPLICATIONSET_CONTROLLER_REQUEUE_AFTER`'s priority

* Git generator
  * ⚠️depends on the ArgoCD Repo Server's Revision Cache Expiration setting⚠️
    * [`--revision-cache-expiration` flag](/reposerver/cache/cache.go)
      * got it -- from -- `ARGOCD_RECONCILIATION_TIMEOUT` environment variable
        * by default, 3m
        * == `timeout.reconciliation` | ["argocd-cm.yaml"](../examples/argocd-cm.yaml)
    * ❌if Revision Cache Expiration > ApplicationSet Controller Polling Interval -> Git generator does NOT see NEW commits | files OR directories❌

## The `argocd.argoproj.io/application-set-refresh` Annotation

TODO: 
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

## Repository credentials

TODO: 
If your [ApplicationSets](index.md) uses a repository where you need credentials to be able to access it _and_ if the
ApplicationSet project field is templated (i.e. the `project` field of the ApplicationSet contains `{{ ... }}`), you need to add the repository as a "non project scoped" repository.  
- When doing that through the UI, set this to a **blank** value in the dropdown menu.
- When doing that through the CLI, make sure you **DO NOT** supply the parameter `--project` ([argocd repo add docs](../../user-guide/commands/argocd_repo_add.md))
- When doing that declaratively, make sure you **DO NOT** have `project:` defined under `stringData:` ([complete yaml example](../examples/argocd-repositories.yaml))
