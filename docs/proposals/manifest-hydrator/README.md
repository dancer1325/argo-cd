# Argo CD Manifest Hydrator

* Argo CD
  * [Application sources](/docs/user-guide/application_sources.md)
    * NORMALLY -- through -- tools (Helm, Kustomize, Jsonnet, ...)
      * ❌NOT plain Kubernetes manifests❌
      * cons
        * harder to understand the FULL application's state
  * provides
    * first-class tooling -- to -- hydrate manifests + push the manifests | git

* 💡Hydrating the sources + pushing the hydrated manifests | git💡
  * == common technique / preserve a full history of an Application's state
  * pros
    * FULL manifests VISIBLE | Git
    * complete audit trail
    * easier debugging
  * ⚠️requirements⚠️
    * Argo CD needs [Git write access](#git-write-access)
    * additional branch

## WITHOUT source hydrator vs WITH source hydrator 

### WITHOUT Source Hydrator (Traditional Flow)

* cons
  * FINAL manifests are NOT visible | Git

```
┌─────────────────────────────────────────────────────────────┐
│  Git Repository                                              │
│  ┌────────────────────────────────────────────────────┐     │
│  │  Helm Chart / Kustomize / Jsonnet                  │     │
│  │  (Dry source - templates only)                     │     │
│  └────────────────────────────────────────────────────┘     │
└────────────────────↑────────────────────────────────────────┘
                     │ READ only (git fetch/pull)
                     │
            ┌────────────────────┐
            │  ArgoCD            │
            │  • Fetch source    │
            │  • Hydrate in-mem  │
            │  • Generate YAML   │
            └────────┬───────────┘
                     │
                     │ Apply manifests
                     ↓
            ┌────────────────────┐
            │  Kubernetes        │
            │  Cluster           │
            └────────────────────┘
```

### WITH source hydrator

```
┌─────────────────────────────────────────────────────────────┐
│  Git Repository                                              │
│                                                              │
│  ┌────────────────────────────────────────────────────┐     │
│  │  Branch: main                                       │     │
│  │  Helm Chart / Kustomize / Jsonnet                  │     │
│  │  (Dry source - templates only)                     │     │
│  └────────────────────────────────────────────────────┘     │
│                     ↑                                        │
│                     │ READ (git fetch)                       │
│                     │                                        │
│            ┌────────────────────┐                            │
│            │  ArgoCD            │                            │
│            │  • Fetch source    │                            │
│            │  • Hydrate         │                            │
│            │  • Generate YAML   │                            │
│            └────────┬───────────┘                            │
│                     │                                        │
│                     │ WRITE (git push -- via -- Commit Server)     │
│                     ↓                                        │
│  ┌────────────────────────────────────────────────────┐     │
│  │  Branch: hydrated/prod                             │     │
│  │  deployment.yaml (final)                           │     │
│  │  service.yaml (final)                              │     │
│  │  configmap.yaml (final)                            │     │
│  │  (Hydrated manifests - ready to apply)             │     │
│  └────────────────────────────────────────────────────┘     │
└────────────────────↑────────────────────────────────────────┘
                     │ READ (git fetch)
                     │
            ┌────────────────────┐
            │  ArgoCD Sync       │
            │  from hydrated     │
            │  branch            │
            └────────┬───────────┘
                     │
                     │ Apply manifests
                     ↓
            ┌────────────────────┐
            │  Kubernetes        │
            │  Cluster           │
            └────────────────────┘
```

## Git write access

### security considerations

* Argo CD
  * 👀stores git push secrets SEPARATELY👀
    * -- from --
      * the main Argo CD components
      * git pull credentials
    * Reason:🧠minimize the possibility of a malicious actor🧠

* recommended actions to take
  * configure your SCM's security mechanisms / Argo CD ONLY push | 
    * SPECIFIC repository
    * SPECIFIC branches

### how to add access credentials?

* steps
  * add a secret | `argocd-push` namespace

    ```yaml
    apiVersion: v1
    kind: Secret
    metadata:
      name: argocd-example-apps
      labels:
        # Note that this is "repository-push" instead of "repository"
        # The same secret should never be used for both push and pull access.
        argocd.argoproj.io/secret-type: repository-push
    type: Opaque
    stringData:
      url: https://github.com/argoproj/argocd-example-apps.git
      username: '****'
      password: '****'
    ```

* enable
  * 👀Application / has pull access | GIVEN repo -> can push -- , via source hydration, to -- this GIVEN repo👀
