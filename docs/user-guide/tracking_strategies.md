# Tracking Strategies

* goal
  * how to track Kubernetes resource manifests

* Argo CD application tracking strategies
  * 👀-- depend on -- ALLOWED Argo CD's Application `spec.source.repoURL`👀   ==
    * [Helm repo](#helm)
    * [Git repo](#git)
  * 👀how to configure?👀
    * | Argo CD Application.yaml, 
      * specify `spec.source.targetRevision`

## Helm

* Helm chart 
  * follow [Semantic Versions](https://semver.org/) -- MAJOR.MINOR.PATCH -- 
    * -> MULTIPLE ways to specify the version
  * tracking strategies
    * how to configure?
      * | Argo CD Application.yaml,
        * specify `spec.source.targetRevision`
    * ALLOWED ones
      * next table

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
  * tracking strategies
    * how to configure?
      * | Argo CD Application.yaml, 
        * specify `spec.source.targetRevision`
    * ALLOWED ones
      * next table

| Use Case                                                                 | How                                   | Examples                         | Notes                                             |
|--------------------------------------------------------------------------|---------------------------------------|----------------------------------|---------------------------------------------------|
| Pin -- to a -- version                    (_Example:_ production)        | Use tag OR commit SHA                 | `v1.2.0` OR `1a2b3c4`            | [commit pinning](#commit-pinning)                 |
| Track patches                             (_Example:_ pre-production)    | Use a range                           | `1.2.*` OR `>=1.2.0 <1.3.0`      | [tag tracking](#tag-tracking)                     |
| Track minor releases                      (_Example:_ QA)                | Use a range                           | `1.*` OR `>=1.0.0 <2.0.0`        | [tag tracking](#tag-tracking)                     |
| Use the latest OR branch tracking         (_Example:_ local development) | Use `HEAD` or your master branch name | `HEAD` OR `master` OR `main`     | [HEAD / Branch Tracking](#head-branch-tracking)   |
| Use the latest including pre-releases                                    | Use star range / `-0` suffix          | `*-0` OR `>=0.0.0-0`             | [tag tracking](#tag-tracking)                     |

### HEAD / Branch Tracking

* `spec.source.targetRevision` == branch name OR symbolic reference (_Example:_ HEAD)
* anytime you push -> desired state changes

### Tag Tracking

* `spec.source.targetRevision` == tag name
* anytime you change the source code | tag -> desired state changes
  * change the source code | tag == retagging it | DIFFERENT commit SHA
* vs [HEAD / Branch Tracking](#head--branch-tracking)
  * 👀MORE stable == LESS frequently updated👀

### Commit Pinning

* `spec.source.targetRevision` == Git commit SHA
  * -> ❌desired state does NOT change❌
    * Reason:🧠commit SHAs content can NOT change🧠
    * if you want to change -> [override parameters](parameters.md) 
* allow
  * pin -- to the -- manifests / defined | specified commit
* use cases
  * production environments

### how to handle AMBIGUOUS Git references | Argo CD?

* use case
  * MULTIPLE Git references / have the SAME name
    * _Example:_ branch name _== tag name

* POSSIBLE PROBLEMS:
  * constant reconciliation loops

* recommendations
  * | Argo CD Application.yaml,
    * specify `spec.source.targetRevision` == [FULLY-qualified Git reference](https://git-scm.com/book/en/v2/Git-Internals-Git-References)
      * _ExampleS:_
        * `refs/heads/release-1.0` -- for -- branches
        * `refs/tags/release-1.0` -- for -- tags
  * | Git repository,
    * avoid branch name == tag name
