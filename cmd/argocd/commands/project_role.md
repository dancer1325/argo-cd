# `func NewProjectRoleCommand(clientOpts *argocdclient.ClientOptions) *cobra.Command {`
* `argocd proj role COMMAND`
  * manage a project's roles
  * `COMMAND`
    * ALLOWED
      * NewProjectRoleListCommand(clientOpts)
      * NewProjectRoleGetCommand(clientOpts)
      * NewProjectRoleCreateCommand(clientOpts)
      * NewProjectRoleDeleteCommand(clientOpts)
      * NewProjectRoleCreateTokenCommand(clientOpts)
      * NewProjectRoleListTokensCommand(clientOpts)
      * NewProjectRoleDeleteTokenCommand(clientOpts)
      * NewProjectRoleAddPolicyCommand(clientOpts)
      * NewProjectRoleRemovePolicyCommand(clientOpts)
      * NewProjectRoleAddGroupCommand(clientOpts)
      * NewProjectRoleRemoveGroupCommand(clientOpts)

## `func NewProjectRoleAddPolicyCommand(clientOpts *argocdclient.ClientOptions) *cobra.Command {`
* `argocd proj role add-policy PROJECT ROLE-NAME [FLAG]`
  * add a policy -- to a -- project role
  * `[FLAG]`
    * `-a` / `--action`
      * TODO:
    * `-p` / `--permission`
      * ALLOWED values: `allow`, `deny`
    * `-r` / `--resource`
      * TODO:
    * `-o` / `--object`
      * TODO:

* _Examples:_
	```
	# Before adding new policy
	$ argocd proj role get test-project test-role
	Role Name:     test-role
	Description:
	Policies:
	p, proj:test-project:test-role, projects, get, test-project, allow
	JWT Tokens:
	ID          ISSUED-AT                                EXPIRES-AT
	1696759698  2023-10-08T11:08:18+01:00 (3 hours ago)  <none>
	
	# Add a new policy to allow update to the project
	$ argocd proj role add-policy test-project test-role -a update -p allow -o project
	
	# Policy should be updated
	$  argocd proj role get test-project test-role
	Role Name:     test-role
	Description:
	Policies:
	p, proj:test-project:test-role, projects, get, test-project, allow
	p, proj:test-project:test-role, applications, update, test-project/project, allow
	JWT Tokens:
	ID          ISSUED-AT                                EXPIRES-AT
	1696759698  2023-10-08T11:08:18+01:00 (3 hours ago)  <none>
	
	# Add a new policy to allow get logs to the project
	$ argocd proj role add-policy test-project test-role -a get -p allow -o project -r logs
	
	# Policy should be updated
	$  argocd proj role get test-project test-role
	Role Name:     test-role
	Description:
	Policies:
	p, proj:test-project:test-role, projects, get, test-project, allow
	p, proj:test-project:test-role, applications, update, test-project/project, allow
	p, proj:test-project:test-role, logs, get, test-project/project, allow
	JWT Tokens:
	ID          ISSUED-AT                                EXPIRES-AT
	1696759698  2023-10-08T11:08:18+01:00 (3 hours ago)  <none>
	```

## `func NewProjectRoleRemovePolicyCommand(clientOpts *argocdclient.ClientOptions) *cobra.Command {`
* `argocd proj role remove-policy PROJECT ROLE-NAME`
  * Remove a policy -- from a -- project's role
  * `[FLAG]`
    * `-a` / `--action`
      * TODO:
    * `-p` / `--permission`
      * ALLOWED values: `allow`, `deny`
    * `-r` / `--resource`
      * TODO:
    * `-o` / `--object`
      * TODO:

* _Examples:_ 
	```
	# List the policy of the test-role before removing a policy
	$ argocd proj role get test-project test-role
	Role Name:     test-role
	Description:
	Policies:
	p, proj:test-project:test-role, projects, get, test-project, allow
	p, proj:test-project:test-role, applications, update, test-project/project, allow
	p, proj:test-project:test-role, logs, get, test-project/project, allow
	JWT Tokens:
	ID          ISSUED-AT                                EXPIRES-AT
	1696759698  2023-10-08T11:08:18+01:00 (3 hours ago)  <none>
	
	# Remove the policy to allow update to objects
	$ argocd proj role remove-policy test-project test-role -a update -p allow -o project
	
	# The role should be removed now.
	$ argocd proj role get test-project test-role
	Role Name:     test-role
	Description:
	Policies:
	p, proj:test-project:test-role, projects, get, test-project, allow
	p, proj:test-project:test-role, logs, get, test-project/project, allow
	JWT Tokens:
	ID          ISSUED-AT                                EXPIRES-AT
	1696759698  2023-10-08T11:08:18+01:00 (4 hours ago)  <none>
	
	
	# Remove the logs read policy
	$ argocd proj role remove-policy test-project test-role -a get -p allow -o project -r logs
	
	# The role should be removed now.
	$ argocd proj role get test-project test-role
	Role Name:     test-role
	Description:
	Policies:
	p, proj:test-project:test-role, projects, get, test-project, allow
	JWT Tokens:
	ID          ISSUED-AT                                EXPIRES-AT
	1696759698  2023-10-08T11:08:18+01:00 (4 hours ago)  <none>
	```

## `func NewProjectRoleCreateCommand(clientOpts *argocdclient.ClientOptions) *cobra.Command {`
* `argocd proj role create PROJECT ROLE-NAME`
  * create a project role
    * ⚠️ALTHOUGH you do NOT specify ANY policy -> by default create a policy / allow get the policy⚠️
