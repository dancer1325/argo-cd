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

# RBAC 
## requirements: >=1 local user OR SSO configuration
* Reason:🧠OTHERWISE, ONLY exist built-in admin / ACCESS -- to -- ALL🧠

## RBAC Model
### model syntax
#### is -- based on -- Casbin
* check [builtin-policy.csv](/assets/builtin-policy.csv)
#### types of syntax
* check [builtin-policy.csv](/assets/builtin-policy.csv)

### Policy
#### allows: assign permissions -- to an -- entity
* check built-in admin rights
  * `argocd admin settings rbac can admin get applications --namespace argocd`
  * ...
#### `p, <role/user/group>, <resource>, <action>, <object>, <effect>`
##### -- for -- `role`
* [builtin-policy.csv](/assets/builtin-policy.csv)
  * check it uses `role:` prefix
##### -- for -- `user`
* [patchArgoCDRBACCMWithApplicationSpecificPolicy.yaml](patchArgoCDRBACCMWithApplicationSpecificPolicy.yaml)
##### -- for -- `group`
* TODO: 
##### `<object>` 
###### 's format -- , depend on the -- resource
* check rest of below resources section
##### `<effect>`
###### ALLOWED values
* [patchArgoCDRBACCMWithApplicationSpecificPolicy.yaml](patchArgoCDRBACCMWithApplicationSpecificPolicy.yaml)
  * check `deny` & `allow` effect

### `g, <user/group>, <role>`
#### user
* `kubectl patch configmap argocd-cm -n argocd --type merge --patch-file patchLocalExampleUser.yaml`
* `argocd account update-password --account reader-user`
  * admin's password:
  * example-user's new password: aaaaaaaa
* `kubectl patch configmap argocd-rbac-cm -n argocd --type merge --patch-file patchArgoCDRBACCMWithApplicationSpecificPolicy.yaml`
  * `kubectl describe cm/argocd-rbac-cm -n argocd`
#### group
TODO:

### actions / EACH [resource

