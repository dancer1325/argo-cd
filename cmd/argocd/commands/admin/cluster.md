# `func NewClusterCommand(clientOpts *argocdclient.ClientOptions, pathOpts *clientcmd.PathOptions) *cobra.Command {`
* `argocd admin cluster COMMAND`
  * Manage clusters configuration
  * COMMAND
    * NewClusterConfig()
    * NewGenClusterConfigCommand(pathOpts)
    * NewClusterStatsCommand(clientOpts)
    * NewClusterShardsCommand(clientOpts)
    * NewClusterNamespacesCommand()
    * NewClusterEnableNamespacedMode()
    * NewClusterDisableNamespacedMode()
* _Examples:_
	```
	#Generate declarative config for a cluster
	argocd admin cluster generate-spec my-cluster -o yaml
	
	#Generate a kubeconfig for a cluster named "my-cluster" and display it in the console
	argocd admin cluster kubeconfig my-cluster
	
	#Print information namespaces which Argo CD manages in each cluster
	argocd admin cluster namespaces my-cluster 
	```

## `func NewClusterShardsCommand(clientOpts *argocdclient.ClientOptions) *cobra.Command {`
* `argocd admin cluster shards [FLAG]`
  * print information -- about -- 
    * EACH controller shard
      * ALSO, the estimated portion of Kubernetes resources / controller shard is responsible for
  * `FLAG`
    * `shard`
      * == Cluster shard filter
      * by default, 
        * -1
    * `--replicas`
      * == Application controller replicas count
        * if NOT specified -> inferred -- from -- number of running controller pods
      * by default,
        * `0`
    * `--sharding-method`
      * == sharding method
      * by default,
        * `legacy`
      * ALLOWED values
        * `legacy`, `round-robin`, `consistent-hashing`
    * `--port-forward-redis`
      * if `true` -> automatically port-forward HA proxy Redis -- from -- current namespace
      * by default,
        * `true`


## `func NewClusterNamespacesCommand() *cobra.Command {`
* `argocd admin cluster namespaces`
  * print cluster's information namespaces -- about -- clusters / Argo CD manages

## `func NewClusterEnableNamespacedMode() *cobra.Command {`
* `argocd admin cluster enable-namespaced-mode PATTERN [FLAG]`
  * enable namespaced mode | clusters / ' name matches the specified `PATTERN`
  * `FLAG`
    * `--dry-run`
      * print what will be performed
      * by default,
        * `true`
    * `--cluster-resources`
      * if `true` -> cluster level resources should be managed
      * by default,
        * `false`
    * `--max-namespace-count`
      * == max number of namespaces / cluster should manage
        * managed namespaces <= specified count
      * by default,
        * `0`

## `func NewClusterDisableNamespacedMode() *cobra.Command {`
* `argocd admin cluster disable-namespaced-mode PATTERN [FLAG]`
  * disable namespaced mode | clusters / ' name matches the specified `PATTERN`
  * `FLAG`
    * `--dry-run`
      * print what will be performed
      * by default,
        * `true`


## `func NewClusterStatsCommand(clientOpts *argocdclient.ClientOptions) *cobra.Command {`
* `argocd admin cluster stats [FLAG]`
  * print cluster statistics + inferred shard number
  * `FLAG`
    * `--shard`
      * == cluster shard filter
      * by default,
        * `-1`
    * `--replicas`
      * == Application controller replicas count
        * if NOT specified -> inferred -- from -- number of running controller pods
      * by default,
        * `0`
    * `--sharding-method`
      * == sharding method
      * by default,
        * `legacy`
      * ALLOWED values
        * `legacy`, `round-robin`, `consistent-hashing`
    * `--port-forward-redis`
      * if `true` -> automatically port-forward HA proxy Redis -- from -- current namespace
      * by default,
        * `true`
