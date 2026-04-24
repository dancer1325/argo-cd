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
### you can ALSO do negations -- via -- `!`
* `kubectl apply -f appProjectWithSourceRepoNegations.yaml`
  * `argocd project get appproject-with-sourcerepo-negations`
    * check it exists & it contains negation
* `kubectl apply -f applicationInProject.yaml`
  * MAYBE you need to remove & create again
* `argocd app get guestbook-notallowed-to-deploy-project-dueto-sourcereponegations`
  * 's message: "InvalidSpecError  Application referencing project appproject-with-sourcerepo-negations which does not exist"
#### `!*` ❌NOT useful❌
* `kubectl apply -f appProjectWithSourceRepoNegations.yaml -n argocd`
  * `argocd proj get appproject-with-sourcerepo-negations-all` check that it exists
* `argocd app list --project appproject-with-sourcerepo-negations-all`
  * there are NO Applications / belong to this appProject
#### ⚠️requirements / Application's `spec.source.repoUrl` is valid⚠️
* `kubectl apply -f appProjectWithSourceRepoNegations.yaml`
* `kubectl apply -f applicationInProject.yaml`
* `argocd app get guestbook-allowed`
  * check it's running
## restrict destination clusters & namespaces | apps -- may be -- deployed
* `kubectl create namespace notcontainedinproject`
* `kubectl apply -f applicationInProject.yaml`
* https://localhost:8080/applications
  * projects: example-project
  * \> guestbook-notallowed-to-deploy-project-dueto-destination
      * check the Error & read the message: "application destination server 'https://kubernetes.default.svc' and namespace 'notcontainedinproject' do not match any of the allowed destinations in project 'example-project'"
### you can ALSO do negations -- via -- `!`
* `kubectl apply -f appProjectWithDestinationNegations.yaml`
  * `argocd project get appproject-with-destination-negations`
    * check it exists & it contains negation
* `kubectl apply -f applicationInProject.yaml`
  * MAYBE you need to remove & create again
* `argocd app get guestbook-notallowed-to-deploy-project-dueto-sourcereponegations`
  * 's message: "InvalidSpecError  Application referencing project appproject-with-sourcerepo-negations which does not exist"
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

# how to modify projects?
## ways
### -- via -- `argocd`
```bash
# check EXISTING configuration
argocd proj get new

# argocd proj add-source PROJECT URL
## if URL ALREADY valid -> NOT specified EXPLICITLY
argocd proj add-source default https://github.com/argocd/argocd-example-apps.git
## if URL NOT YET valid -> add it EXPLICITLY
argocd proj add-source new https://github.com/argocd/argocd-example-apps.git

# argocd proj remove-source PROJECT URL
## if URL NOT EXPLICITLY specified -> NOTHING is removed NOR denied
argocd proj remove-source default https://github.com/argocd/argocd-example-apps.git
## if URL EXPLICITLY specified -> it's removed
argocd proj remove-source new https://github.com/argocd/argocd-example-apps.git

# argocd proj add-destination PROJECT SERVER NAMESPACE OR argocd proj add-destination PROJECT NAME NAMESPACE --name
argocd proj add-destination new https://kubernetes.default.svc default

# argocd proj remove-destination PROJECT SERVER NAMESPACE
argocd proj remove-destination new https://kubernetes.default.svc default

# argocd proj allow-cluster-resource PROJECT GROUP KIND [NAME] [FLAG]
argocd proj allow-cluster-resource new "" pod

# argocd proj deny-namespace-resource PROJECT GROUP KIND [FLAG]
#   add /pod  | Denied Namespaced Resources
argocd proj deny-namespace-resource new "" pod

# argocd proj allow-namespace-resource PROJECT GROUP KIND [FLAG]
#   remove /pod  | Denied Namespaced Resources
#     restricted -- via a -- deny list
argocd proj allow-namespace-resource new "" pod

# argocd proj allow-cluster-resource PROJECT GROUP KIND
#   add /pod  | Allowed Cluster Resources
argocd proj allow-cluster-resource new "" pod

# argocd proj allow-namespace-resource PROJECT GROUP KIND [FLAG]
#   remove /pod  | Allowed Cluster Resources
#     restricted -- via a -- allowed list
argocd proj deny-cluster-resource new "" pod
```
### -- via -- ArgoCD UI
* https://localhost:8080/
  * user: admin
  * password: <PREVIOUS_GOT_ADMIN_PASSWORD>
  * settings > repository > edit
### declaratively
* modify something | this path's yaml
* `kubectl apply -f <FILE_NAME>.yaml`

