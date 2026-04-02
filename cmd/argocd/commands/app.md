# `func NewApplicationCommand(clientOpts *argocdclient.ClientOptions) *cobra.Command {`
* `argocd app COMMAND`
  * Manage applications
  * `COMMAND`
    * NewApplicationCreateCommand(clientOpts)
    * NewApplicationGetCommand(clientOpts)
    * NewApplicationDiffCommand(clientOpts)
    * NewApplicationSetCommand(clientOpts)
    * NewApplicationUnsetCommand(clientOpts)
    * NewApplicationSyncCommand(clientOpts)
    * NewApplicationHistoryCommand(clientOpts)
    * NewApplicationRollbackCommand(clientOpts)
    * NewApplicationListCommand(clientOpts)
    * NewApplicationDeleteCommand(clientOpts)
    * NewApplicationWaitCommand(clientOpts)
    * NewApplicationManifestsCommand(clientOpts)
    * NewApplicationTerminateOpCommand(clientOpts)
    * NewApplicationEditCommand(clientOpts)
    * NewApplicationPatchCommand(clientOpts)
    * NewApplicationGetResourceCommand(clientOpts)
    * NewApplicationPatchResourceCommand(clientOpts)
    * NewApplicationDeleteResourceCommand(clientOpts)
    * NewApplicationResourceActionsCommand(clientOpts)
    * NewApplicationListResourcesCommand(clientOpts)
    * NewApplicationLogsCommand(clientOpts)
    * NewApplicationAddSourceCommand(clientOpts)
    * NewApplicationRemoveSourceCommand(clientOpts)
    * NewApplicationConfirmDeletionCommand(clientOpts)

* _Examples:_

	```
	# List all the applications.
	argocd app list
	
	# Get the details of a application
	argocd app get my-app
	
	# Set an override parameter
	argocd app set my-app -p image.tag=v1.0.1
	```

# `func NewApplicationCreateCommand(clientOpts *argocdclient.ClientOptions) *cobra.Command {`
* `argocd app create APPNAME [FLAG]`
  * Create an application
  * `FLAG`
    * `--name`
      * == name for the app
        * ⚠️ignored if `--file` is set⚠️
      * ⚠️DEPRECATED⚠️
      * by default,
        * ""
    * `--upsert`
      * if `true` -> override application / same name even if supplied spec != existing spec
      * by default,
        * `false`
    * `--file` / `-f`
      * == Filename OR URL -- to -- Kubernetes manifests for the app
      * by default,
        * ""
      * ALLOWED extensions
        * json, yaml, yml
    * `--label` / `-l`
      * == labels -- to apply to -- the app
      * by default,
        * `[]`
    * `--annotations`
      * == metadata annotations
      * _Example:_ `example=value`
      * by default,
        * `[]`
    * `--set-finalizer`
      * if `true` -> sets deletion finalizer on the application
        * application resources will be cascaded on deletion
      * by default,
        * `false`
    * `--app-namespace` / `-N`
      * == namespace / application will be created in
      * by default,
        * ""

* _Example:_ 

	```
	# Create a directory app
	argocd app create guestbook --repo https://github.com/argoproj/argocd-example-apps.git --path guestbook --dest-namespace default --dest-server https://kubernetes.default.svc --directory-recurse
	
	## Create aJsonnet app
	argocd app create jsonnet-guestbook --repo https://github.com/argoproj/argocd-example-apps.git --path jsonnet-guestbook --dest-namespace default --dest-server https://kubernetes.default.svc --jsonnet-ext-str replicas=2
	
	## Create aHelm app
	argocd app create helm-guestbook --repo https://github.com/argoproj/argocd-example-apps.git --path helm-guestbook --dest-namespace default --dest-server https://kubernetes.default.svc --helm-set replicaCount=2
	
	## Create aHelm app from a Helm repo
	argocd app create nginx-ingress --repo https://charts.helm.sh/stable --helm-chart nginx-ingress --revision 1.24.3 --dest-namespace default --dest-server https://kubernetes.default.svc
	
	## Create aKustomize app
	argocd app create kustomize-guestbook --repo https://github.com/argoproj/argocd-example-apps.git --path kustomize-guestbook --dest-namespace default --dest-server https://kubernetes.default.svc --kustomize-image quay.io/argoprojlabs/argocd-e2e-container:0.1
	
	## Create aMultiSource app while yaml file contains an application with multiple sources
	argocd app create guestbook --file <path-to-yaml-file>
	
	## Create aapp using a custom tool:
	argocd app create kasane --repo https://github.com/argoproj/argocd-example-apps.git --path plugins/kasane --dest-namespace default --dest-server https://kubernetes.default.svc --config-management-plugin kasane
	```

