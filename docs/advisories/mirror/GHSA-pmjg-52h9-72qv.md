# A leaked API server encryption key can allow XSS for SSO users

- **GHSA:** [GHSA-pmjg-52h9-72qv](https://github.com/argoproj/argo-cd/security/advisories/GHSA-pmjg-52h9-72qv)
- **CVE:** CVE-2022-31102
- **Severity:** low
- **Published:** 2022-07-12T16:24:44Z

## Description

### Impact

All versions of Argo CD starting with 2.3.0 are vulnerable to a cross-site scripting (XSS) bug which could allow an attacker to inject arbitrary JavaScript in the `/auth/callback` page in a victim's browser. 

This vulnerability only affects Argo CD instances which have SSO enabled.

The exploit also assumes the attacker has 1) access to the API server's encryption key, 2) a method to add a cookie to the victim's browser, and 3) the ability to convince the victim to visit a malicious `/auth/callback` link.

The vulnerability is classified as low severity, because access to the API server's encryption key already grants a high level of access. Exploiting the XSS would allow the attacker to impersonate the victim, but would not grant any privileges which the attacker could not otherwise gain using the encryption key.

### Patches

A patch for this vulnerability has been released in the following Argo CD versions:

* v2.4.5
* v2.3.6

### Workarounds

There is no workaround besides upgrading.

### Credits

Disclosed by ADA Logics in a security audit of the Argo project sponsored by CNCF and facilitated by OSTIF. Thanks to Adam Korczynski and David Korczynski for their work on the audit.

### For more information

* Open an issue in [the Argo CD issue tracker](https://github.com/argoproj/argo-cd/issues) or [discussions](https://github.com/argoproj/argo-cd/discussions)
* Join us on [Slack](https://argoproj.github.io/community/join-slack) in channel #argo-cd


## Affected Versions

| Package | Vulnerable Range | Patched |
|---------|-----------------|---------|
| github.com/argoproj/argo-cd | 2.3.0 through 2.3.5, 2.4.4 | 2.3.6, 2.4.5 |
