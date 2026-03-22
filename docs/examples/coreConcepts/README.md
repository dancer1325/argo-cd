# Application
## == CRD 
### == group of Kubernetes resources / defined -- by a -- manifest
* [here](/manifests/crds/application-crd.yaml)
  * group
    * Reason: 🧠define `spec.group`🧠

# Application Source Type
## == tool / used -- to -- build the application
TODO: 

# Target State

The desired state of an application, represented as files in a Git repository.

# Live State

The current live state of the application running in the cluster.

# Sync Status

The comparison between the live state and the target state, indicating whether they match.

# Sync

The process of moving an application to its target state, ensuring the live state matches the desired state.

# Sync Operation Status

The result of a sync operation. Allowed values:
- succeeded
- failed

# Refresh

The process of comparing the latest code in Git against the live state in the cluster.

# Health

The health status of an application, indicating:
- Is it running correctly?
- Can it serve requests?

# Tool
