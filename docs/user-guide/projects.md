## Projects

* Projects
  * allows
    * grouping logically applications
      * ⚠️ALL application -- belongs to -- 1! project ⚠️
  * use cases
    * Argo CD -- is used by -- MULTIPLE teams
      * _Example:_ DIFFERENT access level | namespaces / teams
  * features
    * restrict what may be deployed 
      * -- via -- `spec.sourceRepos`
        * you can ALSO do negations -- via -- `!`
          * `!*`
            * ❌NOT useful❌
          * ⚠️requirements / Application's `spec.source.repoUrl` is valid⚠️
            * allow source rule (== NOT contain `!`) permits the value
            * NO deny source rule (== contain `!`) rejects the value
    * restrict destination clusters & namespaces | apps -- may be -- deployed
      * -- via -- `spec.destinations`
        * you can ALSO do negations -- via -- `!`
          * ⚠️requirements / Application's `spec.destination` is valid⚠️
            * allow destination rule (== NOT contain `!`) permits the value
            * NO deny destinations rule (== contain `!`) rejects the value
    * restrict the kinds of objects may be deployed
      * _Example:_ RBAC, CRDs, DaemonSets, NetworkPolicy, ...
      * -- via -- `*ResourceWhitelist/Blacklist`
        * 👀if you want to check if a resource is cluster-scoped OR namespace-scoped -> `kubectl api-resources` & check column: "namespace"👀
    * define project roles -- to provide -- [application RBAC](../operator-manual/rbac.md)

### Default Project

* `default` project
  * [source code](/server/server.go)'s `initializeDefaultProject`
  * use cases
    * initial testing
    * if unspecified (ONLY -- through -- `argocd`) -> an application -- belongs to the -- default project
      * Reason why ONLY -- through -- `argocd`: 🧠declaratively & ArgoCD UI validate it beforehand🧠
  * created AUTOMATICALLY / 
    * ORIGINALLY (== | install), MOST permissive
        ```yaml
        spec:
          sourceRepos:
          - '*'
          destinations:
          - namespace: '*'
              server: '*'
          clusterResourceWhitelist:
          - group: '*'
              kind: '*'
        ```
  * allows
    * | ANY source repo -- deployments to -- ANY cluster
      * Reason: 🧠-- thanks to -- `spec.sourceRepos` & `spec.destinations`🧠
    * ALL resource Kinds 
      * Reason: 🧠-- thanks to -- `spec.clusterResourceWhitelist`🧠
    * being modified
      * ❌if there are applications / using it & you edit / stop matching it -> it can NOT be modified❌
      * ❌NOT deleted ❌
  * if you want to remove ALL `default` project's permissions  -> apply a manifest | namespace / Argo CD is installed
  * recommendations
    * create DEDICATED projects / EXPLICIT source + destination + resource permissions

### how to create projects & assign the Applications -- to a -- project?

* ways to ocreate projects
  * declaratively
  * ArgoCD UI
    * Settings > Projects > New
      * name: <SOME_NAME>
      * description: <SOME_DESCRIPTION>
  * `argocd proj create <SOME_PROJECT_NAME>`
    * _Example:_

### how to modify projects?

* == modify (add, remove) 
  * `sourceRepos`
  * `destinations`
  * `clusterResource` & `namespaceResource`
    * ⚠️namespace-scoped resources are restricted -- via a -- deny list⚠️
    * ⚠️cluster-scoped resources are restricted -- via a -- allow list⚠️

* ways
  * `argocd`
  * ArgoCD UI
  * declaratively

## Project Roles

* projects roles
  * == feature /
    * allows
      * determining
        * WHO
        * WHAT can be done | applications / associated -- with the -- project
  * use cases
    * | CI pipeline, set RESTRICTED set of permissions / enable sync operations | 1! app
      * NOT change its source OR destination
    * OIDC groups / restricted access
  * can 
    * exist MULTIPLE projects roles / project 
    * have MULTIPLE policies
    * be -- bound to -- OIDC groups &/OR JWT tokens
  * ' policies
    * == permissions /
      * stored | role -- as a -- list(policy strings)
    * `p, proj:<PROJECT_NAME>:<ROLE_NAME>, <resource>, <action>, <PROJECT_NAME>/<object>, <effect>`
      * 💡pattern💡
        * [MORE](../operator-manual/rbac.md)
      * `<object>`
        * ALLOWED ones
          * [here](/util/rbac/rbac.go)'s `ProjectScoped`
          * are
            * applications
            * applicationsets
            * logs
            * exec
            * clusters
            * repositories

### how to modify?

* ways
  * declaratively
  * `argocd`
  * ArgoCD UI

### JWT tokens / -- bound to a -- role 

