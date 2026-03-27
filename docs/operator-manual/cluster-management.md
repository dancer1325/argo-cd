# Cluster Management

* goal
  * how to manage clusters -- through -- CLI
* audience
  * operators

* MORE
  * if you want to handle declaratively -> [Declarative Setup](./declarative-setup.md#clusters)
  * [`argocd cluster` Command Reference](../user-guide/commands/argocd_cluster.md)

## Adding a cluster

* `argocd cluster add contextName`
  * allows
    * 💡Argo CD can deploy Applications | MULTIPLE clusters (EVEN != cluster | Argo CD is installed)💡
      * Reason:🧠
        * ArgoCD does NOT have access -- to your -- local kubeconfig
        * OTHERWISE, Argo CD can NOT install Applications | OTHER clusters🧠
  * ⚠️requirements⚠️
    * privileged access -- to the -- cluster
    * `contextName` MUST ALREADY exist
      * check the AVAILABLE one -- via -- `kubectl config get-contexts`
  * what does Argo CD under the hood?
    1. creates SA "argocd-manager" | target cluster / FULL cluster RBAC
    2. gets its bearer token
    3. stores token + server URL + TLS -- as a -- Secret | "argocd" namespace
       * label `argocd.argoproj.io/secret-type: cluster`
    4. | sync an `Application` / `destination.server: https://...`, Application Controller connect -- , via that Secret, to -- that cluster 

## Skipping cluster reconciliation

TODO:
You can stop the controller from reconciling a cluster without removing it by annotating its secret:

```bash
kubectl -n argocd annotate secret <cluster-secret-name> argocd.argoproj.io/skip-reconcile=true
```

The cluster will still appear in `argocd cluster list` but the controller will skip reconciliation
for all apps targeting it
* To resume, remove the annotation:

```bash
kubectl -n argocd annotate secret <cluster-secret-name> argocd.argoproj.io/skip-reconcile-
```

See [Declarative Setup - Skipping Cluster Reconciliation](./declarative-setup.md#skipping-cluster-reconciliation) for details.

## Removing a cluster

* `argocd cluster rm contextName`

* "in-cluster"
  * ❌can NOT be removed❌
  * if you want to disable the `in-cluster` configuration -> | "argocd-cm" ConfigMap,
    * set `.data.cluster.inClusterEnabled: "false"`
    * _Example of "argocd-cm": [here](examples/argocd-cm.yaml)
