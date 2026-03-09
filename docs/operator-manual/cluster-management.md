# Cluster Management

* goal
  * how to manage clusters | CLI
* audience
  * operators

* MORE
  * if you want to handle declaratively -> [Declarative Setup](./declarative-setup.md#clusters)
  * [`argocd cluster` Command Reference](../user-guide/commands/argocd_cluster.md)

## Adding a cluster

* `argocd cluster add contextName`
  * `contextName`
    * check the AVAILABLE one -- via -- `kubectl config get-contexts`
  * how does it work?
    * connect -- to the -- cluster
    * install the necessary resources / ArgoCD can connect -- to -- it 
  * requirements
    * privileged access -- to the -- cluster 

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
