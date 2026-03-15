# Kubernetes-native CD tool /
## 's design
### GitOps-based

#### Git repositories -- as -- 1! source of truth
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
#### declarative

* [here](declarative-vs-imperative.md)

### application-centric view

* == ALL Kubernetes objects grouped -- based on -- Argo CD's Application
  * != namespace-view OR cluster-view

* TODO: link to simple case
