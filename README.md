**Releases:**
[![Release Version](https://img.shields.io/github/v/release/argoproj/argo-cd?label=argo-cd)](https://github.com/argoproj/argo-cd/releases/latest)
[![Artifact HUB](https://img.shields.io/endpoint?url=https://artifacthub.io/badge/repository/argo-cd)](https://artifacthub.io/packages/helm/argo/argo-cd)

# Argo CD - Declarative Continuous Delivery for Kubernetes

* Argo CD
  * == CD tool for Kubernetes /
    * declarative
      * == define the desired application state
    * follow GitOps pattern 
      * == Git repositories == source of truth
  * [video](https://youtu.be/0WAm0y2vLIo) 
    * TODO: 
  * benefits
    * ⚠️force you to follow GitOps model | your Kubernetes manifests (Deployment, ConfigMaps, namespaces, ..) or environment (cluster + namespace)⚠️
      * otherwise, people MANUALLY or via scripts running `kubectl apply ...` commands
    * application deployment (specifying the target environment) & lifecycle management are
      * automated
      * auditable

![Argo CD UI](docs/assets/argocd-ui.gif)

## Who uses Argo CD?

* [Official organizations / use Argo CD](USERS.md)

## Documentation

* [here](docs)

## Community

### Contribution, Discussion and Support

* [Q & A](https://github.com/argoproj/argo-cd/discussions)
* [Slack discussions](https://argoproj.github.io/community/join-slack)
* User Community meeting
  * [First Wednesday of the month](https://calendar.google.com/calendar/u/0/embed?src=argoproj@gmail.com)
  * [Agenda](https://docs.google.com/document/d/1ttgw98MO45Dq7ZUHpIiOIEfbyeitKHNfMjbY5dLLMKQ)

### Blogs and Presentations

TODO: check which one make sense

1. [Awesome-Argo: A Curated List of Awesome Projects and Resources Related to Argo](https://github.com/terrytangyuan/awesome-argo)
1. [Unveil the Secret Ingredients of Continuous Delivery at Enterprise Scale with Argo CD](https://akuity.io/blog/secret-ingredients-of-continuous-delivery-at-enterprise-scale-with-argocd/)
1. [GitOps Without Pipelines With ArgoCD Image Updater](https://youtu.be/avPUQin9kzU)
1. [Combining Argo CD (GitOps), Crossplane (Control Plane), And KubeVela (OAM)](https://youtu.be/eEcgn_gU3SM)
1. [How to Apply GitOps to Everything - Combining Argo CD and Crossplane](https://youtu.be/yrj4lmScKHQ)
1. [Couchbase - How To Run a Database Cluster in Kubernetes Using Argo CD](https://youtu.be/nkPoPaVzExY)
1. [Automation of Everything - How To Combine Argo Events, Workflows & Pipelines, CD, and Rollouts](https://youtu.be/XNXJtxkUKeY)
1. [Environments Based On Pull Requests (PRs): Using Argo CD To Apply GitOps Principles On Previews](https://youtu.be/cpAaI8p4R60)
1. [Argo CD: Applying GitOps Principles To Manage Production Environment In Kubernetes](https://youtu.be/vpWQeoaiRM4)
1. [Creating Temporary Preview Environments Based On Pull Requests With Argo CD And Codefresh](https://codefresh.io/continuous-deployment/creating-temporary-preview-environments-based-pull-requests-argo-cd-codefresh/)
1. [Tutorial: Everything You Need To Become A GitOps Ninja](https://www.youtube.com/watch?v=r50tRQjisxw) 90m tutorial on GitOps and Argo CD.
1. [Comparison of Argo CD, Spinnaker, Jenkins X, and Tekton](https://www.inovex.de/blog/spinnaker-vs-argo-cd-vs-tekton-vs-jenkins-x/)
1. [Simplify and Automate Deployments Using GitOps with IBM Multicloud Manager 3.1.2](https://www.ibm.com/cloud/blog/simplify-and-automate-deployments-using-gitops-with-ibm-multicloud-manager-3-1-2)
1. [GitOps for Kubeflow using Argo CD](https://v0-6.kubeflow.org/docs/use-cases/gitops-for-kubeflow/)
1. [GitOps Toolsets on Kubernetes with CircleCI and Argo CD](https://www.digitalocean.com/community/tutorials/webinar-series-gitops-tool-sets-on-kubernetes-with-circleci-and-argo-cd)
1. [CI/CD in Light Speed with K8s and Argo CD](https://www.youtube.com/watch?v=OdzH82VpMwI&feature=youtu.be)
1. [Machine Learning as Code](https://www.youtube.com/watch?v=VXrGp5er1ZE&t=0s&index=135&list=PLj6h78yzYM2PZf9eA7bhWnIh_mK1vyOfU). Among other things, describes how Kubeflow uses Argo CD to implement GitOPs for ML
1. [Argo CD - GitOps Continuous Delivery for Kubernetes](https://www.youtube.com/watch?v=aWDIQMbp1cc&feature=youtu.be&t=1m4s)
1. [Introduction to Argo CD : Kubernetes DevOps CI/CD](https://www.youtube.com/watch?v=2WSJF7d8dUg&feature=youtu.be)
1. [GitOps Deployment and Kubernetes - using Argo CD](https://medium.com/riskified-technology/gitops-deployment-and-kubernetes-f1ab289efa4b)
1. [Deploy Argo CD with Ingress and TLS in Three Steps: No YAML Yak Shaving Required](https://itnext.io/deploy-argo-cd-with-ingress-and-tls-in-three-steps-no-yaml-yak-shaving-required-bc536d401491)
1. [GitOps Continuous Delivery with Argo and Codefresh](https://codefresh.io/events/cncf-member-webinar-gitops-continuous-delivery-argo-codefresh/)
1. [Stay up to date with Argo CD and Renovate](https://mjpitz.com/blog/2020/12/03/renovate-your-gitops/)
1. [Setting up Argo CD with Helm](https://www.arthurkoziel.com/setting-up-argocd-with-helm/)
1. [Applied GitOps with Argo CD](https://thenewstack.io/applied-gitops-with-argocd/)
1. [Solving configuration drift using GitOps with Argo CD](https://www.cncf.io/blog/2020/12/17/solving-configuration-drift-using-gitops-with-argo-cd/)
1. [Decentralized GitOps over environments](https://blogs.sap.com/2021/05/06/decentralized-gitops-over-environments/)
1. [Getting Started with ArgoCD for GitOps Deployments](https://youtu.be/AvLuplh1skA)
1. [Using Argo CD & Datree for Stable Kubernetes CI/CD Deployments](https://youtu.be/17894DTru2Y)
1. [How to create Argo CD Applications Automatically using ApplicationSet? "Automation of GitOps"](https://amralaayassen.medium.com/how-to-create-argocd-applications-automatically-using-applicationset-automation-of-the-gitops-59455eaf4f72)
1. [Progressive Delivery with Service Mesh – Argo Rollouts with Istio](https://www.cncf.io/blog/2022/12/16/progressive-delivery-with-service-mesh-argo-rollouts-with-istio/)
