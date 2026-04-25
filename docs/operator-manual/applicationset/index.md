# ApplicationSet controller

## Introduction

* ApplicationSet controller
  * == [Kubernetes controller](https://kubernetes.io/docs/concepts/architecture/controller/) / support -- for -- `ApplicationSet` [CRD](https://kubernetes.io/docs/tasks/extend-kubernetes/custom-resources/custom-resource-definitions/)
  * | Argo CD v2.3,
    * ApplicationSet controller is bundled | Argo CD
      * == installed INDEPENDENTLY
  * allows
    * | 1! Kubernetes manifest,
      * target MULTIPLE Kubernetes clusters
      * 💡manage MULTIPLE Argo CD Applications 💡-- as a -- 1! unit
      * deploy MULTIPLE applications -- from -- >=1 Git repositories
  * use cases
    * | [monorepos](Use-Cases.md#use-case-monorepos)
    * | [multitenant clusters](Use-Cases.md#use-case-self-service-of-argo-cd-applications--multitenant-clusters)
  * cons
    * ⚠️[security implications](./Security.md)⚠️

* [Generators](Generators.md)

## Parameter substitution | ApplicationSet's `spec.template`
 
* use cases
  * ANY generator
* allows
  * parameters / generated -- by a -- generator,
    * can be substituted | `spec.template` -- via -- `{{parameter_name}}`

* steps to processing it
  * ArgoCD ApplicationSet controller
    * produces -- , based on generator's entries -- a set of template parameters
    * substitute the template parameters | template
    * converts EACH rendered template -- into an -- Argo CD `Application` resource 
    * handles the Application
  * Argo CD controller
    * handle (deploy) the `Application` resource

TODO:


The ApplicationSet controller will ensure that any changes, updates, or deletions made to `ApplicationSet` resources are automatically
applied to the corresponding `Application`(s).

For instance, if a new cluster/URL list entry was added to the List generator, a new Argo CD `Application` resource
would be accordingly created 
for this new cluster
* Any edits made to the `guestbook` `ApplicationSet` resource will affect all the Argo CD Applications that were instantiated
by that resource, including the new Application.

While the List generator's literal list of clusters is fairly simplistic, much more sophisticated scenarios are supported 
by the other available
generators in the ApplicationSet controller.
