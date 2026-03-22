# Custom Tooling

* goal
  * customize Kubernetes manifest templating tools

* Argo CD
  * Argo CD repo-server
    * responsible -- for -- generating Kubernetes manifests
  * about supported templating tools (helm, kustomize, ks, jsonnet)
    * 👀bundled PREFERRED versions 👀
      * == -- as part of -- Argo CD container images
    * 💡if you want a specific version -> customize Argo CD repo-server💡
      * POSSIBLE Reasons:🧠
        * upgrade/downgrade -- to a -- specific version
          * _ExampleS:_ bugs OR bug fixes
        * install 
          * ADDITIONAL dependencies / used -- by -- kustomize's configmap/secret generators (_Examples:_ curl, vault, gpg, AWS CLI)
          * [config management plugin](config-management-plugins.md)🧠
      * ways
        * [add tools -- via -- volume mounts](#adding-tools----via----volume-mounts)
        * [build your own image](#byoi-build-your-own-image) 

## Adding tools -- via -- volume mounts

* approach: | [Argo CD Reposerver `Deployment`](/manifests/base/repo-server/argocd-repo-server-deployment.yaml)
  * add `initContainers` + `volumeMount`
    * copy a DIFFERENT version of a tool | repo-server container

* _Example:_ init container overwrites the helm binary / 's version != helm binary / bundled | Argo CD

  ```yaml
      spec:
        # 1. Define an emptyDir volume / hold the custom binaries
        volumes:
        - name: custom-tools
          emptyDir: {}
        # 2. init container -- to -- download/copy custom binaries | emptyDir
        initContainers:
        - name: download-tools
          image: alpine:3.8
          command: [sh, -c]
          args:
          - wget -qO- https://get.helm.sh/helm-v2.12.3-linux-amd64.tar.gz | tar -xvzf - &&
            mv linux-amd64/helm /custom-tools/
          volumeMounts:
          - mountPath: /custom-tools
            name: custom-tools
        # 3. Volume mount the custom binary | bin directory (overriding the existing version)
        containers:
        - name: argocd-repo-server
          volumeMounts:
          - mountPath: /usr/local/bin/helm
            name: custom-tools
            subPath: helm
  ```

## BYOI (Build Your Own Image)

* approach: build ENTIRELY CUSTOMIZED Argo CD Reposerver

* use cases
  * you need to install OTHER dependencies
    * ❌replace a binary is NOT sufficient❌
