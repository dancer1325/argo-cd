### Automating the generation of Argo CD Applications -- via -- ApplicationSet Controller

* [ApplicationSet controller](../operator-manual/applicationset/index.md)
  * 's goal
    * improve | Argo CD, 
      * multi-cluster support &
      * cluster multitenant support  
  * allows
    * adding AUTOMATION of Argo CD Application 
      * == generate OR remove -- AUTOMATICALLY, based on `ApplicationSet` CR's contents, -- Argo CD Applications
        * == 💡managing MULTIPLE Argo CD Applications 💡
    * developers / NO access to Argo CD namespace,
      * INDEPENDENTLY create -- WITHOUT cluster-administrator intervention -- Applications
        * [security implications](../operator-manual/applicationset/Security.md)

* Argo CD Applications
  * 👀are templated -- from -- [generators](../operator-manual/applicationset/generators.md) 👀

* _Example:_ `ApplicationSet` resource / Argo CD Application -- targeted, via list generator, to -- MULTIPLE clusters
  * TODO: use it
    ```yaml
    apiVersion: argoproj.io/v1alpha1
    kind: ApplicationSet
    metadata:
      name: guestbook
    spec:
      goTemplate: true
      goTemplateOptions: ["missingkey=error"]
      # create 1 Argo CD application / EACH generator
      generators:
      - list:
          elements:
          - cluster: engineering-dev
            url: https://1.2.3.4
          - cluster: engineering-prod
            url: https://2.4.6.8
          - cluster: finance-preprod
            url: https://9.8.7.6
      template:
        metadata:
          name: '{{.cluster}}-guestbook'    # {{.cluster}}    generator's parameter 
        spec:
          project: my-project
          source:
            repoURL: https://github.com/infra-team/cluster-deployments.git
            targetRevision: HEAD
            path: guestbook/{{.cluster}}
          destination:
            server: '{{.url}}'      # {{.url}}    generator's parameter
            namespace: guestbook
    ```

* see [ApplicationSet documentation](../operator-manual/applicationset/index.md)
