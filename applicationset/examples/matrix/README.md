# Git Directory generator + Cluster generator
* goal
  * deploy BOTH applications | BOTH clusters
  * if NEW applications appear | Git repository -> AUTOMATICALLY deploy | NEW clusters / defined | Argo CD 

* requirements
  * 2 clusters

* ApplicationSet
  * with [goTemplate](cluster-and-git.yaml)
  * with [fastTemplate](cluster-and-git-fasttemplate.yaml)

## how to run locally?
* recommendations
  * `kind create cluster` & `kind create cluster --name kind2`
* `KIND2_IP=$(docker inspect kind2-control-plane --format '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}')`
* `CA_DATA=$(kubectl config view --raw -o jsonpath='{.clusters[?(@.name=="kind-kind2")].cluster.certificate-authority-data}')`
* `CERT_DATA=$(kubectl config view --raw -o jsonpath='{.users[?(@.name=="kind-kind2")].user.client-certificate-data}')`
* `KEY_DATA=$(kubectl config view --raw -o jsonpath='{.users[?(@.name=="kind-kind2")].user.client-key-data }')`
* `kubectl apply -f clusterSecret.yaml`
* `kubectl apply -f cluster-and-gitfile.yaml`
* `argocd app list | grep cluster-git`
  * ONLY returns 1! -- prod one
    * Reason: `selector.matchLabels`

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

# Git generator + List generator

* ApplicationSet
  * with [goTemplate](list-and-git.yaml)
  * with [fastTemplate](list-and-git-fasttemplate.yaml)

# List generator + List generator

* ApplicationSet
  * with [goTemplate](list-and-list.yaml)
  * with [fastTemplate](list-and-list-fasttemplate.yaml)

# Union generator + Matrix generator

* ApplicationSet
  * with [goTemplate](matrix-and-union-in-matrix.yaml)
  * with [fastTemplate](matrix-and-union-in-matrix-fasttemplate.yaml)
