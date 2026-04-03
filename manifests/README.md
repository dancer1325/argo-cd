# Argo CD Installation Manifests

## Multi-Tenant

* MOST common way
* use cases
  * \>1 application developer teams /
    * Reason: 🧠enables you configure (== set the pillars, != PRE configured) 
      * RBAC model &
        * if you want to configure -> [here](/docs/operator-manual/rbac.md)
      * OIDC authentication
        * if you want to configure -> [here](/docs/operator-manual/user-management/index.md)🧠
    * share SAME Argo CD instance
    * maintained -- by a -- platform team
    * can access Argo CD's API server -- via --
      * Web UI OR
      * [`argocd` CLI](/docs/user-guide/commands/argocd_login.md)

### Non-High Availability

* 👀recommendations👀
  * use | testing & demos
  * ❌NOT use | production ❌

#### -- via -- 1! step

* [install.yaml](install.yaml)
  * standard Argo CD installation
  * requirements
    * cluster-admin access
      * Reason: 🧠manifest contains `ClusterRole`🧠
  * uses
    * deploy applications | 
      * SAME cluster / Argo CD runs
        * by default
      * external clusters
        * specify [inputted credentials](/docs/operator-manual/cluster-management.md)
        * external cluster ==     != cluster / Argo CD runs

* steps
  * `kubectl apply -f install.yaml`
    * Problems:
      * Problem1: "too long"
        * Solution: `kubectl apply --server-side --force-conflicts -f install.yaml`

#### -- via -- 2 steps

* [namespace-install.yaml](namespace-install.yaml) 
  * ❌NOT include ArgoCD CRDs❌
  * ⚠️requirements ⚠️
    * namespace level privileges
      * == ❌NOT need cluster roles❌
      * Reason: 🧠manifest contains `Role`🧠
  * allows
    * specifying the cluster | install Argo CD
  * uses
    * deploy applications |
      * SAME cluster / Argo CD runs
        * ❌NOT deployed DIRECTLY❌
        * requirements
          * specify [inputted credentials](/docs/operator-manual/cluster-management.md) 
      * external clusters
        * external cluster ==     != cluster / Argo CD runs
        * specify [inputted credentials](/docs/operator-manual/cluster-management.md)
  * use cases
    * run >1 Argo CD instances / 
      * DIFFERENT teams
      * EACH instance deploy applications -- to -- external clusters

* steps
  * `kubectl apply --server-side --force-conflicts -k crds/`
  * `kubectl apply -f namespace-install.yaml` OR `kubectl create namespace randomname && kubectl apply -n randomname -f namespace-install.yaml`

### High Availability

* recommendations
  * use | production

#### -- via -- 1! step

* [ha/install.yaml](ha/install.yaml)
  * == [install.yaml](install.yaml) + MULTIPLE replicas / supported components
    * MULTIPLE replicas 
      * `spec.replicas` | `kind: StatefulSet`
      * `spec.replicas` | `kind: Deployment`

#### -- via -- 2 steps

* [ha/namespace-install.yaml](ha/namespace-install.yaml) 
  * == [namespace-install.yaml](namespace-install.yaml) + MULTIPLE replicas / supported components
    * MULTIPLE replicas
      * `spec.replicas` | `kind: StatefulSet`
      * `spec.replicas` | `kind: Deployment`

## Core

* [manifest](core-install.yaml)
* [guide](/docs/operator-manual/core.md)
