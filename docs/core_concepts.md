# Core Concepts

* requirements
  * [here](understand_the_basics.md)

## ArgoCD main concepts

* **Application**
  * == Custom Resource Definition (CRD) / 
    * group Kubernetes resources / defined -- by a -- manifest 
* **Application source type**
  * == tool + source location
  * [here](user-guide/application_sources.md)
* **ApplicationSet**
  * == Custom Resource Definition (CRD) /
    * FROM 1! Argo CD Application template, generate -- , via generators, -- MULTIPLE Applications
* **Project**
  * == Custom Resource Definition (CRD) /
    * group Argo CD ApplicationS
* **Target state** 
  * application's desired state
  * == files | Git repository
* **Live state**
  * application's live state
  * application's state | cluster
* **Sync**
  * == process / application is moved -- to -- its target state
* **Sync status**
  * | sync, 
    * live state vs target state
  * ALLOWED values
    * synced
    * outOfSync
    * unknown
* **Sync operation status**
  * ALLOWED values
    * syncing
    * sync ok
    * sync error
    * sync failed
    * unknown
* **Refresh**
  * compare the latest code | Git vs live state
* **Health** 
  * == application's health
    * is it running correctly?
    * Can it serve requests?
  * ALLOWED values
    * progressing
    * suspended
    * healthy
    * degraded
    * missing
    * unknown
* **Tool** 
  * == tool /
    * FROM a directory of files, create manifests
  * [here](user-guide/application_sources.md)
