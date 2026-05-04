# Secret values are not scrubbed from patch errors

- **GHSA:** [GHSA-47g2-qmh2-749v](https://github.com/argoproj/argo-cd/security/advisories/GHSA-47g2-qmh2-749v)
- **CVE:** CVE-2025-23216
- **Severity:** medium
- **Published:** 2025-01-30T13:27:52Z

## Description

### Impact

A vulnerability was discovered in Argo CD that exposed secret values in error messages and the diff view when an invalid Kubernetes Secret resource was synced from a repository. 

The vulnerability assumes the user has write access to the repository and can exploit it, either intentionally or unintentionally, by committing an invalid Secret to repository and triggering a Sync. Once exploited, any user with read access to Argo CD can view the exposed secret data.

### Patches
A patch for this vulnerability is available in the following Argo CD versions:
- v2.13.4
- v2.12.10
- v2.11.13

### Workarounds
There is no workaround other than upgrading.

### References
Fixed with commit https://github.com/argoproj/argo-cd/commit/6f5537bdf15ddbaa0f27a1a678632ff0743e4107 & https://github.com/argoproj/gitops-engine/commit/7e21b91e9d0f64104c8a661f3f390c5e6d73ddca


## Affected Versions

| Package | Vulnerable Range | Patched |
|---------|-----------------|---------|
| github.com/argoproj/argo-cd | <=v2.13.3, <=v2.12.9, <=v2.11.12 | v2.13.4, v2.12.10, v2.11.13 |
