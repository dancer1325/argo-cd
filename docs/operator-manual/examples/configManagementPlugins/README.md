# TODO:

# how to install a config management plugin?
* [MORE EXAMPLES](/examples/plugins/helm)
## -- as -- sidecar plugin to repo-server
### write the plugin configuration file
* [here](configManagementPlugin.yaml)
### place the plugin configuration file | sidecar
#### | "argocd-repo-server" deployment's sidecar container, set `spec.template.spec.containers[0].volumeMounts[*].mountPath: /home/argocd/cmp-server/config/plugin.yaml`
* [here](repo-server-patch.yaml)
#### if you use a
##### custom image for the sidecar -> add the file directly | that image
* [dockerfile](Dockerfile)
* [repo-server-patch-custom-image.yaml](repo-server-patch-custom-image.yaml)
* steps
  * TODO: docker build
##### stock image for the sidecar OR rather maintain the plugin configuration | ConfigMap -> NEST the plugin config file | ConfigMap's `plugin.yaml` key
* [here](repo-server-patch.yaml)
* TODO: use [configMapNestingPluginConfigFile.yaml](configMapNestingPluginConfigFile.yaml)
### register the plugin sidecar | argocd-repo-server
#### | "argocd-repo-server" deployment's sidecar container, set `spec.template.spec.containers[0].command: [/var/run/argocd/argocd-cmp-server]`
* [here](repo-server-patch.yaml)
#### argocd-cmp-server
##### == GRPC service
* [here](/cmpserver/server.go)

# how to use a config management plugin | Application?
## ⚠️ONLY 1! POSSIBLE CMP / EACH Application⚠️
* [Application's `spec.source.plugin`](/manifests/crds/application-crd.yaml)
  * ONLY POSSIBLE 1
## 

# TODO:

# how to migrate argocd-cm plugins -- to -- sidecar plugins?
## convert the "argocd-cm" ConfigMap entry `data.configManagementPlugins` -- into a -- `ConfigManagementPlugin` manifest
* ["argocd-cm" ConfigMap / contains entry `data.configManagementPlugins`](argocdcmConfigMapWithConfigManagementPlugin.yaml)
* [converted `ConfigManagementPlugin` manifest](configManagementPluginMigratedFromArgoCDCM.yaml)

