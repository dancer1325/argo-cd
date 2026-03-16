TODO: add prerequisites + clen steps

## build & publish a NEW container image
```bash
docker build -t mycompany/guestbook:v2.0 .
docker push mycompany/guestbook:v2.0
```

## update the local manifests -- via -- your preferred templating tool + push the changes | Git
```bash
git clone https://github.com/mycompany/guestbook-config.git
cd guestbook-config

# kustomize
kustomize edit set image mycompany/guestbook:v2.0

# plain yaml
kubectl patch --local -f config-deployment.yaml -p '{"spec":{"template":{"spec":{"containers":[{"name":"guestbook","image":"mycompany/guestbook:v2.0"}]}}}}' -o yaml > config-deployment.yaml

git commit -am "Update guestbook to v2.0"
git push
```