* JWT token
  * allows
    * authenticate to a role
  * | use it, evaluate DYNAMICALLY the ALLOWED policies
    * ==
      * ❌JWT is NOT related -- with a -- role's policies❌
      * if you change the role's policies & use the SAME JWT -> ALLOWED rights change
  * ⚠️ONLY | being created, 
    * they can be retrieved⚠️
      * Reason:🧠
        * NOT stored | Argo CD
        * ArgoCD validates cryptographically -- via -- iat🧠
  * ways to be used
    * -- via -- CL's `--auth-token` flag
    * set `ARGOCD_AUTH_TOKEN` environment variable
  * can be used UNTIL they
    * expire OR
      * ❌by default, NO expire❌
    * are deleted
      * ⚠️revokation's priority > expirations's priority⚠️
        * == if token NOT expired BUT revoked -> can NOT be used

## Global Projects

* requirements
  * Argo CD v1.8

* Global projects
  * provide
    * configurations / OTHER projects can inherit from
      * are
        * `clusterResourceBlacklist`
        * `clusterResourceWhitelist`
        * `destinations`
        * `namespaceResourceBlacklist`
        * `namespaceResourceWhitelist`
        * `sourceRepos`
        * `syncWindows`
      * -> you can use global project's configuration
  * how to configure
    * | "argocd-cm" ConfigMap,
      * 💡[`type GlobalProjectSettings struct`](/util/settings/settings.go)💡
        * child project is matched -- via -- "k8s.io/apimachinery/pkg/apis/meta/v1.LabelSelector"

## Repositories & Clusters / project-scoped 

* history
  * Argo CD admin
    * ORIGINALLY
      * creates a project
      * decides the clusters & Git repositories / it defines
  * ⚠️PROBLEMS AFTERWARD use cases⚠️ 
    * if developer add a repository OR cluster -> need to contact -- to -- their Argo CD admin

* 

TODO: 
It is possible to offer a self-service process for developers so that
they can add a repository and/or cluster in a project on their own even 
after the initial creation of the project.

To begin the process, Argo CD admins must configure RBAC security to 
allow this self-service behavior.
For example, to allow users to add project scoped repositories an 
admin would have to add the following RBAC rules:

```
p, proj:my-project:admin, repositories, create, my-project/*, allow
p, proj:my-project:admin, repositories, delete, my-project/*, allow
p, proj:my-project:admin, repositories, update, my-project/*, allow
```

This provides extra flexibility so that admins can have stricter rules. e.g.:

```
p, proj:my-project:admin, repositories, update, my-project/https://github.example.com/*, allow
```

Once the appropriate RBAC rules are in place, developers can create 
their own Git repositories and (assuming they have the correct credentials)
can add them in an existing project either from the UI or the CLI.
Both the User interface and the CLI have the ability to optionally specify a project
* If a project is specified then the respective cluster/repository is considered project scoped:

```argocd repo add --name stable https://charts.helm.sh/stable --type helm --project my-project```

For the declarative setup both repositories and clusters are stored as Kubernetes Secrets, and
so a new field is used to denote that this resource is project scoped:

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: argocd-example-apps
  labels:
    argocd.argoproj.io/secret-type: repository
type: Opaque
stringData:
  project: my-project1                                     # Project scoped 
  name: argocd-example-apps
  url: https://github.com/argoproj/argocd-example-apps.git
  username: ****
  password: ****
```

> [!WARNING]
> Please keep in mind when using a project-scoped repository, only applications or applicationsets with a matching project 
> name can make use of it
* When using an applicationset with a Git generator that also makes use of a templated `project` 
> (i.e. it contains ``{{ ... }}``) only non-scoped repositories can be used with the applicationset (i.e. repositories 
> that do _not_ have a `project` set).

All the examples above concern Git repositories, but the same principles apply to clusters as well.

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: mycluster-secret
  labels:
    argocd.argoproj.io/secret-type: cluster
type: Opaque
stringData:
  name: mycluster.example.com
  project: my-project1 # Project scoped 
  server: https://mycluster.example.com
  config: |
    {
      "bearerToken": "<authentication token>",
      "tlsClientConfig": {
        "insecure": false,
        "caData": "<base64 encoded certificate>"
      }
    }
```

With project-scoped clusters we can also restrict projects to only allow applications whose destinations belong to the same project
* The default behavior allows for applications to be installed onto clusters which are not a part of the same project, as the example below demonstrates:

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: "some-ns"
spec:
  destination:
    # This destination might not actually be a cluster which belongs to `foo-project`
    server: https://some-k8s-server/
    namespace: "some-ns"
  project: foo-project
```

To prevent this behavior, we can set the attribute `permitOnlyProjectScopedClusters` on a project.

```yaml
spec:
  permitOnlyProjectScopedClusters: true
```

With this set, the application above would no longer be allowed to be synced 
to any cluster other than the ones which are a part of the same project.
