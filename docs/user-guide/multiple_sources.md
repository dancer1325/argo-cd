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
    * `RepeatedResourceWarning` is produced
    * STILL sync the resources 

TODO:
* This provides a convenient way to override a resource from a chart with a resource from a Git repo.

## Helm value files -- from -- external Git repository

* use case
  * combine the external Helm chart + your own local values

* how to configure the external Git repository / contain the value files
  * | "Application", 
    * | Values git repo, 
      * specify `spec.sources[*].ref: ValuesGitRepoReference`
    * | helm chart git repo,
      * specify `spec.sources[*].helm.valueFiles`
        * `$ValuesGitRepoReference` variable
          * can ONLY be used | beginning
          * == 👀Values git repo's root 👀
TODO: 
If the `path` field is set in the `$values` source, Argo CD will attempt to generate resources
from the git repository
at that URL
* If the `path` field is not set, Argo CD will use the repository solely as a source of value files.


* ❌NOT specify `spec.sources[*].chart`❌

> [!NOTE]
> Even when the `ref` field is configured with the `path` field, `$value` still
> represents the root of sources with the `ref` field
* Consequently, `valueFiles` must be specified as relative paths from the root of sources.
