* notice this path's structure

```
├── cluster-addons
│   ├── argo-workflows
│   │   └── kustomization.yaml
│   └── prometheus-operator
│       ├── Chart.yaml
│       ├── requirements.yaml
│       └── values.yaml
├── excludes
│   ├── cluster-addons
│   │   ├── argo-workflows
│   │   │   └── kustomization.yaml
│   │   ├── exclude-helm-guestbook
│   │   │   ├── Chart.yaml
│   │   │   ├── templates/
│   │   │   ├── values-production.yaml
│   │   │   └── values.yaml
│   │   └── prometheus-operator
│   │       ├── Chart.yaml
│   │       ├── requirements.yaml
│   │       └── values.yaml
│   ├── git-directories-exclude-example-fasttemplate.yaml
│   └── git-directories-exclude-example.yaml
├── git-directories-example-fasttemplate.yaml
└── git-directories-example.yaml
```
  * 1 directory / EACH workload -- to -- deploy
    * [Argo Workflow controller](cluster-addons/argo-workflows)
    * [Prometheus Operator Helm chart](cluster-addons/prometheus-operator)

# requirements
* clusters ALREADY defined | Argo CD
