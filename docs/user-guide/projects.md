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
    * restrict destination clusters & namespaces | apps -- may be -- deployed
      * -- via -- `spec.destinations`
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

### how to create projects?

* ways to ocreate projects
  * declaratively
  * ArgoCD UI
    * Settings > Projects > New
      * name: <SOME_NAME>
      * description: <SOME_DESCRIPTION>
  * `argocd proj create <SOME_PROJECT_NAME>`
    * _Example:_

### how to manage (modify) projects?

* modify (add, remove) `sourceRepos`
  * you can ALSO do negations

* ways
  * `argocd`
  * ArgoCD UI
  * declaratively

TODO: 
A source repository is considered valid if the following conditions hold:

1. _Any_ allow source rule (i.e. a rule which isn't prefixed with `!`) permits the source
2. AND *no* deny source (i.e. a rule which is prefixed with `!`) rejects the source

Keep in mind that `!*` is an invalid rule, since it doesn't make any sense to disallow everything.

Permitted destination clusters and namespaces are managed with the commands (for clusters always provide server, 
the name is not used for matching):

```bash
argocd proj add-destination <PROJECT> <CLUSTER>,<NAMESPACE>
argocd proj remove-destination <PROJECT> <CLUSTER>,<NAMESPACE>
```

As with sources, we can also do negations of destinations (i.e. install anywhere _apart from_).

```bash
argocd proj add-destination <PROJECT> !<CLUSTER>,!<NAMESPACE>
argocd proj remove-destination <PROJECT> !<CLUSTER>,!<NAMESPACE>
```

Declaratively we can do something like this:

```yaml
spec:
  destinations:
  # Do not allow any app to be installed in `kube-system`  
  - namespace: '!kube-system'
    server: '*'
  # Or any cluster that has a URL of `team1-*`   
  - namespace: '*'
    server: '!https://team1-*'
    # Any other namespace or server is fine though.
  - namespace: '*'
    server: '*'
```

As with sources, a destination is considered valid if the following conditions hold:

1. _Any_ allow destination rule (i.e. a rule which isn't prefixed with `!`) permits the destination
2. AND *no* deny destination (i.e. a rule which is prefixed with `!`) rejects the destination

Keep in mind that `!*` is an invalid rule, since it doesn't make any sense to disallow everything.

Permitted destination K8s resource kinds are managed with the commands
* Note that namespaced-scoped resources are restricted via a deny list,
whereas cluster-scoped resources are restricted via allow list.

```bash
argocd proj allow-cluster-resource <PROJECT> <GROUP> <KIND>
argocd proj allow-namespace-resource <PROJECT> <GROUP> <KIND> [<NAME>]
argocd proj deny-cluster-resource <PROJECT> <GROUP> <KIND>
argocd proj deny-namespace-resource <PROJECT> <GROUP> <KIND> [<NAME>]
```

#### Restrict Cluster-Scoped Resources by Name

Since the names of certain cluster-scoped resources such as Namespaces and CustomResourceDefinitions (CRDs) 
have special
significance, it can be useful to allow only specific resources of these kinds
* For example, the following AppProject
config allows only namespaces starting with `team1-`:

```yaml
apiVersion: argoproj.io/v1alpha1
kind: AppProject
spec:
  clusterResourceWhitelist:
  - group: ''
    kind: Namespace
    name: team1-*
```

It is also possible to deny specific names of cluster-scoped resources.

```yaml
apiVersion: argoproj.io/v1alpha1
kind: AppProject
spec:
  clusterResourceBlacklist:
  - group: ''
    kind: Namespace
    name: kube-*
```

### how to assign the Application -- to -- a project?

* requirements
  * user needs permissions -- to -- access the NEW project

* ways
  * `argocd`
  * declaratively
  * ArgoCD UI

## Project Roles

* projects roles
  * == feature /
    * allows
      * determining
        * WHO
        * WHAT can be done | applications / associated -- with the -- project
  * uses
    * | CI pipeline, set RESTRICTED set of permissions / enable sync operations | 1! app
      * NOT change its source OR destination
  * exist MULTIPLE projects roles / projects
  * can have DIFFERENT policies

* policies
  * == permissions / 
    * follows the SAME [RBAC pattern / used | Argo CD configuration](../operator-manual/rbac.md)
    * stored | role
      * -- as a -- list(policy strings)

* TODO: A role's policy can only grant access to that role
* Users are associated with roles based on the groups list
* Consider the hypothetical AppProject definition below:

-- bound to -- OIDC groups &/OR JWT tokens

```yaml
apiVersion: argoproj.io/v1alpha1
kind: AppProject
metadata:
  name: sample-test-project
spec:
  ...
  roles:
  - name: custom-project-role
    description: The "custom-project-role" will be applied to the `some-user` group.
    groups:
    - some-user
    policies:
    - p, proj:sample-test-project:custom-project-role, applications, *, *, allow
  ...
```

Argo CD will use the policies defined in the AppProject roles while authorizing users actions
* To determine which role a given users is associated with, it will dynamically create groups based on the role name in runtime
* The project definition above will generate the following Casbin RBAC rules:

```
    p, proj:sample-test-project:custom-project-role, applications, *, *, allow
    g, some-user, proj:sample-test-project:custom-project-role
```

_Note 1_: It is very important that policy roles follow the pattern `proj:<project-name>:<role-name>` or they won't be effective during the Argo CD authorization process.

_Note 2_: The example above used `applications` as the resource for the policy definition
* However other types of resources can also be used: `applicationsets`, `repositories`, `clusters`, `logs` and `exec`
* See the [RBAC documentation](../operator-manual/rbac.md) for more details about those resources.

In order to create roles in a project and add policies to a role, a user will need permission to update a project
*  The following commands can be used to manage a role.

```bash
argocd proj role list
argocd proj role get
argocd proj role create
argocd proj role delete
argocd proj role add-policy
argocd proj role remove-policy
```

Project roles in itself are not useful without generating a token to associate to that role
* Argo CD supports JWT tokens as the means to authenticate to a role
* Since the JWT token is associated with a role's policies, any changes to the role's policies will immediately take effect for that JWT token.

The following commands are used to manage the JWT tokens.

```bash
argocd proj role create-token PROJECT ROLE-NAME
argocd proj role delete-token PROJECT ROLE-NAME ISSUED-AT
```

Since the JWT tokens aren't stored in Argo CD, they can only be retrieved when they are created
* A user can leverage them in the cli by either passing them in using the `--auth-token` flag or setting the ARGOCD_AUTH_TOKEN environment variable
* The JWT tokens can be used until they expire or are revoked
*  The JWT tokens can be created with or without an expiration
*  By default, the cli creates them without an expirations date
*  Even if a token has not expired, it cannot be used if the token has been revoked.

Below is an example of leveraging a JWT token to access a guestbook application
*  It makes the assumption that the user already has a project named myproject and an application called guestbook-default.

```bash
PROJ=myproject
APP=guestbook-default
ROLE=get-role
argocd proj role create $PROJ $ROLE
argocd proj role create-token $PROJ $ROLE -e 10m
JWT=<value from command above>
argocd proj role list $PROJ
argocd proj role get $PROJ $ROLE

# This command will fail because the JWT Token associated with the project role does not have a policy to allow access to the application
argocd app get $APP --auth-token $JWT
# Adding a policy to grant access to the application for the new role
argocd proj role add-policy $PROJ $ROLE --action get --permission allow --object $APP
argocd app get $APP --auth-token $JWT

# Removing the policy we added and adding one with a wildcard.
argocd proj role remove-policy $PROJ $ROLE -a get -o $APP
argocd proj role add-policy $PROJ $ROLE -a get --permission allow -o '*'
# The wildcard allows us to access the application due to the wildcard.
argocd app get $APP --auth-token $JWT
argocd proj role get $PROJ $ROLE


argocd proj role get $PROJ $ROLE
# Revoking the JWT token
argocd proj role delete-token $PROJ $ROLE <id field from the last command>
# This will fail since the JWT Token was deleted for the project role.
argocd app get $APP --auth-token $JWT
```

## Configuring RBAC With Projects

* project Roles
  * allows
    * configuring RBAC rules / ⚠️project-scope ⚠️

* _Example:_ TODO: add | SOME project
    ```yaml
    apiVersion: argoproj.io/v1alpha1
    kind: AppProject
    metadata:
      name: my-project
      namespace: argocd
    spec:
      roles:
      # A role which provides read-only access -- to -- ALL applications | project
      - name: read-only
        description: Read-only privileges to my-project
        policies:
        - p, proj:my-project:read-only, applications, get, my-project/*, allow
        groups:
        - my-oidc-group
    ```

* ways to configure the policy
  * `argocd proj role` 
  * | UI, project details page  

* if you want to configure CROSS project RBAC rules -> use `argocd-rbac-cm` ConfigMap
  * see [RBAC](../operator-manual/rbac.md) documentation 

## Configuring Global Projects (v1.8)

* Global projects
  * provide
    * configurations / OTHER projects can inherit from
  * how to configure
    * | "argocd-cm" ConfigMap

      ```yaml
      data:
        globalProjects: |-
          - labelSelector:
              matchExpressions:
                - key: opt
                  operator: In
                  values:
                    - prod
            # GLOBAL project name
            projectName: proj-global-test
      kind: ConfigMap
      ``` 

* projects / match `matchExpressions` specified | `argocd-cm` ConfigMap,
  * -> inherit the global project's following fields
    * `namespaceResourceBlacklist`
    * `namespaceResourceWhitelist`
    * `clusterResourceBlacklist`
    * `clusterResourceWhitelist`
    * `SyncWindows`
    * `SourceRepos`
    * `Destinations`

* ALLOWED operators
  * `In`
  * `NotIn`
  * `Exists`
  * `DoesNotExist`

## Project scoped Repositories and Clusters

* Argo CD admin
  * ORIGINALLY
    * creates a project
    * decides the clusters & Git repositories / it defines
  * PROBLEMS AFTERWARD use cases
    * add a repository OR cluster
      * -> developer need to contact -- to -- their Argo CD admin

TODO: 
It is possible to offer a self-service process for developers so that
they can add a repository and/or cluster in a project on their own even after the initial creation of the project.

For this purpose Argo CD supports project-scoped repositories and clusters.

To begin the process, Argo CD admins must configure RBAC security to allow this self-service behavior.
For example, to allow users to add project scoped repositories an admin would have to add the following RBAC rules:

```
p, proj:my-project:admin, repositories, create, my-project/*, allow
p, proj:my-project:admin, repositories, delete, my-project/*, allow
p, proj:my-project:admin, repositories, update, my-project/*, allow
```

This provides extra flexibility so that admins can have stricter rules. e.g.:

```
p, proj:my-project:admin, repositories, update, my-project/https://github.example.com/*, allow
```

Once the appropriate RBAC rules are in place, developers can create their own Git repositories and (assuming they have the correct credentials)
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
