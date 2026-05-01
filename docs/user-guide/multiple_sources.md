# Multiple Sources for an Application

* Argo CD application
  * == link BETWEEN 
    * 1! source -- & -- 1 Application
      * by default
    * 👀\>1 sourceS -- & -- 1 Application👀
      * how does it work?
        * Argo CD
          * compiles ALL the sources
            * == generate SEPARATELY the manifests / EACH source
      * `spec.sources`
        * == MULTIPLE entries
        * if you specify it -> Argo CD ignores `spec.source`

* MULTIPLE sources
  * ❌NOT abuse of it❌
    * == NOT use -- as -- common strategy
  * recommended ALTERNATIVES
    * [applicationsets](../user-guide/application-set.md)
    * [app-of-apps](../operator-manual/cluster-bootstrapping.md)
  * if MULTIPLE sources produce the SAME resource (== SAME `group`, `kind`, `name`, and `namespace`) -> 
    * the last source to produce the resource take precedence
      * == resource | chart is override -- with a -- resource | Git repo
    * `RepeatedResourceWarning` is produced
    * STILL sync the resources

## Helm value files -- from -- external Git repository

* use case
  * combine the external Helm chart + your own local values

* how to configure the ArgoCD Application?

  ```yaml
  spec:
    sources:
    # Helm chart repo
    - repoURL: <HELM_CHART_REPO_URL>
      path: <PATH_TO_CHART>
      helm:
        valueFiles:
        # $<REF_NAME> = root of the values repo
        - $<REF_NAME>/<PATH_TO_VALUES_FILE>
    # Values repo
    - repoURL: <VALUES_REPO_URL>
      targetRevision: <BRANCH_OR_TAG>
      ref: <REF_NAME>       # creates the $<REF_NAME> variable
      # path: <OPTIONAL>    # if set, also generates manifests from this repo
  ```
