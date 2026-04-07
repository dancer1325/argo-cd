# Getting Started

* requirements
  * [Argo CD basic](../../core_concepts.md)
  * install [kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl/)

## ways to install ApplicationSet controller

### | Argo CD v2.3+, ALREADY part of Argo CD

* steps
  * [here](../../getting_started.md)

### | Argo CD v2.3-, install ApplicationSet

* requirements
  * | Argo CD v2.3.0-
  * install ApplicationSet controller | namespace / == namespace / Argo CD is targeting

* steps
  * `kubectl apply -n argocd --server-side --force-conflicts -f https://raw.githubusercontent.com/argoproj/applicationset/v0.4.0/manifests/install.yaml`

* Kubernetes manifests / require the ApplicationSet controller
  * | [manifests/install.yaml](/manifests/install.yaml), see
    - CRD -- for -- `ApplicationSet` resource
    - Deployment -- for -- `argocd-applicationset-controller`
    - ServiceAccount / used -- by -- ApplicationSet controller
      - enable access Argo CD resources
    - Role / 
      - grant RBAC access 
        - -- to -- needed resources
        - -- for -- ServiceAccount
    - RoleBinding /
      - bind the ServiceAccount -- & -- Role

## Enabling high availability mode

* steps
  * | `Deployment` / "argocd-applicationset-controller" name
    * adjust `spec.replicas`
    * set the command ` --enable-leader-election=true` 

        ```bash
            spec:
              containers:
              - command:
                - entrypoint.sh
                - argocd-applicationset-controller
                - --enable-leader-election=true
        ```

* see [ha/install.yaml](/manifests/ha/install.yaml)

### Optional: Additional Post-Upgrade Safeguards

* TODO:
See the [Controlling Resource Modification](Controlling-Resource-Modification.md) page for information on additional parameters you may wish to 
add to the ApplicationSet Resource in `install.yaml`, to provide extra security against any initial, 
unexpected post-upgrade behaviour. 

For instance, to temporarily prevent the upgraded ApplicationSet controller from making any changes, you could:

- Enable dry-run
- Use a create-only policy
- Enable `preserveResourcesOnDeletion` on your ApplicationSets
- Temporarily disable automated sync in your ApplicationSets' template

These parameters would allow you to observe/control the behaviour of the new version of the ApplicationSet controller in your environment,
to ensure you are happy with the result (see the ApplicationSet log file for details)
* Just don't forget to remove any temporary changes when you are done testing!

However, as mentioned above, these steps are not strictly necessary: upgrading the ApplicationSet controller should be a minimally invasive process,
and these are only suggested as an optional precaution for extra safety.
