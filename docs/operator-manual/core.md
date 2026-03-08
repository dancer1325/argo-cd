# Argo CD Core

## Introduction

* Argo CD Core
  * == runs Argo CD / headless mode
  * features / 
    * AVAILABLE
      * GitOps functionality
    * NOT AVAILABLE
      - Argo CD RBAC model
      - Argo CD API
      - Argo CD Notification Controller
      - OIDC based authentication
    * [partially available](#using)
      - Argo CD Web UI
      - Argo CD CLI
      - Multi-tenancy (strictly GitOps based on git push permissions)
  * use cases
    - ONLY rely on 
      - Kubernetes RBAC
      - Kubernetes API
    - NOT provide to developers
      - Argo CD UI
      - Argo CD CLI 
  * audience
    * cluster admin

## Architecture

* install fewer components

![Argo CD Core](../assets/argocd-core-components.png)

* Redis
  * STILL included here
  * it can be uninstalled
    * ❌NOT recommended❌
      * Reason:🧠reduce the load |
        * Kube API
        * Git🧠
    * Reason:🧠Argo CD controller can run WITHOUT Redis🧠
  * uses
    * as caching mechanism -- by -- Argo CD controller

## Installing

* steps

  ```
  export ARGOCD_VERSION=<desired argo cd release version (e.g. v2.7.0)>
  kubectl create namespace argocd
  kubectl apply -n argocd --server-side --force-conflicts -f https://raw.githubusercontent.com/argoproj/argo-cd/$ARGOCD_VERSION/manifests/core-install.yaml
  ```

## Using

TODO: 
Once Argo CD Core is installed, users will be able to interact with it
by relying on GitOps. The available Kubernetes resources will be the
`Application` and the `ApplicationSet` CRDs. By using those resources,
users will be able to deploy and manage applications in Kubernetes.

It is still possible to use Argo CD CLI even when running Argo CD
Core. In this case, the CLI will spawn a local API server process that
will be used to handle the CLI command. Once the command is concluded,
the local API Server process will also be terminated. This happens
transparently for the user with no additional command required. Note
that Argo CD Core will rely only on Kubernetes RBAC and the user (or
the process) invoking the CLI needs to have access to the Argo CD
namespace with the proper permission in the `Application` and
`ApplicationSet` resources for executing a given command.

To use [Argo CD CLI](https://argo-cd.readthedocs.io/en/stable/cli_installation) in core mode, it is required to pass the `--core`
flag with the `login` subcommand. The `--core` flag is responsible for spawning a local Argo CD API server
process that handles CLI and Web UI requests.

Example:

```bash
kubectl config set-context --current --namespace=argocd # change current kube context to argocd namespace
argocd login --core
```

Similarly, users can also run the Web UI locally if they prefer to
interact with Argo CD using this method. The Web UI can be started
locally by running the following command:

```
argocd admin dashboard -n argocd
```

Argo CD Web UI will be available at `http://localhost:8080`