# `func NewApplicationGetCommand(clientOpts *argocdclient.ClientOptions) *cobra.Command {`
* `argocd app get APPNAME [FLAG]`
  * Get application details
    * `FLAG`
      * `--output` / `-o`
        * == output format
        * by default,
          * `wide`
        * ALLOWED values
          * `json`, `yaml`, `wide`, `tree`, `tree=detailed`
      * `--timeout`
        * == time out -- after -- this many seconds
        * by default,
          * `defaultCheckTimeoutSeconds`
      * `--show-operation`
        * if `true` -> show application operation
        * by default,
          * `false`
      * `--show-params`
        * if `true` -> show application parameters & overrides
        * by default,
          * `false`
      * `--refresh`
        * if `true` -> refresh application data when retrieving
        * by default,
          * `false`
      * `--hard-refresh`
        * if `true` -> refresh application data + target manifests cache
        * by default,
          * `false`
      * `--app-namespace` / `-N`
        * == namespace / get application from
        * by default,
          * ""
      * `--source-position`
        * == position of the source -- from the -- list of sources of the app
          * counting starts at `1`
        * by default,
          * `-1`
      * `--source-name`
        * == name of the source -- from the -- list of sources of the app
        * by default,
          * ""

* _Examples:_
	```
	# Get basic details about the application "my-app" in wide format
	argocd app get my-app -o wide
	
	# Get detailed information about the application "my-app" in YAML format
	argocd app get my-app -o yaml
	
	# Get details of the application "my-app" in JSON format
	argocd get my-app -o json
	
	# Get application details and include information about the current operation
	argocd app get my-app --show-operation
	
	# Show application parameters and overrides
	argocd app get my-app --show-params
	
	# Show application parameters and overrides for a source at position 1 under spec.sources of app my-app
	argocd app get my-app --show-params --source-position 1
	
	# Show application parameters and overrides for a source named "test"
	argocd app get my-app --show-params --source-name test
	
	# Refresh application data when retrieving
	argocd app get my-app --refresh
	
	# Perform a hard refresh, including refreshing application data and target manifests cache
	argocd app get my-app --hard-refresh
	
	# Get application details and display them in a tree format
	argocd app get my-app --output tree
	
	# Get application details and display them in a detailed tree format
	argocd app get my-app --output tree=detailed
	```

# func NewApplicationLogsCommand(clientOpts *argocdclient.ClientOptions) *cobra.Command {
* `argocd app logs APPNAME [FLAG]`
  * Get logs of application pods
  * `FLAG`
    * `--group`
      * == resource group
      * by default,
        * ""
    * `--kind`
      * == resource kind
      * by default,
        * ""
    * `--namespace`
      * == resource namespace
      * by default,
        * ""
    * `--name`
      * == resource name
      * by default,
        * ""
    * `--follow` / `-f`
      * if `true` -> logs are streamed
      * by default,
        * `false`
    * `--tail`
      * == number of lines -- from the -- end of logs to show
      * by default,
        * `0`
    * `--since-seconds`
      * == relative time in seconds before current time -- from which to -- show logs
      * by default,
        * `0`
    * `--until-time`
      * == show logs until this time
      * by default,
        * ""
    * `--filter`
      * == show logs / contain this string
      * by default,
        * ""
    * `--container` / `-c`
      * == container name
      * by default,
        * ""
    * `--previous` / `-p`
      * if `true` -> return previously terminated container logs
      * by default,
        * `false`
    * `--match-case` / `-m`
      * if `true` -> filter is case-sensitive
      * by default,
        * `false`

* _Examples:_ 
    ```
    # Get logs of pods associated with the application "my-app"
    argocd app logs my-app
    
    # Get logs of pods associated with the application "my-app" in a specific resource group
    argocd app logs my-app --group my-group
    
    # Get logs of pods associated with the application "my-app" in a specific resource kind
    argocd app logs my-app --kind my-kind
    
    # Get logs of pods associated with the application "my-app" in a specific namespace
    argocd app logs my-app --namespace my-namespace
    
    # Get logs of pods associated with the application "my-app" for a specific resource name
    argocd app logs my-app --name my-resource
    
    # Stream logs in real-time for the application "my-app"
    argocd app logs my-app -f
    
    # Get the last N lines of logs for the application "my-app"
    argocd app logs my-app --tail 100
    
    # Get logs since a specified number of seconds ago
    argocd app logs my-app --since-seconds 3600
    
    # Get logs until a specified time (format: "2023-10-10T15:30:00Z")
    argocd app logs my-app --until-time "2023-10-10T15:30:00Z"
    
    # Filter logs to show only those containing a specific string
    argocd app logs my-app --filter "error"
    
    # Filter logs to show only those containing a specific string and match case
    argocd app logs my-app --filter "error" --match-case
    
    # Get logs for a specific container within the pods
    argocd app logs my-app -c my-container
    
    # Get previously terminated container logs
    argocd app logs my-app -p
    ```

// NewApplicationSetCommand returns a new instance of an `argocd app set` command

# `func NewApplicationSetCommand(clientOpts *argocdclient.ClientOptions) *cobra.Command {`
* `argocd app set APPNAME [FLAG]`
  * Set application parameters
  * `FLAG`
    * `--app-namespace` / `-N`
      * == namespace / set application parameters in
      * by default,
        * ""
    * `--source-position`
      * == position of the source -- from the -- list of sources of the app
        * counting starts at `1`
      * by default,
        * `-1`

