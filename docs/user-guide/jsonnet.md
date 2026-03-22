# Jsonnet

* Jsonnet
  * Jsonnet file
    * == "*.jsonnet" | directory app 
  * can generate
    * object
    * array
* Argo CD 
  * evaluates the Jsonnet' output
  * parse  the Jsonnet' output

## Build Environment

* Jsonnet apps
  * can access -- , via substitution | *TLAs* & *external variables*, to the -- [standard build environment](build-environment.md)  

TODO: 
  It is also possible to add a shared library (e.g. `vendor` folder) relative to the repository root.

E.g. via the CLI:

```bash
argocd app create APPNAME \
  --jsonnet-ext-var-str 'app=${ARGOCD_APP_NAME}' \
  --jsonnet-tla-str 'ns=${ARGOCD_APP_NAMESPACE}' \
  --jsonnet-libs 'vendor'
```

Or by declarative syntax:

```yaml
  directory:
    jsonnet:
      extVars:
        - name: app
          value: $ARGOCD_APP_NAME
      tlas:
        - name: ns
          value: $ARGOCD_APP_NAMESPACE
      libs:
        - vendor
```
