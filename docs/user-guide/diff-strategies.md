# Diff Strategies

* [diffing](diffing.md)

* Argo CD
  * diff strategies
    - **Legacy**
      * default one
      * -- based on -- 3-way diff states
        * live state
          * == | Cluster
        * desired state
          * == | Git
        * [`kubectl.kubernetes.io/last-applied-configuration`](https://kubernetes.io/docs/reference/labels-annotations-taints/#kubectl-kubernetes-io-last-applied-configuration) 
          * == | Cluster's SOME resource, metadata.annotation
    - **Structured-Merge Diff**
      * [MORE](#structured-merge-diff)
    - **Server-Side Diff**
      * [MORE](#server-side-diff)

## Structured-Merge Diff

* ⚠️Discontinued⚠️
  * -> 👀use [Server-Side Diff](#server-side-diff)👀
  * Reason:🧠issues identified -- by the -- community🧠
    * _Example:_ calculate diffs -- for -- CRDs / define default values 

* if you enable Server-Side Apply sync option -> AUTOMATICALLY used

* calculate diffs -- based on -- fields ownership  
  * -- thanks to -- [structured-merge-diff](https://github.com/kubernetes-sigs/structured-merge-diff) library

## Server-Side Diff

* | Argo CD v3.1.0,
  * stable 

* predicted live state
  * generated -- by -- invoking a Server-Side Apply /
    * dry-run mode
    * EACH application's resource

* Server-Side Diff 
  * == Server-Side Apply / dry-run mode 

* diff results
  * == predicted live state vs live state
  * are cached

* Server-Side Apply requests -- to -- Kube API 
  * use cases to be triggered (== ❌NOT use cache values❌):
    - request an 
      - Application refresh OR
      - Application hard-refresh
    - NEW revision | repo / Argo CD Application is targeting
    - Argo CD Application spec changed
    - | live state,
      - [Resource Version](https://kubernetes.io/docs/reference/using-api/api-concepts/#resourceversion-in-metadata) changed
  * ❌NOT use cases❌
    * creation of NEW resources
      * == NO ADDITIONAL call to KubeAPI 
        * -> lighter & faster diff calculation
      * Reason:🧠NOTHING to compare -- since -- PREVIOUSLY NOT existed 🧠

* advantage
  * | diff calculation,
    * Kubernetes Admission Controllers participate 
      * -> happen | diff stage (❌NOT | sync stage❌)

### how to enable it?

* ways
  * [| Argo CD Controller level](#-argo-cd-controller-level)
  * [| Argo CD Application level](#-argo-cd-application-level)

#### | Argo CD Controller level

* valid | ALL Argo CD Applications

* steps
  * | "argocd-cmd-params-cm" configmap

    ```yaml
    apiVersion: v1
    kind: ConfigMap
    metadata:
      name: argocd-cmd-params-cm
    data:
      controller.diff.server.side: "true"
      ...
    ```
  * restart the `argocd-application-controller`

#### | Argo CD Application level

* valid | 1! Argo CD Application

* steps
  * | Argo CD Application

    ```yaml
    apiVersion: argoproj.io/v1alpha1
    kind: Application
    metadata:
      annotations:
        argocd.argoproj.io/compare-options: ServerSideDiff=true
    ...
    ```

### how to disable it?

* use cases
  * Server-Side Diff is enabled GLOBALLY
    * == [| Argo CD Controller level](#-argo-cd-controller-level) 

* steps
  * | Argo CD Application

    ```yaml
    apiVersion: argoproj.io/v1alpha1
    kind: Application
    metadata:
      annotations:
        argocd.argoproj.io/compare-options: ServerSideDiff=false
    ...
    ```

### [Mutation Webhooks](https://kubernetes.io/docs/reference/access-authn-authz/admission-controllers/)

* changes / made -- by -- mutation webhooks
  * by default, 
    * ❌NOT take in account | Server-Side Diff❌
  * ⚠️ONLY valid | Server-Side Diff strategy⚠️

* steps to enable it
  * | Argo CD Application

    ```yaml
    apiVersion: argoproj.io/v1alpha1
    kind: Application
    metadata:
      annotations:
        argocd.argoproj.io/compare-options: IncludeMutationWebhook=true
    ...
    ```
