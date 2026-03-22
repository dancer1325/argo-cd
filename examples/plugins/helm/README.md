# Simple Helm plugin

* TODO: The directory path to the shell scripts will need to be updated based on how you mount them
into the sidecar.

## how to install?

```shell
kustomize build examples/plugins/helm/ | kubectl apply -n argocd -f -
```
