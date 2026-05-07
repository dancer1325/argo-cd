# Custom Tooling

* goal
  * customize Kubernetes manifest templating tools

* Argo CD
  * Argo CD repo-server
    * [responsible -- for -- generating Kubernetes manifests](architecture.md)
  * about supported templating tools (helm, kustomize, ks, jsonnet)
    * 👀bundled PREFERRED versions 👀
      * == -- as part of -- Argo CD container images
    * 💡if you want a specific version -> customize Argo CD repo-server💡
      * use cases
        * upgrade/downgrade -- to a -- specific version
          * _ExampleS:_ bugs OR bug fixes
        * install 
          * ADDITIONAL dependencies / used -- by -- kustomize's configmap/secret generators (_Examples:_ curl, vault, gpg, AWS CLI)
          * [config management plugin](config-management-plugins.md)
      * ways
        * [add tools -- via -- volume mounts](#adding-tools----via----volume-mounts)
        * [build your own image](#byoi-build-your-own-image) 

## adding tools -- via -- volume mounts

* approach: | [Argo CD Reposerver `Deployment`](/manifests/base/repo-server/argocd-repo-server-deployment.yaml)
  * add `initContainers` + `volumeMount`
    * copy a DIFFERENT version of a tool | repo-server container

## BYOI (Build Your Own Image)

* approach: build ENTIRELY CUSTOMIZED Argo CD Reposerver

* use cases
  * you need to install OTHER dependencies
    * ❌replace a binary is NOT sufficient❌
