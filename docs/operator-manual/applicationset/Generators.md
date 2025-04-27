# Generators

* Generators
  * 👀generate parameters / 
    * are rendered | ApplicationSet resource's `template:` 👀
    * -- primarily based on -- data sources 
      * _Example:_
        * list generator's data source == literal list
        * cluster generator's data source == Argo CD cluster list
        * Git generator's data source == Git repository's files/directories 
  * see [Introduction](index.md)
  * if you want to filter -> use [Post Selector](Generators-Post-Selector.md)

* built-in generators:
  - [List generator](Generators-List.md)
    - allows you to
      - target Argo CD Applications -- , based on fixed list of key/value pairs, to -- clusters 
  - [Cluster generator](Generators-Cluster.md)
    - The Cluster generator allows you to target Argo CD Applications to clusters, based on the list of clusters defined within (and managed by) Argo CD (which includes automatically responding to cluster addition/removal events from Argo CD).
  - [Git generator](Generators-Git.md)
    - The Git generator allows you to create Applications based on files within a Git repository, or based on the directory structure of a Git repository.
  - [Matrix generator](Generators-Matrix.md)
    - uses
      - combine SEVERAL separate generators' generated parameters
  - [Merge generator](Generators-Merge.md)
    - The Merge generator may be used to merge the generated parameters of two or more generators. Additional generators can override the values of the base generator.
  - [SCM Provider generator](Generators-SCM-Provider.md)
    - The SCM Provider generator uses the API of an SCM provider (eg GitHub) to automatically discover repositories within an organization.
  - [Pull Request generator](Generators-Pull-Request.md)
    - The Pull Request generator uses the API of an SCMaaS provider (eg GitHub) to automatically discover open pull requests within an repository.
  - [Cluster Decision Resource generator](Generators-Cluster-Decision-Resource.md)
    - The Cluster Decision Resource generator is used to interface with Kubernetes custom resources that use custom resource-specific logic to decide which set of Argo CD clusters to deploy to.
  - [Plugin generator](Generators-Plugin.md)
    - The Plugin generator make RPC HTTP request to provide parameters.
