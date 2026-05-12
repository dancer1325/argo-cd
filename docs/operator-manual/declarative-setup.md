# Declarative Setup

* goal
  * 💡define declaratively 💡, -- via -- Kubernetes manifests,
    * Argo CD applications,
    * Argo CD projects
    * Argo CD settings

## Quick Reference

* ⚠️install Argo CD's CRD (`Application` & `AppProject`) | Argo CD namespace (by default, `argocd`)⚠️ 

### Atomic configuration

| Sample File                                                          | Resource Name                                                                      | Kind      | Description                                                                          |
|----------------------------------------------------------------------|------------------------------------------------------------------------------------|-----------|--------------------------------------------------------------------------------------|
| [`argocd-cm.yaml`](examples/argocd-cm.yaml)                       | argocd-cm                                                                          | ConfigMap | General Argo CD configuration                                                        |
| [`argocd-repositories.yaml`](examples/argocd-repositories.yaml)            | my-private-repo / istio-helm-repo / private-helm-repo / private-repo               | Secrets   | SAMPLE repository connection details                                                 |
| [`argocd-repo-creds.yaml`](examples/argocd-repo-creds.yaml)                | argoproj-https-creds / argoproj-ssh-creds / github-creds / github-enterprise-creds | Secrets   | SAMPLE repository credential templates                                               |
| [`argocd-cmd-params-cm.yaml`](examples/argocd-cmd-params-cm.yaml)          | argocd-cmd-params-cm                                                               | ConfigMap | Argo CD env variables configuration                                                  |
| [`argocd-secret.yaml`](examples/argocd-secret.yaml)                        | argocd-secret                                                                      | Secret    | User Passwords <br/> Certificates (⚠️deprecated⚠️) <br/> Signing Key <br/> Dex secrets <br/> Webhook secrets |
| [`argocd-rbac-cm.yaml`](examples/argocd-rbac-cm.yaml)                      | argocd-rbac-cm                                                                     | ConfigMap | RBAC Configuration                                                                   |
| [`argocd-tls-certs-cm.yaml`](examples/argocd-tls-certs-cm.yaml)            | argocd-tls-certs-cm                                                                | ConfigMap | Custom TLS certificates -- for connecting, via HTTPS (v1.2+), -- Git repositories    |
| [`argocd-ssh-known-hosts-cm.yaml`](examples/argocd-ssh-known-hosts-cm.yaml) | argocd-ssh-known-hosts-cm                                                          | ConfigMap | SSH known hosts data -- for connecting, via SSH (v1.2+), -- Git repositories         |

* ⚠️1! ALLOWED resource name (PREVIOUS table) / EACH specific kind of ConfigMap & Secret resource ⚠️
  * if you need to merge things -> BEFORE creating them, do it 

* ⚠️ConfigMap resources -> MUST be annotated -- by -- `app.kubernetes.io/part-of: argocd` label ⚠️ 
  * Reason: 🧠OTHERWISE, Argo CD -- will NOT be able to -- use them🧠

### MULTIPLE configuration objects

| Sample File                                                     | Kind        | Description              |
|-----------------------------------------------------------------|-------------|--------------------------|
| [`application.yaml`](examples/application.yaml)                 | Application | Example application spec |
| [`project.yaml`](examples/project.yaml)                         | AppProject  | Example project spec     |
| [`argocd-repositories.yaml`](examples/argocd-repositories.yaml) | Secret      | Repository credentials   |

* `Application`'s name 
  * == applicationName | Argo CD
  * UNIQUE | Argo CD installation
* `AppProject`'s name
  * == projectName | Argo CD
  * UNIQUE | Argo CD installation 

## Applications -- `Application` --

