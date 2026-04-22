* goal
  * example RBAC for Kubernetes / enable
    * Argo CD API Server (`argocd-server`) can perform CRUD operations | `Application` CRs | ALL cluster's namespaces
    * "argocd-notifications-controller" can notify apps | ALL namespaces

* requirements
  * Argo CD is installed | default namespace (`argocd`)
    * OTHERWISE, edit the "*-clusterrolebinding" / bind to the ServiceAccount | correct namespace
