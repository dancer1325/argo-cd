# Git Directory generator + Cluster generator
* goal
  * deploy BOTH applications | BOTH clusters
  * if NEW applications appear | Git repository -> AUTOMATICALLY deploy | NEW clusters / defined | Argo CD 

* requirements
  * 2 clusters
    * `staging` cluster | `https://1.2.3.4`
    * `production` cluster | `https://2.4.6.8`

* ApplicationSet
  * [normal](cluster-and-git.yaml)
  * [fastTemplate](cluster-and-git-fasttemplate.yaml)

# Git File generator + Cluster generator

* [ApplicationSet](cluster-and-gitfile.yaml)

* goal
  * child generator's parameters can be used | POST child generatorS
    * == git generator parameters can be used | cluster generators

# Git + Git

* goal
  * ⚠️if matrix generator use 2 child Git generators -> 1 OR BOTH MUST use the `pathParamPrefix` option⚠️

```
├── apps
│   ├── app-one.json
│   │   { "appName": "app-one" }
│   └── app-two.json
│       { "appName": "app-two" }
└── targets
    ├── app-one
    │   ├── east-cluster-one.json
    │   │   { "region": "east", "clusterName": "cluster-one" }
    │   └── east-cluster-two.json
    │       { "region": "east", "clusterName": "cluster-two" }
    └── app-two
        ├── east-cluster-one.json
        │   { "region": "east", "clusterName": "cluster-one" }
        └── west-cluster-three.json
            { "region": "west", "clusterName": "cluster-three" }
```

* [Applicationset](git-and-git.yaml)

# TODO:
TODO: