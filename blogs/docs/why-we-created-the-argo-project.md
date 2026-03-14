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
      * Reason to build it: 🧠 there was NO tool / manage
        * MANY Kubernetes clusters
        * MANY namespaces
        * deployment of applications -- through -- stages🧠
      * 's goal
        * developer experience
      * FIRST design
        * 1! ArgoCD instance
          * cons:
            * 1 attack point
              * SOLUTION: [App Of Apps Pattern](/docs/operator-manual/cluster-bootstrapping.md)
  * | 2022,
    * CNCF' graduation status
    * HIGH adoption
  * 's benefits
    * spend MORE time writing code
      * rather than: figure out how to deploy & manage infrastructure

TODO: 
The second one was to empower teams to work together - the platform and the application teams
* This is why we’ve put emphasis on the GUI of the tool and decided to implement an application-centric view
* Application resource (rather than namespace or cluster view) provides the best granularity for app developers, SREs, and DevOps engineers to work together and improve the application
as well as its deployment and maintenance processes.

With Argo CD you can run your application deployments on auto-pilot, without the need of manually inspecting every change - the GitOps way
* However, to limit the risk of failed deployments to minimum, you still can apply changes one-by-one by reviewing the real-time diff based on the live cluster status.

What’s also important is that in case of an incident in production, you can rollback to the previous version of the application with confidence in a short turnaround time,
assure business continuity and customer satisfaction, while the technical team will inspect what went wrong and ship the fixed version when ready.


How Argo CD Improved Business Metrics and Delivered Business Value
What we were aiming at business-wise was to have great development velocity metrics (nowadays often referred to as the DORA metrics) - 
innovation has to happen frequently and to do that it has to be automated and visual, because if we won’t onboard developers quickly it will take around a year to just teach Kubernetes and then migrate everything to it.

To name just a few things Argo CD helps in:

increasing visibility into Kubernetes infrastructure and helping teams navigate it

visualizing how Kubernetes actually works

introducing various views to understand what’s happening under the hood (ie
* networking view)

showing the connections between Kubernetes pods, clusters, apps,

improving business metrics such as

release frequency

MTTD, MTTR (with Intuit being a fintech company, every downtime period actually costs millions of dollars)

handling crisis situations without “throwing logs over the fence” (ie
* with notifications to inform relevant teams and all the views in one place)

As Argo CD was crucial for a big team at Intuit, we also see now how it’s crucial for teams that are smaller and just want to adopt Kubernetes and improve their business metrics.

The missing piece - Argo Rollouts
As we shipped more and more to Kubernetes across the Intuit microservices landscape, utilizing the deployment generic workflows, we’ve noticed two things:

a big percentage of incidents (around 50%) happened around the software release periods

paying millions of dollars for observability tools led only to finding the causes of issues and not actively preventing them from happening or shortening the meantime to remedy (MTTR)

Here’s where the need of creating a fast feedback loop after triggering a release was really crucial
* We talked with our application team about the idea of using the data matrix pattern for dry-running our software releases and they really loved it.

We’ve also decided to introduce the two substantial deployment strategies:

blue-green (a gradual user traffic transfer from a previous version of an app to a nearly identical new release)

canary (split the users into two groups where a small percentage will go to the canary while the rest stay on the old version)

With Argo Rollouts, when a business/product team wants to tiptoe into production and make sure everything works, 
it can quickly roll back to find and fix the issue in staging/QA and not lose money and decrease clients satisfaction.

Argo Rollouts was first championed by the payment product team at Intuit who wanted to make sure every single release
is stable just to handle all the millions of transactions taking place inside their products.

After a successful implementation at Intuit (TurboTax, QuickBooks), Argo Rollouts is now powering a lot of large-scale application releases in the cloud - at Salesforce and Spotify,
to just name a few.

Innovation on Top of Argo - Akuity Platform
While the Argo Project largely improved the lives of both business and platform teams, there are still many challenges that we want to face by building innovative solutions on top of this recently CNCF-graduated project.

With the Akuity Platform and its unique architecture we want to increase the velocity of teams even more and take it to a completely new level
* Our “Argo CD as a managed service” offer is already meeting its early adopters and enabling them to quickly scale applications at an enterprise scale.

Still, we think that Argo is just another layer on top of Kubernetes
* We believe there are many use cases that will become best practices as quickly as Argo became the recommended solution for Kubernetes application delivery.

Akuity is perfectly positioned to bring innovation on top of Argo and focus on what’s next
* This includes creating new open source projects (have you heard about Kargo yet?) as well as delivering premium enterprise features to
bridge the gap between GitOps and multi-step processes needed to satisfy business, compliance, security, and testing requirements.

Don’t hesitate to get in touch with me to share your pains, bottle necks, and ideas on how to level up cloud native deployment (and improve the sleep quality of every professional involved 😉)
* I’m also available on the CNCF Slack (`argo-*` channels), LinkedIn, or you can just drop us a message.

Additional Resources
Loved this blog post? Check out other relevant resources:

[Blog Post] Argo Graduation Day!

[Blog Post] The Argo Trio Comes Back Together

[Video] Argo Graduation Q&A - Open Meeting with the Creators of Argo

[Video] Introduction to Argo CD Using the Akuity Platform

Ready to simplify delivery with Akuity?
Deploy, promote, and operate applications reliably, powered by OSS you trust and Intelligence you control.

Request a Demo
Try it for free
Sign Up for Akuity Updates

Practical guidance on MTTR reduction, GitOps at scale, and safe automation, with product updates from the Argo CD and Kargo team.
