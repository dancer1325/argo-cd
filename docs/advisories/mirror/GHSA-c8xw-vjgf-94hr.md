# Web terminal session doesn't expire

- **GHSA:** [GHSA-c8xw-vjgf-94hr](https://github.com/argoproj/argo-cd/security/advisories/GHSA-c8xw-vjgf-94hr)
- **CVE:** CVE-2023-40025
- **Severity:** medium
- **Published:** 2023-08-23T14:10:47Z

## Description

### Impact
All versions of Argo CD starting from v2.6.0 have a bug where open web terminal sessions do not expire. This bug allows users to send any websocket messages even if the token has already expired. The most straightforward scenario is when a user opens the terminal view and leaves it open for an extended period. This allows the user to view sensitive information even when they should have been logged out already.

### Patches
A patch for this vulnerability has been released in the following Argo CD version:

* v2.6.14
* v2.7.12
* v2.8.1

### Workarounds
The only way to completely resolve the issue is to upgrade.

#### Mitigations
Disable web-based terminal or define RBAC rules to it
[https://argo-cd.readthedocs.io/en/latest/operator-manual/web_based_terminal/](https://argo-cd.readthedocs.io/en/latest/operator-manual/web_based_terminal/)

### For more information
If you have any questions or comments about this advisory:
* Open an issue in [the Argo CD issue tracker](https://github.com/argoproj/argo-cd/issues) or [discussions](https://github.com/argoproj/argo-cd/discussions)
* Join us on [Slack](https://argoproj.github.io/community/join-slack) in channel #argo-cd

### Credits

Thank you to bean.zhang (@zhlu32 ) of HIT-IDS ChunkL Team who discovered the issue and reported it confidentially according to our [guidelines](https://github.com/argoproj/argo-cd/blob/master/SECURITY.md#reporting-a-vulnerability).

## Affected Versions

| Package | Vulnerable Range | Patched |
|---------|-----------------|---------|
| github.com/argoproj/argo-cd | 2.6.0 through 2.6.13, 2.7.11, 2.8.0 | 2.6.14, 2.7.12, 2.8.1 |
