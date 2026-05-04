# Unprotected endpoint leaks deployment details

- **GHSA:** [GHSA-pfgj-mh5m-2p48](https://github.com/argoproj/argo-cd/security/advisories/GHSA-pfgj-mh5m-2p48)
- **CVE:** CVE-2021-26923
- **Severity:** medium
- **Published:** 2021-03-02T19:34:00Z

## Description

### Impact

Version endpoint is unauthenticated and returns version information about Argo CD, and underlying tooling

### Fixes

After reviewing the version endpoint, maintainers decided a minimal amount of information can be exposed when accessing the API with an unauthenticated request. The version of Argo CD is still exposed, but version of tooling will not.

The fix is included with the `1.7.12` and `1.8.4` releases of Argo CD.

### Workarounds

N/A

### References

N/A

### Notes

This is a known/understood behavior of Argo CD and exposing version information is desirable in some CI use cases where the correct version of the CLI needs to be downloaded to match the Argo CD version. Furthermore, placing the `/version` endpoint under an authenticated endpoint, would not enhance security. This is due to the fact that Argo CD version can be inferred in other, trivial ways, namely:

* Argo CD UI assets, which must be served publicly, also reveals the version of Argo CD based on the signature of the assets (e.g. javascript filenames), which are tied to the release.
* Argo CD additionally makes the argocd CLI binary available along with the UI assets. The version of Argo CD can be trivially inferred by downloading the binary and running `argocd version`, which will always match the version of the server.

### For more information

If you have any questions or comments about this advisory:

* Open an issue in [the Argo CD issue tracker](https://github.com/argoproj/argo-cd/issues) or [discussions](https://github.com/argoproj/argo-cd/discussions)
* Join us on [Slack](https://argoproj.github.io/community/join-slack) in channel `#argo-cd`

### Credits

This vulnerability was found & reported by SAP SE, T&I area, BTP Foundational Plane, K8S Delivery Team – Dimitar Kiryakov, Anatoli Krastev. 

The Argo team would like to thank these contributors for their responsible disclosure and constructive communications during the resolve of this issue

## Affected Versions

| Package | Vulnerable Range | Patched |
|---------|-----------------|---------|
| Argo CD | All versions prior to 1.7.12 and 1.8.4 | 1.7.12, 1.8.4 |
