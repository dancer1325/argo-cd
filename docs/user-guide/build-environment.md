# Build Environment variables

* supported -- by -- 
  * [custom tools](../operator-manual/config-management-plugins.md)
  * [Helm](helm.md)
  * [Jsonnet](jsonnet.md)
  * [Kustomize](kustomize.md)

* AVAILABLE build environment variables

| Variable                            | Description                                              |
|-------------------------------------|----------------------------------------------------------|
| `ARGOCD_APP_NAME`                   | Argo CD Application name                                 |
| `ARGOCD_APP_NAMESPACE`              | Argo CD Application's destination namespace              |
| `ARGOCD_APP_PROJECT_NAME`           | project name / application belongs to                    |
| `ARGOCD_APP_REVISION`               | Argo CD Application resolved revision                    |
| `ARGOCD_APP_REVISION_SHORT`         | Argo CD Application resolved short revision              |
| `ARGOCD_APP_REVISION_SHORT_8`       | Argo CD Application resolved short revision / length = 8 |
| `ARGOCD_APP_SOURCE_PATH`            | Argo CD Application's path \| source repo                |
| `ARGOCD_APP_SOURCE_REPO_URL`        | Argo CD Application's source repo URL                    |
| `ARGOCD_APP_SOURCE_TARGET_REVISION` | Argo CD Application's source target revision (== \| spec) |
| `KUBE_VERSION`                      | Kubernetes semantic version / WITHOUT trailing metadata  |
| `KUBE_API_VERSIONS`                 | Kubernetes API version                                   |

* ❌if you do NOT want to interpolate a variable -> escape `$` == `$$`❌
