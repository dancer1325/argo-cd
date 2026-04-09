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

* steps
  * | Github, 
    * register a NEW application

      ![Register OAuth App](/docs/assets/register-app.png "Register OAuth App")
      * authorization callback URL: https://argocd.example.com/api/dex/callback
      * you receive OAuth2 client ID & OAuth2 client secret

        ![OAuth2 Client Config](/docs/assets/oauth2-config.png "OAuth2 Client Config")

### steps to configure

* `kubectl edit configmap argocd-cm -n argocd`

    ```yaml
    data:
      # url: ArgoCD base URL
      url: https://argocd.example.com
    
      # OPTIONAL
      additionalUrls:
        ArgoCDBaseURL1
        ArgoCDBaseURL2
        ...
    
      # see https://github.com/dexidp/website/blob/main/content/docs/connectors/github.md
      dex.config: |
        connectors:
          # GitHub example
          # 1. public Github
          - type: github
            id: github
            name: GitHub
            config:
              # MANDATORY / got -- from -- PREVIOUS step
              clientID: aabbccddeeff00112233
              
              # MANDATORY / got -- from -- PREVIOUS step
              # $<some_K8S_secret>:dex.github.clientSecret
              #   <some_K8S_secret>
              #     by default, | "argocd-secret"
              #     requirements for the "<some_K8S_secret>" secret
              #       label `app.kubernetes.io/part-of: argocd`
              clientSecret: $dex.github.clientSecret  
              
              # recommended / restrict Github Organizations -> ANY Github Organization's member can perform management tasks
              orgs:
              - name: your-github-org
        
              # OPTIONAL  
              #   Reason: AUTOMATICALLY use the correct one 
              #       / any OAuth2 connectors
              #       -- to -- match the correct external callback
              redirectURI: 
    
          # 2. GitHub enterprise
          - type: github
            id: acme-github
            name: Acme GitHub
            config:
              hostName: github.acme.example.com
              clientID: abcdefghijklmnopqrst
              clientSecret: $dex.acme.clientSecret  # Alternatively $<some_K8S_secret>:dex.acme.clientSecret
              orgs:
              - name: your-github-org
    ```
  

