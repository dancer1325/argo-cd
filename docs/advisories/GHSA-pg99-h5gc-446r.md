# Missing XSS Protection Header

- **GHSA:** [GHSA-pg99-h5gc-446r](https://github.com/argoproj/argo-cd/security/advisories/GHSA-pg99-h5gc-446r)
- **CVE:** CVE-2021-26924
- **Severity:** low
- **Published:** 2021-03-02T19:34:07Z

## Description

### Impact

Missing XSS Protection Header puts the Argo CD UI at risk of a cross-site scripting attack (XSS). This should only impact users who are using legacy browsers, such as Internet Explorer.

### Fixes

Argo CD from version `1.7.12` and `1.8.4` are now properly setting the `X-XSS-Protection` header to support better protection in legacy browsers.

### Workarounds

N/A

### References

* https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/X-XSS-Protection

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
