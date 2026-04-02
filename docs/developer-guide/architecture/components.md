# Component Architecture

* goal
  * ArgoCD components

* Argo CD
  * 💡's design: component-based💡
    * Reason:🧠separate the responsibility | DIFFERENT deployable units🧠
  * [default installation](/manifests/install.yaml) 
    * MULTIPLE DIFFERENT components
    * Kubernetes controllers
      * == ArgoCD's GitOps logic
      * ❌!= "components"❌
        * Reason:🧠
          * ArgoCD's core == main logic
          * MANDATORY == NOT replaceable 🧠

* separate the responsibility
  * benefits
    - **Modularity**
      - == pretty flexible
        - == components can be replaced & omit 
          - requirements: fit the contract interface
      - components interact -- , via an interface, with -- each other
    - **1! responsibility**
      - == 1 responsibility / EACH component
    - **Reusability**
      - Reason: 🧠thanks to meet contract interface🧠

## Dependencies

![Components Diagram](../../assets/argocd-components.png)

* logical layers
  - 👀dependency relationship: top-down👀
    - == components | top layers can depend -- on -- components | below layers
  - are
    - **UI**
      - audience
        - users
    - **Application**
      - == BFF BETWEEN UI -- & -- Core layer
    - **Core**
      - implement
        - main Argo CD GitOps functionality
    - **Infra**
      - == tools / Argo CD depends on

## Responsibility

### Webapp

* allows
  * managing applications / deployed | Kubernetes cluster

### ArgoCD CLI 

* allows 
  * interacting -- with -- Argo CD API
* audience
  * users
  * CI
* use cases
  * automation & scripting

### API Server

* define the Argo CD API
* audience
  * UI layer components

### Application Controller

* responsible for
  * reconciling the
    * Application resource | Kubernetes
      * == 
        * application's desired state (== provided in Git) == application's live state (== real one)
    * Project resource

### ApplicationSet Controller

* responsible for
  * reconciling the ApplicationSet resource

### Repo Server

* responsible for
  * interacting with the Git repository
    * Reason:🧠get application's Kubernetes resources' desired state🧠 

### Redis

* responsible for
  * reducing requests to
    * Kube API
    * Git provider
  * few UI operations

### Kube API

* == kube-api-server
* audience
  * Argo CD controllers
* responsible for
  * run the reconciliation loop

### Git

* provide
  * Kubernetes object's desired state

* "git"
  * ALLOWED values
    * git repo
    * Helm repo
    * OCI artifact repo

### Dex

* [here](../../operator-manual/user-management/index.md)
