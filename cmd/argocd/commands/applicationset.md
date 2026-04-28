# `func NewAppSetCommand(clientOpts *argocdclient.ClientOptions) *cobra.Command {`
* `argocd appset <COMMAND>`
  * NewApplicationSetGetCommand(clientOpts)
  * NewApplicationSetCreateCommand(clientOpts)
  * NewApplicationSetListCommand(clientOpts)
  * NewApplicationSetDeleteCommand(clientOpts)
  * NewApplicationSetGenerateCommand(clientOpts)
* Manage ApplicationSets
* _Example:_
	```
	# Get an ApplicationSet.
	argocd appset get APPSETNAME
	
	# List all the ApplicationSets
	argocd appset list
	
	# Create an ApplicationSet from a YAML stored in a file or at given URL
	argocd appset create <filename or URL> (<filename or URL>...)
	
	# Delete an ApplicationSet
	argocd appset delete APPSETNAME (APPSETNAME...)
	```


## `func NewApplicationSetGetCommand(clientOpts *argocdclient.ClientOptions) *cobra.Command {`
* `argocd appset get APPSETNAME [FLAG]`
  * `[FLAG]`
    * `--output` / `-o`
      * ALLOWED values: `yaml` | `json` | `url` | `wide`
    * `--show-params`
      * by default, false
      * show 
        * ApplicationSet parameters 
        * overrides
* Get ApplicationSet details
* _Examples:_
```
# Get ApplicationSets
argocd appset get APPSETNAME
```


## `func NewApplicationSetCreateCommand(clientOpts *argocdclient.ClientOptions) *cobra.Command {`
* `argocd appset create <FILE_NAME_OR_URL> [FLAG]`
  * `[FLAG]`
    * `--upsert`
      * by default, `false`
      * allows
        * override ApplicationSet / SAME name
          * ALTHOUGH supplied ApplicationSet spec != EXISTING spec
    * `--dry-run`
      * by default, `false`
      * allows
        * get a preview of the applications / would be created
      * uses
        * evaluate the ApplicationSet template | server  
    * `--output` / `-o`
      * ALLOWED values: `yaml` | `json` | `url` | `wide`
* Create >=1 ApplicationSets
* _Examples:_
```
# Create ApplicationSets
argocd appset create <filename or URL> (<filename or URL>...)

# Dry-run AppSet creation to see what applications would be managed
argocd appset create --dry-run <filename or URL> -o json | jq -r '.status.resources[].name' 
```



## `func NewApplicationSetGenerateCommand(clientOpts *argocdclient.ClientOptions) *cobra.Command {`
* `argocd appset generate <FILE_NAME_OR_URL> [FLAG]`
  * `[FLAG]`
    * `--output` / `-o`
      * ALLOWED values: `yaml` | `json` | `url` | `wide`
* Generate apps -- of -- ApplicationSet rendered templates
* _Example:_
	```
	# Generate apps of ApplicationSet rendered templates
	argocd appset generate <filename or URL> (<filename or URL>...)
	```


## `func NewApplicationSetListCommand(clientOpts *argocdclient.ClientOptions) *cobra.Command {`
* `argocd appset list [FLAG]`
  * `[FLAG]`
    * `--output` / `-o`
      * ALLOWED values: `yaml` | `json` | `url` | `wide`
    * `--selector` / `-l`
      * List applicationsets -- by -- label
    * `--project` / `-p`
      * `:[]string`
      * Filter -- by -- project name
    * `--appset-namespace` / `-N`
      * filter -- by -- namespace
* List ApplicationSets
* _Example:_
```
argocd appset list
```


## `func NewApplicationSetDeleteCommand(clientOpts *argocdclient.ClientOptions) *cobra.Command {`
* `argocd appset delete [FLAG]`
  * `[FLAG]`
    * `--yes` / `-y`
      * by default, false
      * Turn off prompting / confirm cascade deletion
* Delete >=1 ApplicationSets
* _Example:_
```
argocd appset delete APPSETNAME (APPSETNAME...)
```
