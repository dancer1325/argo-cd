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
* [install Argo CD cluster-scoped](../installation.md)
* deploy [example apps](https://github.com/dancer1325/argocd-example-apps/blob/master/apps/README.md)

# allow: grouping logically applications
* `kubectl get secret argocd-initial-admin-secret -n argocd -o jsonpath='{.data.password}' | base64 -d`
  * get admin password
* `kubectl apply -f appProject.yaml`
* `kubectl apply -f applicationInProject.yaml`
* ways to check
  * ArgoCD UI
    * https://localhost:8080/
      * user: admin
      * password: <PREVIOUS_GOT_ADMIN_PASSWORD>
      * | left panel,
        * project: example-project
          * see ONLY "guestbook-in-project" Application is displayed
  * ArgoCD cli 
    * `argocd login locahost:8080 --insecure`
      * user: admin
      * password: <PREVIOUS_GOT_ADMIN_PASSWORD>
    * `argocd app list --project example-project`
      * see ONLY "guestbook-in-project" Application is displayed
## ⚠️ALL application -- belongs to -- 1! project ⚠️
* specified | Kind: Application's `.spec.project`
  * see [applicationInProject.yaml](applicationInProject.yaml)
  * if NOT specified -> belong to default

# use cases: Argo CD -- is used by -- MULTIPLE teams
* `kubectl create namespace frontend` && `kubectl create namespace backend`
* `kubectl apply -f multipleTeamsAppProjects.yaml`
* `kubectl apply -f multipleTeamsApplications.yaml`
* ApplicationS are isolated
  * `argocd app list --project team-frontend`
  * `argocd app list --project team-backend`
* if you try to deploy the ArgoCD Application | namespace / NOT ALLOWED by the project -> error 
  * `argocd app set frontend-app --dest-namespace backend`
    * 's return: PermissionDenied

# features
## restrict what may be deployed -- via -- `spec.sourceRepos`
* `kubectl apply -f applicationInProject.yaml`
* https://localhost:8080/applications
  * projects: example-project
  * \> guestbook-notallowed-to-deploy-project-dueto-sourcerepo
    * check the Error & read the message: "InvalidSpecError
      application repo https://github.com/argoproj/argocd-example-apps.git is not permitted in project 'example-project'"
## restrict destination clusters & namespaces | apps -- may be -- deployed
* `kubectl create namespace notcontainedinproject`
* `kubectl apply -f applicationInProject.yaml`
* https://localhost:8080/applications
  * projects: example-project
  * \> guestbook-notallowed-to-deploy-project-dueto-destination
      * check the Error & read the message: "application destination server 'https://kubernetes.default.svc' and namespace 'notcontainedinproject' do not match any of the allowed destinations in project 'example-project'"
## restrict the kinds of objects may be deployed
* `kubectl apply -f appProject.yaml`
* `kubectl apply -f applicationInProject.yaml`
* https://localhost:8080/applications
  * projects: example-namespaceresourcewhiteandblacklist-project
  * \> guestbook-restrictions-dueto--namespaceblackorwhitelist
    * | Service,
      * check the Error & read the message: "Resource not found in cluster: v1/Service:guestbook-ui"
    * | Deployment,
      * deployed correctly
## define project roles -- to provide -- application RBAC
* [here](#project-roles)

# default project
## if unspecified (ONLY -- through -- `argocd`) -> an application -- belongs to the -- default project
### -- via -- declaratively
* `kubectl apply -f applicationWithoutSpecifyingProject.yaml`
  * 's return the error: "The Application "guestbook-without-specifying-project" is invalid: spec.project: Required value"
### -- via -- ArgoCD UI
* https://localhost:8080/
  * user: admin
  * password: 
  * Applications > New 
    * | General,
      * application name: no-project
    * | Source,
      * repository url: https://github.com/dancer1325/argocd-example-apps.git
      * path: guestbook
    * | Destination,
      * cluster url: https://kubernetes.default.svc
      * namespace: argocd
    * Create
      * 's return error message: "Project Name is required"
### -- via -- `argocd`
* `argocd login localhost:8080 --insecure`
  * user: admin
  * password: <PREVIOUSLY_GOT_PASSWORD>
* `argocd app create my-app  --repo https://github.com/argoproj/argocd-example-apps.git --path guestbook --dest-server https://kubernetes.default.svc --dest-namespace argocd`
* `argocd app get my-app -o json | grep project`
  * 's return: default
## created AUTOMATICALLY
* | IMMEDIATELY AFTER installing ArgoCD,
  * `argocd proj list`
    * 's return: at least default
### ORIGINALLY (== | install), MOST permissive
* ways to check
  * -- via -- `argocd`
    * `argocd proj get default`
  * -- via -- ArgoCD UI
    * https://localhost:8080/settings/projects/default?tab=summary
## allows
### from ANY source repo -- deployments to -- ANY cluster
* ALL BEFORE resources were deployed
* `argo proj get default`
  * 's return: "Destinations:                *,*"
### ALL resource Kinds
* ALL BEFORE resources were deployed
* `argo proj get default`
  * 's return: "Allowed Cluster Resources:   */*"
### being modified
* FIRST, make NEXT subsection
* bootstrap a [NEW cluster](#requirements)
* `argocd proj set default --src 'https://github.com/dancer1325/argocd-example-apps.git'`
* `argocd proj get default`
#### ❌if there are applications / using it & you edit / stop matching it -> it can NOT be modified❌
* using ALL projects & apps created so far
* `argocd proj set default --src 'https://github.com/dancer1325/argocd-example-apps.git'`
  * 's return: error'
#### ❌NOT deleted ❌
* `argocd proj delete default`
  * 's return: "InvalidArgument desc = name 'default' is reserved and cannot be deleted"
## if you want to remove ALL `default` project's permissions  -> apply a manifest | namespace / Argo CD is installed
* `kubectl apply -f appProjectWithMostPermissivePermissions.yaml -n argocd`
* `argocd proj get default`
  * 's return: "Denied Namespaced Resources: */*"

# how to create projects?
* follow mentioned steps

# how to manage (modify) projects? 
## -- via -- `argocd`
```bash
argocd proj add-source default https://github.com/argocd/argocd-example-apps.git
argocd proj remove-source default https://github.com/argocd/argocd-example-apps.git
```
## -- via -- ArgoCD UI


# how to assign the Application -- to -- a project?
## declaratively
* done here -- through -- `kubectl apply ...`
## `argocd`
* TODO:
* argocd app set APPLICATION_NAME --project PROJECT_NAME
## ArgoCD UI
* TODO:

# TODO:

# Project Roles
TODO:

# TODO: