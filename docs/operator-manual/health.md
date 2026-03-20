# Resource Health

* Argo CD
  * 's types of health checks
    * [built-in standard health checks](#built-in-standard-health-checks)
    * [custom health checks](#custom-health-checks)

## types of health checks

* health check type priority: 
  * [| "argocd-cm" ConfigMap](#-argocd-cm-configmap) > [bundled | /resource_customizations](#custom-built-in-health-checks) > [Go-based](#built-in-standard-health-checks)

### Built-in standard health checks

* MOSTLY ALL
  * were hardcoded -- as -- [Go code](/gitops-engine/pkg/health)
    * Reason: 🧠
      * Lua support was introduced later
      * health check logic: too complex
        * == easier -- to -- implement it | Go🧠

* uses
  * | standard Kubernetes types

#### | Deployment, ReplicaSet, StatefulSet, DaemonSet
* health check source code -- for --
  * [Deployment](/gitops-engine/pkg/health/health_deployment.go)
  * [ReplicaSet](/gitops-engine/pkg/health/health_replicaset.go)
  * [StatefulSet](/gitops-engine/pkg/health/health_statefulset.go)
  * [DaemonSet](/gitops-engine/pkg/health/health_daemonset.go)

* check
  * `metadata.generation` == `status.observedGeneration`
  * `spec.replicas` == `status.updatedReplicas`

#### | Service
* [health check source code](/gitops-engine/pkg/health/health_service.go)
* if service type == `LoadBalancer` -> `status.loadBalancer.ingress` != empty / contains
  * `hostname` OR `IP`

#### | Ingress
* [health check source code](/gitops-engine/pkg/health/health_ingress.go)
* `status.loadBalancer.ingress` != empty / contains
  * `hostname` OR `IP`

#### | CronJob
* [health check source code](/gitops-engine/pkg/health/health_job.go)
* if this CronJob's last scheduled job  
  * failed -> CronJob marked -- as -- "Degraded"
  * is running -> CronJob marked -- as -- "Progressing"

#### | Job
* if job's `.spec.suspended: 'true'` -> 
  * job's health marked -- as -- suspended 
  * app health marked -- as -- suspended

#### | PersistentVolumeClaim
* [health check source code](/gitops-engine/pkg/health/health_pvc.go)
* `status.phase` = `Bound`

#### | Argocd App

* == health check -- of -- `argoproj.io/Application` CRD 
* | Argo CD v1.8,
  * ⚠️[removed](https://github.com/argoproj/argo-cd/issues/3781)⚠️
    * TODO: You might need to restore it if you are using app-of-apps pattern and orchestrating synchronization using sync waves
* steps
  * add ["argocd-cm" ConfigMap](examples/health/healthCheckOwnArgoCDApplicationConfigMap.yaml)

### Custom Health Checks

* written | [Lua](https://www.lua.org/)

* use cases
  * `Ingress` OR `StatefulSet` resources / stuck | `Progressing` state
    * POSSIBLE Reasons:🧠bug | your resource controller🧠
  * custom resource
    * Reason:🧠Argo CD provides built-in health check -- for -- standard Kubernetes types🧠

* ways -- to -- configure a CUSTOM health check
  * [| "argocd-cm" ConfigMap](#-argocd-cm-configmap)
  * [custom built-in health checks](#custom-built-in-health-checks) 

#### | "argocd-cm" ConfigMap

* steps
  * | "argocd-cm" ConfigMap,
    * define

      ```yaml
      data:  
        # <group>   ==  API Group
        # <kind>   ==  API Kind
        # 1. ALL | SAME line
        resource.customizations.health.<group>_<kind>: |
          ScriptBasedOnLua
      
        # 2. | SEPARATED lines
       #resource.customizations.health: |
       #  "<group>/<kind>": 
       #    ScriptBasedOnLua
      ```
      * if you are using `argocd-operator` -> it's overridden -- by the -- [argocd-operator `resourceCustomizations`](https://argocd-operator.readthedocs.io/en/latest/reference/argocd/#resource-customizations)
      * if you want to apply SAME health check | MULTIPLE resources -> use `*` (wildcard) | API group OR API kind
        * requirements:
          * use expression / SEPARATED lines

            ```yaml
            data:
              resource.customizations: |
                ec2.aws.crossplane.io/*:
                  health.lua: |
                    ...
              
              # ❌NOT valid * / ALL | SAME line❌
              #resource.customizations.health.ec2.aws.crossplane.io/*: |  
            ```
          * if you use beginning `*` -> wrap with `""`

            ```yaml
            data:
              # if the key _begins_ with * -> quote the GVK key
              resource.customizations: |
                "*.aws.crossplane.io/*":
                  health.lua: |
                    ...
            ```

* `ScriptBasedOnLua`
  * requirements
    * ⚠️return an object⚠️ / contain
      * `.status`
        * ALLOWED values
          * `Healthy`
            * == resource is healthy
          * `Progressing`
            * == resource
              * is NOT YET healthy
              * STILL making progress
              * might be healthy soon
            * MOST common one
          * `Degraded`
            * == resource is degraded
          * `Suspended`
            * == resource is
              * suspended
              * waiting for some external event -- to -- resume
                * _Examples:_ suspended CronJob OR paused Deployment
      * `.message`
        * OPTIONAL
  * access -- to the -- standard Lua libraries
    * by default, disabled
    * if you want to enable -> set `resource.customizations.useOpenLibs.<group>_<kind>: true`
      * _Example:_ 

        ```yaml
        data:
          resource.customizations.useOpenLibs.cert-manager.io_Certificate: true
          resource.customizations.health.cert-manager.io_Certificate: |
            # Lua standard libraries are enabled for this script
        ```

* `obj`
  * == global variable /
    * injected BEFORE executing this script
    * can be used | `ScriptBasedOnLua`

#### custom built-in health checks

* custom built-in health check
  * 👀[here](/resource_customizations)👀
  * follow this directory structure
      ```
      argo-cd
      |-- resource_customizations
      |    |-- your.crd.group.io               # CRD group
      |    |    |-- MyKind                     # Resource kind
      |    |    |    |-- health.lua            # Health check
      |    |    |    |-- health_test.yaml      # Test inputs and expected results
      |    |    |    +-- testdata              # Directory with test resource YAML definitions
      ```
    * "health_test.yaml"
      * == YAML file / structure

        ```yaml
        tests:
          - healthStatus:
              status: ExpectedStatus
              message: Expected message
            inputPath: testdata/test-resource-definition.yaml
          ```
  * if you want to test the implemented custom health checks -> `go test -v ./util/lua/`

##### Wildcard Support

* `_` character
  * == `*` (wildcard)
  * allows
    * using 1 health check | MULTIPLE resources
  * ALLOWED |
    * CRD group
    * resource kind
  * _Example:_ ANY resource / group ends with `.group.io` -> use the `health.lua` health check
    ```
    argo-cd
    |-- resource_customizations
    |    |-- _.group.io               # CRD group
    |    |    |-- _                   # ANY Resource kind
    |    |    |    |-- health.lua     # Health check
    ```
  * restrictions
    * ❌`_` can NOT be scape❌
      * == if API Group / API Version contains `_` | name -> NO way to specify literally
  * way to choose health check / apply
    1. look for specific health check / resource
       1. if you find specific health check -> apply it
       2. if NO specific health check was found -> look for wildcard checks
          1. if 0 wildcard check found -> NO health check is applied
          2. if 1 wildcard check is found -> apply it
          3. if MULTIPLE wildcard checks match -> use the FIRST one | [/resource_customizations](/resource_customizations)👀
  * if you want to match the wildcard checks -> use the [doublestar glob library](https://github.com/bmatcuk/doublestar)  
  * recommendations
    * avoid massive scripts -- to -- handle MULTIPLE resources
      * Reason:🧠hard to read & maintain🧠

## Health Checks

### Argo CD's Application health checks

* Argo CD's Application's health status
  * -- depends on -- EACH Kubernetes resource's health status
  * 👀== its IMMEDIATE child resources' WORST health status👀 /
    * Best-To-Worst: Healthy, Suspended, Progressing, Missing, Degraded, Unknown
      * _Example:_ if an App has a `Missing` resource & `Degraded` resource -> App's health == `Degraded`
    * ⚠️if you want to ignore a child's health status -> | child, set `argocd.argoproj.io/ignore-healthcheck: "true"`⚠️

### Resource's health checks

* resource
  * 's health 
    * ❌NOT inherited -- from -- child resources' health❌
      * if you want that it takes child resources' health into account -> you need to configure it
        * steps
          * parent resource's controller needs to make the child resource's health AVAILABLE | parent resource's `.status`
      * Reason: 🧠
        * by design
        * child resources' health may NOT be relevant -- to the -- parent resource's health🧠
      * _Example:_ deployment's health is NOT NECESSARILY affected -- by the -- pods' health

        ```
        App (healthy)
        └── Deployment (healthy)
            └── ReplicaSet (healthy)
                └── Pod (healthy)
            └── ReplicaSet (unhealthy)
                └── Pod (unhealthy)
        ```

    * calculated -- from -- ONLY resource's information itself
  * 's status field 
    * may OR may NOT contain information -- about the -- child resource's health
  * 's health check 
    * may OR may NOT take child resource's health into account
