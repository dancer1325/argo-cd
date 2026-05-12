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
* [install Argo CD](../../installation.md)
* recommendations
  * `kind create cluster` & `kind create cluster --name kind2` 

# TODO:

# Repositories
## 💡globally registered💡
* `argocd repo --help`
  * that's why it exists INDEPENDENTLY an Application
## | SOME Git hosters, | Application, set `spec.source.repoUrl: ...git`
TODO: check GitLab & on-premise GitLab instances
## TODO:

# Clusters
## Cluster credentials
### allows: ArgoCD can connect -- to -- Kubernetes cluster
* `kubectl config view --raw --context kind-kind2 -o jsonpath='{.users[?(@.name=="kind-kind2")].user}' | jq keys`
  * check type of keys
    * | Kind, == TLS
* `KIND2_IP=$(docker inspect kind2-control-plane --format '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}')`
* `CA_DATA=$(kubectl config view --raw -o jsonpath='{.clusters[?(@.name=="kind-kind2")].cluster.certificate-authority-data}')`
* `CERT_DATA=$(kubectl config view --raw -o jsonpath='{.users[?(@.name=="kind-kind2")].user.client-certificate-data}')`
* `KEY_DATA=$(kubectl config view --raw -o jsonpath='{.users[?(@.name=="kind-kind2")].user.client-key-data }')`
* `kubectl apply -f clusterSecret.yaml`
* `argocd cluster list`
  * recognize the kind2 cluster
* `argocd app create -f applicationInCluster2.yaml`
  * `argocd app list` & `argocd app get test-kind2`
    * Application is deployed | kind cluster
* `argocd app sync test-kind2`
  * `kubectl get all -n default --context kind-kind2`
    * check k8s resources are deployed | cluster kind2
### 💡are stored | secrets💡
* [here](clusterSecret.yaml)
### ❌MANUAL ALTERNATIVE NOT recommended / WITHOUT using credentials❌
* `kubectl config use-context kind-kind`
* `ARGOCD_PASSWORD=$(kubectl get secret argocd-initial-admin-secret -n argocd -o jsonpath='{.data.password}' | base64 -d)`
  * export Argo CD password
* create configMap / has cluster configurations
  * `kind get kubeconfig --name kind2 > /tmp/kind2-kubeconfig`
    * copy Kube config file
* `KIND2_IP=$(docker inspect kind2-control-plane --format '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}')`
  * export a kind2's internal IP
* `sed -i '' "s|server: https://.*:.*|server: https://$KIND2_IP:6443|g" /tmp/kind2-kubeconfig`
  * | the copied kube config file,
    * update the kind2's server  
* `kubectl create configmap kind2-kubeconfig --from-file=config=/tmp/kind2-kubeconfig -n argocd`
* `kubectl apply -f podWithArgoCD.yaml`
* `kubectl -n argocd exec -it argocd-cli -- sh`
  * `argocd login argocd-server.argocd.svc.cluster.local --insecure --username admin --password <PREVIOUS_EXPORTED_PASSWORD>`
  * `argocd cluster add kind-kind2 --insecure`
  * 's return succeed
  * `exit`
## Skipping Cluster Reconciliation
* `kubectl -n argocd annotate secret mycluster-secret argocd.argoproj.io/skip-reconcile="true"`
* `argocd app create -f applicationInCluster2.yaml`
* `kubectl rollout restart -n argocd statefulset argocd-application-controller`
* `argocd app sync test-kind2`
* `kubectl get all --context kind-kind2`
* `argocd app get test-kind2`
* `kubectl scale deployment guestbook-ui --replicas=5 --context kind-kind2`
  * force the drift BETWEEN GitOps & cluster state
* `argocd app get test-kind2`
  TODO: 

# Resource Exclusion/Inclusion
## -- from -- discovery & sync
TODO:
## those / ALWAYS excluded
* [source code](/util/settings/filtered_resource.go)'s `coreExcludedResources`
* TODO: | running Argo CD
## use cases
### resources / impacts Argo CD's performance
TODO:
## steps
* `kubectl patch configmap argocd-cm -n argocd --type merge --patch-file patchArgoCDCMResourceExclusionInclusion.yaml`
* TODO: 
## final list of resources == group/kinds / specified | `resource.inclusions` - group/kinds / specified | `resource.exclusions`
* TODO:
## if you add a inclusion / matches EXISTING resources -> these resources appear as `OutOfSync`
* TODO:
## recommendations
### | your YAML, if you use `SOME_GLOB` -> wrap it ('') == `'SOME_GLOB'`
* TODO:
### if you add a exclusion | ALREADY EXISTING resource -> restart the controller
* TODO:


# TODO:

* TODO:

# "self-managed" Argo CD
## == 💡Argo CD is managed -- by -- Argo CD 💡
* prepare stack / deploy SAME Argo CD / you are going to track
  * `kubectl create namespace argocd`
  * `kubectl apply -n argocd --server-side --force-conflicts -k https://github.com/dancer1325/argo-cd/manifests/cluster-install`
* `kubectl apply -f applicationToMonitorArgoCD.yaml`
* `kubectl port-forward svc/argocd-server -n argocd 8080:443`
  * port-forward "argocd-server" locally
* `kubectl get secret argocd-initial-admin-secret -n argocd -o jsonpath='{.data.password}' | base64 -d`
  * copy the password
* https://localhost:8080/
  * login
    * user: admin
    * password: previouslyCopiedPassword
  * \> Applications > argocd
