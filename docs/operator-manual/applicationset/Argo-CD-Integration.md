* goal
  * how ApplicationSet controller interacts -- with -- Argo CD?

* ApplicationSet controller 
  * 's responsibility
    * 👀ensure that the `Application`S remain consistent -- with -- the defined declarative `ApplicationSet` resource👀 
      * == ⚠️ONLY create/modify/delete `Application`⚠️
      * == `Application` 'factory'
      * _Example:_ | create, update, or delete an `ApplicationSet` resource -> the ApplicationSet controller creates, updates, or deletes >=1 Argo CD `Application` resources
  * ⚠️limitations⚠️
    * ONLY connect -- to the -- cluster | Argo CD is deployed to
    * ONLY interact -- with -- namespace | Argo CD is deployed
      * ⚠️EXCEPT FOR: enabling [this feature](Appset-Any-Namespace.md)⚠️

* Argo CD itself
  * 's responsibility
    * deploy -- , based on the Git repository, -- the generated child `Application` resources
      * _Examples:_ Deployments, Services, and ConfigMaps

![ApplicationSet controller vs Argo CD, interaction diagram](../../assets/applicationset/Argo-CD-Integration/ApplicationSet-Argo-Relationship-v2.png)
