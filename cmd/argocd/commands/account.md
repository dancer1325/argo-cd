# `func NewAccountCommand(clientOpts *argocdclient.ClientOptions) *cobra.Command {`
* `argocd account COMMAND`
  * allows
    * managing account settings
  * AVAILABLE `COMMAND`
    * NewAccountUpdatePasswordCommand(clientOpts)
    * NewAccountGetUserInfoCommand(clientOpts)
    * NewAccountCanICommand(clientOpts)
    * NewAccountListCommand(clientOpts)
    * NewAccountGenerateTokenCommand(clientOpts)
    * NewAccountGetCommand(clientOpts)
    * NewAccountDeleteTokenCommand(clientOpts)
    * NewBcryptCmd()
* _Examples:_
	```
	# List accounts
	argocd account list
	
	# Update the current user's password
	argocd account update-password
	
	# Can I sync any app?
	argocd account can-i sync applications '*'
	
	# Get User information
	argocd account get-user-info
	```

# `func NewAccountUpdatePasswordCommand(clientOpts *argocdclient.ClientOptions) *cobra.Command {`
	var (
		account         string
		currentPassword string
		newPassword     string
	)
* `argocd account update-password`
  * allows
    * Update an account's password /
      * get a NEW JWT token

* _Examples:_
	```
	# Update the current user's password
	argocd account update-password
	
	# Update the password for user foobar
	argocd account update-password --account foobar
	```

# `func NewAccountGetUserInfoCommand(clientOpts *argocdclient.ClientOptions) *cobra.Command {`
	var output string
* `argocd account get-user-info -o AVAILABLE_OUTPUT` OR `argocd account whoami -o AVAILABLE_OUTPUT`
  * allows
    * Get user info
  * `AVAILABLE_OUTPUT`
	  * "yaml", "json"
	  * ""
        * == default one
* _Examples:_ 
	```
	# Get User information for the currently logged-in user (see 'argocd login')
	argocd account get-user-info
	
	# Get User information in yaml format
	argocd account get-user-info -o yaml
	```

# `func NewAccountCanICommand(clientOpts *argocdclient.ClientOptions) *cobra.Command {`
* `argocd account can-i ACTION RESOURCE SUBRESOURCE`
* _Examples:_ 
	```
	# Can I sync any app?
	argocd account can-i sync applications '*'
	
	# Can I update a project?
	argocd account can-i update projects 'default'
	
	# Can I create a cluster?
	argocd account can-i create clusters '*'
	
	Actions: %v
	Resources: %v
	```

# `func NewAccountListCommand(clientOpts *argocdclient.ClientOptions) *cobra.Command {`
* `argocd account list -o AVAILABLE_OUTPUT`
  * `AVAILABLE_OUTPUT`
    * "yaml", "json"
    * "name"
    * "wide", ""
      * == default one

# `func NewAccountGetCommand(clientOpts *argocdclient.ClientOptions) *cobra.Command {`
* `argocd account get -o AVAILABLE_OUTPUT`
  * Get account details
  * `AVAILABLE_OUTPUT`
    * "yaml", "json"
    * "name"
    * "wide", ""
      * == default one
* _Examples:_
	```
	# Get the currently logged in account details
	argocd account get
	
	# Get details for an account by name
	argocd account get --account <account-name>
	```

# `func NewAccountGenerateTokenCommand(clientOpts *argocdclient.ClientOptions) *cobra.Command {`
* `argocd account generate-token`
  * Generate account token
* _Examples:_
	```
	# Generate token for the currently logged in account
	argocd account generate-token
	
	# Generate token for the account with the specified name
	argocd account generate-token --account <account-name>
	```

# `func NewAccountDeleteTokenCommand(clientOpts *argocdclient.ClientOptions) *cobra.Command {`
* var account string
* `argocd account delete-token`
  * allows
    * deletes account token
* _Examples:_ 
	```
	# Delete token of the currently logged in account
	argocd account delete-token ID
	
	# Delete token of the account with the specified name
	argocd account delete-token --account <account-name> ID
	```