# how to assign the Application -- to -- a project?
## declaratively
* done here -- through -- `kubectl apply ...`
## `argocd`
* [install ArgoCD Applications](https://github.com/dancer1325/argocd-example-apps/tree/master/apps)
* `argocd app list --project example-project`
* `argocd app set argocd/example.blue-green --project example-project`
## ArgoCD UI
* TODO:

# Project Roles
## allows: determining
### WHO
* -- through -- attaching the defined policy's role -- to -- user 
  * [appProjectWithroles.yaml](appProjectWithroles.yaml)
### WHAT can be done | applications / associated -- with the -- project
* -- through -- attaching the defined policy
  * [appProjectWithroles.yaml](appProjectWithroles.yaml)
## uses cases
### | CI pipeline, set RESTRICTED set of permissions / enable sync operations | 1! app
TODO: use [appProjectWithroles.yaml](appProjectWithroles.yaml)
### OIDC groups / restricted access
TODO: use [appProjectWithroles.yaml](appProjectWithroles.yaml)
## can 
### exist MULTIPLE projects roles / project
* [appProjectWithroles.yaml](appProjectWithroles.yaml)
### have MULTIPLE policies
* [appProjectWithroles.yaml](appProjectWithroles.yaml)
## -- bound to -- OIDC groups &/OR JWT tokens
* [appProjectWithroles.yaml](appProjectWithroles.yaml)
## ' policies
### == permissions / stored | role -- as a -- list(policy strings)
* [appProjectWithroles.yaml](appProjectWithroles.yaml)
### `p, proj:<PROJECT_NAME>:<ROLE_NAME>, <resource>, <action>, <object>, <effect>` == pattern
* [appProjectWithroles.yaml](appProjectWithroles.yaml)
## how to modify?
### declaratively
* modify [appProjectWithroles.yaml](appProjectWithroles.yaml)
* `kubectl apply -f appProjectWithroles.yaml`
### `argocd`
```
argocd proj role list sample-test-project

# ⚠️return ALL project's policies⚠️
##  ❌NOT ONLY project's role policies❌
argocd proj role get sample-test-project sample-test-project-role

# ⚠️ALTHOUGH you do NOT specify ANY policy -> by default create a policy / allow get the policy⚠️
argocd proj role create sample-test-project sample-test-project-role-two

argocd proj role create sample-test-project sample-test-project-role-two
# check it was deleted
argocd proj role list sample-test-project   

argocd proj role add-policy sample-test-project sample-test-project-role -a update -p allow -o logs
# check role's policy was created
argocd proj role get sample-test-project sample-test-project-role

argocd proj role remove-policy sample-test-project sample-test-project-role -a update -p allow -o logs
# check role's policy was removed
```
### ArgoCD UI
* https://localhost:8080/
  * user: admin
  * password: <PREVIOUS_GOT_ADMIN_PASSWORD>
  * Settings > Projects > choose 1 project (sample-test-project) > ADD ROLE (top bar button)
    * | General
      * role name: sample-another-role
      * role description: role created via UI
    * | Policy rules
      * applications, delete, sample-test-project/*, allow
    * | Group
      * (enter whatever) aaa
## JWT tokens / -- bound to a -- role
### allows: authenticate to a role
* `kubectl apply -f applicationInProject.yaml`
* `argocd proj role create-token sample-test-project sample-test-project-role`
  * copy the output token
    * eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJhcmdvY2QiLCJzdWIiOiJwcm9qOnNhbXBsZS10ZXN0LXByb2plY3Q6c2FtcGxlLXRlc3QtcHJvamVjdC1yb2xlIiwibmJmIjoxNzc3MDQ2MTQ2LCJpYXQiOjE3NzcwNDYxNDYsImp0aSI6ImZkZTExNDM5LTgxYWYtNGJkZC1iMDcyLTk4OTg0NzcxMWVlNyJ9.eN1isDKIDgfdGggWV-_UiLR1hJWJjcKvs6INQV70WPw
* `argocd app list --auth-token <TOKEN>`
  * list ONLY the Applications / allowed the sample-test-project-role
* `argocd app delete argocd/guestbook-projectrole-jwttoken --auth-token <TOKEN>`
  * 's return: 'PermissionDenied'
### | use it, evaluate DYNAMICALLY the ALLOWED policies
* comment [appProjectWithroles.yaml](appProjectWithroles.yaml)'s sample-test-project-role's `deny` effect
* `kubectl apply -f appProjectWithroles.yaml`
* `argocd app delete argocd/guestbook-projectrole-jwttoken --auth-token <TOKEN>`
  * RIGHT now, it worked
* `argocd app list --project sample-test-project`
  * 's return: empty
### ⚠️ONLY | being created, they can be retrieved⚠️
* `argocd proj role get sample-test-project sample-test-project-role`
  * NOT return's JWT value
### ways to be used
#### -- via -- CL's `--auth-token` flag
* `argocd app list --auth-token <TOKEN>`
#### set `ARGOCD_AUTH_TOKEN` environment variable
TODO:
### can be used UNTIL they
#### expire
* `argocd proj role create-token sample-test-project jwt-expiration-role --expires-in 3m`
  * copy the retunred token
* eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJhcmdvY2QiLCJzdWIiOiJwcm9qOnNhbXBsZS10ZXN0LXByb2plY3Q6and0LWV4cGlyYXRpb24tcm9sZSIsImV4cCI6MTc3NzA0OTQ5MCwibmJmIjoxNzc3MDQ5MzEwLCJpYXQiOjE3NzcwNDkzMTAsImp0aSI6IjM1ZGNjMGJmLTdiMDktNDI1Yy04MWZlLWNjN2ZkMmRlMTdlNiJ9.qNzp1mrPxdaI43rdVFOSF9YAzrQKfxrA4Cj22TfRvV0
* `argocd proj role get sample-test-project jwt-expiration-role --auth-token <TOKEN>`
  * return value
  * AFTER 3', if you re-trigger -> 's return: Unauthenticated desc
##### by default, NO expire
* `argocd proj role get sample-test-project sample-test-project-role`
  * check JWT Tokens / EXPIRES-AT == <none>
#### are revoked
* `argocd proj role get sample-test-project jwt-expiration-role`
  * 's return 2 JWT
* `argocd proj role delete-token sample-test-project jwt-expiration-role 1535390316`
* `argocd proj role get sample-test-project jwt-expiration-role`
  * 's return 1 JWT

# TODO: