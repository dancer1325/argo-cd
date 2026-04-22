# `func NewProjectCommand(clientOpts *argocdclient.ClientOptions) *cobra.Command {`
* `argocd proj <COMMAND>` OR `argocd project <COMMAND>`
  * `COMMAND`
    * NewProjectRoleCommand(clientOpts)
    * NewProjectCreateCommand(clientOpts)
    * NewProjectGetCommand(clientOpts)
    * NewProjectDeleteCommand(clientOpts)
    * NewProjectListCommand(clientOpts)
    * NewProjectSetCommand(clientOpts)
    * NewProjectEditCommand(clientOpts)
    * NewProjectAddSignatureKeyCommand(clientOpts)
    * NewProjectRemoveSignatureKeyCommand(clientOpts)
    * NewProjectAddDestinationCommand(clientOpts)
    * NewProjectRemoveDestinationCommand(clientOpts)
    * NewProjectAddSourceCommand(clientOpts)
    * NewProjectRemoveSourceCommand(clientOpts)
    * NewProjectAllowClusterResourceCommand(clientOpts)
    * NewProjectDenyClusterResourceCommand(clientOpts)
    * NewProjectAllowNamespaceResourceCommand(clientOpts)
    * NewProjectDenyNamespaceResourceCommand(clientOpts)
    * NewProjectWindowsCommand(clientOpts)
    * NewProjectAddOrphanedIgnoreCommand(clientOpts)
    * NewProjectRemoveOrphanedIgnoreCommand(clientOpts)
    * NewProjectAddSourceNamespace(clientOpts)
    * NewProjectRemoveSourceNamespace(clientOpts)
    * NewProjectAddDestinationServiceAccountCommand(clientOpts)
    * NewProjectRemoveDestinationServiceAccountCommand(clientOpts)

## `func NewProjectCreateCommand(clientOpts *argocdclient.ClientOptions) *cobra.Command {`
* `argocd proj create [FLAG]`
  * `[FLAG]`
    * `-f` / `--file`
      * Filename OR URL -- to -- Kubernetes project manifest
    * `--upsert`
      * by default, `false`
      * if you supply a project / ALREADY exist -> override the project
* create a project
* _Example:_
	```
	# Create a new project with name PROJECT
	argocd proj create PROJECT
	
	# Create a new project with name PROJECT from a file or URL to a Kubernetes manifest
	argocd proj create PROJECT -f FILE|URL
	```


## `func NewProjectSetCommand(clientOpts *argocdclient.ClientOptions) *cobra.Command {`
* `argocd proj set`
* Set project parameters
* _Example:_
	```
	# Set project parameters with some allowed cluster resources [RES1,RES2,...] for project with name PROJECT
	argocd proj set PROJECT --allow-cluster-resource [RES1,RES2,...]
	
	# Set project parameters with some denied namespaced resources [RES1,RES2,...] for project with name PROJECT
	argocd proj set PROJECT ---deny-namespaced-resource [RES1,RES2,...]
	```



## `func NewProjectAddSignatureKeyCommand(clientOpts *argocdclient.ClientOptions) *cobra.Command {`
* `argocd proj add-signature-key` 
* Add GnuPG signature key | project
* _Example:_
	```
	# Add GnuPG signature key KEY-ID to project PROJECT
	argocd proj add-signature-key PROJECT KEY-ID
	```


## `func NewProjectRemoveSignatureKeyCommand(clientOpts *argocdclient.ClientOptions) *cobra.Command {`
* `argocd proj remove-signature-key`
* Remove project's GnuPG signature key
* _Example:_
	```
	# Remove GnuPG signature key KEY-ID from project PROJECT
	argocd proj remove-signature-key PROJECT KEY-ID
	```

## `func NewProjectAddDestinationCommand(clientOpts *argocdclient.ClientOptions) *cobra.Command {`
* `argocd proj add-destination [FLAG]`
  * `[FLAG]`
    * `--name trueOrFalse`
      * by default, `false`
      * if `true` -> use name -- as -- destination
        * instead of sever
