---
title: "Argo CD vs. Flux - 2024 Edition"
subtitle: "Unveiling the path to effortless GitOps orchestration"
source: "Brought to you by Akuity - akuity.io"
date: 2024
---

# Argo CD vs. Flux

**Unveiling the path to effortless GitOps orchestration**

*2024 Edition*

## Introduction

TODO: 
* A method of operationalizing a Kubernetes platform, GitOps has been the operating model for Kubernetes in many organizations - to which it has been adopted by Platform Engineers, DevOps Engineers, and SRE teams alike
* In fact, it has become so popular that an open standard of how GitOps is implemented has emerged in the form of [OpenGitOps](https://opengitops.dev/) (CNCF Sandbox project).

When organizations are on their Kubernetes adoption journey, they undoubtedly run into two big players when researching GitOps: Argo CD and Flux
* A tale as old as Ford vs Chevy and VIM vs Emacs - the two major players in this space both have a large community, large user base, and seemingly have the same end goal of easing the use of Kubernetes via GitOps
* Both projects have reached graduation status in the CNCF and both projects continue to grow.

So, the elephant in the room, is the very question that the title of this whitepaper alludes to
* What are the differences between Flux and Argo CD? What kind of things do you need to take into consideration when deciding? What are some of the advantages and disadvantages of their different approaches?

In this whitepaper, we'll explore these questions in depth in order to get a clear understanding on what to look at when exploring both solutions
* It's important to disclose that, while I spent a lot of time evaluating (and yes even using) both tools, I am a contributor to the Argo Project working for Akuity.

### Versions Used

| TOOL       | VERSION | DATE         |
|------------|---------|--------------|
| Kubernetes | v1.27.3 | July 2023    |
| Argo CD    | v2.7.7  | July 2023    |
| Flux       | v2.2.0  | December 2023|

---

## 1. Philosophical Differences

First thing to take into account is the background of each tool
* It's important to know how each tool came about and their respective philosophies before you try to analyze the technical differences between them
* Here, I'm going to explore the background and some of the philosophical differences between the two tools.

### 1.1. Argo CD

Argo CD is a part of a suite of DevOps centric tools developed internally at Intuit, known as the Argo Project
* Other tools include Argo Workflows, Argo Rollouts, and Argo Events
* The Argo Project has its roots at Applatix, and continued to flourish after the acquisition by Intuit
* The goal of the Argo Project was simple: operationalize Kubernetes while making it easy for developers to onboard their applications to the platform
* In a way, the Argo Project can be seen as an early attempt at an Internal Development Platform (IDP)
* The focus of the tools within the Argo Project was to abstract away Kubernetes primitives
* When Argo CD was introduced; the approach was to make Kubernetes accessible and easy to use for Administrators and Developers alike.

Another important aspect of Argo CD, was that it is Kubernetes-centric - meaning that it was built as a true interface into the Kubernetes environment
* This is the reason why the choice was made to make Argo CD "act" as a Kubernetes client (namely: `kubectl`)
* To that end, one of the most important philosophical choices was made - Argo CD will only interact with RAW, Kubernetes native, manifests
* In other words, only JSON/YAML of objects that Kubernetes "understands".

### 1.2. Flux

It's important to note that while there was a previous version of Flux, this whitepaper will concentrate on the latest version known as "Flux v2"
* Just for the sake of simplicity, anytime we mention Flux; I am referring to Flux v2.

Flux was developed internally at Weaveworks, then open-sourced/donated to the CNCF
* Weaveworks developed Flux out of their SRE/DevOps teams
* They needed a way to not only manage their infrastructure, but also wanted the ability to recover fast if they needed to and wanted to prevent any drift on their infrastructure
* Flux was a controller that reflected how the SRE/DevOps engineers managed Weaveworks SaaS offerings at the time
* It was born out of the principles these engineers used by which they operated their Kubernetes system.

Building on their experience with managing their Kubernetes systems, Weaveworks released Flux ("version 1" as it's known) and was open-sourced
* After feedback from the community, the Flux project refactored the codebase to build on top of "[The GitOps Toolkit](https://fluxcd.io/flux/components/)".

The GitOps Toolkit is a set of composable APIs and specialized tools that can be used to build a GitOps centric toolset on top of Kubernetes
* Flux (version 2 as it's called now) is constructed with the GitOps Toolkit components, and can be seen as the baseline implementation of it
* The idea behind the GitOps Toolkit is to use native tooling via Go (for example [Kustomizations](https://github.com/kubernetes-sigs/kustomize) use the Kustomize Go library and [HelmReleases](https://fluxcd.io/flux/components/helm/) uses the Helm Go library) to interact with manifests being deployed to the target Kubernetes cluster.

### 1.3. Different Sides to the Same Coin

It's important to note that there are a lot of similarities (at least at the core) between Argo CD and Flux
* The venn diagram of functionality overlaps a LOT and any technical differences often stem from their philosophical approach
* Although both tools reached (almost) the same conclusion, they reached it from different perspectives.

The thing to keep in mind is that Argo CD was built for Developers, and with the Developer Experience in mind
* Flux was built for the SREs and with the SREs experience in mind.

---

## 2. Technical Differences

Since each tool came from a different philosophical background, the technical differences are small but significant.

### 2.1. UI

The biggest difference between the two tools that folks will notice is their UI
* That difference comes in the form of, to put it bluntly, one tool having a native UI and the other not.

#### Argo CD

Argo CD comes with a native web UI that is feature-rich for both Developers and Operations teams alike.

![Argo CD UI Screenshot](static/argocd-ui-screenshot.png)

This is one of the most attractive features of Argo CD
* Since the UI is part of the core codebase, anyone using Argo CD can receive the benefit of any and all updates and new features released.

#### Flux

Flux does not have a native UI, however there are other projects that attempt to build a UI for it - like [Weave GitOps Core](https://www.weave.works/product/gitops-core/) by Weaveworks
* However, there's nothing built into the upstream Flux project.

### 2.2. CLI

Both Flux and Argo CD can be managed, exclusively, via their command line client
* The differences are nuanced, but important to point out.

#### Argo CD

Argo CD's CLI client (`argocd`) is feature rich and Argo CD can be fully managed with it
* Administrators can manage users and clusters, set repository settings, initiate syncs, diff state, and create/manage/update Applications
* However, Argo CD CLI client doesn't (nor Argo CD itself) have a concept of "bootstrapping"
* Instead, it leaves that responsibility to the end user
* Also, it's possible (and advisable) to use Argo CD to manage Argo CD itself
* Using the model of Argo CD managing itself, is mainly done using the [App of Apps Pattern](https://argo-cd.readthedocs.io/en/stable/operator-manual/cluster-bootstrapping/) (which can be seen as a form of bootstrapping)
* Also, there are projects like [Argo CD Autopilot](https://argocd-autopilot.readthedocs.io/), that aim to give a bootstrapping interface
* Autopilot isn't an official Argo Project tool; which is why it is in the Argo Project Labs repository.

#### Flux

Flux CLI client also has all the features needed in order to manage everything on a system managed by Flux
* In fact, this is the primary interface to work with Flux
* Where Flux stands out is that it has a **native bootstrapping ability**
* This takes care of a few things for the end user: it installs Flux on the target system, it sets up the Git repository (on either Bitbucket, GitHub, GitLab, or any git compatible repository via ssh), and an opinionated directory structure
* An end user would just have to start adding things to this repository and Flux will take care of deploying those on to the target system
* Flux treats bootstrapping like a first-class citizen and is the primary entry point for users to start using Flux.

### 2.3. Helm

The starkest difference between the two tools is how they manage Helm deployments
* While each method has its roots in the philosophical underpinning of each tool, there are also technical advantages/disadvantages to each.

#### Argo CD

Since Argo CD uses `helm template` to render Kubernetes manifests and apply them to the target cluster, the `helm` CLI can't be used to manage Helm releases.

```bash
$ helm ls -A
NAME    NAMESPACE    REVISION    UPDATED    STATUS    CHART    APP_VERSION
```

The reason Argo CD uses this method is twofold
* First, Argo CD's philosophical stance of only working with native Kubernetes manifests
* Secondly, Argo CD wants to be able to detect differences between the running state and the desired state
* The bottom example shows scaling a Deployment includes a Helm release after it was installed via Argo CD (i.e
* out of band change with `kubectl scale`)

```bash
$ argocd app diff argocd/quarkus-app

===== apps/Deployment demo/quarkus-app ======
144c144
<   replicas: 3
---
>   replicas: 1
```

You can also see this diff in the UI as well.

![Argo CD Diff UI Screenshot](static/argocd-diff-ui.png)

From here you can make the choice of reconciling those differences by syncing the Argo CD Application or doing this automatically by having auto-sync enabled.

#### Flux

Flux uses the native [Helm Golang library](https://pkg.go.dev/helm.sh/helm/v3) in order to install Helm Charts, which means that it works natively with the `helm` CLI
* This emulates the experience of how most folks would interact with Helm on a Kubernetes cluster.

```bash
$ helm ls -A
NAME              NAMESPACE   REVISION   UPDATED                                STATUS      APP_VERSION
quarkus-sample    quarkus     1          2023-06-30  21:47:53 +0000 UTC        deployed    quarkus-0.0.3
```

While using the Helm Golang library gives you the ability to interact with Helm charts the way you're used to, there is an issue with noticing when there's a configuration change
* The following is the same example of scaling the replica count to 3 on a Helm release that was installed via Flux.

```bash
$ flux diff -h
The diff command is used to do a server-side dry-run on flux resources,
then prints the diff.

Usage:
  flux diff [command]

Available Commands:
  artifact  Diff Artifact
  kustomization Diff Kustomization

Flags:
  -h, --help    help for diff
```

As you can see, there's currently no way to do an on-demand diff with HelmReleases with Flux
* On-demand diffs can only be done with `Kustomizations`.

```bash
$ flux diff  kustomization flux-system --path ./
✓ Kustomization diffing...
► Deployment/bgd/bgd drifted

metadata.generation
  ± value change
  - 6
  + 7

spec.replicas
  ± value change
  - 3
  + 1

⚠ identified at least one change, exiting with non-zero exit code
```

#### Helm Diffing and Reconciliation

Starting with Flux version 2.2.0, the Helm Controller can now detect and reconcile differences
* This update allows the end user to (optionally) turn on drift detection in the HelmRelease object by setting `.spec.driftDetection.mode` to `enabled`.

```yaml
spec:
  driftDetection:
    mode: enabled
```

Setting this in the HelmRelease configuration allows the Helm Controller to detect and correct drift.

### 2.4. Authentication

Authentication and Authorization are table stakes features that many organizations will absolutely need to rely on, especially if Multi-Tenancy is something they are going to implement.

#### Argo CD

Argo CD has native support for SSO (Single Sign On) using OIDC (Open ID Connect), and Argo CD bundles [Dex](https://dexidp.io/) for those users that are using something that's not OIDC compliant (like SAML or LDAP)
* Administrators can create rules targeting users that have logged in (by either username or by group membership)
* Once set up, users can login to Argo CD using the configured SSO backend (for example using GitHub below)

![Argo CD SSO Login](static/argocd-sso-login.png)

Once logged in, you'll be able to see the information passed down by the authentication provider (in this instance GitHub) and any group affiliations.

![Argo CD User Info](static/argocd-user-info.png)

RBAC can then be mapped to this user or any groups this user belongs to.

#### Flux

Flux relies on Kubernetes for users and groups and leverages the built in Kubernetes RBAC system
* Now, although users/groups can be provided to Flux via Kubernetes, Flux is designed to work with Kubernetes ServiceAccounts, and it runs synchronization tasks using specific service accounts (depending on how it's configured).

### 2.5. Multi-tenancy

As the adoption of Kubernetes grows, so does the need for support of multi-tenancy within those Kubernetes deployments
* Both Argo CD and Flux support multi-tenancy but approach it in fundamentally different ways.

#### Argo CD

Argo CD was built from the ground up with multi-tenancy in mind
* It provides a feature rich/granular RBAC system that can target specific users, groups, clusters or [Application Projects](https://argo-cd.readthedocs.io/en/stable/user-guide/projects/)
* It also can restrict what action can be performed on a variety of things that Argo CD manages.

Taking a look at Argo CD, you can see that you can configure a variety of things that Argo CD can manage:

![Argo CD Settings](static/argocd-settings.png)

All these objects can be scoped to RBAC policies set by an administrator
* These RBAC rules can be global or they can target a logical grouping known as an [Argo CD Application Project](https://argo-cd.readthedocs.io/en/stable/user-guide/projects/).

Argo CD AppProject is a construct that logically groups together Argo CD Applications
* This can be seen as a logical barrier between tenants
* From within an AppProject, an administrator can restrict not only specific groups or users to an AppProject, but also restrict what a user/group can do within an AppProject
* As an admin you can restrict what can be deployed (scoped down to the specific Git repo or group of Repos), restrict where it gets deployed to (either a specific cluster, namespace, or combination of them both), and also restrict what kinds of objects can be deployed (for example you can allow only `Pod` definitions to be deployed)

#### Flux

Flux has the concept of Multi-tenancy, but relies heavily on Kubernetes RBAC policies to control what can be deployed where and by whom
* Flux does this by relying on the service account that is configured to do the action (which has to be set up beforehand by an administrator)
* While you can target specific Kubernetes clusters via the `kubeConfig` field or `kustomization` or `HelmRelease`, there is no central way to manage clusters or any custom RBAC that specifically targets cluster configurations.

Flux restricts things based solely on Kubernetes objects and Kubernetes RBAC
* If someone needs more fine grained control, they would need to rely on a 3rd party tool in order to get some of the same functionality that's built natively into Argo CD.

### 2.6. Syncing Policies

Syncing, for the purposes of this comparison, is the attempt to match the running state of the system to the desired state of the system
* Both tools do automatic syncs and both tools have a mechanism to pause syncing (the "break glass" concept) for debugging/issue triage
* From a functional perspective (core GitOps principles), both tools are very similar in regards to syncing, but there are a few substantial differences.

#### Argo CD

Syncing in Argo CD can be done in a variety of ways, which allows for fine-grained control in how your application gets deployed
* One method that Argo CD supports is partial and selective syncs
* You can specify what resources get synced and even elect to only sync items that are out of sync (which can also be set as the default)
* On top of that, you can also set up Sync Windows (a time frame only where syncing is allowed) so that changes to the system only happen during, say, a maintenance window.

Argo CD has also a concept of Syncwaves and Sync Phases/Hooks that can be used for more fine-grained control on how your application gets deployed
* Syncwaves, is a sync setting that allows you to order how your manifests get deployed
* For example: you may want to make sure your Deployment and PVC are healthy and bound before your ingress object gets updated, or you want to create a service account before a Deployment, or ensure that network policies exist before a Deployment so that it doesn't briefly have unrestricted access
* Sync Phases help in the event where you need a Job to run right before a sync happens or right after (also, you can run a phase in the event something fails as well).

#### Flux

Flux takes the approach of retrying reconciliation in case the first attempt fails for whatever reason, relying on the "eventual consistency" design of Kubernetes
* While you can't customize how syncs happen, you can ignore certain resources during reconciliation with a label or specifying them in the `Kustomization` object
* You are also able to provide ignore rules for HelmReleases
* Flux does support phases/hooks by the way of Helm (meaning you have to write a Helm Chart if you want to take advantage of hooks in your application with Flux).

### 2.7. Multi-Cluster Management

Managing multiple clusters is an important topic for many organizations
* More often than not, organizations are managing multiple clusters across multiple regions that span multiple environments
* Being able to make sense of what is deployed, and where something is running, becomes paramount to operating Kubernetes at scale.

#### Argo CD

As mentioned in the Multi-Tenancy section, Argo CD's UI is feature-rich and can be used to configure a variety of things
* One of which is the ability to add/remove/update clusters
* Argo CD's UI makes it easy to understand what is happening across all clusters in your environment
* It also has things like `kubeconfig` management built-in to the platform.

![Argo CD Cluster Management](static/argocd-clusters.png)

In the overview page, you can filter out Argo CD Applications based on which cluster they are running on for a clear view of running workloads.

![Argo CD Application Overview](static/argocd-app-overview.png)

Not only can you further refine the overview page to really dig down into your workloads, cluster configurations can also be targeted by Argo CD's RBAC system as well
* This gives Admins and Developers fine-grained control to not only what cluster can be deployed to, but which namespace and which specific manifest as well.

#### Flux

Flux does not have a concept of "clusters"
* Instead, Flux relies on the user providing a Kubeconfig file for each Kustomization/HelmRelease to achieve its multi-cluster design
* This potentially means that users/admins must keep track of all KubeConfig files for each cluster
* While it's possible for Kustomizations/HelmReleases to "share" these KubeConfig files; end users might still need to keep multiple copies in the event that there are different KubeConfig files with different ServiceAccounts for the same cluster.

### 2.8. Custom Tooling

When it comes to tooling around Kubernetes, there is no shortage of tools in the CNCF landscape
* Still, Kustomize and Helm have become the two most popular (and in some cases the default) ways to modify and/or templatize your manifest before they get applied to your clusters
* Both Argo CD and Flux support Kustomize and Helm, but what about other tooling?

#### Argo CD

Earlier in this whitepaper, we explored the philosophical approach that Argo CD took with Helm and using the Helm template
* We went over some of the advantages this gives users with diffing and reconciliation
* But stepping back, Argo CD uses this method to abstract itself away from any one templating engine
* In order to not tie itself down by writing support inside of Argo CD's codebase; Argo CD introduced [ConfigManagement Plugins](https://argo-cd.readthedocs.io/en/stable/operator-manual/config-management-plugins/) (CMPs)

CMPs are the way Argo CD supports custom tooling beyond just Kustomize and Helm
* It's also a method to chain together different tools in order to get a desired result
* Since Argo CD just works with "Raw" Kubernetes manifests, you can provide any custom tooling as long as the end result is a Kubernetes Manifest
* The most popular CMP is Helmfile but really anything that can generate a Kubernetes manifest can be used.

#### Flux

Flux, as mentioned earlier, is an implementation of the GitOps Toolkit
* This toolkit includes custom controllers for Kustomize (known as `Kustomizations`) and Helm (known as `HelmReleases`)
* These controllers are used by Flux to deploy workloads onto the target cluster
* While it's possible to do a Helm `postRender` with Kustomize, there isn't an ability to use other configuration tools on the deployment
* For example, in order to support Carvel's YTT a controller needs to be written for it
* Flux requires deeper integration in order to use other tooling.

### 2.9. Application Templating

Defining your source of truth and your destination is the cornerstone of every GitOps implementation
* Reconciliation can only happen when you define your state and where it needs to be applied
* As your implementation grows, the need to be able to template out these definitions becomes something that is needed when you scale out.

#### Argo CD

Argo CD has a concept called "Applications", which acts as the interface (and the atomic unit of work) into Argo CD
* Users can use Argo CD Applications to define the type (Git, Helm, OCI), the source and destination of their deployments; and Argo CD takes it from there
* The challenge comes when organizations start implementing entire stacks across multiple clusters across multiple environments
* A definition needs to exist for every instance you want your deployment to run on
* The App-of-Apps pattern helps in this regard but there is also a need to templatize.

Argo CD introduced ApplicationSets
* ApplicationSets can be seen as an "Argo CD Application Factory"; users can define various inputs to use to generate Argo CD Applications
* Within ApplicationSets, there is a concept of "Generators"
* Argo CD ApplicationSet Generators defines "how" to get the inputs
* Some of the most popular Generators are "[List Generator](https://argo-cd.readthedocs.io/en/stable/operator-manual/applicationset/Generators-List/)" (which is just a user-defined key/value pairs) and the "[Cluster Generator](https://argo-cd.readthedocs.io/en/stable/operator-manual/applicationset/Generators-Cluster/)" (where values are generated based on the information about the target cluster).

#### Flux

Flux has the concept of [Kustomizations](https://fluxcd.io/flux/components/kustomize/kustomizations/) (even using "just plain YAML" uses Kustomize under the hood) and "[HelmReleases](https://fluxcd.io/flux/components/helm/helmreleases/)"
* These are, effectively, analogous to the Application paradigm that Argo CD has
* In many ways, both tools are identical in this regard (In that they both have a CRD that defines a source and destination).

Flux does not have native support for templating out Kustomizations or HelmReleases,
* Instead, it relies on users creating Helm templates for Kustomizations and HelmReleases templating.

### 2.10. Product vs Toolkit

Since Flux is an implementation of the GitOps Toolkit, other implementations exist; for instance  Weave GitOps, Azure Arc, and Gitlab GitOps Agent
* This is why some implementations have a UI, like Weave GitOps, and others (like Flux v2) do not
* In contrast, Argo CD was built as a complete, feature rich, platform.

This means that once you've installed Argo CD, you're ready to start using the platform and all its "batteries included" toolsets
* In fact, many of Argo CD features (like Argo CD ApplicationSets and Argo CD Notifications) started off incubating in the Argo Project Labs repo before being merged into the main Argo CD codebase in order to provide end users with a more feature rich experience.

With all that Flux provides to you, you need other tools in order to really get the most out of all you're getting with it
* This is why most implementations of the GitOps Toolkit add additional functionalities.

---

## Conclusion

In this whitepaper, we've covered some differences between both Argo CD and Flux; arguably the two most popular GitOps toolsets
* There are a lot of similarities and the differences can seem nuanced at times.

In the end, the choice is ultimately up to the end users and what those users find important
* The old adage of "try it and see" comes to mind here, still, the differences (while subtle) are important to take into account when testing out these two tools
* Hopefully this document helped you in some way to see the differences and save some time in doing your own research.

The following table outlines the important points brought up in this whitepaper.

| Features | Argo CD | Flux |
|----------|---------|------|
| OpenGitOps Compliant (core GitOps Functionality) | Yes | Yes |
| Support for Helm and Kustomized deployments | Yes | Yes |
| Native UI | Yes | No |
| Native Bootstrapping Capability | No | Yes |
| Multi-Tenant Support | Yes | Yes |
| Support for Partial/Selective Syncs | Yes | Helm only |
| Support for native Helm (cli) tooling | No | Yes |
| Natively Support Helm diff-ing and reconciliation | Yes | Yes |
| Support for Enterprise SSO integrations | Yes | No |
| Pause/Restart reconciliation for incident handling | Yes | Yes |
| Support for hooks to pre/post jobs | Yes | via Helm |
| Support for deployment templating | Yes | via Helm |
| Feature Rich RBAC System | Yes | No |
| Support for extending Configuration Management tools like Carvel's YTT, Tanka, Cue, etc | Yes | No |
