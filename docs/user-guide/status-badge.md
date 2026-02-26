# Status Badge

* badge for any application /
  * display
    * health
    * sync status
  * by default, disabled
    * Reason: 🧠 badge image is available to ANY user WITHOUT authentication 🧠
  * `statusbadge.enabled` | [ArgoCd ConfigMap](../operator-manual/argocd-cm.yaml)
  * `${argoCdBaseUrl}/api/badge?name=${appName}`
    * URL syntax to access the status badge
    * _Example:_ http://localhost:8080/api/badge?name=guestbook
    * if you want to override the `${argoCdBaseUrl}` value -> use `argocd-cm` configMap's `statusbadge.url` key 
  * steps to get it
    * | your browser, argoCD
      * application details page > click | 'Details' button
      * 'Status Badge' section
      * Select required template
        * _Example:_ as URL, Markdown etc. 
    * Copy the text and paste it into your README or website.

        ![healthy and synced](../assets/status-badge-healthy-synced.png)

## Additional query parameters options
### showAppName
Display the application name in the status badge.   

Available values: `true/false`

Default value: `false`

Example: `&showAppName=true`

### revision
* revision targeted -- by the -- application
* extend the badge width = 192px
* ALLOWED values
  * `true`
  * `false`
    * by default
* _Example:_ `&revision=true`
* | MULTIPLE sources setup,
  * display ALSO the revision of first defined source

### keepFullRevision
By default, displayed  revision is truncated to 7 characters.

This parameter allows to display it fully if it exceeds that length.

It will also extend the badge width to 400px.

Available values: `true/false`

Default value: `false`

Example: `&keepFullRevision=true`

### width
* Change width of the badge.
  * Completely replace current calculated width.
* Available values: `integer`
* Default value: `nil`
* _Example:_ `&width=500`