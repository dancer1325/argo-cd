# Security Considerations

https://github.com/argoproj/argo-cd/security

* goal
  * [security policy](https://github.com/argoproj/argo-cd/security/policy)
  * security advisories

* Argo CD
  * require
    * have production access
      * -> security is very important topic

## Security policy
### about security scanners

* security scanners
  * uses
    * validate their container images BEFORE letting them | their clusters
  * ⚠️cons⚠️
    * quality & results are NOT greatly
    * MANY produce FALSE positives
  * recommendation
    * ❌NOT use them -- to -- raise issues❌
  * used
    * INTERNALLY -- for -- ArgoCD code

### Supported Versions

* the last Argo CD's 3 minor versions 
  * == apply security fixes & bug fixes | last Argo CD's 3 minor versions 

* PRIOR last Argo CD's 3 minor versions
  * MIGHT receive critical security fixes
    * ❌ALTHOUGH it's NOT guaranteed❌

* RARELY
  * if a security fix needs COMPLEX re-design OR it's very intrusive & there's a workaround -> we should provide a forward-fix
    * Reason:🧠be released | the next minor release
      * != release | patch branch🧠

### Dependency Upgrade Policy

* binaries & libraries / Argo CD relies on
  * _Example:_ Helm, Kustomize, and git
  * ⚠️| SAME minor version, ONLY upgrade -- to -- NEW patch versions⚠️ 
    * Reason:🧠it may include breaking changes OR changes behavior🧠
    * _Example:_ if currently we use Helm 3.12.0 & have Argo CD 3.4.0 -> | Argo CD 3.4.x, ONLY upgrade to Helm 3.12.x 

TODO:
If there is a critical, exploitable vulnerability in a dependency that will not be fixed in a patch release,
we will evaluate the impact of the vulnerability and the risk of not upgrading the dependency
* We ask that, if you believe a version bump is justified, 
please open an issue describing how the vulnerability is exploitable in the context of Argo CD, and 
we will evaluate it and decide whether or not to upgrade the dependency.

### how to report vulnerabilities?

* [here](https://github.com/argoproj/argo-cd/security/advisories/new)

## Security Advisories

* [here](/docs/advisories)
