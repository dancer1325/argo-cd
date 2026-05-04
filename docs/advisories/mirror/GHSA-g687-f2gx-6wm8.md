# Denial of Service to Argo CD repo-server 

- **GHSA:** [GHSA-g687-f2gx-6wm8](https://github.com/argoproj/argo-cd/security/advisories/GHSA-g687-f2gx-6wm8)
- **CVE:** CVE-2023-40584
- **Severity:** medium
- **Published:** 2023-09-07T18:54:37Z

## Description

### Impact
All versions of ArgoCD starting from v2.4 have a bug where the ArgoCD repo-server component is vulnerable to a Denial-of-Service attack vector. Specifically, the said component extracts a user-controlled tar.gz file without validating the size of its inner files. As a result, a malicious, low-privileged user can send a malicious tar.gz file that exploits this vulnerability to the repo-server, thereby harming the system's functionality and availability. Additionally, the repo-server is susceptible to another vulnerability due to the fact that it does not check the extracted file permissions before attempting to delete them. Consequently, an attacker can craft a malicious tar.gz archive in a way that prevents the deletion of its inner files when the manifest generation process is completed.


### Patches
A patch for this vulnerability has been released in the following Argo CD versions:

* v2.6.15
* v2.7.14
* v2.8.3

### Workarounds
The only way to completely resolve the issue is to upgrade.

#### Mitigations
Configure RBAC (Role-Based Access Control) and provide access for configuring applications only to a limited number of administrators. These administrators should utilize trusted and verified Helm charts.

### For more information
If you have any questions or comments about this advisory:
* Open an issue in [the Argo CD issue tracker](https://github.com/argoproj/argo-cd/issues) or [discussions](https://github.com/argoproj/argo-cd/discussions)
* Join us on [Slack](https://argoproj.github.io/community/join-slack) in channel #argo-cd

### Credits
This vulnerability was found & reported by GE Vernova – Amit Laish.

The Argo team would like to thank these contributors for their responsible disclosure and constructive communications during the resolve of this issue


## Affected Versions

| Package | Vulnerable Range | Patched |
|---------|-----------------|---------|
| github.com/argoproj/argo-cd | > v2.4 | v2.6.15, 2.7.14, 2.8.3 |
