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

* parameters
  * == key/value pairs 
    * | template rendering, substituted -- into the -- ApplicationSet resource's `template:` section  

* built-in generators:
  - [List generator](Generators-List.md)
    - allows you to
      - target Argo CD Applications -- , based on fixed list of key/value pairs, to -- clusters 
      - generate -- , based on a fixed list of cluster name/URL values, -- parameters
  - [Cluster generator](Generators-Cluster.md)
    - allows you to
      - target Argo CD Applications -- , based on list of clusters / (defined | Argo CD & managed by Argo CD), to -- clusters
  - [Git generator](Generators-Git.md)
    - allows you to
      - create Applications OR generate parameters -- based on -- Git repository's 
        - files OR
          - _Example:_ files / contains json values -> parsed & converted | template parameters
        - directory structure
  - [Matrix generator](Generators-Matrix.md)
    - uses
      - combine SEVERAL separate generators' generated parameters
  - [Merge generator](Generators-Merge.md)
    - The Merge generator may be used to merge the generated parameters of two or more generators. Additional generators can override the values of the base generator.
  - [SCM Provider generator](Generators-SCM-Provider.md)
    - uses
      - AUTOMATICALLY discover -- ,via SCM provider (eg GitHub)'s API, -- organization's repositories 
  - [Pull Request generator](Generators-Pull-Request.md)
    - The Pull Request generator uses the API of an SCMaaS provider (eg GitHub) to automatically discover open pull requests within an repository.
  - [Cluster Decision Resource generator](Generators-Cluster-Decision-Resource.md)
    - uses
      - \+  Kubernetes CR / use CR-specific logic -- to decide -- set of Argo CD clusters / deploy to
  - [Plugin generator](Generators-Plugin.md)
    - The Plugin generator make RPC HTTP request to provide parameters.
