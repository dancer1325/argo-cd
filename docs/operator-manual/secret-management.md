# Secret Management

* | GitOps  
  * ways to populate secrets  
    * | [destination cluster](#destination-cluster-secret-management)
      * 👀recommended👀
    * | [Argo CD generate a manifest](#argo-cd-manifest-generation-based-secret-management)

* [MORE](https://github.com/argoproj/argo-cd/issues/1364)

## Destination Cluster Secret Management

* approach:
  * populate the secrets | destination cluster
    * -> ❌Argo CD does NOT DIRECTLY manage them❌

* _Examples:_
  * [Sealed Secrets](https://github.com/bitnami-labs/sealed-secrets)
  * [External Secrets Operator](https://github.com/external-secrets/external-secrets)
  * [Kubernetes Secrets Store CSI Driver](https://github.com/kubernetes-sigs/secrets-store-csi-driver)
  * [aws-secret-operator](https://github.com/mumoshu/aws-secret-operator)
  * [Vault Secrets Operator](https://developer.hashicorp.com/vault/docs/platform/k8s/vso)

* advantages
  1) low risk of leaking the secrets
     * Reason: 🧠Argo CD does NOT have access -- to the -- secrets🧠 
  2) \| app update, avoid UNINTENTIONAL secret updates
     * Reason: 🧠secret updates are decoupled -- from -- app sync operations🧠

## Argo CD Manifest Generation-Based Secret Management

* approach:
  * inject secrets | Argo CD's manifest generation 

* ways to address
  * -- via -- [Config Management Plugin](config-management-plugins.md)
* _Example:_ [argocd-vault-plugin](https://github.com/argoproj-labs/argocd-vault-plugin)

* ❌NOT recommended❌
  * Argo CD does NOT prioritize NEW features OR improvements / solely support this approach

* disadvantages
  1) Security
     * risk of leaking the secrets
       * Reason:🧠Argo CD
         * needs access to the secrets
         * stores generated manifests + injected secrets -- as -- plaintext | its Redis cache
           * if you have got access to the Redis instance OR Reposerver -> you can access -- , via repo-server API, to the -- secrets 🧠
  2) User Experience
     * risk of UNINTENTIONALLY applying Secret updates | UNRELATED release
       * Reason: 🧠Secret updates are coupled -- with -- app sync operations🧠 
  3) Rendered Manifests Pattern
     * incompatible -- with -- "Rendered Manifests" pattern (best practice for GitOps)

### how to mitigate the risks?

* steps
  1. set up network policies / prevent direct access -- to -- Argo CD components (Redis & repo-server)
     * ⚠️requirements⚠️
       * cluster supports those network policies
  2. run Argo CD | its OWN cluster / NO OTHER applications run | it
