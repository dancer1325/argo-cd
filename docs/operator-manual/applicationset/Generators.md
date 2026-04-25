# Generators

* Generators
  * 👀generate parameters / 
    * == key/value pairs
      * | render the template, they are substituted | ApplicationSet resource's `spec.template` section
    * are rendered | ApplicationSet resource's `template:` 👀
    * -- primarily based on -- data sources
      * == ⚠️-- depend on -- the generator⚠️
  * if you want to filter -> use [Post Selector](Generators-Post-Selector.md)

* built-in generators:

  | Generator                                                            | Data Source                      | Use Case                                                    |
  |:---------------------------------------------------------------------|:---------------------------------|:------------------------------------------------------------|
  | [List](Generators-List.md)                                           | FIXED list of key/value pairs    | Target apps -- to a -- known set of clusters/environments   |
  | [Cluster](Generators-Cluster.md)                                     | Clusters / registered \| Argo CD | Auto-deploy \| Argo CD's registered clusters                |
  | [Git](Generators-Git.md)                                             | Files OR directories \| Git repo | Generate apps -- from -- repo structure OR JSON/YAML files  |
  | [Matrix](Generators-Matrix.md)                                       | Combination of 2+ generators     | _Example:_ cluster generator + git generator                |
  | [Merge](Generators-Merge.md)                                         | Merge 2+ generators' output      | Override base generator values -- with -- ANOTHER generator |
  | [SCM Provider](Generators-SCM-Provider.md)                           | SCM API (GitHub, GitLab, etc.)   | Auto-discover repos \| organization                         |
  | [Pull Request](Generators-Pull-Request.md)                           | SCM Pull Request API             | Create apps / open PR \| PREVIEW environments               |
  | [Cluster Decision Resource](Generators-Cluster-Decision-Resource.md) | Custom Kubernetes resource       | Delegate cluster selection -- to -- external logic          |
  | [Plugin](Generators-Plugin.md)                                       | External HTTP RPC endpoint       | Custom generator -- via -- external service                 |
