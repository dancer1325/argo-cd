# Unlimited validity of admin JWT

- **GHSA:** [GHSA-9h6w-j7w4-jr52](https://github.com/argoproj/argo-cd/security/advisories/GHSA-9h6w-j7w4-jr52)
- **CVE:** CVE-2021-26921
- **Severity:** critical
- **Published:** 2021-03-02T19:33:49Z

## Description

### Impact

JWT Tokens which were issued via interactive password logins, were able to be used indefinitely, even if the account was subsequently disabled.

### Impacted users and versions

All Argo CD versions prior to `1.7.12` and `1.8.4` where the admin or local users are or have been enabled with interactive password login are impacted by this issue.

### Fixes

When authenticating the token from local users (including admin), the authentication process will now check if the account is disabled, or if login privileges have been removed, before authenticating the request.

The fix for this issue is included in releases `1.7.12` and `1.8.4` Argo CD, respectively.

### Workarounds

* Change the password of the admin/local user. Changing the password revokes all tokens for that user which were issued prior to the  password change, even if those tokens had not yet reached expiration. This can be changed to the same password (if the actual password is desired to remain the same), and it will still invalidate previously issued tokens.
* Disable the admin account if it is not needed
* Disable interactive login capability of local users if interactive password login is not needed

### References

* Argo CD user management docs: https://argo-cd.readthedocs.io/en/stable/operator-manual/user-management/

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
