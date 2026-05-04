# Denial of Service via malicious jqPathExpressions in ignoreDifferences

- **GHSA:** [GHSA-9m6p-x4h2-6frq](https://github.com/argoproj/argo-cd/security/advisories/GHSA-9m6p-x4h2-6frq)
- **CVE:** CVE-2024-32476
- **Severity:** medium
- **Published:** 2024-04-26T14:21:17Z

## Description

### Impact
DoS vuln via OOM using jq in ignoreDifferences.

```
ignoreDifferences:
    - group: apps
       kind: Deployment
       jqPathExpressions: 
	    - 'until(true == false; [.] + [1])'
```

### Patches
A patch for this vulnerability has been released in the following Argo CD versions:

v2.10.8
v2.9.13
v2.8.17

### For more information
If you have any questions or comments about this advisory:

Open an issue in [the Argo CD issue tracker](https://github.com/argoproj/argo-cd/issues) or [discussions](https://github.com/argoproj/argo-cd/discussions)
Join us on [Slack](https://argoproj.github.io/community/join-slack) in channel #argo-cd

Credits
This vulnerability was found & reported by @crenshaw-dev (Michael Crenshaw)

The Argo team would like to thank these contributors for their responsible disclosure and constructive communications during the resolve of this issue


## Affected Versions

| Package | Vulnerable Range | Patched |
|---------|-----------------|---------|
|  | v2.1.0 | v2.10.8, v2.9.13, v2.8.17 |
