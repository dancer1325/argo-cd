# The Argo CD web terminal session does not handle the revocation of user permissions properly.

- **GHSA:** [GHSA-v8wx-v5jq-qhhw](https://github.com/argoproj/argo-cd/security/advisories/GHSA-v8wx-v5jq-qhhw)
- **CVE:** CVE-2024-41666
- **Severity:** medium
- **Published:** 2024-07-24T10:49:21Z

## Description

Dear Argo CD Security Team,
We are a security research group. We studied Argo CD v2.11.3 and before, discovering that even if the user's ```p, role:myrole, exec, create, */*, allow``` permissions are revoked, the user can still send any Websocket message, which allows the user to view sensitive information. Even though they shouldn't have such access.
## Description
Argo CD has a Web-based terminal that allows you to get a shell inside a running pod, just like you would with kubectl exec. However, when the administrator enables this function and grants permission to the user ```p, role:myrole, exec, create, */*, allow```, even if the user revokes this permission, the user can still perform operations in the container, as long as the user keeps the terminal view open for a long time. CVE-2023-40025 Although the token expiration and revocation of the user are fixed, however, the fix does not address the situation of revocation of only user ```p, role:myrole, exec, create, */*, allow``` permissions, which may still lead to the leakage of sensitive information.
## Threat model
As a declarative GitOps CD for Kubernetes, we assume that the administrator has enabled the Web-based Terminal function of Argo CD. The administrator grants permissions to the attacker ```p, role:myrole, exec, create, */*, allow```, and then revokes the permissions.
## Environment
Kubernetes:       v1.30.2
Argo CD:           v2.11.3
## Attack steps
### 1.   Configure Attack Environment. 
#### 1.1 Deploy Argo CD.
```
kubectl create namespace argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/v2.11.3/manifests/install.yaml

```
#### 1.2 The administrator creates the attacker user 'test'.
Add 'accounts.test: login' to the argocd-cm ConfigMap

#### 1.3 The administrator enables the Web-based Terminal feature of Argo CD.
Set 'exec.enabled' to ”true” on the argocd-cm ConfigMap
Patch the argocd-server ClusterRole to allow argocd-server to exec into pods
```
- apiGroups:
  - ""
  resources:
  - pods/exec
  verbs:
  - create

```
#### 1.4 Create a GitHub repository with the following contents in the 'dev' directory.

```
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: Pods-reader
  namespace: test
rules:
- apiGroups:
  - ""
  resources:
  - pods
  verbs:
  - get
  - list
  - watch
—--
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: example-rolebinding
  namespace: test
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: Role
  name: Pods-reader
subjects:
- kind: ServiceAccount
  name: example-serviceaccount
  namespace: test
—--
apiVersion: v1
kind: ServiceAccount
metadata:
  name: example-serviceaccount
  namespace: test
—--
apiVersion: v1
kind: Pod
metadata:
  name: test
  namespace: test
spec:
  serviceAccountName: example-serviceaccount
  containers:
  - name: test
    image: ubuntu:latest
    command: ["sh", "-c", "sleep infinity"]

```
My GitHub repository is located at[ https://github.com/ClownandBox/argocd-lab.git](https://github.com/ClownandBox/argocd-lab.git)
#### 1.5 The administrator creates a project named 'test'.
```
cat <<EOF > appproject.yaml
apiVersion: argoproj.io/v1alpha1
kind: AppProject
metadata:
  name: test
  namespace: argocd
spec:
  sourceRepos:
  - https://github.com/ClownandBox/argocd-lab.git 
  destinations:
  - name: in-cluster
    namespace: test
    server: https://kubernetes.default.svc 
  namespaceResourceWhitelist:
  - group: '*'
    kind: Role
  - group: '*'
    kind: RoleBinding
  - group: '*'
    kind: ServiceAccount
  - group: '*'
    kind: Pod
EOF
```
```
kubectl apply -f appproject.yaml
```
The administrator creates an app named 'test'.
```
kubectl create ns test
```
```
cat <<EOF > app.yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: test
  namespace: argocd
spec:
  destination:
    namespace: test
    server: https://kubernetes.default.svc
  project: test
  source:
    path: dev
    repoURL: https://github.com/ClownandBox/argocd-lab.git
    targetRevision: HEAD
EOF
```
```
kubectl apply -f app.yaml

```
#### 1.6 The administrator performs a ‘sync’ on the app

### 2.   The administrator grants the attacker 'test' permissions.
Add the following content to the argocd-rbac-cm ConfigMap
```
data:
  policy.csv: |-
    p, role:operator1, applications, get, test/*, allow
    p, role:operator1, exec, create, test/*, allow
    g, test, role:operator1

```
### 3.   The attacker logs into the Argo CD UI and accesses the Terminal interface.

### 4.   The administrator revokes all permissions from the attacker but retains access to the UI interface.
Remove the following content from the argocd-rbac-cm ConfigMap
```
data:
  policy.csv: |-
    p, role:operator1, applications, get, test/*, allow
    p, role:operator1, exec, create, test/*, allow
    g, test, role:operator1

```
### 5.  Verify the results.
 At this point, the attacker can remain inside the container and perform operations

Here is the video of the PoC
https://drive.google.com/file/d/1Fynj5Sho8Lf8CETqsNXZyPKlTDdmgJuN/view?usp=sharing


### Patches
A patch for this vulnerability has been released in the following Argo CD versions:

v2.11.7
v2.10.16
v2.9.21

### For more information
If you have any questions or comments about this advisory:

Open an issue in [the Argo CD issue tracker](https://github.com/argoproj/argo-cd/issues) or [discussions](https://github.com/argoproj/argo-cd/discussions)
Join us on [Slack](https://argoproj.github.io/community/join-slack) in channel #argo-cd

### Credits
This vulnerability was found & reported by 
Shengjie Li, Huazhong University of Science and Technology
Zhi Li, Huazhong University of Science and Technology
Weijie Liu, Nankai University

The Argo team would like to thank these contributors for their responsible disclosure and constructive communications during the resolve of this issue

## Affected Versions

| Package | Vulnerable Range | Patched |
|---------|-----------------|---------|
|  github.com/argoproj/argo-cd ( Go ) | 2.6.0through2.11.3 | 2.11.7,2.10.16,2.9.21 |
