# Authenticated but unauthorized users may enumerate Application names via the API

- **GHSA:** [GHSA-2q5c-qw9c-fmvq](https://github.com/argoproj/argo-cd/security/advisories/GHSA-2q5c-qw9c-fmvq)
- **CVE:** CVE-2022-41354
- **Severity:** medium
- **Published:** 2023-03-23T15:34:01Z

## Description

### Impact

All versions of Argo CD starting with v0.5.0 are vulnerable to an information disclosure bug allowing unauthorized users to enumerate application names by inspecting API error messages. An attacker could use the discovered application names as the starting point of another attack. For example, the attacker might use their knowledge of an application name to convince an administrator to grant higher privileges (social engineering).

Many Argo CD API endpoints accept an application name as the only parameter. Since Argo CD RBAC requires both the application name and its configured project name (and, if apps-in-any-namespace is enabled, the application's namespace), Argo CD fetches the requested application before performing the RBAC check. If the application does not exist, the API returns a "not found". If the application does exist, and the user does not have access, the API returns an "unauthorized" error. By trial and error, an attacker can infer which applications exist and which do not.

Note that application resources are not fetched for API calls from _unauthenticated_ users. If your Argo CD instance is accessible from the public internet, unauthenticated users will not be able to cause Argo CD to make Kubernetes API calls.

The patch changes API behavior to return "unauthorized" both when the application is missing and when the user is not authorized to access it. **This change in API behavior may impact API clients.** Check your code to make sure it will handle the new API behavior properly.

### Patches

A patch for this vulnerability has been released in the following Argo CD versions:

* v2.6.7
* v2.5.16
* v2.4.28

### Workarounds

There are no workarounds besides upgrading.

### Credits

Thank you to bean.zhang of HIT-IDS ChunkL Team who discovered the issue and reported it confidentially according to our [guidelines](https://github.com/argoproj/argo-cd/blob/master/SECURITY.md#reporting-a-vulnerability).

### For more information

* Open an issue in [the Argo CD issue tracker](https://github.com/argoproj/argo-cd/issues) or [discussions](https://github.com/argoproj/argo-cd/discussions)
* Join us on [Slack](https://argoproj.github.io/community/join-slack) in channel #argo-cd


## Affected Versions

| Package | Vulnerable Range | Patched |
|---------|-----------------|---------|
| github.com/argoproj/argo-cd | 0.5.0 through 2.4.27, 2.5.17, 2.6.6 | 2.4.28, 2.5.16, 2.6.7 |
