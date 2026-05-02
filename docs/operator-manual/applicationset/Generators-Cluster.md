# Cluster Generator

* managed clusters 
  * are stored | ArgoCD namespace's [secrets](../declarative-setup.md#clusters)

* Cluster generator
  * [data structure](/manifests/crds/applicationset-crd.yaml)'s `spec.generators[*].cluster`
    * [`.flatList`](#flatlist)
    * [`.selector`](#selector-)
    * `.template`
      * override default ApplicationSet `spec.template`
    * [`.values`](#values)
  * generate parameters / EACH registered cluster | Argo CD
    * built-in parameters
      * == 👀[cluster credential secrets](../declarative-setup.md#clusters) 👀
        - `name`
          - == `stringData.name`
        - `nameNormalized`
          - == `name` / ONLY contain
            - lowercase alphanumeric characters
            - '-'
            - '.'
          - uses
            - your cluster name contains characters / NOT valid | k8s resources
              - _Examples:_ `_`
        - `server`
          - == `stringData.server`
        - `project`
          - == `stringData.project`
        - `metadata.labels.<key>` 
          - / EACH Secret's label
        - `metadata.annotations.<key>`
          - / EACH Secret's annotation
        - \| template it,
          - they are decoded

### `.selector` 

* allows
  * narrow the scope of targeted clusters

* types
  * -- by -- [Cluster credential secret](../declarative-setup.md#cluster-credentials)'s labels
    * `.matchLabels`
  * -- by -- [Cluster credential secret](../declarative-setup.md#cluster-credentials)'s expressions
    * `.matchExpressions`

* [Kubernetes resources / support set-based requirements](https://kubernetes.io/docs/concepts/overview/working-with-objects/labels/#resources-that-support-set-based-requirements)

### Deploy | local cluster

TODO: 
In Argo CD, the 'local cluster' is the cluster upon which Argo CD (and the ApplicationSet controller) 
is installed
This is to distinguish it from 'remote clusters', which are those that are added to Argo CD [declaratively](../declarative-setup.md#clusters) or
via the [Argo CD CLI](../../getting_started.md#5-register-a-cluster-to-deploy-apps-to-optional).
 
The cluster generator will automatically target both local and non-local clusters, 
for every cluster that matches the cluster selector.

If you wish to target only remote clusters with your Applications (e.g. you want to exclude the local cluster), 
then use a cluster selector with labels, for example:

```yaml
spec:
  goTemplate: true
  goTemplateOptions: ["missingkey=error"]
  generators:
  - clusters:
      selector:
        matchLabels:
          argocd.argoproj.io/secret-type: cluster
        # The cluster generator also supports matchExpressions.
        #matchExpressions:
        #  - key: staging
        #    operator: In
        #    values:
        #      - "true"
```

This selector will not match the default local cluster, since the default local cluster does not have a Secret 
(and thus does not have the `argocd.argoproj.io/secret-type` label on that secret)
* Any cluster selector that selects on that label will automatically exclude the default local cluster.

However, if you do wish to target both local and non-local clusters, while also using label matching, 
you can create a secret for the local cluster within the Argo CD web UI:

1. Within the Argo CD web UI, select *Settings*, then *Clusters*.
2. Select your local cluster, usually named `in-cluster`.
3. Click the *Edit* button, and change the *NAME* of the cluster to another value, for example `in-cluster-local`
   * Any other value here is fine.
4. Leave all other fields unchanged.
5. Click *Save*.

These steps might seem counterintuitive, but the act of changing one of the default values
for the local cluster causes the Argo CD Web UI to create a new secret for this cluster
In the Argo CD namespace, you should now see a Secret resource named `cluster-(cluster suffix)`
with label `argocd.argoproj.io/secret-type": "cluster"`
You may also create a local [cluster secret declaratively](../declarative-setup.md#clusters), or 
with the CLI using `argocd cluster add "(context name)" --in-cluster`, rather than through the Web UI.

### filter clusters -- based on -- their K8s version

* requirements
  * | [Cluster credential](../declarative-setup.md#cluster-credentials), 
    * set `labels.argocd.argoproj.io/auto-label-cluster-info: true`
      * -> controller label the cluster secret -- with the -- Kubernetes version / it's running on
  * exist PREVIOUS Application | that cluster

* how to use?
  * | `spec.generators.clusters.selector.matchLabels` OR `spec.generators.clusters.selector.matchExpressions`
    * `argocd.argoproj.io/kubernetes-version: <K8S_VERSION>`

### `values`

* allow
  * pass ADDITIONAL key/value pairs
    * value
      * 👀ALSO admit built-in parameters👀

* uses
  * | template,
    * `{{.values.<KEY>}}`

### `.flatList`

* allows
  * gather cluster information -- as a -- flat list
    * == ⚠️deploy 1! application⚠️
    * generator parameter: `.clusters`
      * == ALL clusterS
