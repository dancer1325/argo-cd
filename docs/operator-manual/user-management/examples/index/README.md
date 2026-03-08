
## Local users/accounts

### Create new user
* TODO: use [argocd-cm.yaml](argocd-cm.yaml)

### Delete user
* `kubectl patch -n argocd cm argocd-cm --type='json' -p='[{"op": "remove", "path": "/data/accounts.alice"}]'`
  * remove the `argocd-cm` ConfigMap's entry `/data/accounts.alice`
* `kubectl patch -n argocd secrets argocd-secret --type='json' -p='[{"op": "remove", "path": "/data/accounts.alice.password"}]'`
  * remove the corresponding `argocd-secret` Secret's password entry

### Disable admin user
* TODO: use [argocd-cm.yaml](argocd-cm.yaml)