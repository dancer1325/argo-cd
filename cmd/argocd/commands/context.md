# `func NewContextCommand(clientOpts *argocdclient.ClientOptions) *cobra.Command {`
* 's return
* NEW instance -- of -- `argocd ctx` command 
TODO: 
var deletion bool
command := &cobra.Command{
	Use:     "context [CONTEXT]",
	Aliases: []string{"ctx"},
	Short:   "Switch between contexts",
	Example: ``,
  Run: func(c *cobra.Command, args []string) {
	  localCfg, err := localconfig.ReadLocalConfig(clientOpts.ConfigPath)
	  errors.CheckError(err)
	  if localCfg == nil {
		  fmt.Println("No local configuration found")
		  os.Exit(1)
	  }

	  if deletion {
		  if len(args) == 0 {
			  c.HelpFunc()(c, args)
			  os.Exit(1)
		  }
		  err := deleteContext(args[0], clientOpts.ConfigPath)
		  errors.CheckError(err)
		  return
	  }

	  if len(args) == 0 {
		  printArgoCDContexts(clientOpts.ConfigPath)
		  return
	  }

	  ctxName := args[0]

	  argoCDDir, err := localconfig.DefaultConfigDir()
	  errors.CheckError(err)
	  prevCtxFile := path.Join(argoCDDir, ".prev-ctx")

	  if ctxName == "-" {
		  prevCtxBytes, err := os.ReadFile(prevCtxFile)
		  errors.CheckError(err)
		  ctxName = string(prevCtxBytes)
	  }
	  if localCfg.CurrentContext == ctxName {
		  fmt.Printf("Already at context '%s'\n", localCfg.CurrentContext)
		  return
	  }
	  if _, err = localCfg.ResolveContext(ctxName); err != nil {
		  log.Fatal(err)
	  }
	  prevCtx := localCfg.CurrentContext
	  localCfg.CurrentContext = ctxName

	  err = localconfig.WriteLocalConfig(*localCfg, clientOpts.ConfigPath)
	  errors.CheckError(err)
	  err = os.WriteFile(prevCtxFile, []byte(prevCtx), 0o644)
	  errors.CheckError(err)
	  fmt.Printf("Switched to context '%s'\n", localCfg.CurrentContext)
  },
}
command.Flags().BoolVar(&deletion, "delete", false, "Delete the context instead of switching to it")
return command
}
## _Examples:_ 
```
# List Argo CD Contexts
argocd context

# Switch Argo CD context
argocd context cd.argoproj.io

# Delete Argo CD context
argocd context cd.argoproj.io --delete
```
