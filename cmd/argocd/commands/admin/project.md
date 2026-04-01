# `func NewProjectsCommand() *cobra.Command {`
* `argocd admin proj COMMAND`
  * manage projects configuration
  * `COMMAND`
    * ALLOWED ones
      * NewGenProjectSpecCommand()
      * NewUpdatePolicyRuleCommand()
      * NewProjectAllowListGenCommand()

## `func NewGenProjectSpecCommand() *cobra.Command {`
* `argocd admin proj generate-spec PROJECT [FLAG]`
  * generate project's declarative config 
  * `FLAG`
    * ALLOWED ones
      * `--output` / `-o`
        * == output format
        * by default,
          * "yaml"
        * ALLOWED values
          * json
          * yaml
      * `--file` / `-f`
        * == Filename OR URL -- to -- Argo CD project's manifest
        * by default,
          * ""
        * ALLOWED extensions
          * json, yaml, yml
      * `--inline` / `-i`
        * if `true` -> generated resource is written back | specified `--file`
        * by default,
          * `false`
* _Examples:_ 
	```
	# Generate a YAML configuration for a project named "myproject"
	argocd admin proj generate-spec myproject
	  
	# Generate a JSON configuration for a project named "anotherproject" and specify an output file
	argocd admin proj generate-spec anotherproject --output json --file config.json
	  
	# Generate a YAML configuration for a project named "someproject" and write it back to the input file
	argocd admin proj generate-spec someproject --inline
	```

## `func NewUpdatePolicyRuleCommand() *cobra.Command {`
* `argocd admin proj update-role-policy PROJECT_GLOB MODIFICATION ACTION [FLAG]`
  * implement bulk project role update
  * Useful to back-fill existing project policies or remove obsolete actions.",
  * `FLAG`
    * ALLOWED ones
      * `--resource`
        * == resource
        * _Example:_ `applications`
        * by default,
          * ""
      * `--scope`
        * == resource scope
        * _Example:_ `*`
        * by default,
          * ""
      * `--role`
        * == role name pattern
        * _Example:_ `*deployer*`
        * by default,
          * `*`
      * `--permission`
        * == action permission
        * by default,
          * ""
      * `--dry-run`
        * by default,
          * `true`

* _Examples:_ 
	```
	# Add policy that allows executing any action (action/*) to roles which name matches to *deployer* in all projects  
	argocd admin proj update-role-policy '*' set 'action/*' --role '*deployer*' --resource applications --scope '*' --permission allow
	
	# Remove policy that which manages running (action/*) from all roles which name matches *deployer* in all projects
	argocd admin proj update-role-policy '*' remove override --role '*deployer*'
	```
