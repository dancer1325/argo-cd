# Tools

## | production

* Argo CD
  * supports
    * 💡MULTIPLE ways to define Kubernetes manifests💡
      * [Kustomize](kustomize.md) applications
      * [Helm](helm.md) charts
      * [OCI](oci.md) images
      * directory of YAML + JSON + [Jsonnet](jsonnet.md) manifests
      * [custom config management tool](../operator-manual/config-management-plugins.md) / configured -- as a -- config management plugin
  * 💡[Application's `spec.source`](/manifests/crds/application-crd.yaml)💡
    * == specify application source

## | development

* Argo CD
  * supports
    * uploading DIRECTLY local manifests -- `argocd app sync APPNAME --local ...` -- 
      * ⚠️anti-pattern of the GitOps paradigm⚠️
        * ONLY ALLOWED | development
      * requirements
        * user / `override` permission
      * ALLOWED | [ANY way to define Kubernetes manifests](#-production)
