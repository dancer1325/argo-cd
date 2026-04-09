# API Docs

* | your Argo CD UI,
  * "/swagger-ui"
    * _Example:_ http://localhost:8080/swagger-ui

## Authorization

* steps
  * get a token

    ```bash
    # if you use HTTPS
    $ curl -k -H "Content-Type: application/json" $ARGOCD_SERVER/api/v1/session -d $'{"username":"admin","password":"password"}'
    
    # if you use HTTP
    $ curl -H "Content-Type: application/json" $ARGOCD_SERVER/api/v1/session -d $'{"username":"admin","password":"password"}'
    {"token":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpYXQiOjE1Njc4MTIzODcsImlzcyI6ImFyZ29jZCIsIm5iZiI6MTU2NzgxMjM4Nywic3ViIjoiYWRtaW4ifQ.ejyTgFxLhuY9mOBtKhcnvobg3QZXJ4_RusN_KIdVwao"}
    ```
  * | ANY AFTER call, use this JWT

    ```bash
    $ curl $ARGOCD_SERVER/api/v1/applications -H "Authorization: Bearer $ARGOCD_TOKEN" 
    {"metadata":{"selfLink":"/apis/argoproj.io/v1alpha1/namespaces/argocd/applications","resourceVersion":"37755"},"items":...}
    ```

## Services

### Applications API -- "/api/v1/applications/*" --

* | ALL endpoints,
  * `project`
    * query string parameter
      * OPTIONAL

#### if the applications do NOT exist 
  
* if you specify the `project` & the specified Application
  * does NOT exist -> the API returns a `404` error
  * does NOT exist | that `project` -> the API returns a `403` error
