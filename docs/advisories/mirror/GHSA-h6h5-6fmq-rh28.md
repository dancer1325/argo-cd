# Path traversal allows leaking out-of-bound files from Argo CD repo-server

- **GHSA:** [GHSA-h6h5-6fmq-rh28](https://github.com/argoproj/argo-cd/security/advisories/GHSA-h6h5-6fmq-rh28)
- **CVE:** CVE-2022-24731
- **Severity:** medium
- **Published:** 2022-03-23T13:38:40Z

## Description

### Impact

All unpatched versions of Argo CD starting with v1.5.0 are vulnerable to a path traversal vulnerability allowing a malicious user with read/write access to leak sensitive files from Argo CD's repo-server.

A malicious Argo CD user who has been granted [`create` or `update` access to Applications](https://argo-cd.readthedocs.io/en/stable/operator-manual/rbac/#rbac-resources-and-actions) can leak the contents of any text file on the repo-server. By crafting a malicious Helm chart and using it in an Application, the attacker can retrieve the sensitive file's contents either as part of the generated manifests or in an error message. The attacker would have to know or guess the location of the target file.

Sensitive files which could be leaked include files from other Application's source repositories (potentially decrypted files, if you are using a decryption plugin) or any secrets which have been mounted as files on the repo-server.

### Patches

A patch for this vulnerability has been released in the following Argo CD versions:

* v2.3.0
* v2.2.6
* v2.1.11

### Workarounds

The only certain way to avoid the vulnerability is to upgrade. 

To mitigate the problem, you can 
* avoid storing secrets in git
* avoid mounting secrets as files on the repo-server
* avoid decrypting secrets into files on the repo-server
* carefully [limit who can `create` or `update` Applications](https://argo-cd.readthedocs.io/en/stable/operator-manual/rbac/#rbac-resources-and-actions)

### References

* [Security documentation for the repo-server component](https://argo-cd.readthedocs.io/en/stable/operator-manual/security/#git-helm-repositories)
* [Argo CD RBAC configuration documentation](https://argo-cd.readthedocs.io/en/stable/operator-manual/rbac/#)

### For more information

Open an issue in [the Argo CD issue tracker](https://github.com/argoproj/argo-cd/issues) or [discussions](https://github.com/argoproj/argo-cd/discussions)
Join us on [Slack](https://argoproj.github.io/community/join-slack) in channel #argo-cd


## Affected Versions

| Package | Vulnerable Range | Patched |
|---------|-----------------|---------|
| github.com/argoproj/argo-cd | 1.5.0 through 2.1.10, 2.2.5, 2.3.0-rc5 | 2.1.11, 2.2.6, 2.3.0 |
