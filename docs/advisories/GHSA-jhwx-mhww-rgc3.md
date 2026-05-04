# Uncontrolled Resource Consumption vulnerability in ArgoCD's repo server

- **GHSA:** [GHSA-jhwx-mhww-rgc3](https://github.com/argoproj/argo-cd/security/advisories/GHSA-jhwx-mhww-rgc3)
- **CVE:** CVE-2024-29893
- **Severity:** medium
- **Published:** 2024-03-28T20:32:52Z

## Description

### Impact
All versions of ArgoCD starting from v2.4 have a bug where the ArgoCD repo-server component is vulnerable to a Denial-of-Service attack vector. Specifically,  it's possible to crash the repo server component through an out of memory error by pointing it to a malicious Helm registry.
The loadRepoIndex() function in the ArgoCD's helm package, does not limit the size nor time while fetching the data. It fetches it and creates a byte slice from the retrieved data in one go. If the registry is implemented to push data continuously, the repo server will keep allocating memory until it runs out of it.

### Patches
A patch for this vulnerability has been released in the following Argo CD versions:

v2.10.5
v2.9.10
v2.8.14

### For more information
If you have any questions or comments about this advisory:

Open an issue in [the Argo CD issue tracker](https://github.com/argoproj/argo-cd/issues) or [discussions](https://github.com/argoproj/argo-cd/discussions)
Join us on [Slack](https://argoproj.github.io/community/join-slack) in channel #argo-cd


### Credits
This vulnerability was found & reported by Jakub Ciolek

The Argo team would like to thank these contributors for their responsible disclosure and constructive communications during the resolve of this issue

## Affected Versions

| Package | Vulnerable Range | Patched |
|---------|-----------------|---------|
| github.com/argoproj/argo-cd | > v2.4 | v2.10.5, v2.9.10, v2.8.14 |
