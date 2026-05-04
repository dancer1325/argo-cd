# API server does not enforce project sourceNamespaces

- **GHSA:** [GHSA-2gvw-w6fj-7m3c](https://github.com/argoproj/argo-cd/security/advisories/GHSA-2gvw-w6fj-7m3c)
- **CVE:** CVE-2024-31990
- **Severity:** medium
- **Published:** 2024-04-15T10:45:18Z

## Description

### Impact

I can convince the UI to let me do things with an invalid Application.
1. Admin gives me `p, michael, applications, *, demo/*, allow`, where `demo` can just deploy to the `demo` namespace
2. Admin gives me AppProject `dev` which reconciles from ns `dev-apps`
3. Admin gives me `p, michael, applications, sync, dev/*, allow`, i.e. no updating via the UI allowed, gitops-only
4. I create an Application called `pwn` in `dev-apps` with project dev and sync the app with sources from git
5. I change the Application’s project to demo via kubectl or gitops (whichever mechanism my admins have given me, because it should be safe)
6. I use the UI to edit the resource which should only be mutable via gitops

### Patches
A patch for this vulnerability has been released in the following Argo CD versions:

v2.10.7 
v2.9.12 
v2.8.16

### For more information
If you have any questions or comments about this advisory:

Open an issue in [the Argo CD issue tracker](https://github.com/argoproj/argo-cd/issues) or [discussions](https://github.com/argoproj/argo-cd/discussions)
Join us on [Slack](https://argoproj.github.io/community/join-slack) in channel #argo-cd

### Credits
This vulnerability was found & reported by @crenshaw-dev (Michael Crenshaw)

The Argo team would like to thank these contributors for their responsible disclosure and constructive communications during the resolve of this issue


## Affected Versions

| Package | Vulnerable Range | Patched |
|---------|-----------------|---------|
| argocd | > 2.4 | 2.10.7, 2.9.12, 2.8.16 |
