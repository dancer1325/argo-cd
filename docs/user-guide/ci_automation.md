# Automation from CI Pipelines

* goal
  * how to automate CI pipelines / CD is managed -- by -- Argo CD

* != traditional CI pipeline
  * Reason: 🧠declarative vs imperative🧠

```mermaid
flowchart TB
    SourceRepo["📁 Git Repository<br/>(Source Code Repo)<br/>main.go, pom.xml, package.json, etc."]

    subgraph CIPhase["🔨 CONTINUOUS INTEGRATION (CI)"]
        direction TB
        subgraph CITool["CI Tool: GitHub Actions / Jenkins / Tekton / ..."]
            direction TB
            A[Step 1: Build Container Image<br/>docker build -t image:vX.Y]
            B[Step 2: Push to Registry<br/>docker push image:vX.Y]
            C[Step 3: Update Git Manifests<br/>kustomize edit set image]
            F[Step 4 OPTIONAL:<br/>Trigger Sync<br/>argocd app sync]
        end
        A --> B --> C
        C -.->|optional| F
    end

    GitRepo["📁 Git Repository<br/>(Config Repo)<br/>Kubernetes Manifests:<br/>deployment.yaml, service.yaml, etc."]

    subgraph CDPhase["🚀 CONTINUOUS DELIVERY (CD)"]
        direction TB
        subgraph K8sInfra["☸️ Kubernetes Cluster (Infra)"]
            direction TB
            subgraph ArgoCD["ArgoCD Controller"]
                direction TB
                D[Auto-Detect Changes]
                E[Sync to Cluster<br/>kubectl apply]
            end
            D --> E
        end
    end

    K8s["☸️ Kubernetes Cluster<br/>Running Pods with vX.Y"]

    SourceRepo -->|onPush/onMerge/... triggers| CITool
    C -->|git push| GitRepo
    GitRepo -->|automatic| D
    F -.->|manual trigger| E
    E -->|deploys| K8s

    style CIPhase fill:#e3f2fd,stroke:#1565c0,stroke-width:3px
    style CDPhase fill:#fff3e0,stroke:#e65100,stroke-width:3px
    style K8sInfra fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px
    style CITool fill:#bbdefb,stroke:#1976d2,stroke-width:2px
    style ArgoCD fill:#ffe0b2,stroke:#f57c00,stroke-width:2px
    style GitRepo fill:#f3e5f5,stroke:#7b1fa2,stroke-width:2px
    style K8s fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px
    style SourceRepo fill:#fce4ec,stroke:#c62828,stroke-width:2px
```

## steps

### build & publish a NEW container image

```bash
docker build -t tagName:vX.Y .
docker push tagName:vX.Y
```

* handled -- by -- CI tool

### update the local manifests -- via -- your preferred templating tool + push the changes | Git

```bash
git clone https://github.com/serviceName-config.git
cd serviceName-config

# kustomize
kustomize edit set image tagName:vX.Y

# plain yaml
kubectl patch --local -f config-deployment.yaml -p '{"spec":{"template":{"spec":{"containers":[{"name":"guestbook","image":"mycompany/guestbook:v2.0"}]}}}}' -o yaml > config-deployment.yaml

git commit -am "Update guestbook to v2.0"
git push
```

* recommendations
  * 👀git repository / hold your application source code != git repository / hold your Kubernetes manifests👀
  * [MORE](best_practices.md)

* handled -- by -- CI tool

### Synchronize the app (OPTIONAL)

* `argocd app sync APPNAME`

* handled | CI pipeline
  * ⚠️OPTIONAL⚠️
    * Reason: 🧠if you configure [automated synchronization](auto_sync.md) -> this step is unnecessary🧠

* argocd CLI
  * 👀can be downloaded directly -- from the -- API server👀
    * -> argocd CLI / used | CI pipeline: ALWAYS compatible -- with the -- Argo CD API server

    ```bash
    export ARGOCD_SERVER=argocd.example.com
    export ARGOCD_AUTH_TOKEN=<JWT token generated from project>
    curl -sSL -o /usr/local/bin/argocd https://${ARGOCD_SERVER}/download/argocd-linux-amd64
    argocd app sync guestbook
    argocd app wait guestbook
    ```

* 👀ways of sync👀
  * [automatic sync policy](auto_sync.md)
    * recommended one
  * [`argocd app sync APPNAME`](ci_automation.md)
    * triggered -- by -- CI
    * performed -- by -- Argo CD (`argocd ...`)
