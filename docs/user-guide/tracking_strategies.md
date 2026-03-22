# Tracking and Deployment Strategies

TODO: why tracking & deployment at same time?

* Argo CD application spec
  * provides
    * MULTIPLE ways of tracking Kubernetes resource manifests

* tracking strategies
  * can [auto-sync](auto_sync.md)
  * any [parameter overrides](parameters.md)'s priority > Git state's priority
  * -- depend on -- ALLOWED Argo CD's Application `spec.source.repoURL`   ==
    * [Helm repo](#helm)
    * [Git repo](#git)

## Helm

* Helm chart 
  * follow [Semantic Versions](https://semver.org/) -- MAJOR.MINOR.PATCH -- 
    * -> MULTIPLE ways to specify the version

| Use Case                                                 | How                          | Examples                    |
|----------------------------------------------------------|------------------------------|-----------------------------|
| Pin -- to a -- version   (_Example:_ production)         | Use the version number       | `1.2.0`                     |
| Track patches            (_Example:_ pre-production)     | Use a range                  | `1.2.*` OR `>=1.2.0 <1.3.0` |
| Track minor releases     (_Example:_ QA)                 | Use a range                  | `1.*` or `>=1.0.0 <2.0.0`   |
| Use the latest           (_Example:_ local development)  | Use star range               | `*` or `>=0.0.0`            |
| Use the latest / INCLUDING pre-releases                  | Use star range / `-0` suffix | `*-0` or `>=0.0.0-0`        |

* `-0`
  * == prerelease versions 
  * ALLOWED ALSO | NOT latest 
    * _Example:_ `>=1.2.2-0`
  * [MORE](https://github.com/Masterminds/semver?tab=readme-ov-file#working-with-prerelease-versions)

## Git

* Git
  * ALLOWED
    * Git references
    * tags [Semantic Versions](https://semver.org/)

| Use Case                                               | How                                   | Examples                         | Notes                                             |
|--------------------------------------------------------|---------------------------------------|----------------------------------|---------------------------------------------------|
| Pin -- to a -- version  (_Example:_ production)        | Use tag OR commit SHA                 | `v1.2.0` OR `1a2b3c4`            | [commit pinning](#commit-pinning)                 |
| Track patches           (_Example:_ pre-production)    | Use a range                           | `1.2.*` OR `>=1.2.0 <1.3.0`      | [tag tracking](#tag-tracking)                     |
| Track minor releases    (_Example:_ QA)                | Use a range                           | `1.*` OR `>=1.0.0 <2.0.0`        | [tag tracking](#tag-tracking)                     |
| Use the latest          (_Example:_ local development) | Use `HEAD` or your master branch name | `HEAD` OR `master` OR `main`     | [HEAD / Branch Tracking](#head-branch-tracking)   |
| Use the latest including pre-releases                  | Use star range / `-0` suffix          | `*-0` OR `>=0.0.0-0`             | [tag tracking](#tag-tracking)                     |


### HEAD / Branch Tracking

If a branch name or a symbolic reference (like HEAD) is specified, Argo CD will continually compare
live state against the resource manifests defined at the tip of the specified branch or the
resolved commit of the symbolic reference.

To redeploy an app, make a change to (at least) one of your manifests, commit and push to the tracked branch/symbolic reference
* The change will then be detected by Argo CD.

### Tag Tracking

If a tag is specified, the manifests at the specified Git tag will be used to perform the sync
comparison
* This provides some advantages over branch tracking in that a tag is generally considered
more stable, and less frequently updated, with some manual judgement of what constitutes a tag.

To redeploy an app, the user uses Git to change the meaning of a tag by retagging it to a
different commit SHA
* Argo CD will detect the new meaning of the tag when performing the
comparison/sync.

But if you're using semantic versioning you can set the constraint in your service revision
and Argo CD will get the latest version following the constraint rules.

### Commit Pinning

* == specify a Git commit SHA
  * -> ❌desired state does NOT change❌
    * Reason:🧠commit SHAs content can NOT change🧠
* allow
  * pin -- to the -- manifests / defined | specified commit
* use cases
  * production environments

* TODO: Note that [parameter overrides](parameters.md) can still be set
on an app which is pinned to a revision.

### Handling Ambiguous Git References in Argo CD

When deploying applications, Argo CD relies on the `targetRevision` field to determine
which revision of the Git repository to use
* This can be a branch, tag, or commit SHA.
Sometimes, multiple Git references can have the same name (eg. a branch and a tag both named `release-1.0`).
These ambiguous references can lead to unexpected behavior, such as constant reconciliation loops.

Today, Argo CD fetches all branches and tags from the repository
* If the `targetRevision` matches multiple references, Argo CD
attempts to resolve it and may select a different commit than expected
* For example, suppose your repository has the following references:

```text
refs/heads/release-1.0 -> commit B
refs/tags/release-1.0  -> commit A
```

In the above scenario, `release-1.0` refers to both a branch (pointing to commit B) and a tag (pointing to commit A)
* 
If your application's `targetRevision` is set to `release-1.0`, Argo CD may resolve it to either commit A or commit B.
If the resolved commit differs from what is currently deployed, Argo CD will continuously attempt to sync, causing constant
reconciliation
* In order to avoid this ambiguity, you can follow these best practices:

1. Use fully-qualified Git references in the `targetRevision` field
   * For example, use `refs/heads/release-1.0` for branches
      and `refs/tags/release-1.0` for tags.
2. Avoid using the same name for branches and tags in your Git repository.
