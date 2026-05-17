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
* **Refresh**
  * compare the desired state vs live state
    * desired state, FIRSTLY, checked | repo-server
* **Hard Refresh**
  * compare the desired state vs live state
    * invalidate EXISTING desired state | repo-server
    * fetch Git
* **Sync**
  * == process / application is moved -- to -- its target state
* **Sync status**
  * | sync, 
    * live state vs target state
  * ALLOWED values
    * synced
    * outOfSync
    * unknown
  * per
    * Application
    * Application's resource
* **Sync operation status**
  * ALLOWED values
    * syncing
    * sync ok
    * sync error
    * sync failed
    * unknown
* **Health** 
  * == about resources / are deployed 
    * is it running correctly?
    * Can it serve requests?
  * ALLOWED values
    * progressing
    * suspended
    * healthy
    * degraded
    * missing
    * unknown
  * per
    * Application
    * Application's resource
* **Tool** 
  * == tool /
    * FROM a directory of files, create manifests
  * [here](user-guide/application_sources.md)