* _Examples:_

```shell
# Set application parameters for the application "my-app"
argocd app set my-app --parameter key1=value1 --parameter key2=value2

# Set and validate application parameters for "my-app"
argocd app set my-app --parameter key1=value1 --parameter key2=value2 --validate

# Set and override application parameters for a source at position 1 under spec.sources of app my-app. source-position starts at 1.
argocd app set my-app --source-position 1 --repo https://github.com/argoproj/argocd-example-apps.git

# Set and override application parameters for a source named "test" under spec.sources of app my-app.
argocd app set my-app --source-name test --repo https://github.com/argoproj/argocd-example-apps.git

# Set application parameters and specify the namespace
argocd app set my-app --parameter key1=value1 --parameter key2=value2 --namespace my-namespace
```

# `func NewApplicationUnsetCommand(clientOpts *argocdclient.ClientOptions) *cobra.Command {`
* `argocd unset APPNAME parameters [FLAG]`
  * Unset application parameters
  * `FLAG`
    * ALLOWED ones
      * `--app-namespace` / `-N`
        * == namespace -- in which -- unset application parameters
        * by default,
          * `""`
      * `--parameter` / `-p`
        * == unset a parameter override
        * _Example:_ `-p guestbook=image`
        * by default,
          * `[]`
      * `--values`
        * == unset one or more Helm values files
        * by default,
          * `[]`
      * `--values-literal`
        * == unset literal Helm values block
        * by default,
          * `false`
      * `--ignore-missing-value-files`
        * == unset the helm ignore-missing-value-files option (revert to false)
        * by default,
          * `false`
      * `--namesuffix`
        * == unset Kustomize namesuffix
        * by default,
          * `false`
      * `--nameprefix`
        * == unset Kustomize nameprefix
        * by default,
          * `false`
      * `--kustomize-version`
        * == unset Kustomize version
        * by default,
          * `false`
      * `--kustomize-namespace`
        * == unset Kustomize namespace
        * by default,
          * `false`
      * `--kustomize-image`
        * == unset Kustomize images name
        * _Example:_ `--kustomize-image node --kustomize-image mysql`
        * by default,
          * `[]`
      * `--kustomize-replica`
        * == unset Kustomize replicas name
        * _Example:_ `--kustomize-replica my-deployment --kustomize-replica my-statefulset`
        * by default,
          * `[]`
      * `--ignore-missing-components`
        * == unset the kustomize ignore-missing-components option (revert to false)
        * by default,
          * `false`
      * `--plugin-env`
        * == unset plugin env variables
        * _Example:_ `--plugin-env name`
        * by default,
          * `[]`
      * `--pass-credentials`
        * == unset passCredentials
        * by default,
          * `false`
      * `--ref`
        * == unset ref on the source
        * by default,
          * `false`
      * `--source-position`
        * == position of the source -- from -- the list of sources of the app
        * counting starts at 1
        * by default,
          * `-1`

* _Examples:_ 

