# `func NewCommand() *cobra.Command {`
* `argocd-server [flags]`
  * Run the ArgoCD API server | foreground
  * TODO: 



      clientConfig = cli.AddKubectlFlagsToCmd(command)
      command.Flags().BoolVar(&insecure, "insecure", env.ParseBoolFromEnv("ARGOCD_SERVER_INSECURE", false), "Run server without TLS")
      command.Flags().StringVar(&staticAssetsDir, "staticassets", env.StringFromEnv("ARGOCD_SERVER_STATIC_ASSETS", "/shared/app"), "Directory path that contains additional static assets")
      command.Flags().StringVar(&baseHRef, "basehref", env.StringFromEnv("ARGOCD_SERVER_BASEHREF", "/"), "Value for base href in index.html. Used if Argo CD is running behind reverse proxy under subpath different from /")
      command.Flags().StringVar(&rootPath, "rootpath", env.StringFromEnv("ARGOCD_SERVER_ROOTPATH", ""), "Used if Argo CD is running behind reverse proxy under subpath different from /")
      command.Flags().StringVar(&cmdutil.LogFormat, "logformat", env.StringFromEnv("ARGOCD_SERVER_LOGFORMAT", "json"), "Set the logging format. One of: json|text")
      command.Flags().StringVar(&cmdutil.LogLevel, "loglevel", env.StringFromEnv("ARGOCD_SERVER_LOG_LEVEL", "info"), "Set the logging level. One of: debug|info|warn|error")
      command.Flags().IntVar(&glogLevel, "gloglevel", 0, "Set the glog logging level")
      command.Flags().StringVar(&repoServerAddress, "repo-server", env.StringFromEnv("ARGOCD_SERVER_REPO_SERVER", common.DefaultRepoServerAddr), "Repo server address")
      command.Flags().StringVar(&dexServerAddress, "dex-server", env.StringFromEnv("ARGOCD_SERVER_DEX_SERVER", common.DefaultDexServerAddr), "Dex server address")
      command.Flags().BoolVar(&disableAuth, "disable-auth", env.ParseBoolFromEnv("ARGOCD_SERVER_DISABLE_AUTH", false), "Disable client authentication")
      command.Flags().StringVar(&contentTypes, "api-content-types", env.StringFromEnv("ARGOCD_API_CONTENT_TYPES", "application/json", env.StringFromEnvOpts{AllowEmpty: true}), "Semicolon separated list of allowed content types for non GET api requests. Any content type is allowed if empty.")
      command.Flags().BoolVar(&enableGZip, "enable-gzip", env.ParseBoolFromEnv("ARGOCD_SERVER_ENABLE_GZIP", true), "Enable GZIP compression")
      command.AddCommand(cli.NewVersionCmd(common.CommandServer))
      command.Flags().StringVar(&listenHost, "address", env.StringFromEnv("ARGOCD_SERVER_LISTEN_ADDRESS", common.DefaultAddressAPIServer), "Listen on given address")
      command.Flags().IntVar(&listenPort, "port", common.DefaultPortAPIServer, "Listen on given port")
      command.Flags().StringVar(&metricsHost, env.StringFromEnv("ARGOCD_SERVER_METRICS_LISTEN_ADDRESS", "metrics-address"), common.DefaultAddressAPIServerMetrics, "Listen for metrics on given address")
      command.Flags().IntVar(&metricsPort, "metrics-port", common.DefaultPortArgoCDAPIServerMetrics, "Start metrics on given port")
      command.Flags().StringVar(&otlpAddress, "otlp-address", env.StringFromEnv("ARGOCD_SERVER_OTLP_ADDRESS", ""), "OpenTelemetry collector address to send traces to")
      command.Flags().BoolVar(&otlpInsecure, "otlp-insecure", env.ParseBoolFromEnv("ARGOCD_SERVER_OTLP_INSECURE", true), "OpenTelemetry collector insecure mode")
      command.Flags().StringToStringVar(&otlpHeaders, "otlp-headers", env.ParseStringToStringFromEnv("ARGOCD_SERVER_OTLP_HEADERS", map[string]string{}, ","), "List of OpenTelemetry collector extra headers sent with traces, headers are comma-separated key-value pairs(e.g. key1=value1,key2=value2)")
      command.Flags().StringSliceVar(&otlpAttrs, "otlp-attrs", env.StringsFromEnv("ARGOCD_SERVER_OTLP_ATTRS", []string{}, ","), "List of OpenTelemetry collector extra attrs when send traces, each attribute is separated by a colon(e.g. key:value)")
      command.Flags().IntVar(&repoServerTimeoutSeconds, "repo-server-timeout-seconds", env.ParseNumFromEnv("ARGOCD_SERVER_REPO_SERVER_TIMEOUT_SECONDS", 60, 0, math.MaxInt64), "Repo server RPC call timeout seconds.")
      command.Flags().StringVar(&frameOptions, "x-frame-options", env.StringFromEnv("ARGOCD_SERVER_X_FRAME_OPTIONS", "sameorigin"), "Set X-Frame-Options header in HTTP responses to `value`. To disable, set to \"\".")
      command.Flags().StringVar(&contentSecurityPolicy, "content-security-policy", env.StringFromEnv("ARGOCD_SERVER_CONTENT_SECURITY_POLICY", "frame-ancestors 'self';"), "Set Content-Security-Policy header in HTTP responses to `value`. To disable, set to \"\".")
      command.Flags().BoolVar(&repoServerPlaintext, "repo-server-plaintext", env.ParseBoolFromEnv("ARGOCD_SERVER_REPO_SERVER_PLAINTEXT", false), "Use a plaintext client (non-TLS) to connect to repository server")
      command.Flags().BoolVar(&repoServerStrictTLS, "repo-server-strict-tls", env.ParseBoolFromEnv("ARGOCD_SERVER_REPO_SERVER_STRICT_TLS", false), "Perform strict validation of TLS certificates when connecting to repo server")
      command.Flags().BoolVar(&dexServerPlaintext, "dex-server-plaintext", env.ParseBoolFromEnv("ARGOCD_SERVER_DEX_SERVER_PLAINTEXT", false), "Use a plaintext client (non-TLS) to connect to dex server")
      command.Flags().BoolVar(&dexServerStrictTLS, "dex-server-strict-tls", env.ParseBoolFromEnv("ARGOCD_SERVER_DEX_SERVER_STRICT_TLS", false), "Perform strict validation of TLS certificates when connecting to dex server")
      command.Flags().StringSliceVar(&applicationNamespaces, "application-namespaces", env.StringsFromEnv("ARGOCD_APPLICATION_NAMESPACES", []string{}, ","), "List of additional namespaces where application resources can be managed in")
      command.Flags().BoolVar(&enableProxyExtension, "enable-proxy-extension", env.ParseBoolFromEnv("ARGOCD_SERVER_ENABLE_PROXY_EXTENSION", false), "Enable Proxy Extension feature")
      command.Flags().IntVar(&webhookParallelism, "webhook-parallelism-limit", env.ParseNumFromEnv("ARGOCD_SERVER_WEBHOOK_PARALLELISM_LIMIT", 50, 1, 1000), "Number of webhook requests processed concurrently")
      command.Flags().StringSliceVar(&enableK8sEvent, "enable-k8s-event", env.StringsFromEnv("ARGOCD_ENABLE_K8S_EVENT", argo.DefaultEnableEventList(), ","), "Enable ArgoCD to use k8s event. For disabling all events, set the value as `none`. (e.g --enable-k8s-event=none), For enabling specific events, set the value as `event reason`. (e.g --enable-k8s-event=StatusRefreshed,ResourceCreated)")
      command.Flags().BoolVar(&hydratorEnabled, "hydrator-enabled", env.ParseBoolFromEnv("ARGOCD_HYDRATOR_ENABLED", false), "Feature flag to enable Hydrator. Default (\"false\")")
      command.Flags().BoolVar(&syncWithReplaceAllowed, "sync-with-replace-allowed", env.ParseBoolFromEnv("ARGOCD_SYNC_WITH_REPLACE_ALLOWED", true), "Whether to allow users to select replace for syncs from UI/CLI")

      // Flags related to the applicationSet component.
      command.Flags().StringVar(&scmRootCAPath, "appset-scm-root-ca-path", env.StringFromEnv("ARGOCD_APPLICATIONSET_CONTROLLER_SCM_ROOT_CA_PATH", ""), "Provide Root CA Path for self-signed TLS Certificates")
      command.Flags().BoolVar(&enableScmProviders, "appset-enable-scm-providers", env.ParseBoolFromEnv("ARGOCD_APPLICATIONSET_CONTROLLER_ENABLE_SCM_PROVIDERS", true), "Enable retrieving information from SCM providers, used by the SCM and PR generators (Default: true)")
      command.Flags().StringSliceVar(&allowedScmProviders, "appset-allowed-scm-providers", env.StringsFromEnv("ARGOCD_APPLICATIONSET_CONTROLLER_ALLOWED_SCM_PROVIDERS", []string{}, ","), "The list of allowed custom SCM provider API URLs. This restriction does not apply to SCM or PR generators which do not accept a custom API URL. (Default: Empty = all)")
      command.Flags().BoolVar(&enableNewGitFileGlobbing, "appset-enable-new-git-file-globbing", env.ParseBoolFromEnv("ARGOCD_APPLICATIONSET_CONTROLLER_ENABLE_NEW_GIT_FILE_GLOBBING", false), "Enable new globbing in Git files generator.")
      command.Flags().BoolVar(&enableGitHubAPIMetrics, "appset-enable-github-api-metrics", env.ParseBoolFromEnv("ARGOCD_APPLICATIONSET_CONTROLLER_ENABLE_GITHUB_API_METRICS", false), "Enable GitHub API metrics for generators that use the GitHub API")

      tlsConfigCustomizerSrc = tls.AddTLSFlagsToCmd(command)
      cacheSrc = servercache.AddCacheFlagsToCmd(command, cacheutil.Options{
          OnClientCreated: func(client *redis.Client) {
              redisClient = client
          },
      })
      repoServerCacheSrc = reposervercache.AddCacheFlagsToCmd(command, cacheutil.Options{FlagPrefix: "repo-server-"})


* _Examples:_
```
# Start the Argo CD API server with default settings
$ argocd-server

# Start the Argo CD API server on a custom port and enable tracing
$ argocd-server --port 8888 --otlp-address localhost:4317
```