* Add project destination
* _Example:_
	```
	# Add project destination using a server URL (SERVER) in the specified namespace (NAMESPACE) on the project with name PROJECT
	argocd proj add-destination PROJECT SERVER NAMESPACE
	
	# Add project destination using a server name (NAME) in the specified namespace (NAMESPACE) on the project with name PROJECT
	argocd proj add-destination PROJECT NAME NAMESPACE --name
	```

## `func NewProjectRemoveDestinationCommand(clientOpts *argocdclient.ClientOptions) *cobra.Command {`
* `argocd proj remove-destination`
* _Example:_
	```
	# Remove the destination (SERVER) from the specified namespace (NAMESPACE) on the project with name PROJECT
	argocd proj remove-destination PROJECT SERVER NAMESPACE
	```
* Remove project destination

## `func NewProjectAddOrphanedIgnoreCommand(clientOpts *argocdclient.ClientOptions) *cobra.Command {`
* `argocd proj add-orphaned-ignore [FLAG]`
  * `[FLAG]`
    * `--name ResourceNamePattern`
* Add a resource | orphaned ignore list
* _Examples:_
	```
	# Add a resource of the specified GROUP and KIND to orphaned ignore list on the project with name PROJECT
	argocd proj add-orphaned-ignore PROJECT GROUP KIND
	
	# Add resources of the specified GROUP and KIND using a NAME pattern to orphaned ignore list on the project with name PROJECT
	argocd proj add-orphaned-ignore PROJECT GROUP KIND --name NAME
	```


## `func NewProjectRemoveOrphanedIgnoreCommand(clientOpts *argocdclient.ClientOptions) *cobra.Command {`
* `argocd proj remove-orphaned-ignore [FLAG]`
  * `[FLAG]`
    * `--name ResourceNamePattern`
* Remove a resource -- from -- orphaned ignore list
* _Examples:_
	```
	# Remove a resource of the specified GROUP and KIND from orphaned ignore list on the project with name PROJECT
	argocd proj remove-orphaned-ignore PROJECT GROUP KIND
	
	# Remove resources of the specified GROUP and KIND using a NAME pattern from orphaned ignore list on the project with name PROJECT
	argocd proj remove-orphaned-ignore PROJECT GROUP KIND --name NAME
	```


## `func NewProjectAddSourceCommand(clientOpts *argocdclient.ClientOptions) *cobra.Command {`
* `argocd proj add-source PROJECT URL`
* Add project source repository 
* _Example:_ 
	```
	# Add a source repository (URL) to the project with name PROJECT
	argocd proj add-source PROJECT URL
	```

## `func NewProjectAddSourceNamespace(clientOpts *argocdclient.ClientOptions) *cobra.Command {`
* `argocd proj add-source-namespace`
* Add AppProject's source namespace
* _Example:_
	```
	# Add Kubernetes namespace as source namespace to the AppProject where application resources are allowed to be created in.
	argocd proj add-source-namespace PROJECT NAMESPACE
	```

## `func NewProjectRemoveSourceNamespace(clientOpts *argocdclient.ClientOptions) *cobra.Command {`
* `argocd proj remove-source-namespace`
* Removes the AppProject's source namespace
* _Example:_
	```
	# Remove source NAMESPACE in PROJECT 
	argocd proj remove-source-namespace PROJECT NAMESPACE
	```



