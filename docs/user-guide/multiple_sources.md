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
          * combine BOTH manifests
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
      * == resource | chat is override -- with a -- resource | Git repo
    * `RepeatedResourceWarning` is produced
    * STILL sync the resources

## Helm value files -- from -- external Git repository

* use case
  * combine the external Helm chart + your own local values

* how to configure the external Git repository / contain the value files
  * | "Application", 
    * | Values git repo, 
      * specify 
        * `spec.sources[*].ref: ValuesGitRepoReference`
        * `spec.sources[*].path: PathToKubernetesManifests`
          * OPTIONAL
          * uses
            * generate Kubernetes objects
    * | helm chart git repo,
      * specify `spec.sources[*].helm.valueFiles`
        * `$ValuesGitRepoReference` variable
          * can ONLY be used | beginning
          * == 👀Values git repo's root 👀

* ❌NOT specify `spec.sources[*].chart`❌