```
# --- applications (get ✅, create ✅, update ✅, delete ✅, sync ✅, action ✅, override ✅, invoke ❌) ---
## yes
argocd admin settings rbac can role:admin get applications --namespace argocd
argocd admin settings rbac can role:admin create applications --namespace argocd
argocd admin settings rbac can role:admin update applications --namespace argocd
argocd admin settings rbac can role:admin delete applications --namespace argocd
argocd admin settings rbac can role:admin sync applications --namespace argocd
argocd admin settings rbac can role:admin action applications --namespace argocd
argocd admin settings rbac can role:admin override applications --namespace argocd
## no
argocd admin settings rbac can role:admin invoke applications --namespace argocd

# --- applicationsets (get ✅, create ✅, update ✅, delete ✅, sync ❌, action ❌, override ❌, invoke ❌) ---
## yes
argocd admin settings rbac can role:admin get applicationsets --namespace argocd
argocd admin settings rbac can role:admin create applicationsets --namespace argocd
argocd admin settings rbac can role:admin update applicationsets --namespace argocd
argocd admin settings rbac can role:admin delete applicationsets --namespace argocd
## no
argocd admin settings rbac can role:admin sync applicationsets --namespace argocd
argocd admin settings rbac can role:admin action applicationsets --namespace argocd
argocd admin settings rbac can role:admin override applicationsets --namespace argocd
argocd admin settings rbac can role:admin invoke applicationsets --namespace argocd

# --- clusters (get ✅, create ✅, update ✅, delete ✅, sync ❌, action ❌, override ❌, invoke ❌) ---
## yes
argocd admin settings rbac can role:admin get clusters --namespace argocd
argocd admin settings rbac can role:admin create clusters --namespace argocd
argocd admin settings rbac can role:admin update clusters --namespace argocd
argocd admin settings rbac can role:admin delete clusters --namespace argocd
## no
argocd admin settings rbac can role:admin sync clusters --namespace argocd
argocd admin settings rbac can role:admin action clusters --namespace argocd
argocd admin settings rbac can role:admin override clusters --namespace argocd
argocd admin settings rbac can role:admin invoke clusters --namespace argocd

# --- projects (get ✅, create ✅, update ✅, delete ✅, sync ❌, action ❌, override ❌, invoke ❌) ---
## yes
argocd admin settings rbac can role:admin get projects --namespace argocd
argocd admin settings rbac can role:admin create projects --namespace argocd
argocd admin settings rbac can role:admin update projects --namespace argocd
argocd admin settings rbac can role:admin delete projects --namespace argocd
## no
argocd admin settings rbac can role:admin sync projects --namespace argocd
argocd admin settings rbac can role:admin action projects --namespace argocd
argocd admin settings rbac can role:admin override projects --namespace argocd
argocd admin settings rbac can role:admin invoke projects --namespace argocd

# --- repositories (get ✅, create ✅, update ✅, delete ✅, sync ❌, action ❌, override ❌, invoke ❌) ---
## yes
argocd admin settings rbac can role:admin get repositories --namespace argocd
argocd admin settings rbac can role:admin create repositories --namespace argocd
argocd admin settings rbac can role:admin update repositories --namespace argocd
argocd admin settings rbac can role:admin delete repositories --namespace argocd
## no
argocd admin settings rbac can role:admin sync repositories --namespace argocd
argocd admin settings rbac can role:admin action repositories --namespace argocd
argocd admin settings rbac can role:admin override repositories --namespace argocd
argocd admin settings rbac can role:admin invoke repositories --namespace argocd

# --- accounts (get ✅, create ❌, update ✅, delete ❌, sync ❌, action ❌, override ❌, invoke ❌) ---
## yes
argocd admin settings rbac can role:admin get accounts --namespace argocd
argocd admin settings rbac can role:admin update accounts --namespace argocd
## no
argocd admin settings rbac can role:admin create accounts --namespace argocd
argocd admin settings rbac can role:admin delete accounts --namespace argocd
argocd admin settings rbac can role:admin sync accounts --namespace argocd
argocd admin settings rbac can role:admin action accounts --namespace argocd
argocd admin settings rbac can role:admin override accounts --namespace argocd
argocd admin settings rbac can role:admin invoke accounts --namespace argocd

# --- certificates (get ✅, create ✅, update ❌, delete ✅, sync ❌, action ❌, override ❌, invoke ❌) ---
## yes
argocd admin settings rbac can role:admin get certificates --namespace argocd
argocd admin settings rbac can role:admin create certificates --namespace argocd
argocd admin settings rbac can role:admin delete certificates --namespace argocd
## no
argocd admin settings rbac can role:admin update certificates --namespace argocd
argocd admin settings rbac can role:admin sync certificates --namespace argocd
argocd admin settings rbac can role:admin action certificates --namespace argocd
argocd admin settings rbac can role:admin override certificates --namespace argocd
argocd admin settings rbac can role:admin invoke certificates --namespace argocd

# --- gpgkeys (get ✅, create ✅, update ❌, delete ✅, sync ❌, action ❌, override ❌, invoke ❌) ---
## yes
argocd admin settings rbac can role:admin get gpgkeys --namespace argocd
argocd admin settings rbac can role:admin create gpgkeys --namespace argocd
argocd admin settings rbac can role:admin delete gpgkeys --namespace argocd
## no
argocd admin settings rbac can role:admin update gpgkeys --namespace argocd
argocd admin settings rbac can role:admin sync gpgkeys --namespace argocd
argocd admin settings rbac can role:admin action gpgkeys --namespace argocd
argocd admin settings rbac can role:admin override gpgkeys --namespace argocd
argocd admin settings rbac can role:admin invoke gpgkeys --namespace argocd

# --- logs (get ✅, create ❌, update ❌, delete ❌, sync ❌, action ❌, override ❌, invoke ❌) ---
## yes
argocd admin settings rbac can role:admin get logs --namespace argocd
## no
argocd admin settings rbac can role:admin create logs --namespace argocd
argocd admin settings rbac can role:admin update logs --namespace argocd
argocd admin settings rbac can role:admin delete logs --namespace argocd
argocd admin settings rbac can role:admin sync logs --namespace argocd
argocd admin settings rbac can role:admin action logs --namespace argocd
argocd admin settings rbac can role:admin override logs --namespace argocd
argocd admin settings rbac can role:admin invoke logs --namespace argocd

# --- exec (get ❌, create ✅, update ❌, delete ❌, sync ❌, action ❌, override ❌, invoke ❌) ---
## yes
argocd admin settings rbac can role:admin create exec --namespace argocd
## no
argocd admin settings rbac can role:admin get exec --namespace argocd
argocd admin settings rbac can role:admin update exec --namespace argocd
argocd admin settings rbac can role:admin delete exec --namespace argocd
argocd admin settings rbac can role:admin sync exec --namespace argocd
argocd admin settings rbac can role:admin action exec --namespace argocd
argocd admin settings rbac can role:admin override exec --namespace argocd
argocd admin settings rbac can role:admin invoke exec --namespace argocd

# --- extensions (get ❌, create ❌, update ❌, delete ❌, sync ❌, action ❌, override ❌, invoke ✅) ---
## yes
argocd admin settings rbac can role:admin invoke extensions --namespace argocd
## no
argocd admin settings rbac can role:admin get extensions --namespace argocd
argocd admin settings rbac can role:admin create extensions --namespace argocd
argocd admin settings rbac can role:admin update extensions --namespace argocd
argocd admin settings rbac can role:admin delete extensions --namespace argocd
argocd admin settings rbac can role:admin sync extensions --namespace argocd
argocd admin settings rbac can role:admin action extensions --namespace argocd
argocd admin settings rbac can role:admin override extensions --namespace argocd
```

