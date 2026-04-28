# Application Pruning & Resource Deletion

* if Application is created -- via -- an `ApplicationSet` -> ALL `Application` contain
  * `.metadata.ownerReferences` 
    * == *parent* `ApplicationSet` resource
  * & if `.syncPolicy.preserveResourcesOnDeletion` = `false` -> `.metadata.finalizers` == `resources-finalizer.argocd.argoproj.io`  

* if you delete an ApplicationSet ->
  * `ApplicationSet` resource itself is deleted
  * `Application` resources / were created -- from -- this `ApplicationSet` -> will be deleted
  * ⚠️ANY deployed resources  | managed cluster / were created -- from -- that `Application` resource -> will be deleted⚠️
    * _Example of deployed resources:_ `Deployments`, `Services`, `ConfigMaps`, etc 
    * Argo CD handle -- , via [the deletion finalizer](../../user-guide/app_deletion.md#deletion-finalizer), -- this deletion 
    * 💡if you want to preserve them -> | ApplicationSet, set `.syncPolicy.preserveResourcesOnDeletion` == true 💡
      * [MORE](Controlling-Resource-Modification.md)

* by default,
  * lifecycle of the `ApplicationSet` == lifecycle of the `Application` == lifecycle of the  `Application`'s resources
    * Reason:🧠default behavior🧠

* ways to delete an ApplicationSet
  * `kubectl delete applicationset <APPLICATIONSET_NAME> -n <argocd_OR_NAMESPACE_WHERE_IT_LIVES>`, OR
  * `argocd appset delete <APPLICATIONSET_NAME>`
