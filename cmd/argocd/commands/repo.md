# `func NewRepoCommand(clientOpts *argocdclient.ClientOptions) *cobra.Command {`
* `argocd repo COMMAND`
  * Manage repository CONNECTION parameters
    * if you are using private repositories -> NOTHING MUST be added
  * COMMAND
    * NewRepoAddCommand(clientOpts)
    * NewRepoGetCommand(clientOpts)
    * NewRepoListCommand(clientOpts)
    * NewRepoRemoveCommand(clientOpts)

* _Examples:_
```
# Add git repository connection parameters
argocd repo add git@git.example.com:repos/repo

# Get a Configured Repository by URL
argocd repo get https://github.com/yourusername/your-repo.git

# List Configured Repositories
argocd repo list

# Remove Configured Repositories
argocd repo rm https://github.com/yourusername/your-repo.git
```

## `func NewRepoAddCommand(clientOpts *argocdclient.ClientOptions) *cobra.Command {`
* `argocd repo add REPOURL [FLAG]`
  * Add git, oci OR helm repository connection parameters
  * `FLAG`
    * `upsert`
      * by default,
        * false
      * if there are 2 repositories / SAME name ALTHOUGH the spec differs -> override the EXISTING repository 

* _Examples:_
```
# Add a Git repository via SSH using a private key for authentication, ignoring the server's host key:
argocd repo add git@git.example.com:repos/repo --insecure-ignore-host-key --ssh-private-key-path ~/id_rsa

# Add a Git repository via SSH on a non-default port - need to use ssh:// style URLs here
argocd repo add ssh://git@git.example.com:2222/repos/repo --ssh-private-key-path ~/id_rsa

# Add a Git repository via SSH using socks5 proxy with no proxy credentials
argocd repo add ssh://git@github.com/argoproj/argocd-example-apps --ssh-private-key-path ~/id_rsa --proxy socks5://your.proxy.server.ip:1080

# Add a Git repository via SSH using socks5 proxy with proxy credentials
argocd repo add ssh://git@github.com/argoproj/argocd-example-apps --ssh-private-key-path ~/id_rsa --proxy socks5://username:password@your.proxy.server.ip:1080

# Add a private Git repository via HTTPS using username/password and TLS client certificates:
argocd repo add https://git.example.com/repos/repo --username git --password secret --tls-client-cert-path ~/mycert.crt --tls-client-cert-key-path ~/mycert.key

# Add a private Git repository via HTTPS using username/password without verifying the server's TLS certificate
argocd repo add https://git.example.com/repos/repo --username git --password secret --insecure-skip-server-verification

# Add a public Helm repository named 'stable' via HTTPS
argocd repo add https://charts.helm.sh/stable --type helm --name stable  

# Add a private Helm repository named 'stable' via HTTPS
argocd repo add https://charts.helm.sh/stable --type helm --name stable --username test --password test

# Add a private Helm OCI-based repository named 'stable' via HTTPS
argocd repo add helm-oci-registry.cn-zhangjiakou.cr.aliyuncs.com --type helm --name stable --enable-oci --username test --password test

# Add a private HTTPS OCI repository named 'stable'
argocd repo add oci://helm-oci-registry.cn-zhangjiakou.cr.aliyuncs.com --type oci --name stable --username test --password test

# Add a private OCI repository named 'stable' without verifying the server's TLS certificate
argocd repo add oci://helm-oci-registry.cn-zhangjiakou.cr.aliyuncs.com --type oci --name stable --username test --password test --insecure-skip-server-verification

# Add a private HTTP OCI repository named 'stable'
argocd repo add oci://helm-oci-registry.cn-zhangjiakou.cr.aliyuncs.com --type oci --name stable --username test --password test --insecure-oci-force-http

# Add a private Git repository on GitHub.com via GitHub App. github-app-installation-id is optional, if not provided, the installation id will be fetched from the GitHub API.
argocd repo add https://git.example.com/repos/repo --github-app-id 1 --github-app-installation-id 2 --github-app-private-key-path test.private-key.pem

# Add a private Git repository on GitHub Enterprise via GitHub App. github-app-installation-id is optional, if not provided, the installation id will be fetched from the GitHub API.
argocd repo add https://ghe.example.com/repos/repo --github-app-id 1 --github-app-installation-id 2 --github-app-private-key-path test.private-key.pem --github-app-enterprise-base-url https://ghe.example.com/api/v3

# Add a private Git repository on Google Cloud Sources via GCP service account credentials
argocd repo add https://source.developers.google.com/p/my-google-cloud-project/r/my-repo --gcp-service-account-key-path service-account-key.json
```

## `func NewRepoRemoveCommand(clientOpts *argocdclient.ClientOptions) *cobra.Command {`
* `argocd repo rm REPO ... [FLAG]`
  * Remove configured repositories
  * `FLAG`
    * ALLOWED ones
      * `--project`
        * == project of the repository
        * by default,
          * `""`
* _Examples:_
```
# Remove a single repository
argocd repo rm https://github.com/yourusername/your-repo.git

# Remove multiple repositories
argocd repo rm https://github.com/yourusername/your-repo.git https://git.example.com/repo2.git

# Remove repositories for a specific project
argocd repo rm https://github.com/yourusername/your-repo.git --project myproject

# Remove repository using SSH URL
argocd repo rm git@github.com:yourusername/your-repo.git
```

## func NewRepoListCommand(clientOpts *argocdclient.ClientOptions) *cobra.Command {
* `argocd repo list [FLAG]`
  * List configured repositories
  * `FLAG`
    * ALLOWED ones
      * `--output` / `-o`
        * == output format
        * ALLOWED values: `yaml` | `json` | `url` | `wide`
        * by default,
          * `"wide"`
      * `--refresh`
        * == force a cache refresh on connection status
        * ALLOWED values: `hard`
        * by default,
          * `""`
* _Examples:_ 
	```
	# List all repositories
	argocd repo list
	
	# List repositories in wide format
	argocd repo list -o wide
	
	# List repositories in YAML format
	argocd repo list -o yaml
	
	# List repositories in JSON format
	argocd repo list -o json
	
	# List urls of repositories
	argocd repo list -o url
	
	# Force refresh of cached repository connection status
	argocd repo list --refresh hard
	```

## `func NewRepoGetCommand(clientOpts *argocdclient.ClientOptions) *cobra.Command {`
* `argocd repo get REPO [FLAG]`
  * Get a configured repository -- by -- URL
  * `FLAG`
    * ALLOWED ones
      * `--project`
        * == project of the repository
        * by default,
          * `""`
      * `--output` / `-o`
        * == output format
        * ALLOWED values: `json` | `yaml` | `wide` | `url`
        * by default,
          * `"wide"`
      * `--refresh`
        * == force a cache refresh on connection status
        * ALLOWED values: `hard`
        * by default,
          * `""`

* _Examples:_
	```
	# Get Git or Helm repository details in wide format (default, '-o wide')
	argocd repo get https://git.example.com/repos/repo
	
	# Get repository details in YAML format
	argocd repo get https://git.example.com/repos/repo -o yaml
	
	# Get repository details in JSON format
	argocd repo get https://git.example.com/repos/repo -o json
	
	# Get repository URL
	argocd repo get https://git.example.com/repos/repo -o url
	```
