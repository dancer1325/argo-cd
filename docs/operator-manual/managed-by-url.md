# Managed By URL Annotation

## Overview

* `argocd.argoproj.io/managed-by-url` annotation 
  * enable
    * 👀Application resource can specify the Argo CD instance / manages it👀
  * uses
    * \>1 Argo CD instances & need application links | UI / point -- to the -- correct ArgoCD instance
      * == if you click | child Applications | primary ArgoCD instance's UI -> open them | secondary Argo CD instance 
      * otherwise,
        * if you click | child Applications | primary ArgoCD instance's UI -> tries to open them | primary Argo CD instance
          * -> fail
      * _Example:_ [app-of-apps pattern](cluster-bootstrapping.md)
  * use cases
    * [multi-tenant setups](/manifests/README.md#multi-tenant)
    * [App Of Apps Pattern](cluster-bootstrapping.md#app-of-apps-pattern-alternative)

## Configuration

TODO:
### Annotation Format

| Field | Value |
|-------|-------|
| **Annotation** | `argocd.argoproj.io/managed-by-url` |
| **Target** | Application |
| **Value** | Valid HTTP(S) URL |
| **Required** | No |

### URL Validation

The annotation value **must** be a valid HTTP(S) URL:

- ✅ `https://argocd.example.com`
- ✅ `https://argocd.example.com:8080`
- ✅ `http://localhost:8080` (for development)
- ❌ `argocd.example.com` (missing protocol)
- ❌ `javascript:alert(1)` (invalid protocol)

Invalid URLs will prevent the Application from being created or updated.

### Behavior

When generating application links, Argo CD:
- **Without annotation**: Uses the current instance's base URL
- **With annotation**: Uses the URL from the annotation
- **Invalid annotation**: Falls back to the current instance's base URL and logs a warning

> [!WARNING]
> Ensure the URL in the annotation is accessible from users' browsers
* For internal deployments, use internal DNS names or configure appropriate network access.

## Testing Locally

To test the annotation with two local Argo CD instances:

```bash
# Install primary instance
kubectl create namespace argocd
kubectl apply -n argocd --server-side --force-conflicts -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml

# Install secondary instance
kubectl create namespace namespace-b
kubectl apply -n namespace-b --server-side --force-conflicts -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml

# Port forward both instances
kubectl port-forward -n argocd svc/argocd-server 8080:443 &
kubectl port-forward -n namespace-b svc/argocd-server 8081:443 &

# Wait for Argo CD to be ready
kubectl wait --for=condition=available --timeout=300s deployment/argocd-server -n argocd

# Get the admin password for primary instance
kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d && echo

```

Then:
1
* Open `http://localhost:8080` in your browser
2
* Login with username `admin` and the password from the command above
3
* Navigate to the `parent-app` Application
4
* Click on the `child-app` in the resource tree
5
* It should redirect to `http://localhost:8081/applications/namespace-b/child-app`

You will need to repeat the command to get the password for the secondary instance to login and access the child-app

```bash
# Get the admin password for secondary instance
kubectl -n namespace-b get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d && echo
```

## Troubleshooting

### Links Still Point to Wrong Instance

**Check if the annotation is present:**

```bash
kubectl get application child-app -n instance-b -o jsonpath='{.metadata.annotations.argocd\.argoproj\.io/managed-by-url}'
```

Expected output: A complete URL like `http://localhost:8081` or the url that has been set 
i.e `https://secondary-argocd.example.com`

**If the annotation is present but links still don't work:**
- Verify the URL is accessible from your browser
- Check browser console for errors
- Ensure the URL format is correct (includes `http://` or `https://`)

### Application Creation Fails

If Application creation fails with "invalid managed-by URL" error:

- ✅ URL includes protocol (`https://` or `http://`)
- ✅ URL contains no typos
- ✅ URL uses only valid characters
- ✅ URL is not a potentially malicious scheme (e.g., `javascript:`)

### Nested Applications Not Working

For app-of-apps patterns, ensure:
1
* The child Application YAML in Git includes the annotation
2
* The parent Application has synced successfully
3
* The child Application has been created in the cluster

Verify the child Application exists:

```bash
kubectl get application CHILD-APP-NAME -n NAMESPACE
```

## See Also

- [Application Annotations](../user-guide/annotations-and-labels.md)
- [App of Apps Pattern](cluster-bootstrapping.md)
- [Deep Links](deep_links.md)
