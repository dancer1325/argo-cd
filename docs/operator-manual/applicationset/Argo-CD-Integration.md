* goal
  * How ApplicationSet controller interacts -- with -- Argo CD?

* ApplicationSet controller's 
  * responsibility
    * 👀ensure that the `Application`S remain consistent -- with -- the defined declarative `ApplicationSet` resource👀 
      * == ⚠️ONLY create/modify/delete `Application`⚠️
      * _Example:_ | create, update, or delete an `ApplicationSet` resource -> the ApplicationSet controller creates, updates, or deletes >=1 Argo CD `Application` resources
  * ⚠️limitations⚠️
    * ONLY connect -- to the -- cluster | Argo CD is deployed to
    * ONLY interact -- with -- namespace | Argo CD is deployed
      * EXCEPT FOR: enabling [this feature](Appset-Any-Namespace.md)

TODO: 
It is Argo CD itself that is responsible for the actual deployment of the generated child `Application` resources, 
such as Deployments, Services, and ConfigMaps.

The ApplicationSet controller can thus be thought of as an `Application` 'factory', taking an `ApplicationSet` resource as input, and 
outputting one or more Argo CD `Application` resources that correspond to the parameters of that set.

![ApplicationSet controller vs Argo CD, interaction diagram](../../assets/applicationset/Argo-CD-Integration/ApplicationSet-Argo-Relationship-v2.png)

In this diagram an `ApplicationSet` resource is defined, and it is the responsibility of the ApplicationSet controller 
to create the corresponding `Application` resources. The resulting `Application` resources are then managed Argo CD: 
that is, Argo CD is responsible for actually deploying the child resources. 

Argo CD generates the application's Kubernetes resources based on the contents of the Git repository defined
within the Application `spec` field, deploying e.g. Deployments, Service, and other resources.

Creation, update, or deletion of ApplicationSets will have a direct effect on the Applications present in the Argo CD namespace
Likewise, cluster events (the addition/deletion of Argo CD cluster secrets, when using Cluster generator), or changes 
in Git (when using Git generator), will be used as input to the ApplicationSet controller in constructing `Application` resources.

Argo CD and the ApplicationSet controller work together to ensure a consistent set of Application resources exist, and
are deployed across the target clusters.
