# Installation

* Argo CD
  * types of installations
    * [multi-tenant](/manifests/README.md#multi-tenant)
    * [core](/manifests/README.md#core)
  * [ways to install](#ways-to-install-)

## ways to install 
### -- via -- `kubectl`
* [here](/manifests/README.md)

### -- via -- Kustomize

* recommendations
  * include the manifest -- as a -- remote resource
  * apply ADDITIONAL customizations -- via -- Kustomize patches

* if you want to customize the default namespace ("argocd") -> apply a patch
  * Reason:🧠| `ClusterRoleBinding`, namespace hardcoded to "argocd" (default one)🧠
    * _Example:_ [here](/manifests/install.yaml)'s `kind: ClusterRoleBinding`'s `subjects[*].namespace`

* _Example:_ [kustomization.yaml](https://github.com/argoproj/argoproj-deployments/blob/master/argocd/kustomization.yaml)
  * deploy the [Argoproj CI/CD infrastructure demo](https://cd.apps.argoproj.io/applications/argocd/argo-cd?view=tree&resource=)

### -- via -- Helm

* [Helm chart](https://github.com/argoproj/argo-helm/tree/main/charts/argo-cd)

## Supported versions

* [here](../developer-guide/release-process-and-cadence.md)

## Tested versions

* Argo CD versions & Kubernetes versions table
  * [here](/docs/operator-manual/tested-kubernetes-versions.md)
