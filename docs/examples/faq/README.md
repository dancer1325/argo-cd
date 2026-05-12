# TODO:

# How often does Argo CD check for changes | Git OR Helm repository ?
## MANUAL
### `argocd app get APPNAME --refresh`
TODO:
### UI
TODO: 
## Polling
TODO:
## Webhook
* [here](../../operator-manual/webhook.md)

# TODO:
TODO:

# how to rotate Redis secret?
* `kubectl get secret argocd-redis -n argocd -o jsonpath='{.data.auth}' | base64 -d`
  * check initial Redis admin password
* follow the steps
* `kubectl get secret argocd-redis -n argocd -o jsonpath='{.data.auth}' | base64 -d`
  * check AGAIN the initial Redis admin password / != ORIGINAL one

# TODO:
TODO:
