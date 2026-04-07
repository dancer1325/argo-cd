---
title: "Why Ci And Cd Need To Go Their Separate Ways"
date: 
source: https://akuity.io/blog/why-ci-and-cd-need-to-go-their-separate-ways/
---

# Why Ci And Cd Need To Go Their Separate Ways

Why CI/CD Doesn't Work for Kubernetes
Christian Hernandez

In the constantly evolving landscape of software development, continuous integration (CI) and continuous delivery (CD) have been foundational methodologies for efficient and reliable application deployment.

While CI/CD processes have worked well for previous software development lifecycles, CI/CD is not equipped to handle the complexities of  modern technologies like Kubernetes and GitOps.  In a world where Kubernetes provides an asynchronous deployment mechanism and GitOps offers a declarative approach to manage application states, we need to leverage new tools for software development and delivery.

In this blog we will introduce the concept of continuous promotion and Kargo, a multi-stage GitOps continuous promotion tool that seamlessly orchestrates stage-to-stage deployments, without custom scripts or CI pipelines. We will cover the benefits of continuous promotion for Kubernetes and how to leverage Kargo.

What Is CI/CD? Understanding the Fundamentals
Before we dive into continuous promotion and Kargo, let’s start with the fundamentals of what CI/CD is and how it fits into modern DevOps. Continuous Integration (CI) and Continuous Delivery (CD) are two fundamental DevOps practices that streamline software development and deployment.

Before we dive into why CI and CD need to evolve, let’s start with the fundamentals of what CI/CD is and how it fits into modern DevOps. Continuous Integration (CI) and Continuous Delivery (CD) are two fundamental DevOps practices that streamline software development and deployment.

CI (Continuous Integration) refers to the process of frequently merging code changes into a shared repository, followed by automated testing to detect issues early.

CD (Continuous Delivery) extends this by ensuring that code is always in a deployable state, automating the release process so that teams can push updates to production quickly and reliably.

Together, CI/CD helps organizations accelerate development cycles, reduce manual intervention, and maintain high-quality software releases. However, as modern technologies like Kubernetes and GitOps have evolved, the traditional approach to CI/CD has revealed critical limitations, prompting the need to rethink how these processes interact.


The Evolution of CI/CD
CI and CD are essential practices in software development, designed to enhance the speed and reliability of deploying applications. Initially, CI/CD was a linear process: code was built, tested and then deployed to a target environment. This approach worked well with traditional virtual machines or physical servers, where deployment environments were relatively static.

However, the introduction of containers and Kubernetes changed the landscape drastically. Kubernetes provided a more dynamic, asynchronous deployment mechanism, creating a mismatch with the synchronous nature of traditional CI/CD processes. As a result, teams began to adopt GitOps to better align with this new paradigm and try to mitigate the disconnect with traditional CI/CD processes.

Despite these advancements, CI/CD processes largely remained unchanged, leading to inefficiencies and complexities in managing deployments across different environments. This ongoing evolution highlights the need for more integrated solutions like continuous promotion to bridge these gaps effectively.

The Challenges with Current CI/CD Models
Current CI/CD models face several challenges, especially with the adoption of Kubernetes and GitOps.

Asynchronous vs Synchronous Conflict
The crux of the issue lies in the inherent disconnect between the synchronous nature of traditional CI/CD processes and the asynchronous nature of Kubernetes deployments. This mismatch often leads to inefficiencies where deployment pipelines become cluttered with custom scripts and workarounds to manage the gaps between CI and CD.

GitOps Limitations
GitOps, while effective in managing the last mile of deployment, can’t handle complex multi-environment orchestration. It focuses solely on the final deployment state, leaving a significant operational gap in orchestrating deployments across various stages or environments.

CI Overload
CI pipelines are being overextended and taking on roles they were never designed for, such as managing indefinite deployments and handling complex dependencies. These challenges underscore the need for a more cohesive approach that integrates seamlessly with modern technologies, offering a more flexible and efficient deployment process.

The Complexities of CI/CD Pipelines
Linear vs. Complex Reality
The traditional view of CI/CD as a straightforward, linear process belies the intricate realities faced in modern software development. While initially conceptualized as a sequence of steps — build, test and deploy — the actual deployment pipelines are far more complex. Modern applications often involve numerous interconnected services, each with its own dependencies and lifecycle.

The linear model struggles to accommodate these intricacies, leading to a web of interdependencies and asynchronous processes that must be managed. Additionally, the rise of microservices architecture further complicates this landscape, as each service may have its own CI/CD pipeline with distinct requirements and triggers.

This complexity can lead to issues such as deployment bottlenecks, increased manual intervention and trouble maintaining consistency across environments. Furthermore, the need for continuous monitoring and the ability to handle rapid changes in dynamic cloud environments necessitate a more flexible and adaptive model than the traditional linear approach can provide. Adapting to this complex reality is essential for effective CI/CD implementation.

Overusing CI for CD Tasks
In many organizations, CI pipelines are stretched beyond their intended function, taking on tasks that traditionally belong to the CD domain.

