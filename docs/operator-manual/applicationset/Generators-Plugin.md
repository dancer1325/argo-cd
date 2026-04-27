# Plugin Generator

* allows you to
  * provide , -- through a plugin, -- your OWN custom generator
  * use any CUSTOM code /
    * input & output parameters
    * ❌!= OTHER generators / have predetermined logic ❌
      * _Examples:_
        * [Cluster generator](Generators-Cluster.md) fetch -- , via selector | ArgoCD secrets, -- clusters
        * [Git generator](Generators-Git.md) -- via a -- Git repository 
    * write | any language

* ways to use
  * simple
    * == ONLY respond -- to -- RPC HTTP requests
  * -- as --
    * sidecar
    * standalone deployment 

* uses
  * running today
    * == ❌NO need to wait 3-5 months❌

* use cases
  * \+ 
    * [Matrix generator](Generators-Matrix.md), OR
    * [Merge generator](Generators-Merge.md)
  * retrieve necessary parameters -- from a -- separate data source /
    * use them -- to -- extend the generator's functionality

* flow
  - ApplicationSet controller 
    - sends an HTTP POST -- to -- `baseUrl` / 
      - EACH `requeueAfterSeconds`
      - request includes `input.parameters` / defined | ApplicationSet
  - custom plugin service
    - receives the request
    - reads the input parameters
    - executes its custom logic -- to -- fetch any necessary data
    - construct a list of output parameter objects
    - response -- to the -- ApplicationSet controller
      - returning the parameter list 
  - ApplicationSet controller 
    - iterates through the parameter objects /
      - uses EACH ONE -- to -- fill out the template / defined | ApplicationSet object
        - -> create an Application

* how to create one?
  * generate -- , based on the [applicationset-hello-plugin](https://github.com/argoproj-labs/applicationset-hello-plugin), a -- NEW repository

* recommendations 
  * use as last fallback
    * Reason:🧠keep the spirit of GitOps
      * plugin generator externalize data -- outside of -- Git🧠

* ways to store credentials
  * | "argocd-secret" Kubernetes Secret
  * | ANOTHER Kubernetes Secret
    * requirements
      * label -- with -- `app.kubernetes.io/part-of: argocd`
    * how to use?
      * | "configmap.yaml",
        * `$<k8s_secret_name>:<a_key_in_that_k8s_secret>`
