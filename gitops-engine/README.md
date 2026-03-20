# GitOps Engine

* goal
  * implement core GitOps features
    - Kubernetes resource cache ✅
    - Resources reconciliation ✅
    - Sync Planning ✅
    - Access to Git repositories
    - Manifest Generation

* GitOps operators 
  * SIMILAR core features
  * provide
    * DIFFERENT user experiences 
  * use cases
    * MULTIPLE

## Usage

* -- by -- 
  * Argo CD project
    * MAIN goal
  * OTHER projects / need GitOps features

* steps to use
  * | your Go module

    ```bash
    go get github.com/argoproj/argo-cd/gitops-engine
    ```
