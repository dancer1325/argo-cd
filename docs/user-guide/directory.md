# Directory

* directory-type application
  * == 👀[way to define Kubernetes manifests / supported by ArgoCD](application_sources.md)👀
  * loads plain manifest files -- from -- 
    * ".yml"
    * ".yaml"
    * ".json"
  * ways to be created
    * -- via -- UI
    * -- via -- CLI
    * declaratively
  * `spec.source.directory`
    * ⚠️OPTIONAL⚠️
      * EXCEPT TO: add ADDITIONAL configuration options
      * == 👀Argo CD AUTOMATICALLY detect the application source type👀

## Enabling Recursive Resource Detection

* directory applications
  * by default,
    * ONLY include the files | root of the configured repository/path
  * 👀if you want to enable recursive resource detection👀 
    * -> set
      * -- via -- CL
        * `--directory-recurse`
          * _Example:_ `argocd app set APP_NAME --directory-recurse` 
      * -- via -- declaratively
        * `spec.source.directory.recurse`
    * ONLY ALLOWED | directory types
    * ❌NOT ALLOWED | Kustomize, Helm, or Jsonnet ❌
      * otherwise, fail 

## Including/Excluding Files

### Including ONLY certain Files

* ways
  * -- via -- CL
    * `--directory-include "GlobPattern"` OR `--directory-include "{GlobPattern1,GlobPattern2,...}"` 
      * _Examples:_ 
        * `argocd app set guestbook --directory-include "*.yaml"`
        * `argocd app set guestbook --directory-include "{*.yml,*.yaml}"`
  * -- via -- declaratively
    * `spec.source.directory.include: 'GlobPattern'`

### Excluding Certain Files

TODO: 
It is possible to exclude files matching a pattern from directory applications
* For example, in a repository containing
some manifests and also a non-manifest YAML file, you could exclude the config file like this:

```shell
argocd app set guestbook --directory-exclude "config.yaml"
```

It is possible to exclude more than one pattern
* For example, a config file and an irrelevant directory:

```shell
argocd app set guestbook --directory-exclude "{config.yaml,env-use2/*}"
```

If both `include` and `exclude` are specified, then the Application will include all files which match the `include`
pattern and do not match the `exclude` pattern
* For example, consider this source repository:

```
config.json
deployment.yaml
env-use2/
  configmap.yaml
env-usw2/
  configmap.yaml
```

To exclude `config.json` and the `env-usw2` directory, you could use this combination of patterns:

```shell
argocd app set guestbook --directory-include "*.yaml" --directory-exclude "{config.json,env-usw2/*}"
```

This would be the declarative syntax:

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
spec:
  source:
    directory:
      exclude: '{config.json,env-usw2/*}'
      include: '*.yaml'
```

### Skipping File Rendering

In some cases, repositories may contain YAML files that resemble Kubernetes manifests because they include fields like `apiVersion`, `kind`, and `metadata`, but are not intended to be rendered or applied as actual Kubernetes resources
* Examples include Helm `values.yaml` files or configuration snippets used by CI/CD pipelines.

To prevent Argo CD from attempting to parse these files as manifests (which could result in errors), you can explicitly mark them to be skipped using a special comment directive:

```yaml
# +argocd:skip-file-rendering
```

When this comment is present anywhere in the file, Argo CD will ignore the file during manifest processing
* This allows for safe coexistence of Kubernetes-like files that are not actual manifests.

#### Example

```yaml
# +argocd:skip-file-rendering
apiVersion: v1
kind: ConfigMap
metadata:
  name: example
data:
  not-actually: a-manifest
```

