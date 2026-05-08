# Config Management Plugins

* goal
  * how about config management plugins,
    * create
    * install
    * use

* Argo CD's config management tools
  * "native" ones
    * [Helm](../user-guide/helm.md)
    * [Jsonnet](../user-guide/jsonnet.md)
    * [Kustomize](../user-guide/kustomize.md)
  * custom
    * -- via -- Config Management Plugin (CMP)

* Argo CD "repo server"
  * responsible for
    * building Kubernetes manifests -- based on -- some source files (_Examples:_ Helm, OCI, or Git repository)
  * 💡if the config management plugin is CORRECTLY configured -> repo server may delegate the task of building manifests -- to the -- plugin💡

* Config management plugins
  * recommendations
    * ⚠️implement them SECURELY⚠️
      * == -- as -- Argo CD RepoServer's sidecar🧠
  * _Examples:_ [here](/examples/plugins)

## how to install a config management plugin?

* ways
  * [-- as -- sidecar plugin to repo-server](#---as----sidecar-plugin-to-repo-server)
  * -- by -- modifiying "argocd-cm" ConfigMap
    * | ArgoCD v2.4,
      * deprecated
    * ⚠️| ArgoCD v2.8,
      * removed ⚠️
    * [how to migrate plugins / configured as "argocd-cm" -- to -- sidecar plugins?](#how-to-migrate-argocd-cm-plugins----to----sidecar-plugins)

### -- as -- sidecar plugin to repo-server

* steps 
  * [write the plugin configuration file](#write-the-plugin-configuration-file)
  * [place the plugin configuration file | sidecar](#place-the-plugin-configuration-file--sidecar)
  * [register the plugin sidecar | argocd-repo-server](#register-the-plugin-sidecar--argocd-repo-server)

#### write the plugin configuration file

* [`ConfigManagementPlugin` data structure](/cmpserver/plugin/config.go)
  * ❌NOT a
    * Kubernetes object
    * CR❌
  * [notes](examples/configManagementPlugins/configManagementPlugin.yaml)

#### place the plugin configuration file | sidecar

* | "argocd-repo-server" deployment's sidecar container 
  * set `spec.template.spec.containers[0].volumeMounts[*].mountPath: /home/argocd/cmp-server/config/plugin.yaml` 

* if you use a 
  * custom image for the sidecar -> add the file directly | that image
  * stock image for the sidecar OR rather maintain the plugin configuration | ConfigMap -> NEST the plugin config file | `plugin.yaml` key

#### register the plugin sidecar | argocd-repo-server

* | "argocd-repo-server" deployment's sidecar container
  * set `spec.template.spec.containers[0].command: [/var/run/argocd/argocd-cmp-server]`

* argocd-cmp-server
  * == GRPC service
    * lightweight
    * allows
      * Argo CD can interact -- with the -- plugin

## AVAILABLE environment variables | your plugin

* Plugin commands
  * have access to
    1. sidecar's system environment variables 
    2. [Standard build environment variables](../user-guide/build-environment.md)
    3. variables | `Application`'s `spec.source.plugin.env`
       * ⚠️BEFORE reaching the `init.command`, `generate.command`, and `discover.find.command` commands,
         * Argo CD prefixes them with `ARGOCD_ENV_`⚠️
       * Reason:🧠prevent users can set potentially-sensitive environment variables🧠
    4. parameters | `Application`'s `spec.source.plugin.parameters`
       * AVAILABLE
         * | `ARGOCD_APP_PARAMETERS` environment variable, -- as -- JSON
         * as individual environment variable
           * `PARAM_<PARAMETER_NAME>`
   
* `ConfigManagementPlugin`'s `parameters`
  * ❌NOT AVAILABLE | `ARGOCD_APP_PARAMETERS`❌
    * ⚠️EVEN if you specify defaults⚠️

* recommendations
  * | your plugin,
    * sanitize/escape user input
      * Reason:🧠prevent malicious input can cause unwanted behavior🧠

## how to use a config management plugin | Application?

* ⚠️ONLY 1! POSSIBLE CMP / EACH Application⚠️

* | Application,
  * `spec.source.plugin.name`
    * OPTIONAL
      * if you do NOT specify -> use the plugin / match with, | ConfigManagementPlugin,
        * `spec.discover.fileName`
        * `spec.discover.find.glob`
        * `spec.discover.find.command`
    * allows
      * specify DIRECTLY the plugin / Application use 
    * == `<APPLICATION_metadata.name>-<APPLICATION_spec.version>`
      * `<APPLICATION_spec.version>`
        * ONLY if it's specified | `ConfigManagementPlugin`

* Problems:
  * Problem1: CMP command takes too long -> command will be killed & display an error | UI
    * Reason:🧠CMP server respects the timeouts / set | "argocd-cmd-params-cm"
      * `server.repo.server.timeout.seconds`
      * `controller.repo.server.timeout.seconds`🧠
    * SOLUTION: 
      * | "argocd-cmd-params-cm", increase
        * `server.repo.server.timeout.seconds:60`
        * `controller.repo.server.timeout.seconds:60`
      * | [`ARGOCD_EXEC_TIMEOUT`](high_availability.md),
        * adjust it -- SIMILAR to -- PREVIOUS ones
  * Problem2: if a CMP renders blank manifests & `prune=true` -> Argo CD AUTOMATICALLY remove resources
    * SOLUTION: CMP plugin authors should ensure errors == part of the exit code
      * _Example:_ output ANY error | pipe
  
        ```shell
        # pipe / does NOT pass error
        kustomize build | cat
      
        # pipe / pass error
        set -o pipefail
        kustomize build | cat 
        ```

TODO: 
> [!NOTE]
> If a CMP command fails to gracefully exit on `ARGOCD_EXEC_TIMEOUT`, 
> it will be forcefully killed after an additional timeout of `ARGOCD_EXEC_FATAL_TIMEOUT`.

## how to debug a CMP?

If you are actively developing a sidecar-installed CMP, keep a few things in mind:

1. If you are mounting plugin.yaml from a ConfigMap, you will have to restart the repo-server Pod so the plugin will
   pick up the changes.
2. If you have baked plugin.yaml into your image, you will have to build, push, and force a re-pull of that image on the
   repo-server Pod so the plugin will pick up the changes. If you are using `:latest`, the Pod will always pull the new
   image. If you're using a different, static tag, set `imagePullPolicy: Always` on the CMP's sidecar container.
3. CMP errors are cached by the repo-server in Redis. Restarting the repo-server Pod will not clear the cache. Always
   do a "Hard Refresh" when actively developing a CMP so you have the latest output.
4. Verify your sidecar has started properly by viewing the Pod and seeing that two containers are running `kubectl get pod -l app.kubernetes.io/component=repo-server -n argocd`
5. Write log message to stderr and set the `--loglevel=info` flag in the sidecar. This will print everything written to stderr, even on successful command execution.


### Common Errors
#### "no matches for kind "ConfigManagementPlugin" in version "argoproj.io/v1alpha1"" 
* Reason: 🧠you are using ["argocd-cm" ConfigMap approach](#how-to-install-a-config-management-plugin)🧠
* Solution: use ["repo-server"'s sidecar](#---as----sidecar-plugin-to-repo-server)

## Plugin tar stream exclusions

In order to increase the speed of manifest generation, certain files and folders can be excluded from being sent to your
plugin. We recommend excluding your `.git` folder if it isn't necessary. Use Go's
[filepatch.Match](https://pkg.go.dev/path/filepath#Match) syntax. For example, `.git/*` to exclude `.git` folder.

You can set it one of three ways:

1. The `--plugin-tar-exclude` argument on the repo server.
2. The `reposerver.plugin.tar.exclusions` key if you are using `argocd-cmd-params-cm`
3. Directly setting `ARGOCD_REPO_SERVER_PLUGIN_TAR_EXCLUSIONS` environment variable on the repo server.

For option 1, the flag can be repeated multiple times. For option 2 and 3, you can specify multiple globs by separating
them with semicolons.

## Application manifests generation using argocd.argoproj.io/manifest-generate-paths

To enhance the application manifests generation process, you can enable the use of the `argocd.argoproj.io/manifest-generate-paths` annotation. When this flag is enabled, the resources specified by this annotation will be passed to the CMP server for generating application manifests, rather than sending the entire repository. This can be particularly useful for monorepos.

You can set it one of three ways:

1. The `--plugin-use-manifest-generate-paths` argument on the repo server.
2. The `reposerver.plugin.use.manifest.generate.paths` key if you are using `argocd-cmd-params-cm`
3. Directly setting `ARGOCD_REPO_SERVER_PLUGIN_USE_MANIFEST_GENERATE_PATHS` environment variable on the repo server to `true`.

## how to migrate argocd-cm plugins -- to -- sidecar plugins?

TODO: 
CMP plugins work by adding a sidecar to `argocd-repo-server` along with a configuration in that sidecar located at `/home/argocd/cmp-server/config/plugin.yaml`. A argocd-cm plugin can be easily converted with the following steps.

### Convert the ConfigMap entry into a config file

First, copy the plugin's configuration into its own YAML file. Take for example the following ConfigMap entry:

```yaml
data:
  configManagementPlugins: |
    - name: pluginName
      init:                          # Optional command to initialize application source directory
        command: ["sample command"]
        args: ["sample args"]
      generate:                      # Command to generate Kubernetes Objects in either YAML or JSON
        command: ["sample command"]
        args: ["sample args"]
      lockRepo: true                 # Defaults to false. See below.
```

The `pluginName` item would be converted to a config file like this:

```yaml
apiVersion: argoproj.io/v1alpha1
kind: ConfigManagementPlugin
metadata:
  name: pluginName
spec:
  init:                          # Optional command to initialize application source directory
    command: ["sample command"]
    args: ["sample args"]
  generate:                      # Command to generate Kubernetes Objects in either YAML or JSON
    command: ["sample command"]
    args: ["sample args"]
```

> [!NOTE]
> The `lockRepo` key is not relevant for sidecar plugins, because sidecar plugins do not share a single source repo
> directory when generating manifests.

Next, we need to decide how this yaml is going to be added to the sidecar. We can either bake the yaml directly into the image, or we can mount it from a ConfigMap. 

If using a ConfigMap, our example would look like this:

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: pluginName
  namespace: argocd
data:
  pluginName.yaml: |
    apiVersion: argoproj.io/v1alpha1
    kind: ConfigManagementPlugin
    metadata:
      name: pluginName
    spec:
      init:                          # Optional command to initialize application source directory
        command: ["sample command"]
        args: ["sample args"]
      generate:                      # Command to generate Kubernetes Objects in either YAML or JSON
        command: ["sample command"]
        args: ["sample args"]
```

Then this would be mounted in our plugin sidecar.

### Write discovery rules for your plugin

Sidecar plugins can use either discovery rules or a plugin name to match Applications to plugins. If the discovery rule is omitted 
then you have to explicitly specify the plugin by name in the app spec or else that particular plugin will not match any app.

If you want to use discovery instead of the plugin name to match applications to your plugin, write rules applicable to 
your plugin [using the instructions above](#write-discovery-rules-for-your-plugin) and add them to your configuration 
file.

To use the name instead of discovery, update the name in your application manifest to `<metadata.name>-<spec.version>` 
if version was mentioned in the `ConfigManagementPlugin` spec or else just use `<metadata.name>`. For example:

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: guestbook
spec:
  source:
    plugin:
      name: pluginName  # Delete this for auto-discovery (and set `plugin: {}` if `name` was the only value) or use proper sidecar plugin name
```

### Make sure the plugin has access to the tools it needs

Plugins configured with argocd-cm ran on the Argo CD image. This gave it access to all the tools installed on that
image by default (see the [Dockerfile](https://github.com/argoproj/argo-cd/blob/master/Dockerfile) for base image and
installed tools).

You can either use a stock image (like ubuntu, busybox, or alpine/k8s) or design your own base image with the tools your plugin needs. For
security, avoid using images with more binaries installed than what your plugin actually needs.

### Test the plugin

After installing the plugin as a sidecar [according to the directions above](#installing-a-config-management-plugin),
test it out on a few Applications before migrating all of them to the sidecar plugin.

Once tests have checked out, remove the plugin entry from your argocd-cm ConfigMap.

### Additional Settings

#### Preserve repository files mode

By default, config management plugin receives source repository files with reset file mode. This is done for security
reasons. If you want to preserve original file mode, you can set `preserveFileMode` to `true` in the plugin spec:

> [!WARNING]
> Make sure you trust the plugin you are using. If you set `preserveFileMode` to `true` then the plugin might receive
> files with executable permissions which can be a security risk.

```yaml
apiVersion: argoproj.io/v1alpha1
kind: ConfigManagementPlugin
metadata:
  name: pluginName
spec:
  init:
    command: ["sample command"]
    args: ["sample args"]
  generate:
    command: ["sample command"]
    args: ["sample args"]
  preserveFileMode: true
```

##### Provide Git Credentials

By default, the config management plugin is responsible for providing its own credentials to additional Git repositories
that may need to be accessed during manifest generation. The reposerver has these credentials available in its git creds
store. When credential sharing is allowed, the git credentials used by the reposerver to clone the repository contents
are shared for the lifetime of the execution of the config management plugin, utilizing git's `ASKPASS` method to make a
call from the config management sidecar container to the reposerver to retrieve the initialized git credentials.

Utilizing `ASKPASS` means that credentials are not proactively shared, but rather only provided when an operation requires
them.

`ASKPASS` requires a socket to be shared between the config management plugin and the reposerver. To mitigate path traversal
attacks, it's recommended to use a dedicated volume to share the socket, and mount it in the reposerver and sidecar.
To change the socket path, you must set the `ARGOCD_ASK_PASS_SOCK` environment variable for both containers.

To allow the plugin to access the reposerver git credentials, you can set `provideGitCreds` to `true` in the plugin spec:

> [!WARNING]
> Make sure you trust the plugin you are using. If you set `provideGitCreds` to `true` then the plugin will receive
> credentials used to clone the source Git repository.

```yaml
apiVersion: argoproj.io/v1alpha1
kind: ConfigManagementPlugin
metadata:
  name: pluginName
spec:
  init:
    command: ["sample command"]
    args: ["sample args"]
  generate:
    command: ["sample command"]
    args: ["sample args"]
  provideGitCreds: true
```

