* notification services 
  * == 💡integration -- with -- [services](#service-types)💡
  * how to configure?
    * | "argocd-notifications-cm" ConfigMap,
      * add
        * key == `data.service.<type>.(<custom-name>)`
          * `(<custom-name>)`
            * OPTIONAL
            * [here](#custom-names)
        * value could refer -- to -- "argocd-notifications-secret" Secret entries
    * _Examples:_ [here](../examples/argocd-notifications-cm.yaml)

## Sensitive Data

* _Example of sensitive data:_ authentication tokens

* if it's stored | `<secret-name>` secret & you want to interpolate -> use `$<secret-key>`
  * _Example:_ [secret](../examples/argocd-notifications-secret.yaml) & [configMap](../examples/argocd-notifications-cm.yaml)

## Custom Names

* allows
  * configuring MULTIPLE instances -- of the -- SAME service type

* _Examples:_
  * _Example1:_ [here](../examples/argocd-notifications-cm.yaml)
  * _Example2:_

    ```yaml
      service.slack.workspace1: |
        token: $slack-token-workspace1
      service.slack.workspace2: |
        token: $slack-token-workspace2
    ```

    ```yaml
    apiVersion: argoproj.io/v1alpha1
    kind: Application
    metadata:
      annotations:
        notifications.argoproj.io/subscribe.on-sync-succeeded.workspace1: my-channel
        notifications.argoproj.io/subscribe.on-sync-succeeded.workspace2: my-channel
    ```

## Service Types

* [AwsSqs](./awssqs.md)
* [Email](./email.md)
* [GitHub](./github.md)
* [Slack](./slack.md)
* [Mattermost](./mattermost.md)
* [Opsgenie](./opsgenie.md)
* [Grafana](./grafana.md)
* [Webhook](./webhook.md)
* [Telegram](./telegram.md)
* [Teams (Office 365 Connectors)](./teams.md)
  * Legacy service
    * replace -- by -- [Teams Workflows](teams-workflows.md)
  * | March 31, 2026, retires 
* [Teams Workflows](./teams-workflows.md)
* [Google Chat](./googlechat.md)
* [Rocket.Chat](./rocketchat.md)
* [Pushover](./pushover.md)
* [Alertmanager](./alertmanager.md)