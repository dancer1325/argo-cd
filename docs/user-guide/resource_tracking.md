# Resource Tracking

* goal
  * how to track Kubernetes resources -- by -- annotation

* ways to track resources
  * [-- by -- annotation](#---by----annotation)
  * [-- by -- label](#---by----label)
  * [-- by -- annotation + label](#---by----annotation--label)

* how to specify the track resource method?
  * steps
    * | "argocd-cm" ConfigMap,
      * specify `data.application.resourceTrackingMethod`
        * ALLOWED values
          * `label`
          * `annotation+label`
          * `annotation`

* how to update the track resource method?
  * steps
    * change the value
    * sync your applications again
      * ways
        * trigger it
        * wait for the sync mechanism

## -- by -- annotation

* 👀default one👀
* | tracked Kubernetes resource,
  * 💡ONCE Argo CD syncs it -> add `metadata.annotations.argocd.argoproj.io/tracking-id: <app-name>:<group>/<kind>:<namespace>/<resource-name>`💡
    * == 👀handled -- by -- Argo CD👀
      * ❌NOT set MANUALLY❌
        * == ❌NOT specified | Git manifest❌

* pros
  * there are NO clashes -- with -- other Kubernetes tools
    * != [-- by -- labels](#---by----label)
  * Argo CD knows the owner of a resource

### Installation ID

* allows  
  * prevent conflicts BETWEEN DIFFERENT Argo CD instances / try to manage SAME resource
    * _Example:_ allowed >1 Argo CD instances / SAME name

* how to configure?
  * | "argocd-cm" ConfigMap,
    * set

      ```yaml
        ...
      data:
        installationID: SomeValueYouGive
      ```

* use case
  * \>1 Argo CD instances | 1 cluster

* | tracked Kubernetes resource,
  * ONCE Argo CD syncs it -> add `metadata.annotations.argocd.argoproj.io/installation-id: <installationIdYouConfigureInTheConfigMap>`

### NON self-referencing annotations

* goal
  * other Kubernetes tools (_Example:_ [HNC](https://github.com/kubernetes-sigs/hierarchical-namespaces)) copy a resource -- to a -- DIFFERENT namespace /
    * NO impact the Argo CD application's sync status
    * copied resources
      * are visible | UI | top level
      * NO have sync status

* requirements
  * tracking method ==
    * `annotation` OR
    * `annotation+label`

* NON self-referencing annotations
  * == `metadata.annotations.argocd.argoproj.io/tracking-id`'s value (`<app-name>:<group>/<kind>:<namespace>/<resource-name>`)  !=  OWN resource properties
  * -> the resource will ❌NOT
    * affect the application's sync status
    * be marked for pruning❌

## -- by -- label

* | tracked Kubernetes resource,
  * 💡ONCE Argo CD syncs it -> add `metadata.labels.someLabel:ArgoCDApplicationNameWhichManageIt`💡 
    * `someLabel`
      * by default `app.kubernetes.io/instance`
        * == `metadata.labels.app.kubernetes.io/instance:ArgoCDApplicationNameWhichManageIt`

* allows
  * identifying the Argo CD application / manage the resource

* ⚠️limitations⚠️
  * labels' length <= 63 characters
  * OTHER external tools might write/append | this label -> create conflicts with Argo CD
    * Reason: 🧠`app.kubernetes.io/instance` is a COMMON label🧠
    * _Example:_ used by several Helm charts & operators

* use cases
  * cluster / > 1 Argo CD instance

### custom label

* how to configure?
  * | "argocd-cm" ConfigMap,
    * set

      ```yaml
      ...
      data:
        application.instanceLabelKey: YourDesiredLabel
      ```

## -- by -- annotation + label

* label
  * uses
    * informative
  * ❌NOT used for❌
    * tracking purposes

* annotation
  * uses
    * track application resources

* use cases
  * OTHER tools / need the label 

### NON self-referencing annotations

* [here](#non-self-referencing-annotations)