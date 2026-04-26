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
      * 💡manage (update, create, delete, ...) MULTIPLE Argo CD Applications 💡-- as a -- 1! unit
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

* how does it work?
  * ArgoCD ApplicationSet controller
    * produces -- , based on generator's entries -- a set of template parameters
    * substitute the template parameters | template
    * converts EACH rendered template -- into an -- Argo CD `Application` resource 
    * handles the Application
  * Argo CD controller
    * handle (deploy) the `Application` resource
