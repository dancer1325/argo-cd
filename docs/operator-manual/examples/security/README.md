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
* [install Argo CD](../../installation.md)

# Authentication | Argo CD API server
## ONLY -- through -- [JSON Web Tokens (JWTs)](https://jwt.io)
* if you do NOT pass JWT -> it fails
  * `curl -k https://localhost:8080/api/v1/applications`
    * 's return ""error":"no session information"
### ❌NOT -- through username/password❌
* `echo -n "admin:<ARGO_CD_INITIAL_ADMIN_PASSWORD>" | base64`
  * got it in base64
* `curl -k https://localhost:8080/api/v1/applications -H "Authorization: Basic <AUTH_PASSWORD_BASE_64>"`
  * ❌it does NOT work❌
    * Reason: 🧠you need to get ALWAYS the JWT🧠
### ways to be obtained/managed
#### local `admin` user has a username/password /
##### gets -- , via `/api/v1/session` endpoint, -- a JWT /
* `curl -k -H "Content-Type: application/json" https://localhost:8080/api/v1/session -d '{"username":"admin","password":"<ARGO_CD_INITIAL_ADMIN_PASSWORD>"}'`
  * 's return: token 
###### signed
* | https://www.jwt.io/
    * paste the PREVIOUS got it token > check Decoded Header's `alg`
###### issued -- by the -- Argo CD API server
* | https://www.jwt.io/
  * paste the PREVIOUS got it token > check Decoded Payload's `iss`
###### lifetime = 24hours
* | https://www.jwt.io/
  * paste the PREVIOUS got it token > check Decoded Payload's `exp` (== expiration time) vs `iat` (== emision time)
##### if the admin password is updated -> ALL existing admin JWT tokens are IMMEDIATELY revoked
* `curl -k https://localhost:8080/api/v1/applications -H "Authorization: Bearer <PREVIOUS_GOT_BEARER_TOKEN>"`
  * it works
* `argocd login localhost:8080 --insecure`
  * user: admin
  * password: <ARGO_CD_ADMIN_INITIAL_PASSWORD>
* `argocd account get-user-info`
  * current password: <ARGO_CD_ADMIN_INITIAL_PASSWORD>
  * NEW password: aaaaaaaa
* `curl -k https://localhost:8080/api/v1/applications -H "Authorization: Bearer <PREVIOUS_GOT_BEARER_TOKEN>"`
  * ❌NOT work anymore❌
##### password is stored -- as a -- bcrypt hash | "argocd-secret" Secret
* `kubectl get secret argocd-secret -n argocd -o jsonpath='{.data.admin\.password}' | base64 -d`
  * 's return SOMETHING / `$2` sounds to bcrypt hash
#### | Single Sign-On users, the user completes | OAuth2 login flow -- to the -- configured OIDC identity provider
##### delegated -- through the -- 
###### bundled Dex provider, OR
TODO:
####### lifetime == 24 hours
TODO:
###### self-managed OIDC provider
TODO:
#### Automation tokens -- via -- `/api/v1/projects/{project}/roles/{role}/token`
##### project-scope
* `kubectl apply -f appProjectWithroles.yaml`
  * `argocd proj role list sample-test-project`
    * check EXISTING roles | "sample-test-project" project
* hit [sample.http](sample.http)
  * 2.3.1
  * 2.3.2
* `argocd proj role get sample-test-project sample-test-project-role`
  * check NEW JWT is created
##### privilege-limited (== role-related)
* hit [sample.http](sample.http)
  * 2.3.3
##### signed & issued -- by -- Argo CD
* | https://www.jwt.io/
  * paste the PREVIOUS got it token > check Decoded Payload's `iss`
##### configurable expiration
* hit [sample.http](sample.http)
  * 2.3.4
* `argocd proj role get sample-test-project sample-test-project-role`
  * check 1 JWT expires soon
##### if you want to revoke IMMEDIATELY -> delete the JWT reference ID | project role 
* `argocd proj role get sample-test-project sample-test-project-role`
  * check 1 JWT & pick ID (== iat)
* hit [sample.http](sample.http)
  * 2.3.5
* `argocd proj role get sample-test-project sample-test-project-role`
  * check that JWT does NOT appear linked to the role ANYMORE

### TODO:

# Authorization
* [here](../rbac)

# plain HTTP
## uses
### communication with Redis
* `kubectl get configmap argocd-cmd-params-cm -n argocd -o yaml | grep redis`
  * return: NOTHING == default == plain HTTP
* `REDIS_PASS=$(kubectl get secret argocd-redis -n argocd -o jsonpath='{.data.auth}' | base64 -d)`
* `kubectl exec -n argocd deploy/argocd-redis -- redis-cli -a "$REDIS_PASS" PING`
  * you do NOT specify tls & respond PONG == plain HTTP

# Git & Helm Repositories
## managed -- by -- the repo-server
### ❌does NOT have Kubernetes privileges❌
* `kubectl get serviceaccount argocd-repo-server -n argocd -o yaml`
* `kubectl auth can-i --list --as=system:serviceaccount:argocd:argocd-repo-server -n argocd`
### ❌does NOT store service's credentials❌
* `kubectl auth can-i get secrets --as=system:serviceaccount:argocd:argocd-repo-server -n argocd`
  * NOT rights to get
* `kubectl exec -n argocd deploy/argocd-repo-server -- ls -la /tmp/reposerver-ask-pass.sock`
  * 's return: "srwxr-xr-x 1 argocd argocd 0 May  5 15:49 /tmp/reposerver-ask-pass.sock"
    * == store in-memory
## POSSIBLE attacks
### Unauthorized Deployments
TODO:
### Tool command invocation
TODO:
### Remote bases & helm chart dependencies
TODO:

# Sensitive Information
## Secrets
### Argo CD
#### NEVER returns sensitive data -- from -- its API
* _Example:_ repo's credentials
  * [source code](/server/repocreds/repocreds.go)'s
    ```go
    items = append(items, appsv1.RepoCreds{
                        URL:      url,
                        Username: repo.Username,
                    })
    ```
* TODO: create repository credential
* hit [sample.http](sample.http)
  * 3.1
#### sanitize/hide ALL sensitive data | API payloads & logs
* hit [sample.http](sample.http)
  * 3.2
    * check NO BearerToken is displayed
## External Cluster Credentials
TODO: 

# Cluster RBAC
TODO: 

# TODO: