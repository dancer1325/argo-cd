* goal
  * | Argo CD Application's `on-sync-succeeded`,
    * configure an email notification

# steps
* steps
  * [install Catalog's Triggers & Templates](../../catalog.md#how-to-install)
  * | "argocd-notifications-secret" Secret,
    * add email username & password token

      ```bash
      EMAIL_USER=<your-username>
      PASSWORD=<your-password>
      
      kubectl apply -n argocd -f - << EOF
      apiVersion: v1
      kind: Secret
      metadata:
      name: argocd-notifications-secret
      stringData:
      email-username: $EMAIL_USER
      email-password: $PASSWORD
      type: Opaque
      EOF
      ```
  * | "argocd-notifications-cm",
    * register email notification service

        ```bash
        kubectl patch cm argocd-notifications-cm -n argocd --type merge -p '{"data": {"service.email.gmail": "{ username: $email-username, password: $email-password, host: smtp.gmail.com, port: 465, from: $email-username }" }}'
        ```

  * | Argo CD application OR ArgoCD project,
    * add `notifications.argoproj.io/subscribe.on-sync-succeeded.slack` annotation
        ```bash
        kubectl patch app <my-app> -n argocd -p '{"metadata": {"annotations": {"notifications.argoproj.io/subscribe.on-sync-succeeded.slack":"<my-channel>"}}}' --type merge
        ```
  * sync the ArgoCD Application
    * check email notified