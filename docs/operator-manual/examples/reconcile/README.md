# requirements
* download software / enable you to run local Kubernetes clusters
  * [Docker desktop](https://docs.docker.com/get-started/introduction/get-docker-desktop/)
  * [kind](https://kind.sigs.k8s.io/) + [install Kubectl](https://kubernetes.io/docs/tasks/tools/#kubectl)
  * [minikube](https://minikube.sigs.k8s.io/docs/)
    * `kubectl` commands are wrapped -- via -- `minikube kubectl`
  * [microk8s](https://canonical.com/microk8s)
    * `kubectl` commands are wrapped -- via -- `microk8s kubectl`
* run a local Kubernetes cluster
  * -- via --
    * [Docker Desktop](https://docs.docker.com/desktop/use-desktop/kubernetes/#enable-kubernetes)
      * | Docker Desktop
        * Kubernetes > Create cluster > choose any cluster type
    * [Kind](https://kind.sigs.k8s.io/#installation-and-usage)
      * `kind create cluster`
    * minikube
      * `minikube start`
    * microk8s
  * `kubectl config current-context`
    * check Kubectl points to a context
* [install Argo CD](../../operator-manual/installation.md)
* [deploy](https://github.com/dancer1325/argocd-example-apps/tree/master/apps#how-to-deploy-locally)

# ⭐️ways to trigger it ⭐️
## live state changes
* `kubectl scale deployment guestbook-ui -n guestbook --replicas=3`
* `kubectl logs -n argocd argocd-application-controller-0 | grep "example.guestbook"`
  * check in the logs
    * "Requesting app refresh caused by object update"
    * "Refreshing app status (controller refresh requested), level"
    * "Comparing app state"
    * "GetRepoObjs stats"
    * "Retrieved live manifests"
    * "Updated sync status:"
    * "Updated health status:"
### how to check that resource updates are ignored?
* `kubectl patch configmap argocd-cmd-params-cm -n argocd --type merge --patch-file argoCDCMDParamsCMPatch.yaml`
  * Reason: 🧠see controller debug level logs🧠
* `kubectl logs -n argocd argocd-application-controller-0 | grep "example.guestbook"`
  * look for "Ignoring change of object because none of the watched resource fields have changed"
  * you can identify by `(1)` 
    * [source code](/controller/appcontroller.go)'s `CompareWithRecent CompareWith = 1` 
### untracked resources
* [example.guestbook](https://github.com/dancer1325/argocd-example-apps/tree/master/guestbook)
#### == resources / NOT exist | Git & exist | cluster
##### types
###### tracked resources' dependant
* `kubectl get all -n guestbook`  
  * 's return: `Pod`, `Service`, `Deployment` & `Replicaset` 
* `argocd app get example.guestbook`
  * ONLY track `Deployment` & `Service`
###### MANUALLY created
TODO: 
#### ArgoCD ❌do NOT reconcile them ❌
* `Pod` & `Replicaset` do NOT exist | [Git](https://github.com/dancer1325/argocd-example-apps/tree/master/guestbook)
#### ArgoCD monitors them 
* `kubectl delete pod $(kubectl get pods -n guestbook -o jsonpath='{.items[0].metadata.name}') -n guestbook`
  * look for "kind":"Pod","level":"debug","msg":"Requesting app refresh caused by object update"
### how to ignore resource updates?
#### way1: | "argocd-cm" ConfigMap
##### `resource.ignoreResourceUpdatesEnabled`
###### by default, `true`
* [source code](/util/settings/settings.go)'s `if argoCDCM.Data[resourceIgnoreResourceUpdatesEnabledKey] == "" {`
###### enable OR disable, Argo CD can ignore resource updates
* `kubectl patch configmap argocd-cm -n argocd --type merge --patch-file ignoreResourceUpdatesArgoCDCMConfigMapPatch.yaml`
* `kubectl -n argocd rollout restart statefulset argocd-application-controller && kubectl -n argocd rollout status statefulset argocd-application-controller`
  * restart argocd-application-controller
* `kubectl scale deployment guestbook-ui -n guestbook --replicas=3`
  * change the number of replicas
* check the reconciliation happened
  * `kubectl logs -n argocd argocd-application-controller-0 | grep "example.guestbook" | grep -E "Requesting app refresh.*Deployment|Reconciliation completed|OutOfSync|auto.sync|Initiated automated sync"`
    * look for
      * "Updated sync status: Synced"
        * == OutOfSync
          * Reason: detected the change
      * "Reconciliation completed"
        * == ALREADY reconciled
      * "Updated sync status: OutOfSync"
        * == auto-sync
##### `resource.customizations.ignoreResourceUpdates.all`
* `kubectl patch configmap argocd-cm -n argocd --type merge --patch-file ignoreResourceUpdatesAllResourcesArgoCDCMConfigMapPatch.yaml`
* `kubectl -n argocd rollout restart statefulset argocd-application-controller && kubectl -n argocd rollout status statefulset argocd-application-controller`
  * restart argocd-application-controller
* `kubectl get deployment -n guestbook`
  * 's return: 2
* `kubectl scale deployment guestbook-ui -n guestbook --replicas=3`
* `kubectl get deployment -n guestbook`
  * 's return: 3
    * AFTER a while, it returns to 2
      * Reason:🧠`kubectl scale` triggers pod updates -> NOT ignored -> reconciled afterwards🧠
* `kubectl logs -n argocd argocd-application-controller-0 --since=2m | grep "Requesting app refresh" | grep "Deployment" | grep "example.guestbook"`
  * 's return: NOTHING
##### `resource.customizations.ignoreResourceUpdates.<group>_<kind>`
###### ⚠️override `resource.customizations.ignoreResourceUpdates.all`⚠️
* `kubectl patch configmap argocd-cm -n argocd --type merge --patch-file ignoreResourceUpdatesArgoCDCMConfigMapPatch.yaml`
* `kubectl -n argocd rollout restart statefulset argocd-application-controller && kubectl -n argocd rollout status statefulset argocd-application-controller`
  * restart argocd-application-controller
* `kubectl get deployment -n guestbook`
  * 's return: 2
* `kubectl scale deployment guestbook-ui -n guestbook --replicas=3`
* `kubectl logs -n argocd argocd-application-controller-0 | grep "example.guestbook"`
  * look for
    * "Requesting app refresh caused"
    * "Refreshing app status"
    * "Comparing app state"
#### way2: | OWN resources, annotate with `argocd.argoproj.io/ignore-resource-updates=true`
##### requirements: | "argocd-cm" ConfigMap, `resource.ignoreResourceUpdatesEnabled: 'true'`
* `kubectl get cm argocd-cm -n argocd -o jsonpath='{.data.resource\.ignoreResourceUpdatesEnabled}'`
  * 's return: false
* [example.guestbook-with-ignoreupdates](https://github.com/dancer1325/argocd-example-apps/tree/master/guestbook-with-ignoreupdates)
  * `kubectl describe deployment guestbook-ui-with-ignoreupdates -n guestbook-with-ignoreupdates | grep Annotations`
    * 's return: Annotations:            argocd.argoproj.io/ignore-resource-updates: true
* `kubectl patch deployment guestbook-ui-with-ignoreupdates -n guestbook-with-ignoreupdates --subresource=status --type merge --patch-file deploymentStatusPatch.yaml`
* `kubectl logs -n argocd argocd-application-controller-0 --since=15s | grep "guestbook-with-ignoreupdates" | grep "Requesting app refresh"`
  * 's return: 
    * "Requesting app refresh caused by object update"
* `kubectl patch configmap argocd-cm -n argocd --type merge -p '{"data":{"resource.ignoreResourceUpdatesEnabled":"true"}}'`
  * for NEXT subsections
* `kubectl -n argocd rollout restart statefulset argocd-application-controller && kubectl -n argocd rollout status statefulset argocd-application-controller`
  * restart argocd-application-controller
##### ⚠️ONLY apply | k8s resource ⚠️
TODO:
##### |
###### tracked resources, ❌does NOT apply | tracked' DEPENDENT resources❌
* [example.guestbook-with-ignoreupdates](https://github.com/dancer1325/argocd-example-apps/tree/master/guestbook-with-ignoreupdates)
  * `kubectl describe deployment guestbook-ui-with-ignoreupdates -n guestbook-with-ignoreupdates | grep Annotations`
    * 's return: Annotations:            argocd.argoproj.io/ignore-resource-updates: true
* `kubectl patch deployment guestbook-ui-with-ignoreupdates -n guestbook-with-ignoreupdates --subresource=status --type merge --patch-file deploymentStatusPatch.yaml`
* `kubectl logs -n argocd argocd-application-controller-0 --since=15s | grep "guestbook-with-ignoreupdates" | grep "Requesting app refresh"`
  * 's return: NOTHING
###### untracked resources, you MUST MANUALLY add
* `kubectl get replicaset -n guestbook-with-ignoreupdates -o jsonpath='{.items[0].metadata.annotations}'`
  * 's return: annotations
    * == propagated
* `kubectl get pods -n guestbook-with-ignoreupdates -o jsonpath='{.items[0].metadata.annotations}'`
  * 's return: NOTHING
* `kubectl annotate pod $(kubectl get pods -n guestbook-with-ignoreupdates -o jsonpath='{.items[0].metadata.name}') -n guestbook-with-ignoreupdates argocd.argoproj.io/ignore-resource-updates=true`
  * apply MANUALLY
* `kubectl get pods -n guestbook-with-ignoreupdates -o jsonpath='{.items[0].metadata.annotations}'`
## Polling
### [`data.timeout.reconciliation`, `data.timeout.reconciliation` + `data.timeout.reconciliation.jitter`]
#### == frequency / Argo CD poll changes -- from -- Git OR helm repository
* [example.guestbook](https://github.com/dancer1325/argocd-example-apps/tree/master/guestbook)
* `kubectl logs -n argocd argocd-application-controller-0 | grep '"application":"example.guestbook"' | grep "comparison expired"`
  * you can identify by `(2)`
    * [source code](/controller/appcontroller.go)'s `CompareWithLatest CompareWith = 2`
##### ❌NOT ALWAYS SAME❌
* `kubectl logs -n argocd argocd-application-controller-0 | grep '"application":"example.guestbook"' | grep "comparison expired"`
  * time BETWEEN logs vary
#### by default, EACH 3'
* NOT set | "argocd-cm" configMap
  * `kubectl get cm argocd-cm -n argocd -o jsonpath='{.data.timeout\.reconciliation}'`
    * 's return: NOTHING
  * `kubectl get cm argocd-cm -n argocd -o jsonpath='{.data.timeout\.jitter}'`
    * 's return: NOTHING
* comes -- from -- [source code](/cmd/argocd-application-controller/commands/argocd_application_controller.go)
  * 120 + 60
#### specified | "argocd-cm" ConfigMap,
* `kubectl patch configmap argocd-cm -n argocd --type merge --patch-file argoCDCMReconciliationPatch.yaml`
* `kubectl -n argocd rollout restart statefulset argocd-application-controller && kubectl -n argocd rollout status statefulset argocd-application-controller`
* `kubectl logs -n argocd argocd-application-controller-0 | grep '"application":"example.guestbook"' | grep "comparison expired"`
  * check expiry: 20s
#### `data.timeout.reconciliation`
##### ⚠️if you set 0 -> disables AUTOMATIC polling⚠️
* modify [this argocd-cm patch](argoCDCMReconciliationPatch.yaml)
* `kubectl patch configmap argocd-cm -n argocd --type merge --patch-file argoCDCMReconciliationPatch.yaml`
* `kubectl -n argocd rollout restart statefulset argocd-application-controller && kubectl -n argocd rollout status statefulset argocd-application-controller`
* `kubectl logs -n argocd argocd-application-controller-0 | grep '"application":"example.guestbook"' | grep "comparison expired"`
  * 's return: NOTHING
###### requirements: configure `ARGOCD_DEFAULT_CACHE_EXPIRATION`
* `kubectl set env statefulset/argocd-application-controller -n argocd ARGOCD_DEFAULT_CACHE_EXPIRATION=12h`
  * AUTOMATICALLY, restart argocd-application-controller
* `kubectl exec -n argocd argocd-application-controller-0 -- env | grep ARGOCD_DEFAULT_CACHE_EXPIRATION`
  * 's return: ARGOCD_DEFAULT_CACHE_EXPIRATION=12h
* [source code](/util/cache/cache.go)'s `env.ParseDurationFromEnv("ARGOCD_DEFAULT_CACHE_EXPIRATION", 24*time.Hour, ...)`
  * by default, 24h

#### TODO: check where comes from (1) == live watch, (2) == polling, (3) == refresh

## Git webhooks
TODO:

## MANUAL refresh
TODO:

# TODO:
* TODO:

* [ignoreResourceUpdatesOwnArgoCDApplicationConfigMap.yaml](ignoreResourceUpdatesOwnArgoCDApplicationConfigMap.yaml)
  * ignore resource updates -- of -- own Argo CD's Application

# Ignoring updates for untracked resources
* [cronJob.yaml](cronJob.yaml)

# default Configuration
## metadata fields / ALWAYS ignored | ALL resources -- via -- `ignoreResourceUpdates` & `ignoreDifferences`
### `metadata.generation`
* [source code](/util/settings/settings.go)'s `GetIgnoreResourceUpdatesOverrides`
* `kubectl get deployment guestbook-ui -n guestbook -o jsonpath='generation={.metadata.generation}'`
  * 's return live state
* `argocd app manifests example.guestbook --source git | grep -cE "generation"`
  * 's return: 0
    * == NOTHING matched
* NO match BUT NOT out of sync
  * `argocd app diff example.guestbook`
    * 's return 0   == sync
  * `argocd app get  example.guestbook`
    * Sync Status:        Synced
### `metadata.resourceVersion`
* [source code](/util/settings/settings.go)'s `GetIgnoreResourceUpdatesOverrides`
* `kubectl get deployment guestbook-ui -n guestbook -o jsonpath='resourceVersion={.metadata.resourceVersion}'`
  * 's return live state
* `argocd app manifests example.guestbook --source git | grep -cE "generation"`
  * 's return: 0
    * == NOTHING matched
* NO match BUT NOT out of sync
  * `argocd app diff example.guestbook`
    * 's return 0   == sync
  * `argocd app get  example.guestbook`
    * Sync Status:        Synced
### `metadata.managedFields`
* [source code](/util/settings/settings.go)'s `GetIgnoreResourceUpdatesOverrides`
* `kubectl get deployment guestbook-ui -n guestbook -o jsonpath='managedFields={.metadata.managedFields[*].manager}'`
  * 's return live state
* `argocd app manifests example.guestbook --source git | grep -cE "generation"`
  * 's return: 0
    * == NOTHING matched
* NO match BUT NOT out of sync
  * `argocd app diff example.guestbook`
    * 's return 0   == sync
  * `argocd app get  example.guestbook`
    * Sync Status:        Synced



# TODO:
* TODO:
