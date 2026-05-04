# Argo CD leaked secret data into error messages and logs on invalid edits via UI

- **GHSA:** [GHSA-fp89-h8pj-8894](https://github.com/argoproj/argo-cd/security/advisories/GHSA-fp89-h8pj-8894)
- **CVE:** CVE-2021-23135
- **Severity:** medium
- **Published:** 2021-03-15T21:27:43Z

## Description

### Impact

When a user with `update` permissions to an Application was editing a `Secret` resources's manifest in the UI with invalid input (e.g. adding a new key with a value not encoded in base64), Argo CD would print the contents of the `Secret` as an error message in JSON format. 

As this error message is user visible, this was effectively circumventing the redaction feature of Argo CD. Also, as this error message is being logged, the plain-text contents of the `Secret` ended up in the log files and possibly, in log management systems.

### Patches

Patches for this issue have been released with the `v1.7.14` and `v1.8.7` versions of Argo CD.

### Workarounds

No workaround available.

### References

N/A

### For more information

If you have any questions or comments about this advisory:

* Open an issue in [the Argo CD issue tracker](https://github.com/argoproj/argo-cd/issues) or [discussions](https://github.com/argoproj/argo-cd/discussions)
* Join us on [Slack](https://argoproj.github.io/community/join-slack) in channel `#argo-cd`

### Credits

This vulnerability was found & reported by Ezekiel Keator and and Kevin Haung of Palo Alto Networks.

The Argo CD team would like to thank these contributors for their responsible disclosure and constructive communications during the resolve of this issue

## Affected Versions

| Package | Vulnerable Range | Patched |
|---------|-----------------|---------|
| Argo CD | All versions prior to 1.7.14 and 1.8.7 | 1.7.14, 1.8.7 |
