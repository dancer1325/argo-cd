# requirements
* download software / enable you to run local Kubernetes clusters
  * [Docker desktop](https://docs.docker.com/get-started/introduction/get-docker-desktop/)
  * [kind](https://kind.sigs.k8s.io/) + [install Kubectl](https://kubernetes.io/docs/tasks/tools/#kubectl)
  * [minikube](https://minikube.sigs.k8s.io/docs/)
    * `kubectl` commands are wrapped -- via -- `minikube kubectl`
  * [microk8s](https://canonical.com/microk8s)
    * `kubectl` commands are wrapped -- via -- `microk8s kubectl`
* run ⚠️2⚠️ local Kubernetes cluster
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
* [install Argo CD](../../../installation.md)
* login
  * `kubectl get secret argocd-initial-admin-secret -n argocd -o jsonpath='{.data.password}' | base64 -d`
    * get initial admin password
  * `argocd login localhost:8080 --insecure`
    * user: admin
    * password: pasteInitialAdminPassword

# Overview
## built-in admin user
* `argocd account list --server localhost:8080 --insecure`
### created | install Argo CD
* | IMMEDIATELY AFTER installing ArgoCD,
  * `argocd account list --server localhost:8080 --insecure`
    * ALREADY exist admin
### FULL access to the system
* `argocd admin settings rbac can admin create applications '*/guestbook' --namespace argocd`
  * 's return: Yes
* `argocd admin settings rbac can admin delete clusters '*' --namespace argocd`
  * 's return: Yes
* `argocd admin settings rbac can admin update accounts '*' --namespace argocd`
  * 's return: Yes

# Local users/accounts

## use cases
### Auth tokens -- for -- Argo CD management automation
* `kubectl patch configmap argocd-cm -n argocd --type merge -p '             
  data:
    accounts.alice: "apiKey, login"
    accounts.alice.enabled: "true"
  '`
  * create an user
* `argocd account get-user-info`
  * check it's admin
* `argocd account update-password --account alice`
  * current admin password: got it from kubectl
  * new password: bbbbbbbb
  * create a password
* `curl -k -H "Content-Type: application/json" https://localhost:8080/api/v1/session -d '{"username":"alice","password":"bbbbbbbb"}'`
  * 's return: token

## ADDITIONAL users / small team
* TODO:

## restrictions
### ❌NOT provide advanced features ❌
* TODO:
### local account's username's lenght <= 253
* `kubectl patch configmap argocd-cm -n argocd --type merge -p '
data:                                                                                         
  accounts.aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa: "apiKey, login"                                                                                            
' `
  * fail

## default policy
### specified | `argocd-rbac-cm` ConfigMap's `policy.default` field
* `kubectl get cm argocd-rbac-cm -n argocd -o jsonpath='{.policy.default}'`
  * if NOTHING is return == NO default policy
### if you need ADDITIONAL rules -> configure [RBAC rules](../rbac.md)
* there

## Create NEW user
* `kubectl patch configmap argocd-cm -n argocd --type merge -p '             
  data:
    accounts.alice: "apiKey, login"
    accounts.alice.enabled: "true"
  '`
  * add alice account
  * `argocd account list`
    * check the account exist
### if you want to create it's password -> | user / has rights: `argocd account update-password --account alice --new-password <PASSWORD>`
* `argocd account get-user-info`
  * check it's admin
* `argocd account update-password --account alice --new-password bbbbbbbb`
### capabilities
#### apiKey enable: generating authentication tokens -- for -- API access
* `curl -k -H "Content-Type: application/json" https://localhost:8080/api/v1/session -d '{"username":"alice","password":"bbbbbbbb"}'`
  * 's return: token
#### login enable: login | UI
* https://localhost:8080/
  * user: alice
  * password: bbbbbbbb

## Delete user
* `kubectl patch -n argocd cm argocd-cm --type='json' -p='[{"op": "remove", "path": "/data/accounts.alice"}]'`
  * remove the `argocd-cm` ConfigMap's entry `/data/accounts.alice`
* `kubectl patch -n argocd secrets argocd-secret --type='json' -p='[{"op": "remove", "path": "/data/accounts.alice.password"}]'`
  * remove the corresponding `argocd-secret` Secret's password entry

## Disable admin user
* `kubectl patch configmap argocd-cm -n argocd --type merge -p '             
  data:
    admin.enabled: "false"
  '`
  * `kubectl get configmap argocd-cm -n argocd -o jsonpath='{.data.admin\.enabled}'`
    * 's return: false

## Manage users
* trigger commented `argocd account` commands
### `argocd account list`
### `argocd account get --account alice`
### `argocd login localhost:8080 --insecure`
### `argocd account generate-token`
* `argocd account get --account alice`
  * check TOKENS-related

## Failed logins rate limiting
### `ARGOCD_SESSION_FAILURE_MAX_FAIL_COUNT`
#### by default, 5
* `kubectl get deployment argocd-server -n argocd -o jsonpath='{.spec.template.spec.containers[0].env[?(@.name=="ARGOCD_SESSION_FAILURE_MAX_FAIL_COUNT")].value}'`
  * 's return NOTHING == default value
* [source code](/util/session/sessionmanager.go)'s `defaultMaxLoginFailures`
### `ARGOCD_SESSION_FAILURE_WINDOW_SECONDS`
#### by default, 5
* `kubectl get deployment argocd-server -n argocd -o jsonpath='{.spec.template.spec.containers[0].env[?(@.name=="ARGOCD_SESSION_FAILURE_WINDOW_SECONDS")].value}'`
  * 's return NOTHING == default value
* [source code](/util/session/sessionmanager.go)'s `defaultFailureWindow`
### `ARGOCD_SESSION_MAX_CACHE_SIZE`
#### by default, 1000
* `kubectl get deployment argocd-server -n argocd -o jsonpath='{.spec.template.spec.containers[0].env[?(@.name=="ARGOCD_SESSION_MAX_CACHE_SIZE")].value}'`
  * 's return NOTHING == default value
* [source code](/util/session/sessionmanager.go)'s `defaultMaxCacheSize`
### `ARGOCD_MAX_CONCURRENT_LOGIN_REQUESTS_COUNT`
#### by default, 1000
* `kubectl get deployment argocd-server -n argocd -o jsonpath='{.spec.template.spec.containers[0].env[?(@.name=="ARGOCD_MAX_CONCURRENT_LOGIN_REQUESTS_COUNT")].value}'`
  * 's return NOTHING == default value
* [source code](/server/server.go)'s `maxConcurrentLoginRequestsCount`

* TODO:

# SSO

* _Example:_ configure Argo CD SSO -- via -- GitHub (OAuth2)

## Dex
### == Identity provider / ALTHOUGH
#### embedded & bundled | ArgoCd
* `kubectl get all -n argocd | grep "dex"`
  * check they are deployed
* check in the [manifests](/manifests) / they are found
#### by default, ❌NOT configured❌
* `kubectl logs -n argocd -l app.kubernetes.io/name=argocd-dex-server`
  * check the message "dex is not configured"
### <DEX_ISSUER_URL>.well-known/openid-configuration
#### == information -- about -- what the provider supports
* requirements
  * [follow how to configure](#how-to-configure)
* https://localhost:8080/api/dex/.well-known/openid-configuration

### how to configure
#### _Example:_ using Github connector

* steps
  * | Github,
    * register a NEW application
      * == Settings > Developer Settings > OAuth Apps > New OAuth App

        ![Register OAuth App](/docs/assets/register-app.png "Register OAuth App")
        * authorization callback URL: https://localhost:8080/api/dex/callback
        * you receive OAuth2 client ID & OAuth2 client secret

          ![OAuth2 Client Config](/docs/assets/oauth2-config.png "OAuth2 Client Config")
  * `kubectl port-forward svc/argocd-server -n argocd 8080:443`
    * Reason: check you can login -- via -- Dex + Github connector
  * `kubectl patch secret argocd-secret -n argocd --type merge -p "{\"data\":{\"dex.github.clientSecret\":\"$(echo -n '<GITHUB_CLIENT_SECRET>' | base64)\"}}"`
  * `kubectl patch configmap argocd-cm -n argocd --type merge --patch-file patchDexGithubConnectorArgoCDCM.yaml`
  * `kubectl rollout restart deployment argocd-dex-server -n argocd`
  * https://localhost:8080/
    * click: Log in via Github
      * get access to ArgoCD UI

### how `to request ADDITIONAL ID token claims?

TODO: set OIDC connector locally

### how to retrieve claims / are NOT specified | ID token?

TODO: set OIDC connector locally

## OIDC Provider DIRECTLY
### TODO: 