* _Examples:_
	```
	#Display stats and shards for clusters 
	argocd admin cluster stats
	
	#Display Cluster Statistics for a Specific Shard
	argocd admin cluster stats --shard=1
	
	#In a multi-cluster environment to print stats for a specific cluster say(target-cluster)
	argocd admin cluster stats target-cluster
	```

## `func NewClusterConfig() *cobra.Command {`
* `argocd admin cluster kubeconfig CLUSTER_URL OUTPUT_PATH`
  * generates kubeconfig -- for the -- specified cluster

* _Examples:_
	```
	#Removing a specific kubeconfig file 
	argocd admin cluster kubeconfig my-cluster --delete
	
	#Generate a Kubeconfig for a Cluster with TLS Verification Disabled
	argocd admin cluster kubeconfig https://cluster-api-url:6443 /path/to/output/kubeconfig.yaml --insecure-skip-tls-verify
	```

# `func NewGenClusterConfigCommand(pathOpts *clientcmd.PathOptions) *cobra.Command {`
* `argocd admin cluster generate-spec CONTEXT`
  * generate cluster's declarative config
    * TODO: 
            Run: func(c *cobra.Command, args []string) {
                ctx := c.Context()

                log.SetLevel(log.WarnLevel)
                var configAccess clientcmd.ConfigAccess = pathOpts
                if len(args) == 0 {
                    log.Error("Choose a context name from:")
                    cmdutil.PrintKubeContexts(configAccess)
                    os.Exit(1)
                }
                cfgAccess, err := configAccess.GetStartingConfig()
                errors.CheckError(err)
                contextName := args[0]
                clstContext := cfgAccess.Contexts[contextName]
                if clstContext == nil {
                    log.Fatalf("Context %s does not exist in kubeconfig", contextName)
                    return
                }

                if clusterOpts.InCluster && clusterOpts.ClusterEndpoint != "" {
                    log.Fatal("Can only use one of --in-cluster or --cluster-endpoint")
                    return
                }

                overrides := clientcmd.ConfigOverrides{
                    Context: *clstContext,
                }
                clientConfig := clientcmd.NewDefaultClientConfig(*cfgAccess, &overrides)
                conf, err := clientConfig.ClientConfig()
                errors.CheckError(err)
                // Seed a minimal in-memory Argo CD environment so settings retrieval succeeds
                argoCDCM := &corev1.ConfigMap{
                    TypeMeta: metav1.TypeMeta{Kind: "ConfigMap", APIVersion: "v1"},
                    ObjectMeta: metav1.ObjectMeta{
                        Name:      common.ArgoCDConfigMapName,
                        Namespace: ArgoCDNamespace,
                        Labels: map[string]string{
                            "app.kubernetes.io/part-of": "argocd",
                        },
                    },
                }
                argoCDSecret := &corev1.Secret{
                    TypeMeta: metav1.TypeMeta{Kind: "Secret", APIVersion: "v1"},
                    ObjectMeta: metav1.ObjectMeta{
                        Name:      common.ArgoCDSecretName,
                        Namespace: ArgoCDNamespace,
                        Labels: map[string]string{
                            "app.kubernetes.io/part-of": "argocd",
                        },
                    },
                    Data: map[string][]byte{
                        "server.secretkey": []byte("test"),
                    },
                }
                kubeClientset := fake.NewClientset(argoCDCM, argoCDSecret)

                var awsAuthConf *v1alpha1.AWSAuthConfig
                var execProviderConf *v1alpha1.ExecProviderConfig
                switch {
                case clusterOpts.AwsClusterName != "":
                    awsAuthConf = &v1alpha1.AWSAuthConfig{
                        ClusterName: clusterOpts.AwsClusterName,
                        RoleARN:     clusterOpts.AwsRoleArn,
                        Profile:     clusterOpts.AwsProfile,
                    }
                case clusterOpts.ExecProviderCommand != "":
                    execProviderConf = &v1alpha1.ExecProviderConfig{
                        Command:     clusterOpts.ExecProviderCommand,
                        Args:        clusterOpts.ExecProviderArgs,
                        Env:         clusterOpts.ExecProviderEnv,
                        APIVersion:  clusterOpts.ExecProviderAPIVersion,
                        InstallHint: clusterOpts.ExecProviderInstallHint,
                    }
                case generateToken:
                    bearerToken, err = GenerateToken(clusterOpts, conf)
                    errors.CheckError(err)
                case bearerToken == "":
                    bearerToken = "bearer-token"
                }
                if clusterOpts.Name != "" {
                    contextName = clusterOpts.Name
                }

                labelsMap, err := label.Parse(labels)
                errors.CheckError(err)
                annotationsMap, err := label.Parse(annotations)
                errors.CheckError(err)

                clst := cmdutil.NewCluster(contextName, clusterOpts.Namespaces, clusterOpts.ClusterResources, conf, bearerToken, awsAuthConf, execProviderConf, labelsMap, annotationsMap)
                if clusterOpts.InClusterEndpoint() {
                    clst.Server = v1alpha1.KubernetesInternalAPIServerAddr
                }
                if clusterOpts.ClusterEndpoint == string(cmdutil.KubePublicEndpoint) {
                    // Ignore `kube-public` cluster endpoints, since this command is intended to run without invoking any network connections.
                    log.Warn("kube-public cluster endpoints are not supported. Falling back to the endpoint listed in the kubconfig context.")
                }
                if clusterOpts.Shard >= 0 {
                    clst.Shard = &clusterOpts.Shard
                }

                settingsMgr := settings.NewSettingsManager(ctx, kubeClientset, ArgoCDNamespace)
                argoDB := db.NewDB(ArgoCDNamespace, settingsMgr, kubeClientset)

                _, err = argoDB.CreateCluster(ctx, clst)
                errors.CheckError(err)

                secName, err := db.URIToSecretName("cluster", clst.Server)
                errors.CheckError(err)

                secret, err := kubeClientset.CoreV1().Secrets(ArgoCDNamespace).Get(ctx, secName, metav1.GetOptions{})
                errors.CheckError(err)

                errors.CheckError(PrintResources(outputFormat, os.Stdout, secret))
            },
        }
        command.PersistentFlags().StringVar(&pathOpts.LoadingRules.ExplicitPath, pathOpts.ExplicitFileFlag, pathOpts.LoadingRules.ExplicitPath, "use a particular kubeconfig file")
        command.Flags().StringVar(&bearerToken, "bearer-token", "", "Authentication token that should be used to access K8S API server")
        command.Flags().BoolVar(&generateToken, "generate-bearer-token", false, "Generate authentication token that should be used to access K8S API server")
        command.Flags().StringVar(&clusterOpts.ServiceAccount, "service-account", "argocd-manager", fmt.Sprintf("System namespace service account to use for kubernetes resource management. If not set then default %q SA will be used", clusterauth.ArgoCDManagerServiceAccount))
        command.Flags().StringVar(&clusterOpts.SystemNamespace, "system-namespace", common.DefaultSystemNamespace, "Use different system namespace")
        command.Flags().StringVarP(&outputFormat, "output", "o", "yaml", "Output format. One of: json|yaml")
        command.Flags().StringArrayVar(&labels, "label", nil, "Set metadata labels (e.g. --label key=value)")
        command.Flags().StringArrayVar(&annotations, "annotation", nil, "Set metadata annotations (e.g. --annotation key=value)")
        cmdutil.AddClusterFlags(command, &clusterOpts)
        return command
    }

func GenerateToken(clusterOpts cmdutil.ClusterOptions, conf *rest.Config) (string, error) {
	clientset, err := kubernetes.NewForConfig(conf)
	errors.CheckError(err)

	bearerToken, err := clusterauth.GetServiceAccountBearerToken(clientset, clusterOpts.SystemNamespace, clusterOpts.ServiceAccount, common.BearerTokenTimeout)
	if err != nil {
		return "", err
	}
	return bearerToken, nil
}
