# Parameter Overrides

* goal
  * how to override the Argo CD applications' parameters -- based on -- [config management tools](application_sources.md)

* Argo CD applications' parameters
  * ⚠️anti-pattern to GitOps⚠️
    * Reason:🧠source of truth == Git repository + application overrides🧠
  * provides
    * 👀flexibility | configure k8s manifest👀
      * Reason:🧠
        * MOST of the application manifests defined | Git
        * SOME parts of the k8s manifests determined DYNAMICALLY🧠
  * allows
    * redeploying -- , by changing application parameters, -- Argo CD Application
  * use cases
    * dev/test environments / needs to be CONTINUALLY updated 
      * ⚠️requirements⚠️
        * declare a parameter / is exposed
      * | CI, 
        * `argocd app set APP_NAME -p EXPOSED_PARAMETER=NEW_VALUE`
    * use public Helm charts / you
      * do NOT want to fork
      * want to customize
  * 💡ways to set -- based on -- [config management tools](application_sources.md)💡
    * | Helm,
      * `-p key=value`
        * == `argocd app set APPNAME -p (COMPONENT=)PARAM=VALUE`
          * `PARAM`
            * == normal YAML path
    * | Kustomize,
      * `--kustomize-*`
        * == `argocd app set APPNAME --kustomize-* VALUE`
        * [`argocd app set`'s tool-specific flags](./commands/argocd_app_set.md)
    * | Jsonnet,
      * `--jsonnet-*`
        * == `argocd app set APPNAME --jsonnet-* VALUE`
        * [`argocd app set`'s tool-specific flags](./commands/argocd_app_set.md)

## | MULTI-Source Applications

* | [MULTIPLE sources](multiple_sources.md)
  * if you want to override 1 SPECIFIC source application -> use `--source-position` flag / >= 0

## store overrides | Git

* ".argocd-source.yaml" 
  * allows
    * | manifest generation, 
      * override application source fields `kustomize`, `helm` etc.
  * stored | Git repository -- of -- source application
  * use cases
    * unified way: 
      * "override" application parameters | Git +
      * enable the projects' "write back" feature
        * _Example:_ [argocd-image-updater](https://github.com/argoproj-labs/argocd-image-updater)
    * "discovering" applications | Git repository -- by -- projects
      * _Example:_ [applicationset](/applicationset)
      * [git files generator](/applicationset/examples/git-generator-files-discovery/git-generator-files.yaml)

* ".argocd-source-<appname>.yaml"
  * `<appname>` 
    * == application name | the overrides are valid for 
  * == application specific file
  * use cases
    * you are sourcing MULTIPLE applications -- from -- 1! path | your repository

* ".argocd-source-<namespace>_<appname>.yaml"
  * == ".argocd-source-<appname>.yaml" + [apps-in-any-namespace feature](../operator-manual/app-any-namespace.md)

* merging order
  * ".argocd-source.yaml" + ".argocd-source-<appname>.yaml" OR ".argocd-source-<namespace>_<appname>.yaml" 
    * == application-specific files' values override application-non-specific files' values
