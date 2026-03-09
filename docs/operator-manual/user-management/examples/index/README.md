
## Local users/accounts

### Create new user
* TODO: use [argocd-cm.yaml](argocd-cm.yaml)

### Delete user
* `kubectl patch -n argocd cm argocd-cm --type='json' -p='[{"op": "remove", "path": "/data/accounts.alice"}]'`
  * remove the `argocd-cm` ConfigMap's entry `/data/accounts.alice`
* `kubectl patch -n argocd secrets argocd-secret --type='json' -p='[{"op": "remove", "path": "/data/accounts.alice.password"}]'`
  * remove the corresponding `argocd-secret` Secret's password entry

### Disable admin user
* TODO: use [argocd-cm.yaml](argocd-cm.yaml)


## SSO

* _Example:_ configure Argo CD SSO -- via -- GitHub (OAuth2)

### Dex

* steps
  * | Github, 
    * register a NEW application

      ![Register OAuth App](/docs/assets/register-app.png "Register OAuth App")
      * authorization callback URL: https://argocd.example.com/api/dex/callback
      * you receive OAuth2 client ID & OAuth2 client secret

        ![OAuth2 Client Config](/docs/assets/oauth2-config.png "OAuth2 Client Config")

#### steps to configure

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
  