* _Examples:_ 
	```
	# Create a project role in the "my-project" project with the name "my-role".
	argocd proj role create my-project my-role --description "My project role description"
	```

## `func NewProjectRoleDeleteCommand(clientOpts *argocdclient.ClientOptions) *cobra.Command {`
* `argocd proj role delete PROJECT ROLE-NAME`
  * delete a project role
* _Examples:_ 
	```
	$ argocd proj role delete test-project test-role
	```


## `func NewProjectRoleCreateTokenCommand(clientOpts *argocdclient.ClientOptions) *cobra.Command {`
* `argocd proj role create-token PROJECT ROLE-NAME [FLAG]` OR `argocd proj token-create PROJECT ROLE-NAME [FLAG]`
  * `[FLAG]`
    * `--expires-in` / `-e`
      * == DURATION BEFORE the token expires
        * _Example:_ 12h, 7d
      * by default, 0
    * `--id` / `-i`
      * == token UID
        * by default, Random UUID
    * `--token-only` / `-t`
      * == OUTPUT token ONLY
      * uses
        * | scripts
  * create a project token
* _Examples:_
```
$ argocd proj role create-token test-project test-role
Create token succeeded for proj:test-project:test-role.
  ID: f316c466-40bd-4cfd-8a8c-1392e92255d4
  Issued At: 2023-10-08T15:21:40+01:00
  Expires At: Never
  Token: xxx
```


## `func NewProjectRoleListTokensCommand(clientOpts *argocdclient.ClientOptions) *cobra.Command {`
* `argocd proj role list-tokens PROJECT ROLE-NAME [FLAG]` OR `argocd proj role token-list PROJECT ROLE-NAME [FLAG]`
  * `[FLAG]`
    * `--unixtime` / `-u`
      * print timestamps -- as -- Unix time
        * -- instead of -- converting
      * use cases
        * piping | delete-token
      * by default, false
* List tokens / given role
* _Examples:_
	```
	$ argocd proj role list-tokens test-project test-role
		ID                                      ISSUED AT                    EXPIRES AT
		f316c466-40bd-4cfd-8a8c-1392e92255d4    2023-10-08T15:21:40+01:00    Never
		fa9d3517-c52d-434c-9bff-215b38508842    2023-10-08T11:08:18+01:00    Never
	```



## `func NewProjectRoleDeleteTokenCommand(clientOpts *argocdclient.ClientOptions) *cobra.Command {`
* `argocd proj role delete-token PROJECT ROLE-NAME ISSUED-AT` OR `argocd proj role token-delete PROJECT ROLE-NAME ISSUED-AT` OR `argocd proj role remove-token PROJECT ROLE-NAME ISSUED-AT` 
* Delete a project token
* _Examples:_
	```
	#Create project test-project
	$ argocd proj create test-project
	
	# Create a role associated with test-project
	$ argocd proj role create test-project test-role
		Role 'test-role' created
	
	# Create test-role associated with test-project
	$ argocd proj role create-token test-project test-role
		Create token succeeded for proj:test-project:test-role.
		  ID: c312450e-12e1-4e0d-9f65-fac9cb027b32
		  Issued At: 2023-10-08T13:58:57+01:00
		  Expires At: Never
		  Token: xxx
	
	# Get test-role id to input into the delete-token command below
	$ argocd proj role get test-project test-role
		Role Name:     test-role
		Description:
		Policies:
		p, proj:test-project:test-role, projects, get, test-project, allow
		JWT Tokens:
		ID          ISSUED-AT                                  EXPIRES-AT
		1696769937  2023-10-08T13:58:57+01:00 (6 minutes ago)  <none>
	
	$ argocd proj role delete-token test-project test-role 1696769937
	```

## `func NewProjectRoleListCommand(clientOpts *argocdclient.ClientOptions) *cobra.Command {`
* `argocd proj role list PROJECT [FLAG]`
  * list ALL project's roles
  * `FLAG`
    * `--output` / `-o`
      * ALLOWED values
        * "json", "yaml"
        * "name"
        * "wide", ""
* _Examples:_ 
	```
	# This command will list all the roles in argocd-project in a default table format.
	argocd proj role list PROJECT
	
	# List the roles in the project in formats like json, yaml, wide, or name.
	argocd proj role list PROJECT --output json
	```


## `func NewProjectRoleGetCommand(clientOpts *argocdclient.ClientOptions) *cobra.Command {`
* `argocd proj role get PROJECT ROLE-NAME`
* Get specific role's details
  * ⚠️return ALL project's policies⚠️
    * ❌NOT ONLY project's role policies❌
* _Example:_
```
$ argocd proj role get test-project test-role
	Role Name:     test-role
	Description:
	Policies:
	p, proj:test-project:test-role, projects, get, test-project, allow
	JWT Tokens:
	ID          ISSUED-AT                                  EXPIRES-AT
	1696774900  2023-10-08T15:21:40+01:00 (4 minutes ago)  <none>
	1696759698  2023-10-08T11:08:18+01:00 (4 hours ago)    <none>
```


## `func NewProjectRoleAddGroupCommand(clientOpts *argocdclient.ClientOptions) *cobra.Command {`
* `argocd proj role add-group PROJECT ROLE-NAME GROUP-CLAIM`
* Add a group claim | project role


## `func NewProjectRoleRemoveGroupCommand(clientOpts *argocdclient.ClientOptions) *cobra.Command {`
* `argocd proj role remove-group PROJECT ROLE-NAME GROUP-CLAIM`
* | project's role
  * remove a group claim
