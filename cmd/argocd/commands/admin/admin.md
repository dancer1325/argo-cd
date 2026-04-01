# `func NewAdminCommand(clientOpts *argocdclient.ClientOptions) *cobra.Command {`
* 's return
  * NEW `argocd` command instance
* `argocd admin COMMAND`
  * requirements
    * direct Kubernetes access
  * audience
    * Argo CD administrators
  * AVAILABLE `COMMAND`
    * NewClusterCommand(clientOpts, pathOpts)
    * NewProjectsCommand()
    * NewSettingsCommand()
    * NewAppCommand(clientOpts)
    * NewRepoCommand()
    * NewImportCommand()
    * NewExportCommand()
    * NewDashboardCommand(clientOpts)
    * NewNotificationsCommand()
    * NewInitialPasswordCommand()
    * NewRedisInitialPasswordCommand()
* _Examples:_
	```
	# Access the Argo CD web UI
	$ argocd admin dashboard
	
	# Reset the initial admin password
	$ argocd admin initial-password reset
	```