### application-specific policy -- `<object>` == `<app-project>/<app-name>` -- 
#### ALLOWED |
##### `applications` resource

```
# yes
argocd admin settings rbac can admin get applications 'default/example.guestbook' --namespace argocd
argocd admin settings rbac can admin create applications 'default/example.guestbook' --namespace argocd
argocd admin settings rbac can admin update applications 'default/example.guestbook' --namespace argocd
argocd admin settings rbac can admin delete applications 'default/example.guestbook' --namespace argocd
argocd admin settings rbac can admin sync applications 'default/example.guestbook' --namespace argocd
argocd admin settings rbac can admin action applications 'default/example.guestbook' --namespace argocd
argocd admin settings rbac can admin override applications 'default/example.guestbook' --namespace argocd
```

##### `applicationsets` resource

```
# yes
argocd admin settings rbac can admin get applicationsets 'default/example.appset' --namespace argocd
argocd admin settings rbac can admin create applicationsets 'default/example.appset' --namespace argocd
argocd admin settings rbac can admin update applicationsets 'default/example.appset' --namespace argocd
argocd admin settings rbac can admin delete applicationsets 'default/example.appset' --namespace argocd
```

##### `logs` resource

```
# yes
argocd admin settings rbac can admin get logs 'default/example.guestbook' --namespace argocd
```

##### `exec` resource

```
# yes
argocd admin settings rbac can admin create exec 'default/example.guestbook' --namespace argocd
```

#### | ANY Namespaces -- `<object>` == `<app-project>/<app-ns>/<app-name>` --
TODO: 

#### TODO: 
TODO: 

### `logs` resource
#### allows: seeing pod's logs
* | browser,
  * https://localhost:8080/
    * user: amdin
    * password
    * Applications > example.guestbook > somePod > logs

### `exec` resource
#### allows: | ArgoCD UI, user can `exec` | Pods
* `kubectl patch configmap argocd-cm -n argocd --type merge --patch-file patchEnableExec.yaml`
* | browser,
  * https://localhost:8080/
    * user: amdin
    * password
    * Applications > example.guestbook > somePod > Terminal
* ⚠️| local, 
  * MULTIPLE errors⚠️

### 
TODO:

## 👀| configure RBAC, main components 👀
### "argocd-rbac-cm" configMap
* `kubectl describe cm argocd-rbac-cm -n argocd`
  * empty
