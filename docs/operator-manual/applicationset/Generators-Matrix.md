# Matrix Generator

* 💡combines 2 child generators' parameters -- by -- iterating through EVERY generator's generated parameters combination 💡
  * -> 👀gain BOTH generators' intrinsic properties 👀
  * ⚠️if matrix generator use 2 child Git generators -> 1 OR BOTH MUST use the `pathParamPrefix` option⚠️
    * Reason: 🧠
      * | merge the child generators’ items, avoid conflicts 
        * BOTH produce `path`-related parameters
        * OTHERWISE, the matrix generator fails🧠 
  * _Example:_
    - *SCM Provider Generator + Cluster Generator*
      - scan the GitHub organization's repositories
      - target those resources -- to -- ALL AVAILABLE clusters
    - *Git File Generator + List Generator*
      - list of applications -- ,via configuration files / optional configuration options, to -- deploy 
      - deploy the applications | fixed list of clusters
    - *Git Directory Generator + Cluster Decision Resource Generator*
      - locate application resources | Git repository's folders
      - deploy application resources | list of clusters / provided -- via an -- EXTERNAL custom resource

* child generator's parameters can be used | POST child generatorS
  * _Example:_ [here](/applicationset/examples/matrix/cluster-and-gitfile.yaml)

## child generatorS's parameters / SAME name, can be overridden | ANOTHER POST child generator

* use cases
  * | one child generator, define default values / ALL stages + override them -- with -- stage-specific values | ANOTHER generator

TODO: 
The example below generates a Helm-based application using a matrix generator with two git generators:
  the first provides stage-specific values (one directory per stage) and 
  the second provides global values for all stages.

```yaml
apiVersion: argoproj.io/v1alpha1
kind: ApplicationSet
metadata:
  name: parameter-override-example
spec:
  generators:
    - matrix:
        generators:
          - git:
              repoURL: https://github.com/example/values.git
              revision: HEAD
              files:
                - path: "**/stage.values.yaml"
          - git:
               repoURL: https://github.com/example/values.git
               revision: HEAD
               files:
                  - path: "global.values.yaml"
  goTemplate: true
  template:
    metadata:
      name: example
    spec:
      project: default
      source:
        repoURL: https://github.com/example/example-app.git
        targetRevision: HEAD
        path: .
        helm:
          values: |
            {{ `{{ . | mustToPrettyJson }}` }}
      destination:
        server: in-cluster
        namespace: default
```

Given the following structure/content of the example/values repository:

```
├── test
│   └── stage.values.yaml
│         stageName: test
│         cpuRequest: 100m
│         debugEnabled: true
├── staging
│   └── stage.values.yaml
│         stageName: staging
├── production
│   └── stage.values.yaml
│         stageName: production
│         memoryLimit: 512Mi
│         debugEnabled: false
└── global.values.yaml
      cpuRequest: 200m
      memoryLimit: 256Mi
      debugEnabled: true
```

The matrix generator above would yield the following results:

```yaml
- stageName: test
  cpuRequest: 100m
  memoryLimit: 256Mi
  debugEnabled: true
  
- stageName: staging
  cpuRequest: 200m
  memoryLimit: 256Mi
  debugEnabled: true

- stageName: production
  cpuRequest: 200m
  memoryLimit: 512Mi
  debugEnabled: false
```

## Restrictions

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
