# Overview

* built-in `admin` user
  * created | install Argo CD
  * FULL access to the system
  * recommendations
    * use ONLY | initial configuration
    * AFTERWARD, switch to some user management

* ways to manage users
  * [local users & passwords](#local-usersaccounts)
  * [SSO](#sso)

## Local users/accounts

* == 👀users/accounts created DIRECTLY | Argo CD👀

* use cases
  * Auth tokens -- for -- Argo CD management automation
    * steps
      * configure an API account / limited permissions
      * generate an authentication token
    * uses
      * AUTOMATICALLY create applications, projects etc.
  * ADDITIONAL users OR small team
    * Reason:🧠use SSO integration could be considered an overkill🧠

* restrictions
  * ❌NOT provide advanced features ❌
    * _Examples:_ groups, login history, etc
  * local account's username's length <= 253
    * Reason:🧠[Kubernetes restriction]()🧠

* default policy
  * specified | `argocd-rbac-cm` ConfigMap's `policy.default` field
  * if you need ADDITIONAL rules -> configure [RBAC rules](../rbac.md)

### Create NEW user

* steps 
  * | `argocd-cm` ConfigMap's `.data`,
    * `accounts.<USER_NAME>.enabled: "trueORfalse"`
      * by default, `"true"`
    * `accounts.<USER_NAME>: CAPABILITIESSEPARATEDBYCOMMA`
      * `CAPABILITIESSEPARATEDBYCOMMA`
        * apiKey
          * enable
            * generating authentication tokens -- for -- API access
        * login
          * enable
            * login | UI
  * if you want to create it's password -> | user / has rights
    * `argocd account update-password --account alice --new-password <PASSWORD>`

### Delete user

* steps
  * remove the corresponding `argocd-cm` ConfigMap's entry
  * remove the corresponding `argocd-secret` Secret's password entry
    * recommended one

### Disable admin user

* steps
  * | `argocd-cm` ConfigMap's `.data`,
    * `admin.enabled: "false"`

* when to do it?
  * AFTER creating ADDITIONAL users

### Manage users

* -- via -- Argo CD CLI

* `argocd account list`
  * get FULL users list
* `argocd account get --account <username>`
  * get specific user details
* `argocd account generate-token`
  * generate auth token | CURRENT user
  * `argocd account generate-token --account <username>`
    * generate auth token | `<username>` user
* set user password
  ```bash
  # if you are managing users as the admin user, <current-user-password> should be the current admin password.
  argocd account update-password \
    --account <name> \
    --current-password <current-user-password> \
    --new-password <new-user-password>
  ```

### Failed logins rate limiting

* goal
  * | login, restrict MAXIMUM NUMBER of failed attempts
    * -- through -- environments variables

* `ARGOCD_SESSION_FAILURE_MAX_FAIL_COUNT`
  * == MAXIMUM number of failed logins
    * AFTERWARD, Argo CD rejects login attempts
  * by default, 
    * 5

* `ARGOCD_SESSION_FAILURE_WINDOW_SECONDS`
  * == number of seconds -- for the -- failure window
    * == reset MAXIMUM NUMBER of attempts
  * by default,
    * 300 (== 5 minutes)
  * if = 0 
    * == failure window is disabled
  * INDEPENDENT of this value, AFTER 10 consecutive logon failures -> login attempts gets rejected

* `ARGOCD_SESSION_MAX_CACHE_SIZE`
  * == MAXIMUM number of entries / allowed | cache
  * by default,
    * 1000

* `ARGOCD_MAX_CONCURRENT_LOGIN_REQUESTS_COUNT`
  * == MAXIMUM number of concurrent login requests
  * if == 0 -> limit is disabled
  * by default,
    * 50

## SSO

* allows
  * manage your users, groups, memberships
  * authenticate once and access multiple applications

* supported providers + Protocols

| Provider                                      | Protocol(s)  | Connection Method |
|-----------------------------------------------|--------------|-------------------|
| [Okta](okta.md)                               | OIDC, SAML   | Direct OR via Dex |
| [OneLogin](onelogin.md)                       | OIDC, SAML   | Direct OR via Dex |
| [Auth0](auth0.md)                             | OIDC         | Direct OR via Dex |
| [Microsoft (Azure AD)](microsoft.md)          | OIDC, SAML   | Direct OR via Dex |
| [Keycloak](keycloak.md)                       | OIDC, SAML   | Direct OR via Dex |
| [Google (G Suite)](google.md)                 | OIDC         | Direct OR via Dex |
| [OpenUnison](openunison.md)                   | OIDC, SAML   | Direct OR via Dex |
| [Zitadel](zitadel.md)                         | OIDC         | Direct OR via Dex |
| [GitHub Action](github-actions.md)            | OAuth2       | Via Dex           |
| [GitLab CI](gitlab-ci.md)                     | OIDC         | Direct OR via Dex |
| [AWS Identity Center](aws-identity-center.md) | OIDC, SAML   | Direct OR via Dex |
| ANY LDAP server                               | LDAP         | Via Dex           |
| Generic SAML                                  | SAML         | Via Dex           |

### ways to configure

#### Dex 

* [Dex](https://github.com/dexidp/dex)
  * == Identity provider / 
    * implement OIDC
    * 👀embedded & bundled | ArgoCd👀
      * ALTHOUGH
        * it can be replaced by your desired one
          * _Examples:_ [keycloack](keycloak.md), [Microsoft Active Directory](microsoft.md), ...
        * by default, ❌NOT configured❌
  * allows
    * delegating authentication -- to an -- external identity provider
      * supported one
        * OIDC
        * SAML
        * LDAP
        * GitHub
        * etc
  * use cases
    * ❌your current provider does NOT support OIDC❌
      * _Example:_ SAML, LDAP
    * leverage any of Dex's connector features
      * _Example:_ ability to map GitHub organizations & teams -- to -- OIDC groups claims
    * if groups can NOT be included | IDToken -> fetch user information -- from the -- external identity provider
  * <DEX_ISSUER_URL>.well-known/openid-configuration
    * == information -- about -- what the provider supports
    * requirements
      * [configure it](#how-to-configure)
    * _Example:_ https://accounts.google.com/.well-known/openid-configuration

##### how to configure?

* steps
  * | identity provider,
    * register the application 
      * callback address endpoint: "/api/dex/callback"
      * you receive: 
        * OAuth2 client ID
        * OAuth2 client secret
  * | Argo CD "argocd-secret" Configmap,
    * add `dex.<YOUR_CHOSEN_CONNECTOR>.clientSecret: <base64-encoded-secret>`
      * _Example:_ if you use OIDC connector -> set `dex.oidc.clientSecret: <base64-encoded-secret>`
  * | "argocd-cm" ConfigMap,
    * add `data.dex.config`'s `connectors`
      * [ALLOWED connectors](https://dexidp.io/docs/connectors/)
  * restart "argocd-dex-server"

##### how to request ADDITIONAL ID token claims?

* `connectors[*].config`
  * `.scopes`
    * ⚠️by default,
      * ONLY `["profile", "email"]`⚠️
        * [here](https://github.com/dancer1325/dex/blob/master/connector/oidc/oidc.md#type-config-struct-)
    * if you want MORE -> specify it
  * `.insecureEnableGroups`
    * enables
      * groups claims
    * TILL [this issue](https://github.com/dexidp/dex/issues/1065) is resolved,
      * by default, disabled
        * == ❌NOT ALLOW group claims❌
    * use cases
      * ⚠️ONLY | refresh the id token, refresh groups claims⚠️
        * == ❌regular refresh flow does NOT update the groups claim❌
        * _Example:_ 
          * Alice logins | 9 AM / JWT contains groups: ["admins", "developers"]
          * | 10 AM, admin removes her from "admins" group
          * Alice has `admins` groups rights TILL JWT expiration

##### how to retrieve claims / are NOT specified | ID token?

* allows
  * retrieving ALL claims -- through -- `userinfo_endpoint` (specified | "<DEX_ISSUER_URL>.well-known/openid-configuration"'s response)
* use cases
  * Identity Providers / ❌do NOR OR can NOT support certain claims | IDToken ❌
    * _Example:_ `groups` claim 

* ⚠️requirements⚠️
  * `connectors[*].config.getUserInfo:true`
  * if you want to retrieve `groups` claim -> ALSO `connectors[*].config.insecureEnableGroups:true`

#### OIDC Provider DIRECTLY

TODO: 
To configure Argo CD to delegate authentication to your existing OIDC provider, add the OAuth2
configuration to the `argocd-cm` ConfigMap under the `oidc.config` key:

```yaml
data:
  url: https://argocd.example.com

  oidc.config: |
    name: Okta
    issuer: https://dev-123456.oktapreview.com
    clientID: aaaabbbbccccddddeee
    clientSecret: $oidc.okta.clientSecret
    
    # Optional list of allowed aud claims
* If omitted or empty, defaults to the clientID value above (and the 
    # cliClientID, if that is also specified)
* If you specify a list and want the clientID to be allowed, you must 
    # explicitly include it in the list.
    # Token verification will pass if any of the token's audiences matches any of the audiences in this list.
    allowedAudiences:
    - aaaabbbbccccddddeee
    - qqqqwwwweeeerrrrttt

    # Optional
* If false, tokens without an audience will always fail validation
* If true, tokens without an audience 
    # will always pass validation.
    # Defaults to true for Argo CD < 2.6.0
* Defaults to false for Argo CD >= 2.6.0.
    skipAudienceCheckWhenTokenHasNoAudience: true

    # Optional set of OIDC scopes to request
* If omitted, defaults to: ["openid", "profile", "email", "groups"]
    requestedScopes: ["openid", "profile", "email", "groups"]

    # Optional set of OIDC claims to request on the ID token.
    requestedIDTokenClaims: {"groups": {"essential": true}}

    # Some OIDC providers require a separate clientID for different callback URLs.
    # For example, if configuring Argo CD with self-hosted Dex, you will need a separate client ID
    # for the 'localhost' (CLI) client to Dex
* This field is optional
* If omitted, the CLI will
    # use the same clientID as the Argo CD server
    cliClientID: vvvvwwwwxxxxyyyyzzzz

    # PKCE is an OIDC extension to prevent authorization code interception attacks.
    # Make sure the identity provider supports it and that it is activated for Argo CD OIDC client.
    # Default is false.
    enablePKCEAuthentication: true
```

> [!NOTE]
> The callback address should be the /auth/callback endpoint of your Argo CD URL
> (e.g
* https://argocd.example.com/auth/callback).

##### Requesting additional ID token claims

Not all OIDC providers support a special `groups` scope
* E.g
* Okta, OneLogin and Microsoft do support a special
`groups` scope and will return group membership with the default `requestedScopes`.

Other OIDC providers might be able to return a claim with group membership if explicitly requested to do so.
Individual claims can be requested with `requestedIDTokenClaims`, see
[OpenID Connect Claims Parameter](https://connect2id.com/products/server/docs/guides/requesting-openid-claims#claims-parameter)
for details
* The Argo CD configuration for claims is as follows:

```yaml
  oidc.config: |
    requestedIDTokenClaims:
      email:
        essential: true
      groups:
        essential: true
        value: org:myorg
      acr:
        essential: true
        values:
        - urn:mace:incommon:iap:silver
        - urn:mace:incommon:iap:bronze
```

For a simple case this can be:

```yaml
  oidc.config: |
    requestedIDTokenClaims: {"groups": {"essential": true}}
```

##### Retrieving group claims when not in the token

Some OIDC providers don't return the group information for a user in the ID token, even if explicitly requested using the `requestedIDTokenClaims` setting (Okta for example)
* They instead provide the groups on the user info endpoint
* With the following config, Argo CD queries the user info endpoint during login for groups information of a user:

```yaml
oidc.config: |
    enableUserInfoGroups: true
    userInfoPath: /userinfo
    userInfoCacheExpiration: "5m"
```

**Note: If you omit the `userInfoCacheExpiration` setting or if it's greater than the expiration of the ID token, the argocd-server will cache group information as long as the ID token is valid!**

##### Configuring a custom logout URL for your OIDC provider

Optionally, if your OIDC provider exposes a logout API and you wish to configure a custom logout URL for the purposes of invalidating 
any active session post logout, you can do so by specifying it as follows:

```yaml
  oidc.config: |
    name: example-OIDC-provider
    issuer: https://example-OIDC-provider.example.com
    clientID: xxxxxxxxx
    clientSecret: xxxxxxxxx
    requestedScopes: ["openid", "profile", "email", "groups"]
    requestedIDTokenClaims: {"groups": {"essential": true}}
    logoutURL: https://example-OIDC-provider.example.com/logout?id_token_hint={{token}}
```
By default, this would take the user to their OIDC provider's login page after logout
* If you also wish to redirect the user back to Argo CD after logout, you can specify the logout URL as follows:

```yaml
...
    logoutURL: https://example-OIDC-provider.example.com/logout?id_token_hint={{token}}&post_logout_redirect_uri={{logoutRedirectURL}}
```

You are not required to specify a logoutRedirectURL as this is automatically generated by ArgoCD as your base ArgoCD url + Rootpath

> [!NOTE]
> The post logout redirect URI may need to be whitelisted against your OIDC provider's client settings for ArgoCD.

##### Configuring a custom root CA certificate for communicating with the OIDC provider

If your OIDC provider is setup with a certificate which is not signed by one of the well known certificate authorities
you can provide a custom certificate which will be used in verifying the OIDC provider's TLS certificate when
communicating with it
*  
Add a `rootCA` to your `oidc.config` which contains the PEM encoded root certificate:

```yaml
  oidc.config: |
    ...
    rootCA: |
      -----BEGIN CERTIFICATE-----
      ..
* encoded certificate data here ...
      -----END CERTIFICATE-----
```

### Sensitive Data and SSO Client Secrets

`argocd-secret` can be used to store sensitive data which can be referenced by ArgoCD
* Values starting with `$` in configmaps are interpreted as follows:

- If value has the form: `$<secret>:a.key.in.k8s.secret`, look for a k8s secret with the name `<secret>` (minus the `$`), and read its value
* 
- Otherwise, look for a key in the k8s secret named `argocd-secret`
* 

##### Example

SSO `clientSecret` can thus be stored as a Kubernetes secret with the following manifests

`argocd-secret`:
```yaml
apiVersion: v1
kind: Secret
metadata:
  name: argocd-secret
  namespace: argocd
  labels:
    app.kubernetes.io/name: argocd-secret
    app.kubernetes.io/part-of: argocd
type: Opaque
data:
  ...
  # The secret value must be base64 encoded **once** 
  # this value corresponds to: `printf "hello-world" | base64`
  oidc.auth0.clientSecret: "aGVsbG8td29ybGQ="
  ...
```

`argocd-cm`:
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: argocd-cm
  namespace: argocd
  labels:
    app.kubernetes.io/name: argocd-cm
    app.kubernetes.io/part-of: argocd
data:
  ...
  oidc.config: |
    name: Auth0
    clientID: aabbccddeeff00112233

    # Reference key in argocd-secret
    clientSecret: $oidc.auth0.clientSecret
  ...
```

##### Alternative

If you want to store webhook data in **another** Kubernetes `Secret`, instead of `argocd-secret`
* ArgoCD knows to check the keys under `data` in your Kubernetes `Secret` starts with `$`, then your Kubernetes `Secret` name and `:` (colon).

Syntax: `$<k8s_secret_name>:<a_key_in_that_k8s_secret>`

> [!NOTE]
> Secret must have label `app.kubernetes.io/part-of: argocd`

If you want to store sensitive data in **another** Kubernetes `Secret`, instead of `argocd-secret`
* ArgoCD knows to check the keys under `data` in your Kubernetes `Secret` for a corresponding key whenever a value in a configmap or secret starts with `$`, then your Kubernetes `Secret` name and `:` (colon).

Syntax: `$<k8s_secret_name>:<a_key_in_that_k8s_secret>`

> [!NOTE]
> Secret must have label `app.kubernetes.io/part-of: argocd`

###### Example

`another-secret`:
```yaml
apiVersion: v1
kind: Secret
metadata:
  name: another-secret
  namespace: argocd
  labels:
    app.kubernetes.io/part-of: argocd
type: Opaque
data:
  ...
  # Store client secret like below.
  # Ensure the secret is base64 encoded
  oidc.auth0.clientSecret: <client-secret-base64-encoded>
  ...
```

`argocd-cm`:
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: argocd-cm
  namespace: argocd
  labels:
    app.kubernetes.io/name: argocd-cm
    app.kubernetes.io/part-of: argocd
data:
  ...
  oidc.config: |
    name: Auth0
    clientID: aabbccddeeff00112233
    # Reference key in another-secret (and not argocd-secret)
    clientSecret: $another-secret:oidc.auth0.clientSecret  # Mind the ':'
  ...
```

### Skipping certificate verification on OIDC provider connections

By default, all connections made by the API server to OIDC providers (either external providers or the bundled Dex
instance) must pass certificate validation
* These connections occur when getting the OIDC provider's well-known
configuration, when getting the OIDC provider's keys, and  when exchanging an authorization code or verifying an ID 
token as part of an OIDC login flow.

Disabling certificate verification might make sense if:
* You are using the bundled Dex instance **and** your Argo CD instance has TLS configured with a self-signed certificate
  **and** you understand and accept the risks of skipping OIDC provider cert verification.
* You are using an external OIDC provider **and** that provider uses an invalid certificate **and** you cannot solve
  the problem by setting `oidcConfig.rootCA` **and** you understand and accept the risks of skipping OIDC provider cert 
  verification.

If either of those two applies, then you can disable OIDC provider certificate verification by setting
`oidc.tls.insecure.skip.verify` to `"true"` in the `argocd-cm` ConfigMap.