* check -- via -- `argocd admin settings rbac can ROLE/SUBJECT ACTION RESOURCE [SUB-RESOURCE] [FLAGS]`
  * run [ALL policy rules](/assets/builtin-policy.csv) / return: Yes

  ```
  # -- role:readonly --
  argocd admin settings rbac can role:readonly get applications --namespace argocd
  argocd admin settings rbac can role:readonly get applicationsets --namespace argocd
  argocd admin settings rbac can role:readonly get certificates --namespace argocd
  argocd admin settings rbac can role:readonly get clusters --namespace argocd
  argocd admin settings rbac can role:readonly get repositories --namespace argocd
  argocd admin settings rbac can role:readonly get write-repositories --namespace argocd
  argocd admin settings rbac can role:readonly get projects --namespace argocd
  argocd admin settings rbac can role:readonly get accounts --namespace argocd
  argocd admin settings rbac can role:readonly get gpgkeys --namespace argocd
  argocd admin settings rbac can role:readonly get logs --namespace argocd
  
  # -- role:admin -- applications
  argocd admin settings rbac can role:admin create applications --namespace argocd
  argocd admin settings rbac can role:admin update applications --namespace argocd
  argocd admin settings rbac can role:admin delete applications --namespace argocd
  argocd admin settings rbac can role:admin sync applications --namespace argocd
  argocd admin settings rbac can role:admin override applications --namespace argocd
  # -- role:admin -- applicationsets
  argocd admin settings rbac can role:admin get applicationsets --namespace argocd
  argocd admin settings rbac can role:admin create applicationsets --namespace argocd
  argocd admin settings rbac can role:admin update applicationsets --namespace argocd
  argocd admin settings rbac can role:admin delete applicationsets --namespace argocd
  # -- role:admin -- certificates
  argocd admin settings rbac can role:admin create certificates --namespace argocd
  argocd admin settings rbac can role:admin update certificates --namespace argocd
  argocd admin settings rbac can role:admin delete certificates --namespace argocd
  # -- role:admin -- clusters
  argocd admin settings rbac can role:admin create clusters --namespace argocd
  argocd admin settings rbac can role:admin update clusters --namespace argocd
  argocd admin settings rbac can role:admin delete clusters --namespace argocd
  # -- role:admin -- repositories
  argocd admin settings rbac can role:admin create repositories --namespace argocd
  argocd admin settings rbac can role:admin update repositories --namespace argocd
  argocd admin settings rbac can role:admin delete repositories --namespace argocd
  # -- role:admin -- write-repositories
  argocd admin settings rbac can role:admin create write-repositories --namespace argocd
  argocd admin settings rbac can role:admin update write-repositories --namespace argocd
  argocd admin settings rbac can role:admin delete write-repositories --namespace argocd
  # -- role:admin -- projects
  argocd admin settings rbac can role:admin create projects --namespace argocd
  argocd admin settings rbac can role:admin update projects --namespace argocd
  argocd admin settings rbac can role:admin delete projects --namespace argocd
  # -- role:admin -- accounts
  argocd admin settings rbac can role:admin update accounts --namespace argocd
  # -- role:admin -- gpgkeys
  argocd admin settings rbac can role:admin create gpgkeys --namespace argocd
  argocd admin settings rbac can role:admin delete gpgkeys --namespace argocd
  # -- role:admin -- exec
  argocd admin settings rbac can role:admin create exec --namespace argocd
  
  # -- role:admin inherits role:readonly (g, role:admin, role:readonly) --
  argocd admin settings rbac can role:admin get applications --namespace argocd
  argocd admin settings rbac can role:admin get clusters --namespace argocd
  argocd admin settings rbac can role:admin get logs --namespace argocd
  
  # -- admin user has role:admin (g, admin, role:admin) --
  argocd admin settings rbac can admin sync applications --namespace argocd
  argocd admin settings rbac can admin delete clusters --namespace argocd
  ```

#### apply | specified policy rule's resource
* [built-in policy](/assets/builtin-policy.csv)
### AppProject's roles
* [here](/docs/user-guide/projects.md)

## steps
### define & apply RBAC roles
* [application-specific-policy.csv](application-specific-policy.csv)
  * ❌can NOT be applied DIRECTLY❌
* `kubectl patch configmap argocd-rbac-cm -n argocd --type merge --patch-file patchArgoCDRBACCMWithApplicationSpecificPolicy.yaml`
  * `kubectl describe cm/argocd-rbac-cm -n argocd` 
  * check the policies

  ```
  # | applications
  ## yes
  argocd admin settings rbac can example-user get applications --namespace argocd
  ## no
  argocd admin settings rbac can example-user delete applications --namespace argocd
  argocd admin settings rbac can example-user create applications --namespace argocd
  
  # logs
  ## yes
  argocd admin settings rbac can example-user get logs example-project/my-app --namespace argocd
  ## no
  argocd admin settings rbac can example-user get logs --namespace argocd
  argocd admin settings rbac can example-user get applications --namespace argocd
  ```
