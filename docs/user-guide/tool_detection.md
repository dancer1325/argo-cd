# Tool Detection

* tool / build an application

TODO: 
If a specific tool is explicitly configured, then that tool is selected to create your application's manifests.

* way to EXPLICITLY specify | Application

You also can select the tool in the Application creation wizard in the web user interface
* The default is 'Directory'
* Press the dropdown button beneath the tool name if you want to choose a different one.


If not, then the tool is detected implicitly as follows:

* **Helm** if there's a file matching `Chart.yaml`. 
* **Kustomize** if there's a `kustomization.yaml`, `kustomization.yml`, or `Kustomization`

Otherwise it is assumed to be a plain **directory** application. 

## Disable built-in tools

* steps
  * | "argocd-cm" ConfigMap,
    ```
    kustomize.enable: false
    helm.enable: false
    jsonnet.enable: false
    ```

* -> Argo CD assume
  * application target directory contains plain Kubernetes YAML manifests

TODO: 
Disabling unused config management tools can be a helpful security enhancement
* Vulnerabilities are sometimes limited to certain config management tools
* Even if there is no vulnerability, an attacker may use a certain tool to take advantage 
of a misconfiguration in an Argo CD instance
* Disabling unused config management tools limits the tools available to malicious actors.