func modifyResourceListCmd(getProjIf func(*cobra.Command) (io.Closer, projectpkg.ProjectServiceClient), cmdUse, cmdDesc, examples string, allow bool, namespacedList bool) *cobra.Command {
	var (
		listType    string
		defaultList string
	)
	if namespacedList {
		defaultList = "deny"
	} else {
		defaultList = "allow"
	}
	command := &cobra.Command{
		Use:     cmdUse,
		Short:   cmdDesc,
		Example: templates.Examples(examples),
		Run: func(c *cobra.Command, args []string) {
			ctx := c.Context()

			if namespacedList && len(args) != 3 {
				c.HelpFunc()(c, args)
				os.Exit(1)
			}

			if !namespacedList && (len(args) < 3 || len(args) > 4) {
				// Cluster-scoped resource command can have an optional NAME argument.
				c.HelpFunc()(c, args)
				os.Exit(1)
			}

			projName, group, kind := args[0], args[1], args[2]
			var name string
			if !namespacedList && len(args) > 3 {
				name = args[3]
			}
			conn, projIf := getProjIf(c)
			defer utilio.Close(conn)

			proj, err := projIf.Get(ctx, &projectpkg.ProjectQuery{Name: projName})
			errors.CheckError(err)
			var list, allowList, denyList *[]metav1.GroupKind
			var clusterList *[]v1alpha1.ClusterResourceRestrictionItem
			var clusterAllowList, clusterDenyList *[]v1alpha1.ClusterResourceRestrictionItem
			var listAction string
			var add bool
			if namespacedList {
				allowList, denyList = &proj.Spec.NamespaceResourceWhitelist, &proj.Spec.NamespaceResourceBlacklist
			} else {
				clusterAllowList, clusterDenyList = &proj.Spec.ClusterResourceWhitelist, &proj.Spec.ClusterResourceBlacklist
			}

			if (listType == "allow") || (listType == "white") {
				list = allowList
				clusterList = clusterAllowList
				listAction = "allowed"
				add = allow
			} else {
				list = denyList
				clusterList = clusterDenyList
				listAction = "denied"
				add = !allow
			}

			if !namespacedList {
				if ok, msg := modifyClusterResourcesList(clusterList, add, listAction, group, kind, name); ok {
					c.Println(msg)
					_, err = projIf.Update(ctx, &projectpkg.ProjectUpdateRequest{Project: proj})
					errors.CheckError(err)
				}
				return
			}

			if ok, msg := modifyNamespacedResourcesList(list, add, listAction, group, kind); ok {
				c.Println(msg)
				_, err = projIf.Update(ctx, &projectpkg.ProjectUpdateRequest{Project: proj})
				errors.CheckError(err)
			}
		},
	}
	command.Flags().StringVarP(&listType, "list", "l", defaultList, "Use deny list or allow list. This can only be 'allow' or 'deny'")
	return command
}


## `func NewProjectAllowNamespaceResourceCommand(clientOpts *argocdclient.ClientOptions) *cobra.Command {`
* `argocd proj allow-namespace-resource PROJECT GROUP KIND [FLAG]`
  * `[FLAG]`
    * `--list` / `-l`
      * == defaultList
      * deny list or allow list
* Removes a namespaced API resource | deny list OR add a namespaced API resource | allow list
* _Example:_
	```
	# Removes a namespaced API resource with specified GROUP and KIND from the deny list or add a namespaced API resource to the allow list for project PROJECT
	argocd proj allow-namespace-resource PROJECT GROUP KIND
	```


## `func NewProjectDenyNamespaceResourceCommand(clientOpts *argocdclient.ClientOptions) *cobra.Command {`
* `argocd proj deny-namespace-resource PROJECT GROUP KIND [FLAG]`
  * `[FLAG]`
    * `--list` / `-l`
      * == defaultList
      * deny list or allow list
* Adds a namespaced API resource | deny list OR removes a namespaced API resource | allow list 
* _Example:_
	```
	# Adds a namespaced API resource with specified GROUP and KIND from the deny list or removes a namespaced API resource from the allow list for project PROJECT
	argocd proj deny-namespace-resource PROJECT GROUP KIND
	```


## `func NewProjectDenyClusterResourceCommand(clientOpts *argocdclient.ClientOptions) *cobra.Command {`
* `argocd proj deny-cluster-resource` 
	use := "deny-cluster-resource PROJECT GROUP KIND"
	desc := "Removes a cluster-scoped API resource from the allow list and adds it to deny list"
	examples := `
	# Removes a cluster-scoped API resource with specified GROUP and KIND from the allow list and adds it to deny list for project PROJECT
	argocd proj deny-cluster-resource PROJECT GROUP KIND
	`
	getProjIf := func(cmd *cobra.Command) (io.Closer, projectpkg.ProjectServiceClient) {
		return headless.NewClientOrDie(clientOpts, cmd).NewProjectClientOrDie()
	}
	return modifyResourceListCmd(getProjIf, use, desc, examples, false, false)
}