CI is designed to automate building and testing code, focusing on creating reliable artifacts. However, as the complexity of deployment environments grows, CI processes are often burdened with tasks like environment provisioning, configuration management and deployment orchestration.

This overextension results in a cumbersome, inefficient CI pipeline that struggles to manage the demands of modern, dynamic deployments. This misuse not only increases the complexity and maintenance overhead of CI pipelines but also leads to longer cycle times and reduced flexibility. Addressing this issue requires a clear delineation of responsibilities between CI and CD, leveraging appropriate tools to keep each process focused on its core objectives without unnecessary overlap.

Introducing Continuous Promotion: The Missing Link
Continuous promotion is a concept designed to bridge the gap between CI and CD, addressing the limitations of traditional CI/CD pipelines when used with modern technologies like Kubernetes and GitOps.

The idea is to insert an intermediary step that focuses on the promotion of artifacts based on predefined rules and conditions. This approach allows more granular control over the deployment process, ensuring that artifacts are promoted only when they meet specific criteria, such as passing certain tests or receiving necessary approvals.

By doing so, continuous promotion decouples the CI and CD processes, allowing each to focus on its core responsibilities without overextension. This not only streamlines the deployment pipeline but also enhances the reliability and efficiency of the entire process. The need for continuous promotion arises from the increasing complexity of modern deployments, where traditional CI/CD approaches struggle to manage the asynchronous and dynamic nature of cloud native environments effectively.

What Are the Benefits of Continuous Promotion?
Continuous promotion offers several advantages that enhance the efficiency and reliability of deployment pipelines including:

Ensures Stable Deployments: By introducing a systematic step between CI and CD, it ensures that only qualified artifacts progress through the pipeline, reducing the risk of faulty deployments

Improves Deployment Flexibility: Supports progressive rollouts and phased releases across multiple environments.

Reduces CI Pipeline Complexity: Reduces the burden on CI pipelines, which are often overloaded with deployment tasks they weren't designed to handle. This separation of concerns allows more focused and efficient CI processes, while CD can concentrate on deployment and management of applications.

Automates Decision-Making: Incorporates predefined rules for approvals and compliance checks, minimizing manual intervention.

Overall, continuous promotion aligns better with the dynamic nature of modern cloud native environments, facilitating smoother and more reliable application rollouts.

Kargo: Bringing Continuous Promotion to Life
Kargo is an open source tool designed to implement the concept of continuous promotion within CI/CD pipelines. It addresses the complexities associated with deploying applications in a Kubernetes and GitOps environment by providing a structured mechanism for promoting changes.

Kargo operates by monitoring changes to artifacts, such as application images or configuration files, and applying predefined promotion rules to determine if these artifacts should progress to the next stage of deployment. This tool effectively bridges the gap between CI and CD by introducing a declarative framework for managing promotions, ensuring that only vetted changes are deployed.

Kargo does not replace existing CI or CD tools but enhances them by adding an intermediary layer that focuses on orchestrating promotion of artifacts. By doing so, it helps facilitate more reliable and efficient deployment processes, reducing the manual effort needed to manage complex deployments and aligning better with the asynchronous nature of cloud native ecosystems.

How Kargo Optimizes CI/CD Pipelines
Kargo facilitates continuous promotion by serving as an intermediary that orchestrates the promotion of artifacts within the CI/CD pipeline. It operates by continuously monitoring changes in the repository, such as updates to code, configurations or Docker images.

Based on predefined rules and conditions, Kargo evaluates whether these changes meet the criteria for promotion. This evaluation considers factors such as successful test results, compliance checks and necessary manual approvals. Once the conditions are satisfied, Kargo automates the promotion process, updating the GitOps repository to reflect the new state and triggering deployments through GitOps controllers like Argo CD.




This approach minimizes the risk of deploying unverified changes, ensuring a higher level of deployment reliability and efficiency. By utilizing Kargo, teams can reduce manual interventions and streamline their deployment processes, allowing CI tools to focus on building artifacts while CD tools manage the rollout. This integration makes Kargo a vital component in modern, dynamic deployment environments.

Start your Continuous Promotion Journey Today
Are you a GitOps practitioner ready to try out Kargo? Head over to the Kargo GitHub page, where you can start your continuous promotion journey. Already a Kargo user and want to take it to the next level? Sign up for our Kargo Enterprise free trial.

*This article was originally published on The New Stack.

Additional Resources
Interested in learning more about Kargo? To get the most out of your learning journey, check out these resources:

[Blog Post] Why Continuous Promotion is Essential

[Blog Post] Promotion Made Easy with Kargo: Kargo for Beginners

Check out our Kargo Documentation!

Kargo GA Webinar:


Ready to simplify delivery with Akuity?
Deploy, promote, and operate applications reliably, powered by OSS you trust and Intelligence you control.

Request a Demo
Try it for free
Sign Up for Akuity Updates

Practical guidance on MTTR reduction, GitOps at scale, and safe automation, with product updates from the Argo CD and Kargo team.