```shell
# Unset kustomize override kustomize image
argocd app unset my-app --kustomize-image=alpine

# Unset kustomize override suffix
argocd app unset my-app --namesuffix

# Unset kustomize override suffix for source at position 1 under spec.sources of app my-app. source-position starts at 1.
argocd app unset my-app --source-position 1 --namesuffix

# Unset kustomize override suffix for source named "test" under spec.sources of app my-app.
argocd app unset my-app --source-name test --namesuffix

# Unset parameter override
argocd app unset my-app -p COMPONENT=PARAM`
```

# `func NewApplicationDiffCommand(clientOpts *argocdclient.ClientOptions) *cobra.Command {`
* `argocd app diff APPNAME [FLAG]`
  * render the difference
    * ⚠️skip Kubernetes Secrets⚠️
    * if you want to select your OWN diff tool -> specify the `KUBECTL_EXTERNAL_DIFF` environment variable 
  * exit codes
    * 2 
      * == general errors
    * 1
      * == diff is found
    * 0
      * == ❌NO diff is found❌
  * `FLAG`
    * ALLOWED ones
      * `--refresh`
        * == refresh application data when retrieving
        * by default,
          * `false`
      * `--hard-refresh`
        * == refresh application data as well as target manifests cache
        * by default,
          * `false`
      * `--exit-code`
        * == return non-zero exit code when there is a diff; may also return non-zero exit code if there is an error
        * by default,
          * `true`
      * `--diff-exit-code`
        * == return specified exit code when there is a diff
        * typical error code is 20; use another exit code to differentiate from the generic exit code (20) returned by all CLI commands
        * by default,
          * `1`
      * `--local`
        * == compare live app -- to -- a local manifests
        * by default,
          * `""`
      * `--revision`
        * == compare live app -- to -- a particular revision
        * by default,
          * `""`
      * `--local-repo-root`
        * == path to the repository root; used together with `--local` allows setting the repository root
        * by default,
          * `"/"`
      * `--server-side-generate`
        * == used with `--local`, sends manifests to the server for diffing
        * by default,
          * `false`
      * `--server-side-diff`
        * == use server-side diff to calculate the diff; defaults to `true` if the ServerSideDiff annotation is set on the application
        * by default,
          * `false`
      * `--local-include`
        * == used with `--server-side-generate`, specify patterns of filenames to send; matching is based on filename and not path
        * by default,
          * `["*.yaml", "*.yml", "*.json"]`
      * `--app-namespace` / `-N`
        * == namespace -- in which -- only render the difference
        * by default,
          * `""`
      * `--revisions`
        * == show manifests at specific revisions for source position in source-positions
        * by default,
          * `[]`
      * `--source-positions`
        * == list of source positions; counting starts at 1
        * by default,
          * `[]`
      * `--source-names`
        * == list of source names
        * by default,
          * `[]`
      * `--ignore-normalizer-jq-execution-timeout`
        * == set ignore normalizer JQ execution timeout
        * by default,
          * `normalizers.DefaultJQExecutionTimeout`

# `func NewApplicationDeleteCommand(clientOpts *argocdclient.ClientOptions) *cobra.Command {`
* `argocd delete APPNAME [FLAG]`
  * Delete an application
  * `FLAG`
    * ALLOWED ones
      * `--cascade`
        * == perform a cascaded deletion of ALL application resources
        * by default,
          * `true`
      * `--propagation-policy` / `-p`
        * == specify propagation policy for deletion of application's resources
        * ALLOWED values: `foreground` | `background`
        * by default,
          * `"foreground"`
      * `--yes` / `-y`
        * == turn off prompting to confirm cascaded deletion of application resources
        * by default,
          * `false`
      * `--selector` / `-l`
        * == delete all apps with matching label; supports `=`, `==`, `!=`, `in`, `notin`, `exists` & `not exists`; matching apps must satisfy all of the specified label constraints
        * by default,
          * `""`
      * `--wait`
        * == wait until deletion of the application(s) completes
        * by default,
          * `false`
      * `--app-namespace` / `-N`
        * == namespace where the application will be deleted from
        * by default,
          * `""`
* _Examples:_ 
```
# Delete an app
argocd app delete my-app

# Delete multiple apps
argocd app delete my-app other-app

# Delete apps by label
argocd app delete -l app.kubernetes.io/instance=my-app
argocd app delete -l app.kubernetes.io/instance!=my-app
argocd app delete -l app.kubernetes.io/instance
argocd app delete -l '!app.kubernetes.io/instance'
argocd app delete -l 'app.kubernetes.io/instance notin (my-app,other-app)'
```

# `func NewApplicationListCommand(clientOpts *argocdclient.ClientOptions) *cobra.Command {`
* `argocd app list [FLAG]`
  * List ALL applications
  * `FLAG`
    * ALLOWED ones
      * `--output` / `-o`
        * == output format
        * ALLOWED values: `wide` | `name` | `json` | `yaml`
        * by default,
          * `"wide"`
      * `--selector` / `-l`
        * == list apps by label; supports `=`, `==`, `!=`, `in`, `notin`, `exists` & `not exists`; matching apps must satisfy all of the specified label constraints
        * by default,
          * `""`
      * `--project` / `-p`
        * == filter by project name
        * by default,
          * `[]`
      * `--repo` / `-r`
        * == list apps by source repo URL
        * by default,
          * `""`
      * `--app-namespace` / `-N`
        * == only list applications in namespace
        * by default,
          * `""`
      * `--cluster` / `-c`
        * == list apps by cluster name or url
        * by default,
          * `""`
      * `--path` / `-P`
        * == list apps by path
        * by default,
          * `""`
* _Examples:_
  ```
  # List all apps
  argocd app list
  
  # List apps by label, in this example we listing apps that are children of another app (aka app-of-apps)
  argocd app list -l app.kubernetes.io/instance=my-app
  argocd app list -l app.kubernetes.io/instance!=my-app
  argocd app list -l app.kubernetes.io/instance
  argocd app list -l '!app.kubernetes.io/instance'
  argocd app list -l 'app.kubernetes.io/instance notin (my-app,other-app)'
  ```

# `func NewApplicationWaitCommand(clientOpts *argocdclient.ClientOptions) *cobra.Command {`
* `argocd app wait [APPNAME.. | -l selector] [FLAG]`
  * Wait for an application reach a synced & healthy state
  * `FLAG`
    * ALLOWED ones
      * `--sync`
        * == wait for sync
        * by default,
          * `false`
      * `--health`
        * == wait for health
        * by default,
          * `false`
      * `--suspended`
        * == wait for suspended
        * by default,
          * `false`
      * `--degraded`
        * == wait for degraded
        * by default,
          * `false`
      * `--delete`
        * == wait for delete
        * by default,
          * `false`
      * `--hydrated`
        * == wait for hydration operations
        * by default,
          * `false`
      * `--selector` / `-l`
        * == wait for apps by label; supports `=`, `==`, `!=`, `in`, `notin`, `exists` & `not exists`; matching apps must satisfy all of the specified label constraints
        * by default,
          * `""`
      * `--resource`
        * == sync only specific resources as `GROUP:KIND:NAME` or `!GROUP:KIND:NAME`; fields may be blank and `*` can be used; option may be specified repeatedly
        * by default,
          * `[]`
      * `--operation`
        * == wait for pending operations
        * by default,
          * `false`
      * `--timeout`
        * == time out after this many seconds
        * by default,
          * `defaultCheckTimeoutSeconds`
      * `--app-namespace` / `-N`
        * == only wait for an application in namespace
        * by default,
          * `""`
      * `--output` / `-o`
        * == output format
        * ALLOWED values: `json` | `yaml` | `wide` | `tree` | `tree=detailed`
        * by default,
          * `"wide"`
* _Examples:_
```
# Wait for an app
argocd app wait my-app

# Wait for multiple apps
argocd app wait my-app other-app

# Wait for apps by resource
# Resource should be formatted as GROUP:KIND:NAME. If no GROUP is specified then :KIND:NAME.
argocd app wait my-app --resource :Service:my-service
argocd app wait my-app --resource argoproj.io:Rollout:my-rollout
argocd app wait my-app --resource '!apps:Deployment:my-service'
argocd app wait my-app --resource apps:Deployment:my-service --resource :Service:my-service
argocd app wait my-app --resource '!*:Service:*'
# Specify namespace if the application has resources with the same name in different namespaces
argocd app wait my-app --resource argoproj.io:Rollout:my-namespace/my-rollout

# Wait for apps by label, in this example we waiting for apps that are children of another app (aka app-of-apps)
argocd app wait -l app.kubernetes.io/instance=my-app
argocd app wait -l app.kubernetes.io/instance!=my-app
argocd app wait -l app.kubernetes.io/instance
argocd app wait -l '!app.kubernetes.io/instance'
argocd app wait -l 'app.kubernetes.io/instance notin (my-app,other-app)'
```

# `func NewApplicationSyncCommand(clientOpts *argocdclient.ClientOptions) *cobra.Command {`
* `argocd app sync [APPNAME... | -l selector | --project project-name] [FLAG]`
  * allows  
    * sync an application -- to -- its target state
  * `FLAG`
    * ALLOWED ones
      * `--dry-run`
        * == preview apply without affecting cluster
        * by default,
          * `false`
      * `--prune`
        * == allow deleting unexpected resources
        * by default,
          * `false`
      * `--revision`
        * == sync to a specific revision; preserves parameter overrides
        * by default,
          * `""`
      * `--resource`
        * == sync only specific resources as `GROUP:KIND:NAME` or `!GROUP:KIND:NAME`; fields may be blank and `*` can be used; option may be specified repeatedly
        * by default,
          * `[]`
      * `--selector` / `-l`
        * == sync apps that match this label; supports `=`, `==`, `!=`, `in`, `notin`, `exists` & `not exists`; matching apps must satisfy all of the specified label constraints
        * by default,
          * `""`
      * `--label`
        * == sync only specific resources with a label; option may be specified repeatedly
        * by default,
          * `[]`
      * `--timeout`
        * == time out after this many seconds
        * by default,
          * `defaultCheckTimeoutSeconds`
      * `--retry-limit`
        * == max number of allowed sync retries
        * by default,
          * `0`
      * `--retry-refresh`
        * == indicates if the latest revision should be used on retry instead of the initial one
        * by default,
          * `false`
      * `--retry-backoff-duration`
        * == retry backoff base duration
        * _Example:_ `2m`, `1h`
        * by default,
          * `argoappv1.DefaultSyncRetryDuration`
      * `--retry-backoff-max-duration`
        * == max retry backoff duration
        * _Example:_ `2m`, `1h`
        * by default,
          * `argoappv1.DefaultSyncRetryMaxDuration`
      * `--retry-backoff-factor`
        * == factor multiplies the base duration after each failed retry
        * by default,
          * `argoappv1.DefaultSyncRetryFactor`
      * `--strategy`
        * == sync strategy
        * ALLOWED values: `apply` | `hook`
        * by default,
          * `""`
      * `--force`
        * == use a force apply
        * by default,
          * `false`
      * `--replace`
        * == use a kubectl create/replace instead apply
        * by default,
          * `false`
      * `--server-side`
        * == use server-side apply while syncing the application
        * by default,
          * `false`
      * `--apply-out-of-sync-only`
        * == sync only out-of-sync resources
        * by default,
          * `false`
      * `--async`
        * == do not wait for application to sync before continuing
        * by default,
          * `false`
      * `--local`
        * == path to a local directory; when this flag is present no git queries will be made
        * by default,
          * `""`
      * `--local-repo-root`
        * == path to the repository root; used together with `--local` allows setting the repository root
        * by default,
          * `"/"`
      * `--info`
        * == a list of key-value pairs during sync process; these infos will be persisted in app
        * by default,
          * `[]`
      * `--assumeYes`
        * == assume yes as answer for all user queries or prompts
        * by default,
          * `false`
      * `--preview-changes`
        * == preview difference against the target and live state before syncing app and wait for user confirmation
        * by default,
          * `false`
      * `--project`
        * == sync apps that belong to the specified projects; option may be specified repeatedly
        * by default,
          * `[]`
      * `--output` / `-o`
        * == output format
        * ALLOWED values: `json` | `yaml` | `wide` | `tree` | `tree=detailed`
        * by default,
          * `"wide"`
      * `--app-namespace` / `-N`
        * == only sync an application in namespace
        * by default,
          * `""`
      * `--ignore-normalizer-jq-execution-timeout`
        * == set ignore normalizer JQ execution timeout
        * by default,
          * `normalizers.DefaultJQExecutionTimeout`
      * `--revisions`
        * == show manifests at specific revisions for source position in source-positions
        * by default,
          * `[]`
      * `--source-positions`
        * == list of source positions; counting starts at 1
        * by default,
          * `[]`
      * `--source-names`
        * == list of source names
        * by default,
          * `[]`

* _Examples:_ 
  ```
  # Sync an app
  argocd app sync my-app
  
  # Sync multiples apps
  argocd app sync my-app other-app
  
  # Sync apps by label, in this example we sync apps that are children of another app (aka app-of-apps)
  argocd app sync -l app.kubernetes.io/instance=my-app
  argocd app sync -l app.kubernetes.io/instance!=my-app
  argocd app sync -l app.kubernetes.io/instance
  argocd app sync -l '!app.kubernetes.io/instance'
  argocd app sync -l 'app.kubernetes.io/instance notin (my-app,other-app)'
  
  # Sync a multi-source application for specific revision of specific sources
  argocd app sync my-app --revisions 0.0.1 --source-positions 1 --revisions 0.0.2 --source-positions 2
  argocd app sync my-app --revisions 0.0.1 --source-names my-chart --revisions 0.0.2 --source-names my-values
  
  # Sync a specific resource
  # Resource should be formatted as GROUP:KIND:NAME. If no GROUP is specified then :KIND:NAME
  argocd app sync my-app --resource :Service:my-service
  argocd app sync my-app --resource argoproj.io:Rollout:my-rollout
  argocd app sync my-app --resource '!apps:Deployment:my-service'
  argocd app sync my-app --resource apps:Deployment:my-service --resource :Service:my-service
  argocd app sync my-app --resource '!*:Service:*'
  # Specify namespace if the application has resources with the same name in different namespaces
  argocd app sync my-app --resource argoproj.io:Rollout:my-namespace/my-rollout
  ```

# `func NewApplicationHistoryCommand(clientOpts *argocdclient.ClientOptions) *cobra.Command {`
* `argocd app history APPNAME [FLAG]`
  * `FLAG`
    * ALLOWED ones
      * `--app-namespace` / `-N`
        * == only show application deployment history in namespace
        * by default,
          * `""`
      * `--output` / `-o`
        * == output format
        * ALLOWED values: `wide` | `id`
        * by default,
          * `"wide"`

# `func NewApplicationRollbackCommand(clientOpts *argocdclient.ClientOptions) *cobra.Command {`
* `argocd app rollback APPNAME [ID] [FLAG]`
  * allows
    * rollback an application 
      * if you omit `ID` -- to a --> PREVIOUS deployed version
      * if you specify ID -- to a -> specified application version
  * `FLAG`
    * ALLOWED ones
      * `--prune`
        * == allow deleting unexpected resources
        * by default,
          * `false`
      * `--timeout`
        * == time out after this many seconds
        * by default,
          * `defaultCheckTimeoutSeconds`
      * `--output` / `-o`
        * == output format
        * ALLOWED values: `json` | `yaml` | `wide` | `tree` | `tree=detailed`
        * by default,
          * `"wide"`
      * `--app-namespace` / `-N`
        * == rollback application in namespace
        * by default,
          * `""`

# `func NewApplicationManifestsCommand(clientOpts *argocdclient.ClientOptions) *cobra.Command {`
* `argocd app manifests APPNAME [FLAG]`
  * print application's manifests
  * `FLAG`
    * ALLOWED ones
      * `--source`
        * == source of manifests
        * ALLOWED values: `live` | `git`
        * by default,
          * `"git"`
      * `--revision`
        * == show manifests at a specific revision
        * by default,
          * `""`
      * `--revisions`
        * == show manifests at specific revisions for the source at position in source-positions
        * by default,
          * `[]`
      * `--source-positions`
        * == list of source positions; counting starts at 1
        * by default,
          * `[]`
      * `--source-names`
        * == list of source names
        * by default,
          * `[]`
      * `--local`
        * == if set, show locally-generated manifests; value is the absolute path to app manifests within the manifest repo
        * _Example:_ `/home/username/apps/env/app-1`
        * by default,
          * `""`
      * `--local-repo-root`
        * == path to the local repository root; used together with `--local` allows setting the repository root
        * _Example:_ `/home/username/apps`
        * by default,
          * `"."`
* _Examples:_ 
  ```
  # Get manifests for an application
  argocd app manifests my-app
  
  # Get manifests for an application at a specific revision
  argocd app manifests my-app --revision 0.0.1
  
  # Get manifests for a multi-source application at specific revisions for specific sources
  argocd app manifests my-app --revisions 0.0.1 --source-names src-base --revisions 0.0.2 --source-names src-values
  
  # Get manifests for a multi-source application at specific revisions for specific sources
  argocd app manifests my-app --revisions 0.0.1 --source-positions 1 --revisions 0.0.2 --source-positions 2
  ```

# `func NewApplicationTerminateOpCommand(clientOpts *argocdclient.ClientOptions) *cobra.Command {`
* `argocd app terminate-op APPNAME`
  * terminate application's running operation

# `func NewApplicationEditCommand(clientOpts *argocdclient.ClientOptions) *cobra.Command {`
* `argocd app edit APPNAME [FLAG]`
  * edit application
  * `FLAG`
    * `app-namespace` / `N`
      * by default,
        * ""
      * Only edit application in namespace

# `func NewApplicationPatchCommand(clientOpts *argocdclient.ClientOptions) *cobra.Command {`
* `argocd app patch APPNAME [FLAG]`
  * Patch application
  * `FLAG`
    * ALLOWED ones
      * `--app-namespace` / `-N`
        * == only patch application in namespace
        * by default,
          * `""`
      * `--patch`
        * == patch body
        * by default,
          * `""`
      * `--type`
        * == the type of patch being provided
        * ALLOWED values: `json` | `merge`
        * by default,
          * `"json"`
* _Examples:_
```
# Update an application's source path using json patch
argocd app patch myapplication --patch='[{"op": "replace", "path": "/spec/source/path", "value": "newPath"}]' --type json

# Update an application's repository target revision using merge patch
argocd app patch myapplication --patch '{"spec": { "source": { "targetRevision": "master" } }}' --type merge
```

# `func NewApplicationAddSourceCommand(clientOpts *argocdclient.ClientOptions) *cobra.Command {`
* `argocd app add-source APPNAME`
  * TODO: 
          Short: "Adds a source to the list of sources in the application",
          Example: `  # Append a source to the list of sources in the application
    argocd app add-source guestbook --repo https://github.com/argoproj/argocd-example-apps.git --path guestbook --source-name guestbook`,
          Run: func(c *cobra.Command, args []string) {
              ctx := c.Context()
              if len(args) != 1 {
                  c.HelpFunc()(c, args)
                  os.Exit(1)
              }

              argocdClient := headless.NewClientOrDie(clientOpts, c)
              conn, appIf := argocdClient.NewApplicationClientOrDie()
              defer utilio.Close(conn)

              appName, appNs := argo.ParseFromQualifiedName(args[0], appNamespace)

              app, err := appIf.Get(ctx, &application.ApplicationQuery{
                  Name:         &appName,
                  Refresh:      getRefreshType(false, false),
                  AppNamespace: &appNs,
              })

              errors.CheckError(err)

              if c.Flags() == nil {
                  errors.Fatal(errors.ErrorGeneric, "ApplicationSource needs atleast repoUrl, path or chart or ref field. No source to add.")
              }

              if len(app.Spec.Sources) > 0 {
                  appSource, _ := cmdutil.ConstructSource(&argoappv1.ApplicationSource{}, appOpts, c.Flags())

                  // sourcePosition is the index at which new source will be appended to spec.Sources
                  sourcePosition := len(app.Spec.GetSources())
                  app.Spec.Sources = append(app.Spec.Sources, *appSource)

                  setParameterOverrides(app, appOpts.Parameters, sourcePosition)

                  _, err = appIf.UpdateSpec(ctx, &application.ApplicationUpdateSpecRequest{
                      Name:         &app.Name,
                      Spec:         &app.Spec,
                      Validate:     &appOpts.Validate,
                      AppNamespace: &appNs,
                  })
                  errors.CheckError(err)

                  fmt.Printf("Application '%s' updated successfully\n", app.Name)
              } else {
                  errors.Fatal(errors.ErrorGeneric, fmt.Sprintf("Cannot add source: application %s does not have spec.sources defined", appName))
              }
          },
      }
      cmdutil.AddAppFlags(command, &appOpts)
      command.Flags().StringVarP(&appNamespace, "app-namespace", "N", "", "Namespace of the target application where the source will be appended")
      return command
  }

// NewApplicationRemoveSourceCommand returns a new instance of an `argocd app remove-source` command
# func NewApplicationRemoveSourceCommand(clientOpts *argocdclient.ClientOptions) *cobra.Command {
	var (
		sourcePosition int
		sourceName     string
		appNamespace   string
	)
	command := &cobra.Command{
		Use:   "remove-source APPNAME",
		Short: "Remove a source from multiple sources application.",
		Example: `  # Remove the source at position 1 from application's sources. Counting starts at 1.
  argocd app remove-source myapplication --source-position 1

  # Remove the source named "test" from application's sources.
  argocd app remove-source myapplication --source-name test`,
		Run: func(c *cobra.Command, args []string) {
			ctx := c.Context()

			if len(args) != 1 {
				c.HelpFunc()(c, args)
				os.Exit(1)
			}

			if sourceName == "" && sourcePosition <= 0 {
				errors.Fatal(errors.ErrorGeneric, "Value of source-position must be greater than 0")
			}

			argocdClient := headless.NewClientOrDie(clientOpts, c)
			conn, appIf := argocdClient.NewApplicationClientOrDie()
			defer utilio.Close(conn)

			appName, appNs := argo.ParseFromQualifiedName(args[0], appNamespace)

			app, err := appIf.Get(ctx, &application.ApplicationQuery{
				Name:         &appName,
				Refresh:      getRefreshType(false, false),
				AppNamespace: &appNs,
			})
			errors.CheckError(err)

			if sourceName != "" && sourcePosition != -1 {
				errors.Fatal(errors.ErrorGeneric, "Only one of source-position and source-name can be specified.")
			}

			if sourceName != "" {
				sourceNameToPosition := getSourceNameToPositionMap(app)
				pos, ok := sourceNameToPosition[sourceName]
				if !ok {
					log.Fatalf("Unknown source name '%s'", sourceName)
				}
				sourcePosition = int(pos)
			}

			if !app.Spec.HasMultipleSources() {
				errors.Fatal(errors.ErrorGeneric, "Application does not have multiple sources configured")
			}

			if len(app.Spec.GetSources()) == 1 {
				errors.Fatal(errors.ErrorGeneric, "Cannot remove the only source remaining in the app")
			}

			if len(app.Spec.GetSources()) < sourcePosition {
				errors.Fatal(errors.ErrorGeneric, fmt.Sprintf("Application does not have source at %d\n", sourcePosition))
			}

			app.Spec.Sources = append(app.Spec.Sources[:sourcePosition-1], app.Spec.Sources[sourcePosition:]...)

			promptUtil := utils.NewPrompt(clientOpts.PromptsEnabled)
			canDelete := promptUtil.Confirm("Are you sure you want to delete the source? [y/n]")
			if canDelete {
				_, err = appIf.UpdateSpec(ctx, &application.ApplicationUpdateSpecRequest{
					Name:         &app.Name,
					Spec:         &app.Spec,
					AppNamespace: &appNs,
				})
				errors.CheckError(err)

				fmt.Printf("Application '%s' updated successfully\n", app.Name)
			} else {
				fmt.Println("The command to delete the source was cancelled")
			}
		},
	}
	command.Flags().StringVarP(&appNamespace, "app-namespace", "N", "", "Namespace of the target application where the source will be appended")
	command.Flags().IntVar(&sourcePosition, "source-position", -1, "Position of the source from the list of sources of the app. Counting starts at 1.")
	command.Flags().StringVar(&sourceName, "source-name", "", "Name of the source from the list of sources of the app.")
	return command
}

# func NewApplicationConfirmDeletionCommand(clientOpts *argocdclient.ClientOptions) *cobra.Command {
	var appNamespace string
	command := &cobra.Command{
		Use:   "confirm-deletion APPNAME",
		Short: "Confirms deletion/pruning of an application resources",
		Run: func(c *cobra.Command, args []string) {
			ctx := c.Context()

			if len(args) != 1 {
				c.HelpFunc()(c, args)
				os.Exit(1)
			}

			argocdClient := headless.NewClientOrDie(clientOpts, c)
			conn, appIf := argocdClient.NewApplicationClientOrDie()
			defer utilio.Close(conn)

			appName, appNs := argo.ParseFromQualifiedName(args[0], appNamespace)

			app, err := appIf.Get(ctx, &application.ApplicationQuery{
				Name:         &appName,
				Refresh:      getRefreshType(false, false),
				AppNamespace: &appNs,
			})
			errors.CheckError(err)

			annotations := app.Annotations
			if annotations == nil {
				annotations = map[string]string{}
				app.Annotations = annotations
			}
			annotations[common.AnnotationDeletionApproved] = metav1.Now().Format(time.RFC3339)

			_, err = appIf.Update(ctx, &application.ApplicationUpdateRequest{
				Application: app,
				Validate:    new(false),
				Project:     &app.Spec.Project,
			})
			errors.CheckError(err)

			fmt.Printf("Application '%s' updated successfully\n", app.Name)
		},
	}
	command.Flags().StringVarP(&appNamespace, "app-namespace", "N", "", "Namespace of the target application where the source will be appended")
	return command
}

