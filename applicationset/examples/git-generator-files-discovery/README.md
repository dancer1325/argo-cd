* notice this path's structure

```
├── apps
│   └── guestbook
│       ├── guestbook-ui-deployment.yaml
│       ├── guestbook-ui-svc.yaml
│       └── kustomization.yaml
├── cluster-config
│   └── engineering
│       ├── dev
│       │   └── config.json
│       └── prod
│           └── config.json
├── excludes
│   ├── git-files-exclude-example-fasttemplate.yaml
│   └── git-files-exclude-example.yaml
├── git-generator-files-fasttemplate.yaml
└── git-generator-files.yaml
```
  * [apps/guestbook](apps/guestbook)
    * == Kubernetes resources / simple guestbook application
  * [cluster-config](cluster-config)
    * == cluster configuration / EACH stage
  * [git-generator-files.yaml](git-generator-files.yaml) OR [git-generator-files-fasttemplate.yaml](git-generator-files-fasttemplate.yaml)
    * == `ApplicationSet` resource / 
      * deploys [apps](apps) | [specified clusters](cluster-config)
      * 👀if your Git commits change cluster-config (-- due -- to `generators[git].files.path`) -> outOfSync👀

# requirements
* clusters ALREADY defined | Argo CD
