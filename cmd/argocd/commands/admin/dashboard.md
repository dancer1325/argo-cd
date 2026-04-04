# `func NewDashboardCommand(clientOpts *argocdclient.ClientOptions) *cobra.Command {`
* `argocd admin dashboard [FLAG]`
  * Starts Argo CD Web UI locally
  * `FLAG`
    * `--port`
      * type: int
      * default: `common.DefaultPortAPIServer`
      * listen | given port
    * `--address`
      * type: string
      * default: `common.DefaultAddressAdminDashboard`
      * listen | given address

* _Examples:_

	```
	# Start the Argo CD Web UI locally | default port & address
	$ argocd admin dashboard
	
	# Start the Argo CD Web UI locally | custom port & address
	$ argocd admin dashboard --port 8080 --address 127.0.0.1
	
	# Start the Argo CD Web UI with GZip compression
	$ argocd admin dashboard --redis-compress gzip
	```
