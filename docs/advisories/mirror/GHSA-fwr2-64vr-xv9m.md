# Cluster secret might leak in cluster details page

- **GHSA:** [GHSA-fwr2-64vr-xv9m](https://github.com/argoproj/argo-cd/security/advisories/GHSA-fwr2-64vr-xv9m)
- **CVE:** CVE-2023-40029
- **Severity:** critical
- **Published:** 2023-09-07T18:54:21Z

## Description

### Impact

Argo CD Cluster secrets might be managed declaratively using Argo CD / kubectl apply. As a result, the full secret body is stored in`kubectl.kubernetes.io/last-applied-configuration` annotation. 

https://github.com/argoproj/argo-cd/pull/7139 introduced the ability to manage cluster labels and annotations. Since clusters are stored as secrets it also exposes the `kubectl.kubernetes.io/last-applied-configuration` annotation which includes full secret body. In order to view the cluster annotations via the Argo CD API, the user must have `clusters, get` RBAC access.

**Note:** In many cases, cluster secrets do not contain any actually-secret information. But sometimes, as in bearer-token auth, the contents might be very sensitive.

### Patches

The bug has been patched in the following versions:

* 2.8.3
* 2.7.14
* 2.6.15

### Workarounds

Update/Deploy cluster secret with `server-side-apply` flag which does not use or rely on `kubectl.kubernetes.io/last-applied-configuration` annotation. Note: annotation for existing secrets will require manual removal.

### For more information

* Open an issue in [the Argo CD issue tracker](https://github.com/argoproj/argo-cd/issues) or [discussions](https://github.com/argoproj/argo-cd/discussions)
* Join us on [Slack](https://argoproj.github.io/community/join-slack) in channel #argo-cd

## Affected Versions

| Package | Vulnerable Range | Patched |
|---------|-----------------|---------|
| github.com/argoproj/argo-cd | 2.2.0 through 2.6.14, 2.7.113, 2.8.2 | 2.8.2, 2.7.14, 2.6.15 |
