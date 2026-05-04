# Matrix Generator

* 💡combines ALL POSSIBLE 2 child generators' parameters💡
  * == / EACH 1@ child generator's parameters, run the 2@ child generator
  * -> 👀gain BOTH generators' intrinsic properties 👀
  * ⚠️if matrix generator use 2 child Git generators -> 1 OR BOTH MUST use the `pathParamPrefix` option⚠️
    * Reason: 🧠
      * | merge the child generators’ items, avoid conflicts 
        * BOTH produce `path`-related parameters
        * OTHERWISE, the matrix generator fails🧠

* child generator's parameters 
  * can be used | POST child generatorS
  * / ⚠️SAME name, FIRST child generator take priority⚠️
    * use cases
      * | one child generator, define default values / ALL stages + override them -- with -- stage-specific values | ANOTHER generator

## Restrictions

TODO:
1. The Matrix generator currently only supports combining the outputs of only two child generators (eg does not support generating combinations for 3 or more).

1. You should specify only a single generator per array entry, eg this is not valid:

        - matrix:
            generators:
            - list: # (...)
              git: # (...)

    - While this *will* be accepted by Kubernetes API validation, the controller will report an error on generation. Each generator should be specified in a separate array element, as in the examples above.

1. The Matrix generator does not currently support [`template` overrides](Template.md#generator-templates) specified on child generators, eg this `template` will not be processed:

        - matrix:
            generators:
              - list:
                  elements:
                    - # (...)
                  template: { } # Not processed

1. Combination-type generators (matrix or merge) can only be nested once. For example, this will not work:

        - matrix:
            generators:
              - matrix:
                  generators:
                    - matrix:  # This third level is invalid.
                        generators:
                          - list:
                              elements:
                                - # (...)

1. When using parameters from one child generator inside another child generator, the child generator that *consumes* the parameters **must come after** the child generator that *produces* the parameters.
For example, the below example would be invalid (cluster-generator must come after the git-files generator):

        - matrix:
            generators:
              # cluster generator, 'child' #1
              - clusters:
                  selector:
                    matchLabels:
                      argocd.argoproj.io/secret-type: cluster
                      kubernetes.io/environment: '{{.path.basename}}' # {{.path.basename}} is produced by git-files generator
              # git generator, 'child' #2
              - git:
                  repoURL: https://github.com/argoproj/applicationset.git
                  revision: HEAD
                  files:
                    - path: "examples/git-generator-files-discovery/cluster-config/**/config.json"

1. You cannot have both child generators consuming parameters from each another. In the example below, the cluster generator is consuming the `{{.path.basename}}` parameter produced by the git-files generator, whereas the git-files generator is consuming the `{{.name}}` parameter produced by the cluster generator. This will result in a circular dependency, which is invalid.

        - matrix:
            generators:
              # cluster generator, 'child' #1
              - clusters:
                  selector:
                    matchLabels:
                      argocd.argoproj.io/secret-type: cluster
                      kubernetes.io/environment: '{{.path.basename}}' # {{.path.basename}} is produced by git-files generator
              # git generator, 'child' #2
              - git:
                  repoURL: https://github.com/argoproj/applicationset.git
                  revision: HEAD
                  files:
                    - path: "examples/git-generator-files-discovery/cluster-config/engineering/{{.name}}**/config.json" # {{.name}} is produced by cluster generator