## `func NewProjectAllowClusterResourceCommand(clientOpts *argocdclient.ClientOptions) *cobra.Command {`
* `argocd proj allow-cluster-resource`
	use := "allow-cluster-resource PROJECT GROUP KIND [NAME]"
	desc := "Adds a cluster-scoped API resource to the allow list and removes it from deny list"
	examples := `
	# Adds a cluster-scoped API resource with specified GROUP and KIND to the allow list and removes it from deny list for project PROJECT
	argocd proj allow-cluster-resource PROJECT GROUP KIND

	# Adds a cluster-scoped API resource with specified GROUP, KIND and NAME pattern to the allow list and removes it from deny list for project PROJECT
	argocd proj allow-cluster-resource PROJECT GROUP KIND NAME
	`
	getProjIf := func(cmd *cobra.Command) (io.Closer, projectpkg.ProjectServiceClient) {
		return headless.NewClientOrDie(clientOpts, cmd).NewProjectClientOrDie()
	}
	return modifyResourceListCmd(getProjIf, use, desc, examples, true, false)
}


## `func NewProjectRemoveSourceCommand(clientOpts *argocdclient.ClientOptions) *cobra.Command {`
* `argocd proj remove-source PROJECT URL`
* Remove project source repository
* _Example:_
```
# Remove URL source repository to project PROJECT
argocd proj remove-source PROJECT URL
```
	

## `func NewProjectDeleteCommand(clientOpts *argocdclient.ClientOptions) *cobra.Command {`
* `argocd proj delete`
* Delete project
* _Example:_
	```
	# Delete the project with name PROJECT
	argocd proj delete PROJECT
	```

## `func NewProjectListCommand(clientOpts *argocdclient.ClientOptions) *cobra.Command {`
* `argocd proj list [FLAG]`
  * `[FLAG]`
    * `-o` / `--output`
      * ALLOWED values: json|yaml|wide
* list projects
* _Example:_ 
```
# List all available projects
argocd proj list

# List all available projects in yaml format (other options are "json" and "name")
argocd proj list -o yaml
```

## `func NewProjectGetCommand(clientOpts *argocdclient.ClientOptions) *cobra.Command {`
* `argocd proj get [FLAG]`
  * `[FLAG]`
    * `-o` / `--output`
      * ALLOWED values: json|yaml|wide
* get project details
* _Example:_
	```
	# Get details from project PROJECT
	argocd proj get PROJECT
	
	# Get details from project PROJECT in yaml format
	argocd proj get PROJECT -o yaml
	```

## `func NewProjectEditCommand(clientOpts *argocdclient.ClientOptions) *cobra.Command {`
* `argocd proj edit PROJECT`
* edit project
* _Example:_
	```
	# Edit the information on project with name PROJECT
	argocd proj edit PROJECT
	```

## `func NewProjectAddDestinationServiceAccountCommand(clientOpts *argocdclient.ClientOptions) *cobra.Command {`
* `argocd proj add-destination-service-account`
* add project destination's default service account
* _Example:_ 
	```
	# Add project destination service account (SERVICE_ACCOUNT) for a server URL (SERVER) in the specified namespace (NAMESPACE) on the project with name PROJECT
	argocd proj add-destination-service-account PROJECT SERVER NAMESPACE SERVICE_ACCOUNT
	
	# Add project destination service account (SERVICE_ACCOUNT) from a different namespace
	argocd proj add-destination PROJECT SERVER NAMESPACE SERVICE_ACCOUNT --service-account-namespace <service_account_namespace>
	```

## `func NewProjectRemoveDestinationServiceAccountCommand(clientOpts *argocdclient.ClientOptions) *cobra.Command {`
* `argocd proj remove-destination-service-account`
  * remove project's default destination service account 
* _Examples:_
	```
	# Remove the destination service account (SERVICE_ACCOUNT) from the specified destination (SERVER and NAMESPACE combination) on the project with name PROJECT
	argocd proj remove-destination-service-account PROJECT SERVER NAMESPACE SERVICE_ACCOUNT
	```