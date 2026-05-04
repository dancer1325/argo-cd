# DoS via credentials updates triggering a race condition  that crashes the Argo CD server

- **GHSA:** [GHSA-g88p-r42r-ppp9](https://github.com/argoproj/argo-cd/security/advisories/GHSA-g88p-r42r-ppp9)
- **CVE:** CVE-2025-55191
- **Severity:** medium
- **Published:** 2025-09-30T16:58:44Z

## Description

### Summary

A race condition in the repository credentials handler can cause the Argo CD server to panic and crash when concurrent operations are performed on the same repository URL.

### Details
The vulnerability is located in numerous repository related handlers in the `util/db/repository_secrets.go` file. For example, in the `secretToRepoCred` function. The issue manifests as a concurrent map access panic:

```
concurrent map read and map write
...
goroutine 1104 [running]:
github.com/argoproj/argo-cd/v2/util/db.(*secretsRepositoryBackend).secretToRepoCred(0xc000e50ea8?, 0xc000c65540)
        /go/src/github.com/argoproj/argo-cd/util/db/repository_secrets.go:404 +0x31e
```

The race condition occurs due to:
1. Concurrent repository credential operations (create/update/delete) accessing the same map
2. Kubernetes informer re-syncs happening simultaneously
3. Background watchers updating the same secret data
4. No mutex protection for map access

A valid API token with `repositories` resource permissions (`create`, `update`, or `delete` actions) is required to trigger the race condition.

### Impact

This vulnerability causes the entire Argo CD server to crash and become unavailable. Attackers can repeatedly and continuously trigger the race condition to maintain a denial-of-service state, disrupting all GitOps operations. Default ArgoCD configuration is vulnerable.

The affected code was originally introduced in [PR #6103](https://github.com/argoproj/argo-cd/pull/6103) and released in [v2.1.0](https://github.com/argoproj/argo-cd/releases/tag/v2.1.0).

This data race was addressed by deep-copying the `Secret` objects before reading/writing.

### Credits

This vulnerability was found, reported and fixed by:

@thevilledev

The Argo team would like to thank him for his responsible disclosure and constructive communications during the resolve of this issue.

## Affected Versions

| Package | Vulnerable Range | Patched |
|---------|-----------------|---------|
| github.com/argoproj/argo-cd/v2 | 2.1.0 through 2.14.19 | 2.14.20 |
| github.com/argoproj/argo-cd/v3 | 3.0.0-rc1 through 3.2.0-rc1, 3.1.7, 3.0.18 | 3.2.0-rc2, 3.1.8, 3.0.19 |
