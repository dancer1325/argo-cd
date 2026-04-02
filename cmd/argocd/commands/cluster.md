# `func NewClusterCommand(clientOpts *argocdclient.ClientOptions, pathOpts *clientcmd.PathOptions) *cobra.Command {`
* `argocd cluster [COMMAND]`
  * allows
    * manage cluster credentials
  * `COMMAND`
    * NewClusterAddCommand(clientOpts, pathOpts)
    * NewClusterGetCommand(clientOpts)
    * NewClusterListCommand(clientOpts)
    * NewClusterRemoveCommand(clientOpts, pathOpts)
    * NewClusterRotateAuthCommand(clientOpts)
    * NewClusterSetCommand(clientOpts)

* _Example:_ 

	```
	# List all known clusters in JSON format:
	argocd cluster list -o json
	
	# requirements: "example-cluster" context MUST exist | your kubectl config
 	# | ArgoCD, add a target cluster configuration 
	argocd cluster add example-cluster
	
	# Get specific details about a cluster in plain text (wide) format:
	argocd cluster get example-cluster -o wide
	
	# Remove a target cluster context from ArgoCD
	argocd cluster rm example-cluster
	
	# Set a target cluster context from ArgoCD
	argocd cluster set CLUSTER_NAME --name new-cluster-name --namespace '*'
	argocd cluster set CLUSTER_NAME --name new-cluster-name --namespace namespace-one --namespace namespace-two
	```

## `func NewClusterAddCommand(clientOpts *argocdclient.ClientOptions, pathOpts *clientcmd.PathOptions) *cobra.Command {`
* `argocd cluster add CONTEXT [FLAG]`
  * `FLAG`
    * `--upsert`
      * Override an existing cluster with the same name even if the spec differs
    * `--service-account`
      * System namespace service account to use for kubernetes resource management
      * If not set then default `argocd-manager` SA will be created
    * `--system-namespace`
      * Use different system namespace
    * `--yes`/`-y`
      * Skip explicit confirmation
    * `--label`
      * Set metadata labels (e.g. --label key=value)
    * `--annotation`
      * Set metadata annotations (e.g. --annotation key=value)
    * `--proxy-url`
      * use proxy to connect cluster

## `func NewClusterSetCommand(clientOpts *argocdclient.ClientOptions) *cobra.Command {`
* `argocd cluster set NAME [FLAG]`
  * set cluster information
  * `FLAG`
    * `--name`
      * Overwrite the cluster name
    * `--namespace`
      * List of namespaces which are allowed to manage. Specify `*` to manage all namespaces
    * `--label`
      * Set metadata labels (e.g. --label key=value)
    * `--annotation`
      * Set metadata annotations (e.g. --annotation key=value)

* _Examples:_ 
    ```
    # Set cluster information
    argocd cluster set CLUSTER_NAME --name new-cluster-name --namespace '*'
    argocd cluster set CLUSTER_NAME --name new-cluster-name --namespace namespace-one --namespace namespace-two
    ```

## `func NewClusterGetCommand(clientOpts *argocdclient.ClientOptions) *cobra.Command {`
* `argocd cluster get SERVER/NAME [FLAG]`
  * Get cluster information
  * `FLAG`
    * `--output`/`-o`
      * Output format. One of: `json`|`yaml`|`wide`|`server`

* _Examples:_ 
    ```
    argocd cluster get https://12.34.567.89
    argocd cluster get in-cluster
    ```


## `func NewClusterRemoveCommand(clientOpts *argocdclient.ClientOptions, pathOpts *clientcmd.PathOptions) *cobra.Command {`
* `argocd cluster rm SERVER/NAME [FLAG]`
  * remove cluster credentials
  * `FLAG`
    * `--yes`/`-y`
      * Turn off prompting to confirm remove of cluster resources

* _Examples:_ 
    ```
    argocd cluster rm https://12.34.567.89
    argocd cluster rm cluster-name
    ```

## `func NewClusterListCommand(clientOpts *argocdclient.ClientOptions) *cobra.Command {`
* `argocd cluster list [FLAG]`
  * list configured clusters
  * `FLAG`
    * `--output`/`-o`
      * Output format. One of: `json`|`yaml`|`wide`|`server`

* _Examples:_

	```
	# List Clusters in Default "Wide" Format
	argocd cluster list
	
	# List Cluster via specifying the server
	argocd cluster list --server <ARGOCD_SERVER_ADDRESS>
	
	# List Clusters in JSON Format
	argocd cluster list -o json --server <ARGOCD_SERVER_ADDRESS>
	
	# List Clusters in YAML Format
	argocd cluster list -o yaml --server <ARGOCD_SERVER_ADDRESS>
	
	# List Clusters that have been added to your Argo CD
	argocd cluster list -o server <ARGOCD_SERVER_ADDRESS>
	```

## `func NewClusterRotateAuthCommand(clientOpts *argocdclient.ClientOptions) *cobra.Command {`
* `argocd cluster rotate-auth SERVER/NAME`

* _Examples:_
    ```
    argocd cluster rotate-auth https://12.34.567.89
    argocd cluster rotate-auth cluster-name
    ```
