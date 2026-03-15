# Kubernetes-native CD tool /
## 's design
### declarative

* [here](declarative-vs-imperative.md)

### GitOps-based

* == Git repositories -- as -- 1! source of truth
  * declared | [Argo CD's Application](simple-application.yaml)

    ```yaml
    source:
      repoURL: https://github.com/argoproj/argocd-example-apps.git
      targetRevision: HEAD
      path: guestbook
    ```
  * workflow

    ```
    Developer → Git commit → Push → ArgoCD detects → Cluster updated
    
    # NO MANUAL cluster operations 
    ```

### application-centric view
TODO:

# allows
## GitOps enforcement
TODO:
## automated continuous delivery
TODO: