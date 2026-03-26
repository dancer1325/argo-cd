# Installation

* Argo CD
  * types of installations
    * [multi-tenant](/manifests/README.md#multi-tenant)
    * [core](/manifests/README.md#core)

## Tools -- to -- install it
### Kustomize

* recommendations
  * include the manifest -- as a -- remote resource
  * apply ADDITIONAL customizations -- via -- Kustomize patches

* _Example:_ [kustomization.yaml](https://github.com/argoproj/argoproj-deployments/blob/master/argocd/kustomization.yaml)
  * deploy the [Argoproj CI/CD infrastructure](https://github.com/argoproj/argoproj-deployments#argoproj-deployments)

#### | CUSTOM namespace

* steps
  * apply a patch / updates the `ClusterRoleBinding`
    * Reason:🧠| `ClusterRoleBinding`, namespace hardcoded to "argocd" (default one)🧠
      * _Example:_ [here](/manifests/install.yaml)'s `kind: ClusterRoleBinding`'s `subjects[*].namespace`

### Helm

* [Helm chart](https://github.com/argoproj/argo-helm/tree/main/charts/argo-cd)

## Supported versions

* [here](../developer-guide/release-process-and-cadence.md)

## Tested versions

* Argo CD versions & Kubernetes versions table

* [here](/docs/operator-manual/tested-kubernetes-versions.md)
