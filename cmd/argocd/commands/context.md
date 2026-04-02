# `func NewContextCommand(clientOpts *argocdclient.ClientOptions) *cobra.Command {`
* `argocd context [CONTEXT]` OR `argocd ctx`
  * allows
    * list BETWEEN contexts
    * switch to -- ANOTHER -- context
    * delete context

  command.Flags().BoolVar(&deletion, "delete", false, "Delete the context instead of switching to it")

* _Examples:_ 
	```
	# List Argo CD Contexts
	argocd context
	
	# Switch Argo CD context
	argocd context cd.argoproj.io
	
	# Delete Argo CD context
	argocd context cd.argoproj.io --delete
	```