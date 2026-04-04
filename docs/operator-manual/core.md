# Argo CD Core

## Introduction

* Argo CD Core
  * [manifest](/manifests/core-install.yaml)
  * == runs Argo CD / headless mode (== WITHOUT UI)
  * features / 
    * AVAILABLE
      * GitOps functionality
    * ❌NOT AVAILABLE❌
      - Argo CD RBAC model
        - _Example:_ ANY command / require RBAC, does NOT work
      - Argo CD API
      - Argo CD Notification Controller
      - OIDC based authentication
    * [partially available](#how-to-use)
      - Argo CD Web UI
      - Argo CD CLI
      - Multi-tenancy 
        - strictly GitOps
          - == -- based on -- git push permissions
  * use cases
    - ONLY rely on 
      - Kubernetes RBAC
      - Kubernetes API
        - Reason:🧠Argo CD API server does NOT exist🧠
    - NOT provide to developers
      - Argo CD UI
      - Argo CD CLI 
  * audience
    * cluster admin

## Architecture

* install fewer components
  * == install non-HA / EACH component

    ![Argo CD Core](../assets/argocd-core-components.png)

* Redis
  * STILL included
  * it can be uninstalled
    * ❌NOT recommended❌
      * Reason:🧠reduce the load |
        * Kube API
        * Git🧠
    * Reason:🧠Argo CD controller can run WITHOUT Redis🧠
  * uses
    * as caching mechanism -- by -- Argo CD controller

## how to install?

* steps

  ```
  # 1. specifying version
  export ARGOCD_VERSION=<desired argo cd release version (e.g. v2.7.0)>
  kubectl create namespace argocd
  kubectl apply -n argocd --server-side --force-conflicts -f .com/argoproj/argo-cd/$ARGOCD_VERSION/manifests/core-install.yaml
  # create MANUALLY the project .yaml
  kubectl apply -f defaultProjectManually.yaml
  
  # 2. | this repo
  kubectl create namespace argocd
  # | this repo's host path
  kubectl apply -n argocd --server-side --force-conflicts -f manifests/core-install.yaml
  # | examples/core, create MANUALLY the project .yaml
  kubectl apply -f defaultProjectManually.yaml
  ```

## how to use?

* steps
  ```bash 
  # context.namespace NOT set
  #   `kubectl config get-contexts kind-kind`  namespace  == empty
  kubectl config set-context --current --namespace=argocd 
  #   `kubectl config get-contexts kind-kind`  namespace  == argocd
  
  argocd login --core
  # `argocd context`    points DIRECTLY -- to -- Kubernetes server
  
  # if you want to run Argo CD Web UI
  argocd admin dashboard -n argocd
  #   | browser,  http://localhost:8080 
  ```

## how does it work?

* Argo CD CLI
  * launches a local API server process /
    * can handle
      * CLI requests
      * Web UI requests
    * | conclude the command, it's terminated
    * transparent -- for the -- user 
      * == NO ADDITIONAL command REQUIRED
