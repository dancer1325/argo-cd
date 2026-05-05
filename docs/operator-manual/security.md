# Security

* goal
  * Argo CD
    * security topics
    * implementation details

* Argo CD
  * satisfy [PCI compliance](https://www.pcisecuritystandards.org) requirements
    * -- thanks to -- 
      * rigorous internal security testing
      * penetration testing

## Authentication | Argo CD API server

* 💡ONLY -- through -- [JSON Web Tokens (JWTs)](https://jwt.io)💡  
  * ❌NOT -- through username/password❌
  * ways to be obtained/managed
    1. local users / contain username/password /  
       * gets -- , via `/api/v1/session` endpoint, -- a JWT /
         * signed
         * issued -- by the -- Argo CD API server
         * lifetime = 24hours
           * [CVE-2021-26921](https://github.com/argoproj/argo-cd/security/advisories/GHSA-9h6w-j7w4-jr52)
       * if the admin password is updated -> ALL existing admin JWT tokens are IMMEDIATELY revoked
       * password is stored -- as a -- bcrypt hash | [`argocd-secret`](/manifests/base/config/argocd-secret.yaml) Secret
    2. | [Single Sign-On](user-management/index.md) users, the user completes | OAuth2 login flow -- to the -- configured OIDC identity provider
       * delegated -- through the --
         * bundled Dex provider, OR
           * lifetime == 24 hours
         * DIRECTLY -- to a -- self-managed OIDC provider
       * JWT is handled -- by the -- provider 
         * handled == signed + issued + expiration + revocation
    3. Automation tokens -- via -- `/api/v1/projects/{project}/roles/{role}/token`
       * project-scope
       * privilege-limited
         * Reason:🧠role-related🧠
       * signed & issued -- by -- Argo CD
       * configurable expiration
       * if you want to revoke IMMEDIATELY -> delete the JWT reference ID | project role

## Authorization

* [RBAC](./rbac.md)

## TLS

* [TLS](tls.md)

* plain HTTP
  * uses
    * communication with Redis
      * [if you want to use TLS -> setup -- via -- CL arguments](server-commands)

## Git & Helm Repositories

* [managed -- by -- the repo-server](architecture.md#repository-server) /
  * ❌does NOT
    * have Kubernetes privileges
    * store service's credentials❌

* POSSIBLE attacks
  * Reason:🧠somebody get write access | git repository🧠
  * [unauthorized deployments](#unauthorized-deployments)
  * [tool command invocation](#tool-command-invocation)
  * [remote bases & helm chart dependencies](#remote-bases--helm-chart-dependencies)

### Unauthorized Deployments

* if an attacker gets access to a trusted git repo & made changes -> modify -- , being deployed by Argo CD, -- Kubernetes resources | live k8s cluster

### Tool command invocation

* if an attacker / write access | trusted git repository, construct malicious helm charts or kustomizations -> take care
  * | render manifests, could intercept it
  * repo-server / configured -- with -- [Config Management Plugins](config-management-plugins.md)
    * [Tool Detection](../user-guide/tool_detection.md)

### Remote bases & helm chart dependencies

* Argo CD's repository 
  * allow-list
    * ONLY restricts the initial repository
  * ⚠️could reference OTHER REMOTE git repositories / contain OTHER Kubernetes resources⚠️
    * Reason:🧠due to kustomize & helm
      * reference & follow ADDITIONAL repositories
        * _Examples:_ `kustomize remote bases`, `helm chart dependencies`🧠

## Sensitive Information

* _Examples:_
  * cluster credentials
  * Git credentials
  * OAuth2 client secrets
  * Kubernetes Secret values

### Secrets

* Argo CD
  * 👀NEVER returns sensitive data -- from -- its API👀
  * sanitize/hide ALL sensitive data | API payloads & logs

### External Cluster Credentials

TODO: 
To manage external clusters, Argo CD stores the credentials of the external cluster as a Kubernetes
Secret in the argocd namespace
* This secret contains the K8s API bearer token associated with the
`argocd-manager` ServiceAccount created during `argocd cluster add`, along with connection options
to that API server (TLS configuration/certs, AWS role-arn, etc...).
The information is used to reconstruct a REST config and kubeconfig to the cluster used by Argo CD
services.

To rotate the bearer token used by Argo CD, the token can be deleted (e.g. using kubectl) which
causes Kubernetes to generate a new secret with a new bearer token
* The new token can be re-inputted
to Argo CD by re-running `argocd cluster add`
* Run the following commands against the *_managed_*
cluster:

```bash
# run using a kubeconfig for the externally managed cluster
kubectl delete secret argocd-manager-token-XXXXXX -n kube-system
argocd cluster add CONTEXTNAME
```

> [!NOTE]
> Kubernetes 1.24 [stopped automatically creating tokens for Service Accounts](https://github.com/kubernetes/kubernetes/blob/master/CHANGELOG/CHANGELOG-1.24.md#no-really-you-must-read-this-before-you-upgrade).
> [Starting in Argo CD 2.4](https://github.com/argoproj/argo-cd/pull/9546), `argocd cluster add` creates a 
> ServiceAccount _and_ a non-expiring Service Account token Secret when adding 1.24 clusters
* In the future, Argo CD 
> will [add support for the Kubernetes TokenRequest API](https://github.com/argoproj/argo-cd/issues/9610) to avoid 
> using long-lived tokens.

To revoke Argo CD's access to a managed cluster, delete the RBAC artifacts against the *_managed_*
cluster, and remove the cluster entry from Argo CD:

```bash
# run using a kubeconfig for the externally managed cluster
kubectl delete sa argocd-manager -n kube-system
kubectl delete clusterrole argocd-manager-role
kubectl delete clusterrolebinding argocd-manager-role-binding
argocd cluster rm https://your-kubernetes-cluster-addr
```

> [!NOTE]
> For AWS EKS clusters, the [get-token](https://docs.aws.amazon.com/cli/latest/reference/eks/get-token.html) command is used to authenticate to the external cluster, which uses IAM roles in lieu of locally stored tokens, so token rotation is not needed, and revocation is handled through IAM.

## Cluster RBAC

By default, Argo CD uses a [clusteradmin level role](https://github.com/argoproj/argo-cd/blob/master/manifests/base/application-controller-roles/argocd-application-controller-role.yaml)
in order to:

1. watch & operate on cluster state
2. deploy resources to the cluster

Although Argo CD requires cluster-wide **_read_** privileges to resources in the managed cluster to
function properly, it does not necessarily need full **_write_** privileges to the cluster. The
ClusterRole used by argocd-server and argocd-application-controller can be modified such
that write privileges are limited to only the namespaces and resources that you wish Argo CD to
manage.

To fine-tune privileges of externally managed clusters, edit the ClusterRole of the `argocd-manager-role`

```bash
# run using a kubeconfig for the externally managed cluster
kubectl edit clusterrole argocd-manager-role
```

To fine-tune privileges which Argo CD has against its own cluster (i.e. `https://kubernetes.default.svc`),
edit the following cluster roles where Argo CD is running in:

```bash
# run using a kubeconfig to the cluster Argo CD is running in
kubectl edit clusterrole argocd-server
kubectl edit clusterrole argocd-application-controller
```

> [!TIP]
> If you want to deny Argo CD access to a kind of resource then add it as an [excluded resource](declarative-setup.md#resource-exclusioninclusion).

## Auditing

As a GitOps deployment tool, the Git commit history provides a natural audit log of what changes
were made to application configuration, when they were made, and by whom. However, this audit log
only applies to what happened in Git and does not necessarily correlate one-to-one with events
that happen in a cluster. For example, User A could have made multiple commits to application
manifests, but User B could have just only synced those changes to the cluster sometime later.

To complement the Git revision history, Argo CD emits Kubernetes Events of application activity,
indicating the responsible actor when applicable. For example:

```bash
$ kubectl get events
LAST SEEN   FIRST SEEN   COUNT   NAME                         KIND          SUBOBJECT   TYPE      REASON               SOURCE                          MESSAGE
1m          1m           1       guestbook.157f7c5edd33aeac   Application               Normal    ResourceCreated      argocd-server                   admin created application
1m          1m           1       guestbook.157f7c5f0f747acf   Application               Normal    ResourceUpdated      argocd-application-controller   Updated sync status:  -> OutOfSync
1m          1m           1       guestbook.157f7c5f0fbebbff   Application               Normal    ResourceUpdated      argocd-application-controller   Updated health status:  -> Missing
1m          1m           1       guestbook.157f7c6069e14f4d   Application               Normal    OperationStarted     argocd-server                   admin initiated sync to HEAD (8a1cb4a02d3538e54907c827352f66f20c3d7b0d)
1m          1m           1       guestbook.157f7c60a55a81a8   Application               Normal    OperationCompleted   argocd-application-controller   Sync operation to 8a1cb4a02d3538e54907c827352f66f20c3d7b0d succeeded
1m          1m           1       guestbook.157f7c60af1ccae2   Application               Normal    ResourceUpdated      argocd-application-controller   Updated sync status: OutOfSync -> Synced
1m          1m           1       guestbook.157f7c60af5bc4f0   Application               Normal    ResourceUpdated      argocd-application-controller   Updated health status: Missing -> Progressing
1m          1m           1       guestbook.157f7c651990e848   Application               Normal    ResourceUpdated      argocd-application-controller   Updated health status: Progressing -> Healthy
```

These events can be then be persisted for longer periods of time using other tools as
[Event Exporter](https://github.com/GoogleCloudPlatform/k8s-stackdriver/tree/master/event-exporter) or
[Event Router](https://github.com/heptiolabs/eventrouter).

## WebHook Payloads

Payloads from webhook events are considered untrusted. Argo CD only examines the payload to infer
the involved applications of the webhook event (e.g. which repo was modified), then refreshes
the related application for reconciliation. This refresh is the same refresh which occurs regularly
at three minute intervals, just fast-tracked by the webhook event.

## Logging

### Security field

Security-related logs are tagged with a `security` field to make them easier to find, analyze, and report on.

| Level | Friendly Level | Description                                                                                       | Example                                     |
|-------|----------------|---------------------------------------------------------------------------------------------------|---------------------------------------------|
| 1     | Low            | Unexceptional, non-malicious events                                                               | Successful access                           |
| 2     | Medium         | Could indicate malicious events, but has a high likelihood of being user/system error             | Access denied                               |
| 3     | High           | Likely malicious events but one that had no side effects or was blocked                           | Out of bounds symlinks in repo              |
| 4     | Critical       | Any malicious or exploitable event that had a side effect                                         | Secrets being left behind on the filesystem |
| 5     | Emergency      | Unmistakably malicious events that should NEVER occur accidentally and indicates an active attack | Brute forcing of accounts                   |

Where applicable, a `CWE` field is also added specifying the [Common Weakness Enumeration](https://cwe.mitre.org/index.html) number.

> [!WARNING]
> Please be aware that not all security logs are comprehensively tagged yet and these examples are not necessarily implemented.

### API Logs

Argo CD logs payloads of most API requests except request that are considered sensitive, such as
`/cluster.ClusterService/Create`, `/session.SessionService/Create` etc. The full list of method
can be found in [server/server.go](https://github.com/argoproj/argo-cd/blob/abba8dddce8cd897ba23320e3715690f465b4a95/server/server.go#L516).

Argo CD does not log IP addresses of clients requesting API endpoints, since the API server is typically behind a proxy. Instead, it is recommended
to configure IP addresses logging in the proxy server that sits in front of the API server.

### Standard Application log fields

For logs related to an Application, Argo CD will log the following standard fields :

* *application*: the Application name, without the namespace
* *app-namespace*: the Application's namespace
* *project*: the Application's project

## ApplicationSets

* [security considerations](./applicationset/Security.md)

## Limiting Directory App Memory Usage

> >2.2.10, 2.1.16, >2.3.5

Directory-type Applications (those whose source is raw JSON or YAML files) can consume significant
[repo-server](architecture.md#repository-server) memory, depending on the size and structure of the YAML files.

To avoid over-using memory in the repo-server (potentially causing a crash and denial of service), set the
`reposerver.max.combined.directory.manifests.size` config option in [argocd-cmd-params-cm](argocd-cmd-params-cm.yaml).

This option limits the combined size of all JSON or YAML files in an individual app. Note that the in-memory
representation of a manifest may be as much as 300x the size of the manifest on disk. Also note that the limit is per
Application. If manifests are generated for multiple applications at once, memory usage will be higher.

**Example:**

Suppose your repo-server has a 10G memory limit, and you have ten Applications which use raw JSON or YAML files. To
calculate the max safe combined file size per Application, divide 10G by 300 * 10 Apps (300 being the worst-case memory
growth factor for the manifests).

```
10G / 300 * 10 = 3M
```

So a reasonably safe configuration for this setup would be a 3M limit per app.

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: argocd-cmd-params-cm
data:
  reposerver.max.combined.directory.manifests.size: '3M'
```

The 300x ratio assumes a maliciously-crafted manifest file. If you only want to protect against accidental excessive
memory use, it is probably safe to use a smaller ratio.

Keep in mind that if a malicious user can create additional Applications, they can increase the total memory usage.
Grant [App creation privileges](rbac.md) carefully.
