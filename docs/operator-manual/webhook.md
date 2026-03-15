# Git Webhook Configuration

* goal
  * how to configure Application Git webhook | some git provider
    * ❌!= [how to configure ApplicationSet Git webhook](applicationset/Generators-Git.md#webhook-configuration)❌

* Argo CD 
  * supports
    * 💡Git webhook notifications💡
      * requirements
        * configure API server / receive webhook events
      * ⚠️vs Argo CD polls Git repositories⚠️
        * NO delay
          * Reason:🧠poll is in intervals🧠
      * -- from -- 
        * GitHub
        * GitLab
        * Bitbucket
        * Bitbucket Server
        * Azure DevOps
        * Gogs

* webhook handler 
  * ❌if branch name == tag name -> NOT differentiate branch event -- & -- tag event ❌

* TODO: A hook event for a push to branch `x` will trigger a refresh for an app pointing at the same repo with `targetRevision: refs/tags/x`

## steps

### 1. Create the WebHook | Git Provider

* | your Git provider,
  * settings > webhooks
    * set 
      * payload URL == your Argo CD instance's "/api/webhook" endpoint
        * _Example:_ https://argocd.example.com/api/webhook
      * secret
        * 👀OPTIONAL👀
          * Reason:🧠ONLY functionality: ArgoCD checks desired state vs live state
            * == NOT take in account webhook payload🧠
          * ⚠️if Argo CD is publicly accessible -> recommended to configure a webhook secret⚠️
            * Reason:🧠prevent a DDoS attack🧠
        * if you specify -> you need to configure [step 2](#2-configure-the-webhook-secret--argo-cd-optional)

* | "argocd-cm" ConfigMap,
  * specify `data.webhook.maxPayloadSizeMB` -- based on -- your use case
    * == limit the payload size
      * Reason:🧠
        * "/api/webhook" endpoint lacks rate limiting protection
        * prevent DDoS attacks -- against -- unauthenticated webhook events🧠
    * by default, 50MB

#### Github

* ADDITIONAL steps,
  * | your GitHub,
    * settings > webhooks
      * set "Content type" == "application/json"
        * Reason:🧠"application/x-www-form-urlencoded" (default value) is NOT supported🧠

![Add Webhook](../assets/webhook-config.png "Add Webhook")

#### Azure DevOps

* OPTIONAL ADDITIONAL steps
  * | your Azure DevOps,
    * settings > webhooks
      * set "basic authentication username" & "basic authentication password"

![Add Webhook](../assets/azure-devops-webhook-config.png "Add Webhook")

### 2. Configure the WebHook secret | Argo CD (OPTIONAL)

* 👀OPTIONAL👀
* depend -- on -- you configured | [step 1](#1-create-the-webhook--git-provider)

* steps
  * | "argocd-secret" Kubernetes secret's `stringData`
    * configure -- based on the -- chosen Git provider's configured | step 1
    * ⚠️if you want to configure | ANOTHER Kubernetes secret -> [here](user-management/index.md#alternative)⚠️
    * vs Kubernetes secret's `data`
      * PREVIOUS step: encode the values base64  

| Provider        | K8s Secret Key                   | K8s Secret Key     |
|-----------------|----------------------------------|--------------------|
| GitHub          | `webhook.github.secret`          | specified \| step1 | 
| GitLab          | `webhook.gitlab.secret`          | specified \| step1 |
| BitBucket       | `webhook.bitbucket.uuid`         | specified \| step1 |
| BitBucketServer | `webhook.bitbucketserver.secret` | specified \| step1 |
| Gogs            | `webhook.gogs.secret`            | specified \| step1 |
| Azure DevOps    | `webhook.azuredevops.username`   | specified \| step1 |
|                 | `webhook.azuredevops.password`   | specified \| step1 |

## Special handling for BitBucket Cloud

TODO: 
BitBucket does not include the list of changed files in the webhook request body.
This prevents the [Manifest Paths Annotation](high_availability.md#manifest-paths-annotation) feature from working with repositories hosted on BitBucket Cloud.
BitBucket provides the `diffstat` API to determine the list of changed files between two commits.
To address the missing changed files list in the webhook, the Argo CD webhook handler makes an API callback to the originating server.
To prevent Server-side request forgery (SSRF) attacks, Argo CD server supports the callback mechanism only for encrypted webhook requests.
The incoming webhook must include `X-Hook-UUID` request header
* The corresponding UUID must be provided as `webhook.bitbucket.uuid` in `argocd-secret` for verification.
The callback mechanism supports both public and private repositories on BitBucket Cloud.
For public repositories, the Argo CD webhook handler uses a no-auth client for the API callback.
For private repositories, the Argo CD webhook handler searches for a valid repository OAuth token for the HTTP/HTTPS URL.
The webhook handler uses this OAuth token to make the API request to the originating server.
If the Argo CD webhook handler cannot find a matching repository credential, the list of changed files would remain empty.
If errors occur during the callback, the list of changed files will be empty.
