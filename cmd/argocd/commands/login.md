// NewLoginCommand returns a new instance of `argocd login` command
# `func NewLoginCommand(globalClientOpts *argocdclient.ClientOptions) *cobra.Command {`
	var (
		ctxName          string
		username         string
		password         string
		sso              bool
		callback         string
		ssoPort          int
		skipTestTLS      bool
		ssoLaunchBrowser bool
	)
	command := &cobra.Command{
		Use:   "login SERVER",
		Short: "Log in to Argo CD",
		Long:  "Log in to Argo CD",
		Example: ``,
		Run: func(c *cobra.Command, args []string) {
			ctx := c.Context()

			var server string

			if len(args) != 1 && !globalClientOpts.PortForward && !globalClientOpts.Core {
				c.HelpFunc()(c, args)
				os.Exit(1)
			}

			switch {
			case globalClientOpts.PortForward:
				server = "port-forward"
			case globalClientOpts.Core:
				server = "kubernetes"
			default:
				server = args[0]

				if !skipTestTLS {
					dialTime := 30 * time.Second
					tlsTestResult, err := grpc_util.TestTLS(server, dialTime)
					errors.CheckError(err)
					if !tlsTestResult.TLS {
						if !globalClientOpts.PlainText {
							if !cli.AskToProceed("WARNING: server is not configured with TLS. Proceed (y/n)? ") {
								os.Exit(1)
							}
							globalClientOpts.PlainText = true
						}
					} else if tlsTestResult.InsecureErr != nil {
						if !globalClientOpts.Insecure {
							if !cli.AskToProceed(fmt.Sprintf("WARNING: server certificate had error: %s. Proceed insecurely (y/n)? ", tlsTestResult.InsecureErr)) {
								os.Exit(1)
							}
							globalClientOpts.Insecure = true
						}
					}
				}
			}
			clientOpts := argocdclient.ClientOptions{
				ConfigPath:           "",
				ServerAddr:           server,
				Insecure:             globalClientOpts.Insecure,
				PlainText:            globalClientOpts.PlainText,
				ClientCertFile:       globalClientOpts.ClientCertFile,
				ClientCertKeyFile:    globalClientOpts.ClientCertKeyFile,
				GRPCWeb:              globalClientOpts.GRPCWeb,
				GRPCWebRootPath:      globalClientOpts.GRPCWebRootPath,
				PortForward:          globalClientOpts.PortForward,
				PortForwardNamespace: globalClientOpts.PortForwardNamespace,
				Headers:              globalClientOpts.Headers,
				KubeOverrides:        globalClientOpts.KubeOverrides,
				ServerName:           globalClientOpts.ServerName,
			}

			if ctxName == "" {
				ctxName = server
				if globalClientOpts.GRPCWebRootPath != "" {
					rootPath := strings.TrimRight(strings.TrimLeft(globalClientOpts.GRPCWebRootPath, "/"), "/")
					ctxName = fmt.Sprintf("%s/%s", server, rootPath)
				}
			}

			// Perform the login
			var tokenString string
			var refreshToken string
			if !globalClientOpts.Core {
				acdClient := headless.NewClientOrDie(&clientOpts, c)
				setConn, setIf := acdClient.NewSettingsClientOrDie()
				defer utilio.Close(setConn)
				if !sso {
					tokenString = passwordLogin(ctx, acdClient, username, password)
				} else {
					httpClient, err := acdClient.HTTPClient()
					errors.CheckError(err)
					ctx = oidc.ClientContext(ctx, httpClient)
					acdSet, err := setIf.Get(ctx, &settingspkg.SettingsQuery{})
					errors.CheckError(err)
					oauth2conf, provider, err := acdClient.OIDCConfig(ctx, acdSet)
					errors.CheckError(err)
					tokenString, refreshToken = oauth2Login(ctx, callback, ssoPort, acdSet.GetOIDCConfig(), oauth2conf, provider, ssoLaunchBrowser)
				}
				parser := jwt.NewParser(jwt.WithoutClaimsValidation())
				claims := jwt.MapClaims{}
				_, _, err := parser.ParseUnverified(tokenString, &claims)
				errors.CheckError(err)
				fmt.Printf("'%s' logged in successfully\n", userDisplayName(claims))
			}

			// login successful. Persist the config
			localCfg, err := localconfig.ReadLocalConfig(globalClientOpts.ConfigPath)
			errors.CheckError(err)
			if localCfg == nil {
				localCfg = &localconfig.LocalConfig{}
			}
			localCfg.UpsertServer(localconfig.Server{
				Server:          server,
				PlainText:       globalClientOpts.PlainText,
				Insecure:        globalClientOpts.Insecure,
				GRPCWeb:         globalClientOpts.GRPCWeb,
				GRPCWebRootPath: globalClientOpts.GRPCWebRootPath,
				Core:            globalClientOpts.Core,
			})
			localCfg.UpsertUser(localconfig.User{
				Name:         ctxName,
				AuthToken:    tokenString,
				RefreshToken: refreshToken,
			})
			if ctxName == "" {
				ctxName = server
			}
			localCfg.CurrentContext = ctxName
			localCfg.UpsertContext(localconfig.ContextRef{
				Name:   ctxName,
				User:   ctxName,
				Server: server,
			})
			err = localconfig.WriteLocalConfig(*localCfg, globalClientOpts.ConfigPath)
			errors.CheckError(err)
			fmt.Printf("Context '%s' updated\n", ctxName)
		},
	}
	command.Flags().StringVar(&ctxName, "name", "", "Name to use for the context")
	command.Flags().StringVar(&username, "username", "", "The username of an account to authenticate")
	command.Flags().StringVar(&password, "password", "", "The password of an account to authenticate")
	command.Flags().BoolVar(&sso, "sso", false, "Perform SSO login")
	command.Flags().IntVar(&ssoPort, "sso-port", DefaultSSOLocalPort, "Port to run local OAuth2 login application")
	command.Flags().StringVar(&callback, "callback", "", "Scheme, Host and Port for the callback URL")
	command.Flags().BoolVar(&skipTestTLS, "skip-test-tls", false, "Skip testing whether the server is configured with TLS (this can help when the command hangs for no apparent reason)")
	command.Flags().BoolVar(&ssoLaunchBrowser, "sso-launch-browser", true, "Automatically launch the system default browser when performing SSO login")
	return command

}
* _Examples:_ 

	```
	# Login to Argo CD using a username and password
	argocd login cd.argoproj.io
	
	# Login to Argo CD using SSO
	argocd login cd.argoproj.io --sso
	
	# Configure direct access using Kubernetes API server
	argocd login cd.argoproj.io --core
	```

