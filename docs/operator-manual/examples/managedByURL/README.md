* goal
  * App Of Apps Pattern

# structure
* [parent Application](parentApplication.yaml) | primary Argo CD instance
* [child application](childApplication.yaml) | secondary Argo CD instance

# Application resource can specify the Argo CD instance / manages it
* steps
  * | primary ArgoCD instance's UI,
    * click | `child-app` -> navigates -- to -- `https://secondary-argocd.example.com/applications/namespace-b/child-app`
      * == opens the child Application | secondary Argo CD instance UI
