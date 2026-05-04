# Helm

* Argo CD 
  * ⭐️ONLY uses Helm -- , through `helm template`, to -- [inflate charts](../faq.md#after-deploying-my-helm-application----with----argo-cd-i-can-not-see-it----through----helm-ls-or-other-helm-commands)⭐️
    * -> (application / helm-based) 's lifecycle
      * ⭐️handled -- by -- Argo CD⭐️
      * ❌NOT handled -- by -- Helm❌

* [data structure / helm-related](/manifests/crds/application-crd.yaml)'s `spec.source.helm`

## Values Files

* | [Application](/manifests/crds/application-crd.yaml),
  * 💡`spec.source.helm.valueFiles`💡
    * == relative path -- to -- `spec.source.repoURL` 
      * | Argo CD v2.6+,
        * git repository | values files (can be) != git repository | Helm chart
          * Reason:🧠thanks -- to -- [multiple sources for Applications](./multiple_sources.md#helm-value-files----from----external-git-repository)🧠
    * ⚠️requirements⚠️
      * | Argo CD v2.6-,
        * git repository | values files (MUST be) == git repository | Helm chart

* ways to specify
  * declaratively
  * `argocd <SOME_COMMAND> --values <RELATIVE_PATH_TO_SOURECE_REPO>` 
    * == Helm CLI command option
      * _Example:_ `helm someCommand --values file1 --values file2 ...`

* if you specify a value file / NO exist -> it fails
  * | template expansion, it errors "Missing"
  * if you want to skip this error -> set `--ignore-missing-value-files: true`

## Values

* `spec.source.helm.valuesObject`
  * == Helm values / passed -- to -- Helm template  
    * defined -- as a -- map
  * ways to specify
    * declaratively
  * 's priority > `spec.source.helm.values`'s priority

* `spec.source.helm.values`
  * == Helm values / passed -- to -- Helm template
    * defined -- as -- a string

## Helm Parameters

* == [parameters / exposed | Helm chart](https://helm.sh/docs/helm/helm_template/#options)
  * allows
    * override values / defined | "values.yaml"
  * uses
    * | manifest generation, -- by -- `helm template`
  * _Example:_ `helm template . --set service.type=LoadBalancer`


* `spec.source.helm.parameters`
  * ways to specify
    * declaratively
    * `argocd app set <ARGO_CD_APPLICATION_NAME> -p <PARAMETER_KEY>=<PARAMETER_VALUE>`

## Helm Value Precedence

Values injections have the following order of precedence
 `parameters > valuesObject > values > valueFiles > helm repository values.yaml`
 Or rather

```
    lowest  -> valueFiles
            -> values
            -> valuesObject
    highest -> parameters
```

So valuesObject trumps values - therefore values will be ignored, and both valuesObject and values trump valueFiles.
Parameters trump all of them.

Precedence of multiple valueFiles:
When multiple valueFiles are specified, the last file listed has the highest precedence:

```
valueFiles:
  - values-file-2.yaml
  - values-file-1.yaml

In this case, values-file-1.yaml will override values from values-file-2.yaml.
```

When multiple of the same key are found the last one wins i.e 

```
e.g. if we only have values-file-1.yaml and it contains

param1: value1
param1: value3000

we get param1=value3000
```

```
parameters:
  - name: "param1"
    value: value2
  - name: "param1"
    value: value1

the result will be param1=value1
```

```
values: |
  param1: value2
  param1: value5

the result will be param1=value5
```

> [!NOTE]
> **When valueFiles or values is used**
>
> The chart is rendered correctly using the set of values from the different possible sources plus any parameters, merged in the expected order as documented here.
> There is a bug (see [this issue](https://github.com/argoproj/argo-cd/issues/9213)) in the UI that only shows the parameters, i.e. it does not represent the complete set of values.
> As a workaround, using parameters instead of values/valuesObject will provide a better overview of what will be used for resources.

## Helm --set-file support

The `--set-file` argument to helm can be used with the following syntax on
the cli:

```bash
argocd app set helm-guestbook --helm-set-file some.key=path/to/file.ext
```

or using the fileParameters for yaml:

```yaml
source:
  helm:
    fileParameters:
      - name: some.key
        path: path/to/file.ext
```

## Helm Release Name

* `spec.source.helm.releaseName`
  * by default, == Application name / it belongs
  * ways to specify 
    * declaratively
    * `argocd app set <ARGO_CD_APPLICATION_NAME> --release-name <SPECIFY_RELEASE_NAME>` 

* use cases
  * centralised Argo CD
    * Reason:🧠OTHERWISE, it's the default one🧠
 
* recommendations
  * ⚠️if the chart / you are deploying is using the `app.kubernetes.io/instance` label -> NOT specify it⚠️
    * Reason:🧠it might cause some selectors | resources, stop working🧠
    * SOLUTION: configure | [ArgoCD configmap "argocd-cm.yaml"](../operator-manual/examples/argocd-cm.yaml), `application.instanceLabelKey`

## Helm Hooks

Helm hooks are similar to [Argo CD hooks](resource_hooks.md)
* In Helm, a hook
is any normal Kubernetes resource annotated with the `helm.sh/hook` annotation.

Argo CD supports many (most?) Helm hooks by mapping the Helm annotations onto Argo CD's own hook annotations:

| Helm Annotation                 | Notes                                                                                         |
| ------------------------------- |-----------------------------------------------------------------------------------------------|
| `helm.sh/hook: crd-install`     | Supported as equivalent to normal Argo CD CRD handling.                                |
| `helm.sh/hook: pre-delete`      | Supported as equivalent to `argocd.argoproj.io/hook: PreDelete`                               |
| `helm.sh/hook: pre-rollback`    | Not supported. Never used in Helm stable.                                                     |
| `helm.sh/hook: pre-install`     | Supported as equivalent to `argocd.argoproj.io/hook: PreSync`.                                |
| `helm.sh/hook: pre-upgrade`     | Supported as equivalent to `argocd.argoproj.io/hook: PreSync`.                                |
| `helm.sh/hook: post-upgrade`    | Supported as equivalent to `argocd.argoproj.io/hook: PostSync`.                               |
| `helm.sh/hook: post-install`    | Supported as equivalent to `argocd.argoproj.io/hook: PostSync`.                               |
| `helm.sh/hook: post-delete`     | Supported as equivalent to `argocd.argoproj.io/hook: PostDelete`.                             |
| `helm.sh/hook: post-rollback`   | Not supported. Never used in Helm stable.                                                     |
| `helm.sh/hook: test-success`    | Not supported. No equivalent in Argo CD.                                                      |
| `helm.sh/hook: test-failure`    | Not supported. No equivalent in Argo CD.                                                      |
| `helm.sh/hook-delete-policy`    | Supported. See also `argocd.argoproj.io/hook-delete-policy`).                                 |
| `helm.sh/hook-delete-timeout`   | Not supported. Never used in Helm stable                                                      |
| `helm.sh/hook-weight`           | Supported as equivalent to `argocd.argoproj.io/sync-wave`.                                    |
| `helm.sh/resource-policy: keep` | Supported as equivalent to `argocd.argoproj.io/sync-options: Delete=false`.                   |

Unsupported hooks are ignored. In Argo CD, hooks are created by using `kubectl apply`, rather than `kubectl create`. This means that if the hook is named and already exists, it will not change unless you have annotated it with `before-hook-creation`.

> [!WARNING]
> **Helm hooks + ArgoCD hooks**
>
> If you define any Argo CD hooks, _all_ Helm hooks will be ignored.   

> [!WARNING]
> **'install' vs 'upgrade' vs 'sync'**
>
> Argo CD cannot know if it is running a first-time "install" or an "upgrade" - every operation is a "sync'. This means that, by default, apps that have `pre-install` and `pre-upgrade` will have those hooks run at the same time.

### Hook Tips

* Make your hook idempotent.
* Annotate  `pre-install` and `post-install` with `hook-weight: "-1"`. This will make sure it runs to success before any upgrade hooks.
* Annotate `pre-upgrade` and `post-upgrade` with `hook-delete-policy: before-hook-creation` to make sure it runs on every sync.

Read more about [Argo hooks](resource_hooks.md) and [Helm hooks](https://helm.sh/docs/topics/charts_hooks/).

## Random Data

Helm templating has the ability to generate random data during chart rendering via the
`randAlphaNum` function. Many helm charts from the [charts repository](https://github.com/helm/charts)
make use of this feature. For example, the following is the secret for the
[redis helm chart](https://github.com/helm/charts/blob/master/stable/redis/templates/secret.yaml):

```yaml
data:
  {{- if .Values.password }}
  redis-password: {{ .Values.password | b64enc | quote }}
  {{- else }}
  redis-password: {{ randAlphaNum 10 | b64enc | quote }}
  {{- end }}
```

The Argo CD application controller periodically compares Git state against the live state, running
the `helm template <CHART>` command to generate the helm manifests. Because the random value is
regenerated every time the comparison is made, any application which makes use of the `randAlphaNum`
function will always be in an `OutOfSync` state. This can be mitigated by explicitly setting a
value in the values.yaml or using `argocd app set` command to override the value such that the value
is stable between each comparison. For example:

```bash
argocd app set redis -p password=abc123
```

## Build Environment

Helm apps have access to the [standard build environment](build-environment.md) via substitution as parameters.

E.g. via the CLI:

```bash
argocd app create APPNAME \
  --helm-set-string 'app=${ARGOCD_APP_NAME}'
```

Or via declarative syntax:

```yaml
  spec:
    source:
      helm:
        parameters:
        - name: app
          value: $ARGOCD_APP_NAME
```

It's also possible to use build environment variables for the Helm values file path:

```yaml
  spec:
    source:
      helm:
        valueFiles:
        - values.yaml
        - myprotocol://somepath/$ARGOCD_APP_NAME/$ARGOCD_APP_REVISION
```

## Helm plugins

Argo CD is un-opinionated on what cloud provider you use and what kind of Helm plugins you are using, that's why there are no plugins delivered with the ArgoCD image.

But sometimes you want to use a custom plugin. Perhaps you would like to use Google Cloud Storage or Amazon S3 storage to save the Helm charts, for example: https://github.com/hayorov/helm-gcs where you can use `gs://` protocol for Helm chart repository access.
There are two ways to install custom plugins; you can modify the ArgoCD container image, or you can use a Kubernetes `initContainer`.

### Modifying the ArgoCD container image

One way to use this plugin is to prepare your own ArgoCD image where it is included.

Example `Dockerfile`:

```dockerfile
FROM argoproj/argocd:v1.5.7

USER root
RUN apt-get update && \
    apt-get install -y \
        curl && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

USER argocd

ARG GCS_PLUGIN_VERSION="0.3.5"
ARG GCS_PLUGIN_REPO="https://github.com/hayorov/helm-gcs.git"

RUN helm plugin install ${GCS_PLUGIN_REPO} --version ${GCS_PLUGIN_VERSION}

ENV HELM_PLUGINS="/home/argocd/.local/share/helm/plugins/"
```

The `HELM_PLUGINS` environment property required for ArgoCD to locate plugins correctly.

Once built, use the custom image for ArgoCD installation.

### Using `initContainers`

Another option is to install Helm plugins via Kubernetes `initContainers`.
Some users find this pattern preferable to maintaining their own version of the ArgoCD container image.

Below is an example of how to add Helm plugins when installing ArgoCD with the [official ArgoCD helm chart](https://github.com/argoproj/argo-helm/tree/master/charts/argo-cd):

```yaml
repoServer:
  volumes:
    - name: gcp-credentials
      secret:
        secretName: my-gcp-credentials
  volumeMounts:
    - name: gcp-credentials
      mountPath: /gcp
  env:
    - name: HELM_CACHE_HOME
      value: /helm-working-dir
    - name: HELM_CONFIG_HOME
      value: /helm-working-dir
    - name: HELM_DATA_HOME
      value: /helm-working-dir
  initContainers:
    - name: helm-gcp-authentication
      image: alpine/helm:3.16.1
      volumeMounts:
        - name: helm-working-dir
          mountPath: /helm-working-dir
        - name: gcp-credentials
          mountPath: /gcp
      env:
        - name: HELM_CACHE_HOME
          value: /helm-working-dir
        - name: HELM_CONFIG_HOME
          value: /helm-working-dir
        - name: HELM_DATA_HOME
          value: /helm-working-dir
      command: [ "/bin/sh", "-c" ]
      args:
        - apk --no-cache add curl;
          helm plugin install https://github.com/hayorov/helm-gcs.git;
          helm repo add my-gcs-repo gs://my-private-helm-gcs-repository;
          chmod -R 777 $HELM_DATA_HOME;
```

## Helm Version

Argo CD will assume that the Helm chart is v3 (even if the apiVersion field in the chart is Helm v2), unless v2 is explicitly specified within the Argo CD Application (see below).

If needed, it is possible to specifically set the Helm version to template with by setting the `helm-version` flag on the cli (either v2 or v3):

```bash
argocd app set helm-guestbook --helm-version v3
```

Or using declarative syntax:

```yaml
spec:
  source:
    helm:
      version: v3
```

## Helm `--pass-credentials`

Helm, [starting with v3.6.1](https://github.com/helm/helm/releases/tag/v3.6.1),
prevents sending repository credentials to download charts that are being served
from a different domain than the repository.

If needed, it is possible to opt into passing credentials for all domains by setting the `helm-pass-credentials` flag on the cli:

```bash
argocd app set helm-guestbook --helm-pass-credentials
```

Or using declarative syntax:

```yaml
spec:
  source:
    helm:
      passCredentials: true
```

## Helm `--skip-crds`

Helm installs custom resource definitions in the `crds` folder by default if they are not existing. 
See the [CRD best practices](https://helm.sh/docs/chart_best_practices/custom_resource_definitions/) for details.

If needed, it is possible to skip the CRD installation step with the `helm-skip-crds` flag on the cli:

```bash
argocd app set helm-guestbook --helm-skip-crds
```

Or using declarative syntax:

```yaml
spec:
  source:
    helm:
      skipCrds: true
```

## Helm `--skip-schema-validation`

Helm validates the values.yaml file using a values.schema.json file. See [Schema files](https://helm.sh/docs/topics/charts/#schema-files) for details.

If needed, it is possible to skip the schema validation step with the `helm-skip-schema-validation` flag on the cli:

```bash
argocd app set helm-guestbook --helm-skip-schema-validation
```

Or using declarative syntax:

```yaml
spec:
  source:
    helm:
      skipSchemaValidation: true
```


## Helm `--skip-tests`

By default, Helm includes test manifests when rendering templates. Argo CD currently skips manifests that include hooks not supported by Argo CD, including [Helm test hooks](https://helm.sh/docs/topics/chart_tests/). While this feature covers many testing use cases, it is not totally congruent with --skip-tests, so the --skip-tests option can be used.

If needed, it is possible to skip the test manifests installation step with the `helm-skip-tests` flag on the cli:

```bash
argocd app set helm-guestbook --helm-skip-tests
```

Or using declarative syntax:

```yaml
spec:
  source:
    helm:
      skipTests: true # or false
```