* Application CRD
  * == Kubernetes resource object / 
    * represent a deployed application instance | environment
    * `spec.source`
      * == desired state | Git (repository, revision, path, environment)
    * `spec.destination`
      * == target cluster & namespace
        * restrictions 
          * | cluster, specify `.server` OR `.name`
            * ❌BUT, NOT BOTH❌
              * Reason: 🧠it causes an error🧠 
            * if you specify `.name` -> used / ANY operations
    * `metadata.finalizers`
      * perform [app deletion](../user-guide/app_deletion.md#deletion-finalizer)

* ways to deploy
  * -- via -- kubectl
    * `kubectl apply -n namespaceWhereLivesArgoCD -f pathToApplicationFile.yaml`
  * -- via -- [helm](../user-guide/helm.md)
    * | "Application.yaml",
      * replace `spec.source.path` -- by -- `spec.source.chart` 
      * modify `spec.source.repoURL`

### App of Apps

* [here](cluster-bootstrapping.md)

## Projects -- `AppProject` --

* `AppProject`
  * := CRD /
    * == logical grouping of applications
  * `spec`
    * `.sourceRepos`
      * == repositories | project's applications -- pull -- manifests from
    * `.destinations`
      * == clusters & namespaces | project's applications -- can -- deploy into
        * ⚠️if you include namespace | Argo CD is installed -> Applications have admin-level access⚠️  
          * SOLUTION: 🧠fine [`.roles`](rbac.md)🧠
    * `.roles`
      * == entitieS / define access -- to -- project's resources

## Repositories

* 💡globally registered💡
  * ❌!= / Application❌
* | SOME Git hosters
  * _ExampleS:_ GitLab & on-premise GitLab instances
  * | Application, set `spec.source.repoUrl: ...git`
    * Reason:🧠
      * otherwise -> send HTTP 301 / "redirect to the repository URL suffixed with `.git`"
        * == Argo CD does NOT follow these redirects🧠

### Repository Credentials

* uses
  * | [private repositories](../user-guide/private-repositories.md#credentials-methods)

### SSH known host public keys

* uses
  * | [private repositories](../user-guide/private-repositories.md#credentials-methods)

### Configure repositories with proxy

TODO: 
Proxy for your repository can be specified in the `proxy` field of the repository secret, 
along with a corresponding `noProxy` config
* Argo CD uses this proxy/noProxy config to access the repository and do related helm/kustomize operations
* Argo CD looks for the standard proxy environment variables in the repository server if the custom proxy config is absent.

An example repository with proxy and noProxy:

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: private-repo
  namespace: argocd
  labels:
    argocd.argoproj.io/secret-type: repository
stringData:
  type: git
  url: https://github.com/argoproj/private-repo
  proxy: https://proxy-server-url:8888
  noProxy: ".internal.example.com,company.org,10.123.0.0/16"
  password: my-password
  username: my-username
```

A note on noProxy: Argo CD uses exec to interact with different tools such as helm and kustomize
* Not all of these tools support the same noProxy syntax as the [httpproxy go package](https://cs.opensource.google/go/x/net/+/internal-branch.go1.21-vendor:http/httpproxy/proxy.go;l=38-50) does
* In case you run in trouble with noProxy not being respected you might want to try using the full domain instead of a wildcard pattern or IP range to find a common syntax that all tools support.

## Clusters

### Cluster credentials

* Cluster credentials
  * allows
    * ArgoCD can connect -- to -- Kubernetes cluster
  * 💡are stored | secrets💡
    * [data structure](/pkg/apis/application/v1alpha1/types.go)'s `type Cluster struct`

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: <SOME_CLUSTER_SECRET_NAME>
  namespace: argocd
  labels:
    argocd.argoproj.io/secret-type: cluster
type: Opaque
stringData:
  # name  
  #   == cluster name
  name: <CLUSTER_NAME>
  server: <CLUSTER_SERVER_URL>
  # server: https://my-cluster.example.com
  
  # namespaces
  #   OPTIONAL
  #     if you specify it -> Argo CD performs a separate list/watch operation / EACH namespace
  #   == namespace1,namespace2, .... / accessible | that cluster
  #     -> cluster-level resources are ignored
  #       ⚠️EXCEPTION: `clusterResources=true`⚠️
  #   POSSIBLE PROBLEMS:
  #     Problem1: Application controller can exceed the MAXIMUM number of Kubernetes API server'S ALLOWED idle connections
  #       Solution: | Application controller, increase the `ARGOCD_K8S_CLIENT_MAX_IDLE_CONNECTIONS` environment variable
  namespaces: "<NAMESPACE_FIRST>,<NAMESPACE_SECOND>"
  
  #   OPTIONAL
  #   ALLOWED values: "true" OR "false"
  #   requirements
  #     specify `namespaces`
  clusterResources: "false"
  
  # OPTIONAL
  # uses
  #   mark this Secret -- as a -- project-scoped cluster
  project: <PROJECT_NAME>
  
  # config: ClusterConfig
  #   `execProviderConfig.command`
  #     requirements: be AVAILABLE | [Build Your Own Image](custom_tools.md#byoi-build-your-own-image)
  config: |
    {
      "username": "<username>",
      "password": "<password>",
      "bearerToken": "<token>",
      "awsAuthConfig": {
        "clusterName": "<eks-cluster-name>",
        "roleARN": "<arn:aws:iam::role>",
        "profile": "<aws-profile>"
      },
      "execProviderConfig": {
        "command": "<binary>",
        "args": ["<arg1>", "<arg2>"],
        "env": {"<key>": "<value>"},
        "apiVersion": "client.authentication.k8s.io/v1beta1",
        "installHint": "<install instructions>"
      },
      "tlsClientConfig": {
        "insecure": false,
        "serverName": "<sni-hostname>",
        "caData": "<base64-encoded-ca>",
        "certData": "<base64-encoded-cert>",
        "keyData": "<base64-encoded-key>"
      },
      "proxyUrl": "http://proxy.example.com:8080",
      "disableCompression": false
    }
```

### Skipping Cluster Reconciliation

* goal
  * cluster skip reconcile ALL their apps

* == [annotation | Application-level](../user-guide/skip_reconcile.md)

* steps
  * | Cluster credential secret, add
    * the `argocd.argoproj.io/skip-reconcile: "true"` annotation
      * if you want to resume afterwards -> `kubectl -n argocd annotate secret <CLUSTER_SECRET> argocd.argoproj.io/skip-reconcile-`

### EKS

TODO: 
EKS cluster secret example using argocd-k8s-auth and [IRSA](https://docs.aws.amazon.com/eks/latest/userguide/iam-roles-for-service-accounts.html) and [Pod Identity](https://docs.aws.amazon.com/eks/latest/userguide/pod-identities.html):

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: mycluster-secret
  labels:
    argocd.argoproj.io/secret-type: cluster
type: Opaque
stringData:
  name: "eks-cluster-name-for-argo"
  server: "https://xxxyyyzzz.xyz.some-region.eks.amazonaws.com"
  config: |
    {
      "awsAuthConfig": {
        "clusterName": "my-eks-cluster-name",
        "roleARN": "arn:aws:iam::<AWS_ACCOUNT_ID>:role/<IAM_ROLE_NAME>"
      },
      "tlsClientConfig": {
        "insecure": false,
        "caData": "<base64 encoded certificate>"
      }        
    }
```

This setup requires:

1. [IRSA enabled](https://docs.aws.amazon.com/eks/latest/userguide/enable-iam-roles-for-service-accounts.html) or [Pod Identity agent](https://docs.aws.amazon.com/eks/latest/userguide/pod-id-agent-setup.html) on your Argo CD EKS cluster  
2. An IAM role ("management role") for your Argo CD EKS cluster that has an appropriate trust policy and permission policies (see below)
3. A role created for each cluster being added to Argo CD that is assumable by the Argo CD management role
4. An [Access Entry](https://docs.aws.amazon.com/eks/latest/userguide/access-entries.html) within each EKS cluster added to Argo CD that gives the cluster's role (from point 3) RBAC permissions
to perform actions within the cluster
    - Or, alternatively, an entry within the `aws-auth` ConfigMap within the cluster added to Argo CD ([deprecated by EKS](https://docs.aws.amazon.com/eks/latest/userguide/auth-configmap.html))

#### Argo CD Management Role

The role created for Argo CD (the "management role") will need to have a trust policy suitable for assumption by certain 
Argo CD Service Accounts *and by itself*.

The service accounts that need to assume this role are:

- `argocd-application-controller`,
- `argocd-applicationset-controller`
- `argocd-server`

If we create role `arn:aws:iam::<AWS_ACCOUNT_ID>:role/<ARGO_CD_MANAGEMENT_IAM_ROLE_NAME>` for this purpose, the following
is an example trust policy suitable for this need. Ensure that the Argo CD cluster has an [IAM OIDC provider configured](https://docs.aws.amazon.com/eks/latest/userguide/enable-iam-roles-for-service-accounts.html) or [Pod Identity agent running](https://docs.aws.amazon.com/eks/latest/userguide/pod-id-agent-setup.html)

**for IRSA:**
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "ExplicitSelfRoleAssumption",
            "Effect": "Allow",
            "Principal": {
                "AWS": "*"
            },
            "Action": "sts:AssumeRole",
            "Condition": {
                "ArnLike": {
                  "aws:PrincipalArn": "arn:aws:iam::<AWS_ACCOUNT_ID>:role/<ARGO_CD_MANAGEMENT_IAM_ROLE_NAME>"
                }
            }
        },
        {
            "Sid": "ServiceAccountRoleAssumption",
            "Effect": "Allow",
            "Principal": {
                "Federated": "arn:aws:iam::<AWS_ACCOUNT_ID>:oidc-provider/oidc.eks.<AWS_REGION>.amazonaws.com/id/EXAMPLED539D4633E53DE1B71EXAMPLE"
            },
            "Action": "sts:AssumeRoleWithWebIdentity",
            "Condition": {
                "StringEquals": {
                    "oidc.eks.<AWS_REGION>.amazonaws.com/id/EXAMPLED539D4633E53DE1B71EXAMPLE:sub": [
                        "system:serviceaccount:argocd:argocd-application-controller",
                        "system:serviceaccount:argocd:argocd-applicationset-controller",
                        "system:serviceaccount:argocd:argocd-server"
                    ],
                    "oidc.eks.<AWS_REGION>.amazonaws.com/id/EXAMPLED539D4633E53DE1B71EXAMPLE:aud": "sts.amazonaws.com"
                }
            }
        }
    ]
}
```

**for Pod Identity:**
```json
{
    "Version":"2012-10-17",		 	 	 
    "Statement": [
        {
            "Sid": "AllowEksAuthToAssumeRoleForPodIdentity",
            "Effect": "Allow",
            "Principal": {
                "Service": "pods.eks.amazonaws.com"
            },
            "Action": [
                "sts:AssumeRole",
                "sts:TagSession"
            ],
            "Condition": {
                "StringEquals": {
                    "aws:RequestTag/kubernetes-namespace": [
                        "argocd"
                    ],
                    "aws:RequestTag/kubernetes-service-account": [
                        "argocd-server",
                        "argocd-application-controller",
                        "argocd-applicationset-controller"
                    ]
                }
            }
        }
    ]
}
```

#### Argo CD Service Accounts

The 3 service accounts need to be modified to include an annotation with the Argo CD management role ARN.

Here's an example service account configurations for `argocd-application-controller`, `argocd-applicationset-controller`, and `argocd-server`.

> [!WARNING]
> Once the annotations has been set on the service accounts, the application controller and server pods need to be restarted.

**for IRSA:**   
```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  annotations:
    eks.amazonaws.com/role-arn: "<arn:aws:iam::<AWS_ACCOUNT_ID>:role/<ARGO_CD_MANAGEMENT_IAM_ROLE_NAME>"
  name: argocd-application-controller
---
apiVersion: v1
kind: ServiceAccount
metadata:
  annotations:
    eks.amazonaws.com/role-arn: "<arn:aws:iam::<AWS_ACCOUNT_ID>:role/<ARGO_CD_MANAGEMENT_IAM_ROLE_NAME>"
  name: argocd-applicationset-controller
---
apiVersion: v1
kind: ServiceAccount
metadata:
  annotations:
    eks.amazonaws.com/role-arn: "<arn:aws:iam::<AWS_ACCOUNT_ID>:role/<ARGO_CD_MANAGEMENT_IAM_ROLE_NAME>"
  name: argocd-server
```

**for Pod Identity:**  
```shell
aws eks associate-pod-identity -- cluster-name <EKS_CLUSTER_NAME> --namespace argocd --service-account argocd-applicationset-controller --role-arn arn:aws:iam::<AWS_ACCOUNT_ID>:role/<ARGO_CD_MANAGEMENT_IAM_ROLE_NAME>
aws eks associate-pod-identity -- cluster-name <EKS_CLUSTER_NAME> --namespace argocd --service-account argocd-application-controller --role-arn arn:aws:iam::<AWS_ACCOUNT_ID>:role/<ARGO_CD_MANAGEMENT_IAM_ROLE_NAME>
aws eks associate-pod-identity -- cluster-name <EKS_CLUSTER_NAME> --namespace argocd --service-account argocd-server --role-arn arn:aws:iam::<AWS_ACCOUNT_ID>:role/<ARGO_CD_MANAGEMENT_IAM_ROLE_NAME>
```

#### IAM Permission Policy

The Argo CD management role (`arn:aws:iam::<AWS_ACCOUNT_ID>:role/<ARGO_CD_MANAGEMENT_IAM_ROLE_NAME>` in our example) additionally
needs to be allowed to assume a role for each cluster added to Argo CD.

If we create a role named `<IAM_CLUSTER_ROLE>` for an EKS cluster we are adding to Argo CD, we would update the permission 
policy of the Argo CD management role to include the following:

**for IRSA:**
```json
{
    "Version" : "2012-10-17",
    "Statement" : {
      "Effect" : "Allow",
      "Action" : "sts:AssumeRole",
      "Resource" : [
        "arn:aws:iam::<AWS_ACCOUNT_ID>:role/<IAM_CLUSTER_ROLE>"
      ]
    }
  }
```

**for Pod Identity:**
```json
{
    "Version" : "2012-10-17",
    "Statement" : {
      "Effect" : "Allow",
      "Action" : [
        "sts:AssumeRole",
        "sts:TagSession"
      ],
      "Resource" : [
        "arn:aws:iam::<AWS_ACCOUNT_ID>:role/<IAM_CLUSTER_ROLE>"
      ]
    }
  }
```

This allows the Argo CD management role to assume the cluster role.

You can add permissions like above to the Argo CD management role for each cluster being managed by Argo CD (assuming you
create a new role per cluster).

#### Cluster Role Trust Policies

As stated, each EKS cluster being added to Argo CD should have its own corresponding role. This role should not have any
permission policies. Instead, it will be used to authenticate against the EKS cluster's API. The Argo CD management role
assumes this role, and calls the AWS API to get an auth token via argocd-k8s-auth. That token is used when connecting to
the added cluster's API endpoint.

If we create role `arn:aws:iam::<AWS_ACCOUNT_ID>:role/<IAM_CLUSTER_ROLE>` for a cluster being added to Argo CD, we should
set its trust policy to give the Argo CD management role permission to assume it. Note that we're granting the Argo CD 
management role permission to assume this role above, but we also need to permit that action via the cluster role's
trust policy.

A suitable trust policy allowing the `IAM_CLUSTER_ROLE` to be assumed by the `ARGO_CD_MANAGEMENT_IAM_ROLE_NAME` role looks like this:

**for IRSA:**
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {
                "AWS": "arn:aws:iam::<AWS_ACCOUNT_ID>:role/<ARGO_CD_MANAGEMENT_IAM_ROLE_NAME>"
            },
            "Action": "sts:AssumeRole"
        }
    ]
}
```

**for Pod Identity:**
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {
                "AWS": "arn:aws:iam::<AWS_ACCOUNT_ID>:role/<ARGO_CD_MANAGEMENT_IAM_ROLE_NAME>"
            },
            "Action": [
                "sts:TagSession",
                "sts:AssumeRole"
            ]
        }
    ]
}
```

#### Access Entries

Each cluster's role (e.g. `arn:aws:iam::<AWS_ACCOUNT_ID>:role/<IAM_CLUSTER_ROLE>`) has no permission policy. Instead, we
associate that role with an EKS permission policy, which grants that role the ability to generate authentication tokens
to the cluster's API. This EKS permission policy decides what RBAC permissions are granted in that process.

An [access entry](https://docs.aws.amazon.com/eks/latest/userguide/access-entries.html) (and the policy associated to the role) can be created using the following commands:

```bash
# For each cluster being added to Argo CD
aws eks create-access-entry \
    --cluster-name my-eks-cluster-name \
    --principal-arn arn:aws:iam::<AWS_ACCOUNT_ID>:role/<IAM_CLUSTER_ROLE> \
    --type STANDARD \
    --kubernetes-groups [] # No groups needed

aws eks associate-access-policy \
    --cluster-name my-eks-cluster-name \
    --policy-arn arn:aws:eks::aws:cluster-access-policy/AmazonEKSClusterAdminPolicy \
    --access-scope type=cluster \
    --principal-arn arn:aws:iam::<AWS_ACCOUNT_ID>:role/<IAM_CLUSTER_ROLE>
```

The above role is granted cluster admin permissions via `AmazonEKSClusterAdminPolicy`. The Argo CD management role that
assume this role is therefore granted the same cluster admin permissions when it generates an API token when adding the 
associated EKS cluster.

**AWS Auth (Deprecated)**

Instead of using Access Entries, you may need to use the deprecated `aws-auth`.

If so, the `roleARN` of each managed cluster needs to be added to each respective cluster's `aws-auth` config map (see
[Enabling IAM principal access to your cluster](https://docs.aws.amazon.com/eks/latest/userguide/add-user-role.html)), as
well as having an assume role policy which allows it to be assumed by the Argo CD pod role.

An example assume role policy for a cluster which is managed by Argo CD:

```json
{
    "Version" : "2012-10-17",
    "Statement" : {
      "Effect" : "Allow",
      "Action" : "sts:AssumeRole",
      "Principal" : {
        "AWS" : "<arn:aws:iam::<AWS_ACCOUNT_ID>:role/<ARGO_CD_MANAGEMENT_IAM_ROLE_NAME>"
      }
    }
  }
```

Example kube-system/aws-auth configmap for your cluster managed by Argo CD:

```yaml
apiVersion: v1
data:
  # Other groups and accounts omitted for brevity. Ensure that no other rolearns and/or groups are inadvertently removed, 
  # or you risk borking access to your cluster.
  #
  # The group name is a RoleBinding which you use to map to a [Cluster]Role. See https://kubernetes.io/docs/reference/access-authn-authz/rbac/#role-binding-examples  
  mapRoles: |
    - "groups":
      - "<GROUP-NAME-IN-K8S-RBAC>"
      "rolearn": "arn:aws:iam::<AWS_ACCOUNT_ID>:role/<IAM_CLUSTER_ROLE>"
      "username": "arn:aws:iam::<AWS_ACCOUNT_ID>:role/<IAM_CLUSTER_ROLE>"
```

Use the role ARN for both `rolearn` and `username`.

#### Alternative EKS Authentication Methods
In some scenarios it may not be possible to use IRSA, such as when the Argo CD cluster is running on a different cloud
provider's platform. In this case, there are two options:
1. Use `execProviderConfig` to call the AWS authentication mechanism which enables the injection of environment variables to supply credentials
2. Leverage the new AWS profile option available in Argo CD release 2.10

Both of these options will require the steps involving IAM and the `aws-auth` config map (defined above) to provide the 
principal with access to the cluster.

##### Using execProviderConfig with Environment Variables
```yaml
---
apiVersion: v1
kind: Secret
metadata:
  name: mycluster-secret
  labels:
    argocd.argoproj.io/secret-type: cluster
type: Opaque
stringData:
  name: mycluster
  server: https://mycluster.example.com
  namespaces: "my,managed,namespaces"
  clusterResources: "true"
  config: |
    {
      "execProviderConfig": {
        "command": "argocd-k8s-auth",
        "args": ["aws", "--cluster-name", "my-eks-cluster"],
        "apiVersion": "client.authentication.k8s.io/v1beta1",
        "env": {
          "AWS_REGION": "xx-east-1",
          "AWS_ACCESS_KEY_ID": "{{ .aws_key_id }}",
          "AWS_SECRET_ACCESS_KEY": "{{ .aws_key_secret }}",
          "AWS_SESSION_TOKEN": "{{ .aws_token }}"
        }
      },
      "tlsClientConfig": {
        "insecure": false,
        "caData": "{{ .cluster_cert }}"
      }
    }
```

This example assumes that the role being attached to the credentials that have been supplied, if this is not the case
the role can be appended to the `args` section like so:

```yaml
...
    "args": ["aws", "--cluster-name", "my-eks-cluster", "--role-arn", "arn:aws:iam::<AWS_ACCOUNT_ID>:role/<IAM_ROLE_NAME>"],
...
```
This construct can be used in conjunction with something like the External Secrets Operator to avoid storing the keys in
plain text and additionally helps to provide a foundation for key rotation.

##### Using An AWS Profile For Authentication
The option to use profiles, added in release 2.10, provides a method for supplying credentials while still using the
standard Argo CD EKS cluster declaration with an additional command flag that points to an AWS credentials file:
```yaml
apiVersion: v1
kind: Secret
metadata:
  name: mycluster-secret
  labels:
    argocd.argoproj.io/secret-type: cluster
type: Opaque
stringData:
  name: "mycluster.com"
  server: "https://mycluster.com"
  config: |
    {
      "awsAuthConfig": {
        "clusterName": "my-eks-cluster-name",
        "roleARN": "arn:aws:iam::<AWS_ACCOUNT_ID>:role/<IAM_ROLE_NAME>",
        "profile": "/mount/path/to/my-profile-file"
      },
      "tlsClientConfig": {
        "insecure": false,
        "caData": "<base64 encoded certificate>"
      }        
    }
```
This will instruct Argo CD to read the file at the provided path and use the credentials defined within to authenticate to AWS. 
The profile must be mounted in both the `argocd-server` and `argocd-application-controller` components in order for this to work.
For example, the following values can be defined in a Helm-based Argo CD deployment:

```yaml
controller:
  extraVolumes:
    - name: my-profile-volume
      secret:
        secretName: my-aws-profile
        items:
          - key: my-profile-file
            path: my-profile-file
  extraVolumeMounts:
    - name: my-profile-mount
      mountPath: /mount/path/to
      readOnly: true

server:
  extraVolumes:
    - name: my-profile-volume
      secret:
        secretName: my-aws-profile
        items:
          - key: my-profile-file
            path: my-profile-file
  extraVolumeMounts:
    - name: my-profile-mount
      mountPath: /mount/path/to
      readOnly: true
```

Where the secret is defined as follows:
```yaml
apiVersion: v1
kind: Secret
metadata:
  name: my-aws-profile
type: Opaque
stringData:
  my-profile-file: |
    [default]
    region = <aws_region>
    aws_access_key_id = <aws_access_key_id>
    aws_secret_access_key = <aws_secret_access_key>
    aws_session_token = <aws_session_token>
```

> ⚠️ Secret mounts are updated on an interval, not real time. If rotation is a requirement ensure the token lifetime outlives the mount update interval and the rotation process doesn't immediately invalidate the existing token

### GKE

GKE cluster secret example using argocd-k8s-auth and [Workload Identity](https://cloud.google.com/kubernetes-engine/docs/how-to/workload-identity):

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
  server: https://mycluster.example.com
  config: |
    {
      "execProviderConfig": {
        "command": "argocd-k8s-auth",
        "args": ["gcp"],
        "apiVersion": "client.authentication.k8s.io/v1beta1"
      },
      "tlsClientConfig": {
        "insecure": false,
        "caData": "<base64 encoded certificate>"
      }
    }
```

Note that you must enable Workload Identity on your GKE cluster, create GCP service account with appropriate IAM role and bind it to Kubernetes service account for argocd-application-controller and argocd-server (showing Pod logs on UI). See [Use Workload Identity](https://cloud.google.com/kubernetes-engine/docs/how-to/workload-identity) and [Authenticating to the Kubernetes API server](https://cloud.google.com/kubernetes-engine/docs/how-to/api-server-authentication).

### AKS

Azure cluster secret example using argocd-k8s-auth and [kubelogin](https://github.com/Azure/kubelogin).  The option *azure* to the argocd-k8s-auth execProviderConfig encapsulates the *get-token* command for kubelogin.  Depending upon which authentication flow is desired (devicecode, spn, ropc, msi, azurecli, workloadidentity), set the environment variable AAD_LOGIN_METHOD with this value.  Set other appropriate environment variables depending upon which authentication flow is desired.

|Variable Name|Description|
|-------------|-----------|
|AAD_LOGIN_METHOD|One of devicecode, spn, ropc, msi, azurecli, or workloadidentity|
|AZURE_CLIENT_CERTIFICATE_PATH|Path to AAD client cert in pfx.  Used in spn login and WorkloadIdentityLogin flow|
|AZURE_CLIENT_CERTIFICATE_PASSWORD|Password for the client cert in pfx.  Used in spn login|
|AZURE_CLIENT_ID|AAD client application ID|
|AZURE_CLIENT_SECRET|AAD client application secret|
|AAD_USER_PRINCIPAL_NAME|Used in the ropc flow|
|AAD_USER_PRINCIPAL_PASSWORD|Used in the ropc flow|
|AZURE_TENANT_ID|The AAD tenant ID.|
|AZURE_AUTHORITY_HOST|Used in the WorkloadIdentityLogin flow|
|AZURE_FEDERATED_TOKEN_FILE|Used in the WorkloadIdentityLogin flow|

In addition to the environment variables above, argocd-k8s-auth accepts two extra environment variables to set the AAD environment, and to set the AAD server application ID.  The AAD server application ID will default to 6dae42f8-4368-4678-94ff-3960e28e3630 if not specified.  See [here](https://github.com/azure/kubelogin#exec-plugin-format) for details.

|Variable Name|Description|
|-------------|-----------|
|AAD_ENVIRONMENT_NAME|The azure environment to use, default of AzurePublicCloud|
|AAD_SERVER_APPLICATION_ID|The optional AAD server application ID, defaults to 6dae42f8-4368-4678-94ff-3960e28e3630|

This is an example of using the [federated workload login flow](https://github.com/Azure/kubelogin#azure-workload-federated-identity-non-interactive).  The federated token file needs to be mounted as a secret into argoCD, so it can be used in the flow.  The location of the token file needs to be set in the environment variable AZURE_FEDERATED_TOKEN_FILE.

If your AKS cluster utilizes the [Mutating Admission Webhook](https://azure.github.io/azure-workload-identity/docs/installation/mutating-admission-webhook.html) from the Azure Workload Identity project, follow these steps to enable the `argocd-application-controller` and `argocd-server` pods to use the federated identity:

1. **Label the Pods**: Add the `azure.workload.identity/use: "true"` label to the `argocd-application-controller` and `argocd-server` pods.

2. **Create Federated Identity Credential**: Generate an Azure federated identity credential for the `argocd-application-controller` and `argocd-server` service accounts. Refer to the [Federated Identity Credential](https://azure.github.io/azure-workload-identity/docs/topics/federated-identity-credential.html) documentation for detailed instructions.

3. **Add Annotations to Service Account** Add `"azure.workload.identity/client-id": "$CLIENT_ID"` and `"azure.workload.identity/tenant-id": "$TENANT_ID"` annotations to the `argocd-application-controller` and `argocd-server` service accounts using the details from the federated credential.

4. **Set the AZURE_CLIENT_ID**: Update the `AZURE_CLIENT_ID` in the cluster secret to match the client id of the newly created federated identity credential.


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
  server: https://mycluster.example.com
  config: |
    {
      "execProviderConfig": {
        "command": "argocd-k8s-auth",
        "env": {
          "AAD_ENVIRONMENT_NAME": "AzurePublicCloud",
          "AZURE_CLIENT_ID": "fill in client id",
          "AZURE_TENANT_ID": "fill in tenant id", # optional, injected by workload identity mutating admission webhook if enabled
          "AZURE_FEDERATED_TOKEN_FILE": "/opt/path/to/federated_file.json", # optional, injected by workload identity mutating admission webhook if enabled
          "AZURE_AUTHORITY_HOST": "https://login.microsoftonline.com/", # optional, injected by workload identity mutating admission webhook if enabled
          "AAD_LOGIN_METHOD": "workloadidentity"
        },
        "args": ["azure"],
        "apiVersion": "client.authentication.k8s.io/v1beta1"
      },
      "tlsClientConfig": {
        "insecure": false,
        "caData": "<base64 encoded certificate>"
      }
    }
```

This is an example of using the spn (service principal name) flow.

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
  server: https://mycluster.example.com
  config: |
    {
      "execProviderConfig": {
        "command": "argocd-k8s-auth",
        "env": {
          "AAD_ENVIRONMENT_NAME": "AzurePublicCloud",
          "AZURE_CLIENT_SECRET": "fill in your service principal client secret",
          "AZURE_TENANT_ID": "fill in tenant id",
          "AZURE_CLIENT_ID": "fill in your service principal client id",
          "AAD_LOGIN_METHOD": "spn"
        },
        "args": ["azure"],
        "apiVersion": "client.authentication.k8s.io/v1beta1"
      },
      "tlsClientConfig": {
        "insecure": false,
        "caData": "<base64 encoded certificate>"
      }
    }
```

## Helm

* Helm charts
  * support the sources
    * [Helm repository](../user-guide/helm.md) OR
    * [OCI registry](../user-guide/oci.md)
  * [if they live | private repository](#repositories)

## Resource Exclusion/Inclusion

* resource exclusion 
  * -- from -- discovery & sync
  * those / ALWAYS excluded
    * `events.k8s.io/*`
    * `metrics.k8s.io/*`
    * `coordination.k8s.io/Lease`

* use cases
  * resources / impacts Argo CD's performance
    * Reason: 🧠TODO:🧠

* steps
  * | "argocd-cm" configMap, 
    * specify `data.resource.exclusions`
      * == [`FilteredResource`](/util/settings/filtered_resource.go)
    * specify `data.resource.inclusions`
      * == [`FilteredResource`](/util/settings/filtered_resource.go)

* final list of resources 
  * == group/kinds / specified | `resource.inclusions` - group/kinds / specified | `resource.exclusions`

* if you add a inclusion / matches EXISTING resources -> these resources appear as `OutOfSync`

* recommendations
  *  | your YAML,
    * if you use `SOME_GLOB` -> wrap it ('') == `'SOME_GLOB'`
      * Reason:🧠avoid parsing errors🧠
  * if you add a exclusion | ALREADY EXISTING resource -> restart the controller
    * Reason: 🧠excluded objects may ALREADY be | controller cache🧠

## Mask sensitive Annotations on Secrets

An optional comma-separated list of `metadata.annotations` keys 
can be configured with `resource.sensitive.mask.annotations` to mask their values in UI/CLI on Secrets.

```yaml
  resource.sensitive.mask.annotations: openshift.io/token-secret.value, api-key
```

## Auto respect RBAC for controller

Argo CD controller can be restricted from discovering/syncing specific resources using just controller RBAC, 
without having to manually configure resource exclusions.
This feature can be enabled by setting `resource.respectRBAC` key in argocd cm, once it is set the controller will automatically stop watching for resources 
that it does not have the permission to list/access. Possible values for `resource.respectRBAC` are:
    - `strict` : This setting checks whether the list call made by controller is forbidden/unauthorized and if it is, it will cross-check the permission by making a `SelfSubjectAccessReview` call for the resource.
    - `normal` : This will only check whether the list call response is forbidden/unauthorized and skip `SelfSubjectAccessReview` call, to minimize any extra api-server calls.
    - unset/empty (default) : This will disable the feature and controller will continue to monitor all resources.

Users who are comfortable with an increase in kube api-server calls can opt for `strict` option while users who are concerned with higher api calls and are willing to compromise on the accuracy can opt for the `normal` option.

Notes:

* When set to use `strict` mode controller must have RBAC permission to `create` a `SelfSubjectAccessReview` resource 
* The `SelfSubjectAccessReview` request will be only made for the `list` verb, it is assumed that if `list` is allowed for a resource then all other permissions are also available to the controller.

Example argocd cm with `resource.respectRBAC` set to `strict`:

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: argocd-cm
data:
  resource.respectRBAC: "strict"
```

## Resource Custom Labels

Custom Labels configured with `resource.customLabels` (comma separated string) will be displayed in the UI (for any resource that defines them). Note that this requires a restart to the Argo CD Application Controller to take effect.

## Labels on Application Events

An optional comma-separated list of `metadata.labels` keys can be configured with `resource.includeEventLabelKeys` to add to Kubernetes events generated for Argo CD Applications. When events are generated for Applications containing the specified labels, the controller adds the matching labels to the event. This establishes an easy link between the event and the application, allowing for filtering using labels. In case of conflict between labels on the Application and AppProject, the Application label values are prioritized and added to the event.

```yaml
  resource.includeEventLabelKeys: team,env*
```

To exclude certain labels from events, use the `resource.excludeEventLabelKeys` key, which takes a comma-separated list of `metadata.labels` keys.

```yaml
  resource.excludeEventLabelKeys: environment,bu
```

Both `resource.includeEventLabelKeys` and `resource.excludeEventLabelKeys` support wildcards.

## SSO & RBAC

* [SSO](./user-management/index.md)
* [RBAC](./rbac.md)

## "self-managed" Argo CD 

* requirements
  * ⚠️FIRSTLY, install Argo CD⚠️

* == 💡Argo CD is managed -- by -- Argo CD 💡
  * Reason: 🧠ALL settings -- are represented by -- Kubernetes manifests 🧠
  * _Examples:_ [ArgoCD demo](https://cd.apps.argoproj.io)
    * [configuration](https://github.com/argoproj/argoproj-deployments/tree/master/argocd)
