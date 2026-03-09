### Application-Specific Policy

* [application-specific-policy.csv](application-specific-policy.csv)
  * `p, <role/user/group>, <resource>, <action>, <object>, <effect>`  
    * `<object>` == `<app-project>/<app-name>`

#### | ANY Namespaces

* [application-specific-policy-any-namespace.csv](application-specific-policy-any-namespace.csv)
  * `p, <role/user/group>, <resource>, <action>, <object>, <effect>`
    * `<object>` == `<app-project>/<app-ns>/<app-name>`