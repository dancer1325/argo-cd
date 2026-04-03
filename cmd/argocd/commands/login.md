# `func NewLoginCommand(globalClientOpts *argocdclient.ClientOptions) *cobra.Command {`
* `argocd login SERVER [FLAG]`
  * log in | Argo CD
  * `FLAG`
    * `--name string`
      * Name to use for the context
    * `--username string`
      * username of an account to authenticate
    * `--password string`
      * The password of an account to authenticate
    * `--sso`
      * Perform SSO login
    * `--sso-port int`
      * Port to run local OAuth2 login application
    * `--callback string`
      * Scheme, Host and Port for the callback URL
    * `--skip-test-tls`
      * Skip testing whether the server is configured with TLS (this can help when the command hangs for no apparent reason)
    * `--sso-launch-browser`
      * Automatically launch the system default browser when performing SSO login (default true)

* _Examples:_ 

	```
	# Login to Argo CD using a username and password
	argocd login cd.argoproj.io
	
	# Login to Argo CD using SSO
	argocd login cd.argoproj.io --sso
	
	# Configure direct access using Kubernetes API server
	argocd login cd.argoproj.io --core
	```

