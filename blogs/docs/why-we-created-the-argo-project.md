---
title: "Why We Created The Argo Project"
date: 
source: https://akuity.io/blog/why-we-created-the-argo-project/
---

# Why We Created The Argo Project

December 5, 2023
Hong Wang

* Kubernetes 
  * | 2015,
    * officially released
  * challenges
    * ⚠️how to make robust application deployments & management | Kubernetes?⚠️
      * == ❌there was NOTHING about deployments❌
      * BEFORE ArgoCD
        * `kubectl apply ...` MANUAL OR script
      * EACH company building their own solutions -> appear other tools
        * Helm
        * Kustomize

* Argo Project
  * | 2016, (origins)       
    * by Applatix startup
    * IT ecosystem trends
      * containers
        * container orchestration products
          * Mesosphere
          * Docker Swarm
          * Kubernetes
      * microservices
      * public cloud
    * goal
      * ⭐️build scalable production systems / enable
        * deploy & maintain containers + container orchestrator | public & private clouds⭐️
          * container orchestrator's chosen
            * FIRSTLY
              * Mesosphere
                * PROBLEMS: ⚠️hard learning curve + difficult troubleshooting + vendor lock-in⚠️ 
            * LASTLY
              * Kubernetes
    * ⭐️release Argo Workflows⭐️
    * Jenkins
      * 's design
        * centralized server + agents + plugins
      * 's origins
        * pre-containers
      * problems | this time
        * == ❌NOT fit | IT ecosystem trend❌
        * UI configuration / 
          * ❌NOT possible to 
            * version
            * reproduce❌
          * DIFFICULT to: scalate
  * | 2017,
    * Kubernetes 
      * released CRD
        * -> easier to extend
    * Argo Workflows
      * open-source
      * FULLY rewrite -- based on -- CRD
        * enable
          * orchestrating parallel jobs
        * define
          * workflows -- as--
            * MULTIPLE steps /
              * EACH steps == container
            * sequence of dependant tasks -- via -- directed acyclic graph (DAG)
  * | 2018,
    * acquired -- by -- Intuit
      * Intuit
        * == end user company
        * 's goal
          * develop -- as -- open source
          * put in practice Argo Workflows | real use cases
    * ⭐️release ArgoCD⭐️
  * | 2019,
    * ⭐️release Argo Rollouts⭐️
  * | 2022,
    * CNCF' graduation status
    * HIGH adoption
  * 's benefits
    * spend MORE time writing code
      * rather than: figure out how to deploy & manage infrastructure

# Argo Workflows

* == FIRST product
  * NOT open source
* Reason of its need | Kubernetes ecosystem: 🧠Kubernetes' 
  * design
    * stateless workloads
    * extensible
  * NOT design
    * workflows
      * requirements
        * share data BETWEEN steps
        * dependency BETWEEN steps
        * ...🧠

# Argo CD

* Reason to build it: 🧠 there was NO tool / manage
  * MANY Kubernetes clusters
  * MANY namespaces
  * deployment of applications -- through -- stages🧠

* 's goal
  * developer experience
    * -> focus |
      * UI
      * 👀application-centric view👀
  * work together: devops + developers

* FIRST design
  * 1! ArgoCD instance
    * cons:
      * 1 attack point
        * SOLUTION: [App Of Apps Pattern](/docs/operator-manual/cluster-bootstrapping.md)

* application-centric view
  * == view | Kubernetes cluster
  * ALTERNATIVES
    * namespace OR cluster view
      * PROBLEMS
        * NO logic context
        * mix applications
        * NO clear ownership
        * hard to track history of changes
  * enable
    * make clear the ownership/responsibility
    * developers + devops working together
    * close to business

* allows
  * run your application deployments -- following -- GitOps approach /
    * you can
      * STILL apply changes 1-by-1
      * rollback quickly

## How does Argo CD impact DORA metrics?

* DORA (DevOps Research and Assessment) metrics
  * == Devops' key metrics
  * ==
    * deployment frequency
      * ArgoCD improves it -- thanks to -- [automated sync](/docs/user-guide/auto_sync.md)
    * lead time for changes
      * ArgoCD decreases it -- thanks to -- [auto-pilot](/README.md)
    * change failure rate
      * ArgoCD decreases it -- thanks to -- GitOps
    * MTTR (Mean Time To Recover)
      * ArgoCD decreases it -- thanks to -- [1-click rollback](/docs/user-guide/commands/argocd_app_rollback.md)

# Argo Rollouts

* Reason to build it:
  * 🧠incidents (50%) happen | software release periods🧠

* incidents (50%) happen | software release periods
  * APPROACHES
    * observability tools
      * ONLY make easier finding the causes of issues
      * ❌NOT actively ❌
        * prevent them from happening
        * shorten the MTTR

* implement
  * | Kubernetes deployments, MULTIPLE deployment strategies
    * blue-green
      * == gradual user traffic transfer of an app
    * canary
      * == split the users | 2 groups
        * small percentage go -- to the -- canary
        * rest users go -- to the -- old version

# Akuity Platform

* built | Argo Project
* 's goal
  * increase the velocity of teams
* 's design
  * “Argo CD -- as a -- managed service”

# Additional

* [The Argo Trio Comes Back Together](the-argo-trio-comes-back-together.md)
