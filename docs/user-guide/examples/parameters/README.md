TODO: clean

```bash
argocd app set guestbook -p image=example/guestbook:abcd123
argocd app sync guestbook
```

```bash
argocd app set guestbook -p ingress.enabled=true
argocd app set guestbook -p ingress.hosts[0]=guestbook.myclusterurl
```

# use cases
## dev/test environments / needs to be CONTINUALLY updated
* _Example:_ [Helm chart microservices](https://github.com/dancer1325/argocd-example-apps/tree/master/helm-guestbook)

## use public Helm charts

```bash
# customize Redis password
# -p  password=abc123
argocd app create redis --repo https://github.com/helm/charts.git --path stable/redis --dest-server https://kubernetes.default.svc --dest-namespace default -p password=abc123
```

# | MULTI-Source Applications

```bash
argocd app set my-app --source-position 1 -p replicaCount=2
```


