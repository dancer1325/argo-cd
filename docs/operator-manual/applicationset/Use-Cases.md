# Use cases / supported -- by the -- ApplicationSet controller

* Generators 
  * produce
    * FROM MULTIPLE sources, template parameter data
      * _Example of MULTIPLE sources:_ Argo CD clusters, Git repositories

## Use case: provision cluster add-ons | >=1 Kubernetes clusters

* audience
  * Kubernetes cluster administrators

* cluster-addons
  * uses
    * development teams' applications
  * _Examples:_
    * [Prometheus operator](https://github.com/prometheus-operator/prometheus-operator)
    * controllers 
      * [argo-workflows controller](https://argoproj.github.io/argo-workflows/) 
      * ...

    ![Cluster add-on diagram](../../assets/applicationset/Use-Cases/Cluster-Add-Ons.png)
  * ways to implement it
    * list generator
      * 's key/value == targeted clusters
    * cluster generator
    * git generator
      * -- via -- git generator file
        * list of clusters / kept -- as a -- ".json" | Git repository 
      * -- via -- git generator directory
        * [here](/applicationset/examples/git-generator-directory)

## Use case: monorepos

* monorepo
  * == MULTIPLE Argo CD Application resources / defined | 1! Git repository
    * _Example:_ Kubernetes cluster entire state managed -- from -- 1! Git repository

    ![Monorepo diagram](../../assets/applicationset/Use-Cases/Monorepos.png)
  * ways to implement it
    * Git generator directories
      * particular subdirectories / contain the individual applications -- to -- deploy
    * Git generator files
      * particular files / contain JSON metadata -- to -- deploy individual applications

## Use case: self-service of Argo CD Applications | MULTITENANT clusters
 
* goal
  * enable developers, greater flexibility 
    * to deploy -- BY THEMSELVES (== ❌NO need cluster administration intervention❌) --
      * MULTIPLE applications | 1! cluster -- via -- Argo CD
      * MULTIPLE clusters -- via -- Argo CD

* ways to implement it
  * Attempt1: | Git repository,
    * ArgoCD Application manifestS / follow [app-of-apps pattern](../cluster-bootstrapping.md#app-of-apps-pattern-alternative)
      * developers team raise PR
      * cluster administrators review/accept those PRs
    * cons
      * ⚠️risk | make changes | ArgoCD Applications⚠️
        * Reason of risk:🧠ArgoCD Application CRD manage the deployment | cluster🧠
        * Solution:💡Kubernetes administrators ONLY enable changing SOME ArgoCD Application's fields
          * _Example of fields / developers could change:_ `spec.source` OR `spec.sources`
          * _Example of fields / developers should NOT change:_ `spec.destination`💡
  * Solution: 💡create an `ApplicationSet` / 
    * restricts IMPORTANT fields
    * enable customization -- , by developers, -- of 'safe' fields💡

* _Example:_ [here](/applicationset/examples/git-generator-files-discovery)