### map SSO groups OR local users -- to -- roles
* [deploy locally example apps](https://github.com/dancer1325/argocd-example-apps/tree/master/apps#steps)
* `kubectl get secret argocd-initial-admin-secret -n argocd -o jsonpath='{.data.password}' | base64 -d`
  * 's return: admin's password
* `kubectl patch configmap argocd-cm -n argocd --type merge --patch-file patchLocalExampleUser.yaml`
* `argocd account update-password --account example-user`
  * admin's password:
  * example-user's new password: aaaaaaaa
* `argocd login localhost:8080 --insecure`
  * user: example-user
  * password: aaaaaaaa
* https://localhost:8080/
  * user: example-user
  * password: aaaaaaaa
  * ONLY view default/example.guestbook

# Built-in 
## RBAC Roles
### `role:readonly`
* `argocd admin settings rbac can role:readonly ...`
  * [here](#argocd-rbac-cm-configmap)
#### read-only access -- to -- ALL resources
```
# no
argocd admin settings rbac can role:readonly create applications --namespace argocd
argocd admin settings rbac can role:readonly delete applicationsets --namespace argocd
...
```
### `role:admin`
* `argocd admin settings rbac can role:admin ...`
  * [here](#argocd-rbac-cm-configmap)
#### unrestricted access -- to -- ALL resources
```
# yes
argocd admin settings rbac can role:admin create applications --namespace argocd
argocd admin settings rbac can role:admin delete applicationsets --namespace argocd
...
```

# default policy
## | "argocd-rbac-cm" ConfigMap, `data.policy.default`
### OPTIONAL
#### if it's omitted OR empty -> users
* `kubectl describe cm/argocd-rbac-cm -n argocd`
  * check there is NO data -- about -- `data.policy.default`
    * OTHERWISE,
      * | [patchArgoCDRBACCMWithApplicationSpecificPolicy.yaml](patchArgoCDRBACCMWithApplicationSpecificPolicy.yaml),
        * remove it
      * `kubectl patch configmap argocd-rbac-cm -n argocd --type merge --patch-file patchArgoCDRBACCMWithApplicationSpecificPolicy.yaml`
* create a local user "user-without-role" / has NO roles
  * `kubectl patch configmap argocd-cm -n argocd --type merge --patch-file patchLocalExampleUser.yaml`
  * `argocd account update-password --account user-without-role`
    * admin's password:
    * user-without-role's new password: aaaaaaaa
##### STILL can login
* https://localhost:8080/
  * user: user-without-role
  * password: aaaaaaaa
##### NO see apps, projects, etc...
* AFTER login it
  * NO see apps, projects, ..
### == default role name / Argo CD will falls back to | authenticated user has NO specific role
* `kubectl patch configmap argocd-rbac-cm -n argocd --type merge --patch-file patchArgoCDRBACCMWithApplicationSpecificPolicy.yaml`
* https://localhost:8080/
  * user: user-without-role
  * password: aaaaaaaa
  * see ALL the Applications
  * ❌BUT can NOT see the logs❌
### can NOT be blocked -- by a -- `deny` rule
* `kubectl describe cm/argocd-rbac-cm -n argocd`
  * check there is NO policy rule `p, user-without-role, applications, get, */*, deny`
    * OTHERWISE,
      * | [patchArgoCDRBACCMWithApplicationSpecificPolicy.yaml](patchArgoCDRBACCMWithApplicationSpecificPolicy.yaml),
        * remove it
      * `kubectl patch configmap argocd-rbac-cm -n argocd --type merge --patch-file patchArgoCDRBACCMWithApplicationSpecificPolicy.yaml`
* https://localhost:8080/
  * user: user-without-role
  * password: aaaaaaaa
  * STILL can see the applications
### recommendations: create a NEW `role:authenticated` / minimum set of permissions
* | [patchArgoCDRBACCMWithApplicationSpecificPolicy.yaml](patchArgoCDRBACCMWithApplicationSpecificPolicy.yaml),
  * see the definition `p, role:readonlyapplications, applications, get, */*, allow`

# Anonymous Access
* `kubectl patch configmap argocd-cm -n argocd --type merge --patch-file patchAnonymousUser.yaml`
* | browser,
  * https://localhost:8080/applications
    * NO login required
  * https://localhost:8080/user-info
    * "You are not logged in"
      * == anonymous user

# TODO:
### Application-Specific Policy

* [application-specific-policy.csv](application-specific-policy.csv)
  * `p, <role/user/group>, <resource>, <action>, <object>, <effect>`  
    * `<object>` == `<app-project>/<app-name>`

#### | ANY Namespaces

* [application-specific-policy-any-namespace.csv](application-specific-policy-any-namespace.csv)
  * `p, <role/user/group>, <resource>, <action>, <object>, <effect>`
    * `<object>` == `<app-project>/<app-ns>/<app-name>`

## -- via -- 
### Local Users/Accounts

* _Examples:_
  * `p, my-local-user, applications, sync, my-project/*, allow`
    * assign a policy DIRECTLY -- to a -- local user
  * `g, my-local-user, role:admin`
    * assign a role -- to a -- local user

### SSO Users/Groups