# TODO:
TODO:

# Configure TLS -- for -- Argocd-server
## check the CURRENT ACTIVE one
* `kubectl run tls-check --rm -it --image=alpine -n argocd`
  * `apk add --no-cache openssl`
  * `openssl s_client -connect argocd-server:443 </dev/null 2>&1 | grep -iE 'Protocol|Cipher'`
    * check the returned protocol TLS
## TODO:
TODO:


# TODO:
TODO:
