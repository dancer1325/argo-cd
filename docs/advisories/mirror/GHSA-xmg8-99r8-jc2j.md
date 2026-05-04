# Login screen allows message spoofing if SSO is enabled

- **GHSA:** [GHSA-xmg8-99r8-jc2j](https://github.com/argoproj/argo-cd/security/advisories/GHSA-xmg8-99r8-jc2j)
- **CVE:** CVE-2022-24905
- **Severity:** low
- **Published:** 2022-05-18T13:08:28Z

## Description

### Impact

A vulnerability was found in Argo CD that allows an attacker to spoof error messages on the login screen when SSO is enabled.

In order to exploit this vulnerability, an attacker would have to trick the victim to visit a specially crafted URL which contains the message to be displayed.

As far as the research of the Argo CD team concluded, it is not possible to specify any active content (e.g. Javascript) or other HTML fragments (e.g. clickable links) in the spoofed message.

### Patched versions

A patch for this vulnerability has been released in the following Argo CD versions:

* v2.3.4
* v2.2.9
* v2.1.15

### Workarounds

No workaround available.

#### Mitigations

It is advised to update to an Argo CD version containing a fix for this issue (see *Patched versions* above).

### Credits

This vulnerability was discovered by Naufal Septiadi (<naufal@horangi.com>) and reported to us in a responsible way. 

### For more information

<!-- Use only one of the paragraphs below. Remove all others. -->

<!-- For Argo CD -->

* Open an issue in [the Argo CD issue tracker](https://github.com/argoproj/argo-cd/issues) or [discussions](https://github.com/argoproj/argo-cd/discussions)
* Join us on [Slack](https://argoproj.github.io/community/join-slack) in channel #argo-cd


## Affected Versions

| Package | Vulnerable Range | Patched |
|---------|-----------------|---------|
| github.com/argoproj/argo-cd | 0.6.1 through 2.1.14, 2.2.8, 2.3.3 | 2.3.4, 2.2.9, 2.1.15 |
