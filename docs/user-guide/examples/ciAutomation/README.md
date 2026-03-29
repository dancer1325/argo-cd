# requirements
* download software / enable you to run local Kubernetes clusters
    * [Docker desktop](https://docs.docker.com/get-started/introduction/get-docker-desktop/)
    * [kind](https://kind.sigs.k8s.io/) + [install Kubectl](https://kubernetes.io/docs/tasks/tools/#kubectl)
    * [minikube](https://minikube.sigs.k8s.io/docs/)
        * `kubectl` commands are wrapped -- via -- `minikube kubectl`
    * [microk8s](https://canonical.com/microk8s)
        * `kubectl` commands are wrapped -- via -- `microk8s kubectl`
* run a local Kubernetes cluster
    * -- via --
        * [Docker Desktop](https://docs.docker.com/desktop/use-desktop/kubernetes/#enable-kubernetes)
            * | Docker Desktop
                * Kubernetes > Create cluster > choose any cluster type
        * [Kind](https://kind.sigs.k8s.io/#installation-and-usage)
            * `kind create cluster`
        * minikube
            * `minikube start`
        * microk8s
    * `kubectl config current-context`
        * check Kubectl points to a context
* [install Argo CD](/docs/operator-manual/installation.md)

# structure

* [source code repo](https://github.com/dancer1325/argo-cd-hello-world-app)
* [config repo](https://github.com/dancer1325/argo-cd-hello-world-config)

```mermaid
flowchart TB
    subgraph CIPhase["🔨 CONTINUOUS INTEGRATION (CI)"]
        direction TB
        subgraph CITool["CI Tool: GitHub Actions"]
            direction TB
            A[Step 1: Bump version and push tag]
            B[Step 2: Build Container Image <br/> Push to Container Registry]
            C[Step 3: Clone config repo <br/> Update Image tag in TEST and push to config repo]
        end
        A --> B --> C
    end

    SourceRepo["📁 Git Repository<br/>(Source Code Repo)<br/>Application source code:<br/>main.go"]

    subgraph GitRepo["📁 Git Repository (Config Repo)"]
        Manifests["deployment.yaml, service.yaml"]
        ValuesTest["values.test.yaml"]
        ValuesPreprod["values.preprod.yaml"]
        ValuesProd["values.prod.yaml"]
    end

    subgraph K8sInfra["☸️ Kubernetes Cluster Infra (ArgoCD)"]
        direction TB
        subgraph ArgoCD["ArgoCD Controller"]
            direction TB
            D[Auto-Detect Changes]
            AppTest["Application<br/>hello-world-test<br/>(application.test.yaml)"]
            AppPreprod["Application<br/>hello-world-preprod<br/>(application.preprod.yaml)"]
            AppProd["Application<br/>hello-world-prod<br/>(application.prod.yaml)"]
            AppSet["ApplicationSet<br/>hello-world<br/>(applicationSet.yaml)<br/>💡alternative to 3 Applications💡"]
        end
        D --> |OPTION1| AppTest
        D --> |OPTION1| AppPreprod
        D --> |OPTION1| AppProd
        D -.->|"OPTION2"| AppSet
    end

    K8sTest["☸️ Kubernetes Cluster Test"]
    K8sPreProd["☸️ Kubernetes Cluster Preprod"]
    K8sProd["☸️ Kubernetes Cluster Prod"]

    SourceRepo -->|onPush master| CITool
    C -->|git push| ValuesTest
    ValuesTest -->|detects changes| D
    ValuesPreprod -->|detects changes| D
    ValuesProd -->|detects changes| D
    AppTest -->|deploys via values.test.yaml| K8sTest
    AppPreprod -->|deploys via values.preprod.yaml| K8sPreProd
    AppProd -->|deploys via values.prod.yaml| K8sProd
    AppSet -.->|deploys all| K8sTest
    AppSet -.->|deploys all| K8sPreProd
    AppSet -.->|deploys all| K8sProd

    style CIPhase fill:#e3f2fd,stroke:#1565c0,stroke-width:3px
    style K8sInfra fill:#e8f5e9,stroke:#e65100,stroke-width:3px
    style CITool fill:#bbdefb,stroke:#1976d2,stroke-width:2px
    style ArgoCD fill:#ffe0b2,stroke:#f57c00,stroke-width:2px
    style SourceRepo fill:#fce4ec,stroke:#c62828,stroke-width:2px
    style GitRepo fill:#f3e5f5,stroke:#7b1fa2,stroke-width:2px
    style K8sTest fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px
    style K8sPreProd fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px
    style K8sProd fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px
    style AppSet fill:#fff9c4,stroke:#f9a825,stroke-width:2px
```

# steps
* TODO: 