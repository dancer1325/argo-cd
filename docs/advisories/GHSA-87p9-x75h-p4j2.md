# Unauthenticated Access to sensitive settings in Argo CD

- **GHSA:** [GHSA-87p9-x75h-p4j2](https://github.com/argoproj/argo-cd/security/advisories/GHSA-87p9-x75h-p4j2)
- **CVE:** CVE-2024-37152
- **Severity:** medium
- **Published:** 2024-06-06T09:55:45Z

## Description

# Summary
The CVE allows unauthorized access to the sensitive settings exposed by  /api/v1/settings endpoint without authentication. 

# Details
## **Unauthenticated Access:**

### Endpoint: /api/v1/settings
Description: This endpoint is accessible without any form of authentication as expected. All sensitive settings are hidden except `passwordPattern`. 

Patches
A patch for this vulnerability has been released in the following Argo CD versions:

v2.11.3
v2.10.12
v2.9.17


# Impact
## Unauthenticated Access:

* Type: Unauthorized Information Disclosure.
* Affected Parties: All users and administrators of the Argo CD instance.
* Potential Risks: Exposure of sensitive configuration data, including but not limited to deployment settings, security configurations, and internal network information.



## Affected Versions

| Package | Vulnerable Range | Patched |
|---------|-----------------|---------|
| argo-cd/server | v2.9.3+6eba5be | 2.11.3, 2.10.12, 2.9.17 |
