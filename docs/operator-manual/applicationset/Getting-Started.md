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

## how to enable high availability mode?

* Reason:🧠[HA](/manifests/ha/install.yaml) do NOT configure ApplicationSet as HA🧠

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

## how to add Post-Upgrade Safeguards?

* [here](Controlling-Resource-Modification.md) 

* TODO:

- Enable `preserveResourcesOnDeletion` on your ApplicationSets
- Temporarily disable automated sync in your ApplicationSets' template

These parameters would allow you to observe/control the behaviour of the new version
of the ApplicationSet controller in your environment,
to ensure you are happy with the result (see the ApplicationSet log file for details)
* Just don't forget to remove any temporary changes when you are done testing!

However, as mentioned above, these steps are not strictly necessary: 
upgrading the ApplicationSet controller should be a minimally invasive process,
and these are only suggested as an optional precaution for extra safety.
