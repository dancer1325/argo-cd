# Users with `create` but not `override` privileges can perform local sync

- **GHSA:** [GHSA-g623-jcgg-mhmm](https://github.com/argoproj/argo-cd/security/advisories/GHSA-g623-jcgg-mhmm)
- **CVE:** CVE-2023-50726
- **Severity:** medium
- **Published:** 2024-03-13T20:11:33Z

## Description

### Impact

"Local sync" is an Argo CD feature that allows developers to temporarily override an Application's manifests with locally-defined manifests. Use of the feature should generally be limited to highly-trusted users, since it allows the user to bypass any merge protections in git.

An improper validation bug allows users who have `create` privileges but not `override` privileges to sync local manifests on app creation. All other restrictions, including AppProject restrictions are still enforced. The only restriction which is _not_ enforced is that the manifests come from some approved git/Helm/OCI source.

The bug was introduced in 1.2.0-rc1 when the local manifest sync feature was added.

### Patches

The bug has been patched in the following versions:

* 2.10.3
* 2.9.8
* 2.8.12

### Workarounds

To immediately mitigate the risk of branch protection bypass, remove `applications, create` RBAC access. The only way to eliminate the issue without removing RBAC access is to upgrade to a patched version.

Branch protection rules and review requirements are a great way to enforce security constraints in a GitOps environment, but they should be just one layer in a multi-layered approach. Make sure your AppProject and RBAC restrictions are as thorough as possible to prevent a review bypass vulnerability from permitting excessive damage.

### References

* [Argo CD RBAC documentation](https://argo-cd.readthedocs.io/en/latest/operator-manual/rbac/)

### For more information

* Open an issue in [the Argo CD issue tracker](https://github.com/argoproj/argo-cd/issues) or [discussions](https://github.com/argoproj/argo-cd/discussions)
* Join us on [Slack](https://argoproj.github.io/community/join-slack) in channel #argo-cd

## Affected Versions

| Package | Vulnerable Range | Patched |
|---------|-----------------|---------|
| github.com/argoproj/argo-cd | 1.2.0-rc1 through 2.10.2, 2.9.7, 2.8.11 | 2.10.3, 2.9.8, and 2.8.12 |
