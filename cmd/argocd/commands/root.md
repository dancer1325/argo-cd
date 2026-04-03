# `func NewCommand() *cobra.Command {`
* `argocd COMMAND [FLAG]` 
  * controls a Argo CD server
  * `COMMAND`
    * NewCompletionCommand()
    * NewVersionCmd(&clientOpts, nil)
    * NewClusterCommand(&clientOpts, pathOpts)
    * NewApplicationCommand(&clientOpts)
    * NewAppSetCommand(&clientOpts)
    * NewLoginCommand(&clientOpts)
    * NewReloginCommand(&clientOpts)
    * NewRepoCommand(&clientOpts)
    * NewRepoCredsCommand(&clientOpts)
    * NewContextCommand(&clientOpts)
    * NewProjectCommand(&clientOpts)
    * NewAccountCommand(&clientOpts)
    * NewLogoutCommand(&clientOpts)
    * NewCertCommand(&clientOpts)
    * NewGPGCommand(&clientOpts)
    * admin.NewAdminCommand(&clientOpts)
    * NewConfigureCommand(&clientOpts)
  * `FLAG`
    * `--config`
      * Path to Argo CD config
    * `--server`
      * Argo CD server address
    * `--plaintext`
      * Disable TLS
    * `--insecure`
      * Skip server certificate and domain verification
    * `--server-crt`
      * Server certificate file
    * `--client-crt`
      * Client certificate file
    * `--client-crt-key`
      * Client certificate key file
    * `--auth-token`
      * Authentication token; set this or the env variable
    * `--grpc-web`
      * Enables gRPC-web protocol. Useful if Argo CD server is behind proxy which does not support HTTP2
    * `--grpc-web-root-path`
      * Enables gRPC-web protocol. Set web root
    * `--logformat`
      * Set the logging format. One of: json|text
    * `--loglevel`
      * Set the logging level. One of: debug|info|warn|error
    * `--header` / `-H`
      * Sets additional header to all requests made by Argo CD CLI
    * `--port-forward`
      * Connect to a random argocd-server port using port forwarding
    * `--port-forward-namespace`
      * Namespace name which should be used for port forwarding
    * `--http-retry-max`
      * Maximum number of retries to establish http connection to Argo CD server
    * `--core`
      * if `true` -> CLI talks DIRECTLY -- to -- Kubernetes
        * ❌!= talk -- to -- Argo CD API server❌
    * `--argocd-context`
      * The name of the Argo-CD server context to use
    * `--server-name`
      * Name of the Argo CD API server
    * `--controller-name`
      * Name of the Argo CD Application controller
    * `--redis-haproxy-name`
      * Name of the Redis HA Proxy
    * `--redis-name`
      * Name of the Redis deployment
    * `--repo-server-name`
      * Name of the Argo CD Repo server
    * `--redis-compress`
      * Enable this if the application controller is configured with redis compression enabled. (possible values: gzip, none)
    * `--prompts-enabled`
      * Force optional interactive prompts to be enabled or disabled, overriding local configuration
    * `--kube-context`
      * Directs the command to the given kube-context

