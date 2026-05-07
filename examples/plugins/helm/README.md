# Simple Helm plugin

## how to install?

* steps
  * | [plugin.yaml](plugin.yaml),
    * adjust the `<path>` -- based on -- where you mount the scripts | sidecar
  * `kustomize build examples/plugins/helm/ | kubectl apply -n argocd -f -`
    * TODO: check
