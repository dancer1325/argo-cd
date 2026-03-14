# Installation

* Argo CD
  * types of installations
    * [multi-tenant](/manifests/README.md#multi-tenant)
    * [core](/manifests/README.md#core)

## Kustomize

TODO; 
The Argo CD manifests can also be installed using Kustomize
* It is recommended to include the manifest as a remote resource and apply additional customizations
using Kustomize patches.


```yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

namespace: argocd
resources:
- https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
```

For an example of this, see the [kustomization.yaml](https://github.com/argoproj/argoproj-deployments/blob/master/argocd/kustomization.yaml)
used to deploy the [Argoproj CI/CD infrastructure](https://github.com/argoproj/argoproj-deployments#argoproj-deployments).

#### Installing Argo CD in a Custom Namespace
If you want to install Argo CD in a namespace other than the default argocd, you can use Kustomize to apply a patch that updates the ClusterRoleBinding to reference the correct namespace for the ServiceAccount
* This ensures that the necessary permissions are correctly set in your custom namespace.

Below is an example of how to configure your kustomization.yaml to install Argo CD in a custom namespace:
```yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

namespace: <your-custom-namespace>
resources:
  - https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml


patches:
  - patch: |-
      - op: replace
        path: /subjects/0/namespace
        value: <your-custom-namespace>
    target:
      kind: ClusterRoleBinding
```

This patch ensures that the ClusterRoleBinding correctly maps to the ServiceAccount in your custom namespace, preventing any permission-related issues during the deployment.

## Helm

The Argo CD can be installed using [Helm](https://helm.sh/)
* The Helm chart is currently community maintained and available at
[argo-helm/charts/argo-cd](https://github.com/argoproj/argo-helm/tree/main/charts/argo-cd).

## Supported versions

For detailed information regarding Argo CD's version support policy, please refer to the [Release Process and Cadence documentation](../developer-guide/release-process-and-cadence.md).

## Tested versions

The following table shows the versions of Kubernetes that are tested with each version of Argo CD.

{!docs/operator-manual/tested-kubernetes-versions.md!}
