# Core Concepts

* requirements
  * [here](understand_the_basics.md)

## ArgoCD main concepts

* **Application**
  * == Custom Resource Definition (CRD) 
    * == group of Kubernetes resources / defined -- by a -- manifest 
* **Application source type**
  * == tool + source location
  * [here](user-guide/application_sources.md)
* **Target state** 
  * application's desired state
  * == files | Git repository
* **Live state**
  * application's live state
  * application's state | cluster
* **Sync status**
  * live state vs target state
* **Sync**
  * == process / application is moved -- to -- its target state
* **Sync operation status**
  * ALLOWED values
    * succeeded
    * failed
* **Refresh**
  * compare the latest code | Git vs live state
* **Health** 
  * == application's health
    * is it running correctly?
    * Can it serve requests?
* **Tool** 
  * == tool /
    * FROM a directory of files, create manifests
  * [here](user-guide/application_sources.md)
