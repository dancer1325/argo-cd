* 👀events | you can subscribe👀
  * / EACH Argo CD application
  * | ALL ArgoCD project's applications

## subscribe | 1 Argo CD application events 

* steps
  * | "Application.yaml",
    * add `notifications.argoproj.io/subscribe.<triggerName>.<notificationServiceName>: <recipientListCommaSeparated>` annotation
      * _Examples:_ `notifications.argoproj.io/subscribe.on-sync-succeeded.slack: my-channel1;my-channel2`

## subscribe | ALL ArgoCD project's applications

* ways to subscribe
  * OPTION1
    * | "AppProject.yaml"
      * add `notifications.argoproj.io/subscribe.<triggerName>.<notificationServiceName>: <recipientListCommaSeparated>` annotation
        * _Examples:_ `notifications.argoproj.io/subscribe.on-sync-succeeded.slack: my-channel1;my-channel2`
  * OPTION2,
    * | "argocd-notifications-cm" ConfigMap,
      * configure `data.subscriptions`
        * by default, apply | ALL applications
