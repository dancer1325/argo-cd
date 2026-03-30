# Tools

## | production

* Argo CD
  * supports
    * 💡MULTIPLE ways to define Kubernetes manifests💡
      * raw yaml
      * [Kustomize](kustomize.md) applications
      * [Helm](helm.md) charts
      * [OCI](oci.md) images
      * [Jsonnet](jsonnet.md) manifests
      * [custom config management tool](../operator-manual/config-management-plugins.md) / configured -- as a -- config management plugin
        * == custom tools
  * 💡[Application's `spec.source`](/manifests/crds/application-crd.yaml)💡
    * == specify application source

* how are those Kubernetes manifests used?
  * Argo CD transforms -- to -- FINAL FULL Kubernetes manifest 

## | development

* Argo CD
  * supports
    * uploading DIRECTLY local manifests -- `argocd app sync APPNAME --local ...` -- 
      * local
        * != push | Git
      * ⚠️anti-pattern of the GitOps paradigm⚠️
        * ONLY ALLOWED | development
      * requirements
        * user / `override` permission
      * ALLOWED | [ANY way to define Kubernetes manifests](#-production)

```mermaid
flowchart LR
    subgraph LocalMachine["💻 Local Machine"]
        Local["📁 Local Directory<br/>manifests/ or helm/ or kustomize/"]
        CLI["argocd app sync APPNAME --local PATH"]
        Local --> CLI
    end

    subgraph Cluster["☸️ Kubernetes Cluster"]
        ArgoCD["⚙️ ArgoCD Server<br/>(renders manifests)"]
        K8s["🗂️ Kubernetes Resources<br/>(Deployments, Services, ...)"]
        ArgoCD -->|kubectl apply| K8s
    end

    CLI -->|sends local files| ArgoCD

    Git["📁 Git Repository"]
    Git -. "NOT involved\n(anti-pattern)" .-> ArgoCD

    style LocalMachine fill:#e3f2fd,stroke:#1565c0,stroke-width:2px
    style Local fill:#bbdefb,stroke:#1976d2,stroke-width:2px
    style CLI fill:#fff3e0,stroke:#e65100,stroke-width:2px
    style ArgoCD fill:#ffe0b2,stroke:#f57c00,stroke-width:2px
    style K8s fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px
    style Cluster fill:#f3e5f5,stroke:#7b1fa2,stroke-width:2px
    style Git fill:#fce4ec,stroke:#c62828,stroke-width:2px
```
