# Triggers and Templates Catalog

* [Kubernetes manifest](/notifications_catalog/install.yaml)

## how to install?
* Install Triggers and Templates from the catalog
  ```bash
  kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/notifications_catalog/install.yaml
  
  # if you get kubectl errors -> use
  # kubectl apply -n argocd --server-side --force-conflicts -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/notifications_catalog/install.yaml
  ```

## Triggers

|          NAME          | DESCRIPTION & DEFINITION                                            |                      TEMPLATE                       |
|------------------------|---------------------------------------------------------------------|-----------------------------------------------------|
| on-created             | [here](/notifications_catalog/triggers/on-created.yaml)             | [app-created](#app-created)                         |
| on-deleted             | [here](/notifications_catalog/triggers/on-deleted.yaml)             | [app-deleted](#app-deleted)                         |
| on-deployed            | [here](/notifications_catalog/triggers/on-deployed.yaml)            | [app-deployed](#app-deployed)                       |
| on-health-degraded     | [here](/notifications_catalog/triggers/on-health-degraded.yaml)     | [app-health-degraded](#app-health-degraded)         |
| on-sync-failed         | [here](/notifications_catalog/triggers/on-sync-failed.yaml)         | [app-sync-failed](#app-sync-failed)                 |
| on-sync-running        | [here](/notifications_catalog/triggers/on-sync-running.yaml)        | [app-sync-running](#app-sync-running)               |
| on-sync-status-unknown | [here](/notifications_catalog/triggers/on-sync-status-unknown.yaml) | [app-sync-status-unknown](#app-sync-status-unknown) |
| on-sync-succeeded      | [here](/notifications_catalog/triggers/on-sync-succeeded.yaml)      | [app-sync-succeeded](#app-sync-succeeded)           |

## Templates
### app-created

* [definition](/notifications_catalog/templates/app-created.yaml)

### app-deleted

* [definition](/notifications_catalog/templates/app-deleted.yaml)

### app-deployed

* [definition](/notifications_catalog/templates/app-deployed.yaml)

### app-health-degraded

* [definition](/notifications_catalog/templates/app-health-degraded.yaml)

### app-sync-failed

* [definition](/notifications_catalog/templates/app-sync-failed.yaml)

### app-sync-running

* [definition](/notifications_catalog/templates/app-sync-running.yaml)

### app-sync-status-unknown

* [definition](/notifications_catalog/templates/app-sync-status-unknown.yaml)

### app-sync-succeeded

* [definition](/notifications_catalog/templates/app-sync-succeeded.yaml)
