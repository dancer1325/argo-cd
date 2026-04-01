# `func NewSettingsCommand() *cobra.Command {`
* `argocd admin settings COMMAND [FLAGS]`
  * allows
    * about COMMANDs,
      * validate
      * troubleshoot
  * AVAILABLE `COMMAND`
    * NewValidateSettingsCommand(&opts)
    * NewResourceOverridesCommand(&opts)
    * NewRBACCommand()
  * AVAILABLE `[FLAGS]` 
    * `argocd-cm-path`
      * == Path -- to -- local argocd-cm.yaml file
    * `argocd-secret-path`
      * == Path -- to -- local argocd-secret.yaml file
    * `load-cluster-settings`
      * by default,
        * false
      * UNLESS local file path is provided, config map & secret should be loaded -- from -- cluster

# `func NewValidateSettingsCommand(cmdCtx commandContext) *cobra.Command {`
* `argocd admin settings validate [FLAGS]`
  * validate the settings / specified | 
    * 'argocd-cm' ConfigMap
    * 'argocd-secret' Secret
  * AVAILABLE `[FLAGS]`
    * `group`
      * 1 of ALLOWED
        * accounts
        * general
        * kustomize
        * resource-overrides
* _Examples:_
	```
	#Validates all settings in the specified YAML file
	argocd admin settings validate --argocd-cm-path ./argocd-cm.yaml
	
	#Validates accounts and plugins settings in Kubernetes cluster of current kubeconfig context
	argocd admin settings validate --group accounts --group plugins --load-cluster-settings
	```

# `func NewResourceOverridesCommand(cmdCtx commandContext) *cobra.Command {`
* `argocd admin settings resource-overrides COMMAND`
  * troubleshoot resource overrides
  * AVAILABLE `COMMAND`
    * NewResourceIgnoreDifferencesCommand(cmdCtx)
    * NewResourceIgnoreResourceUpdatesCommand(cmdCtx)
    * NewResourceActionListCommand(cmdCtx)
    * NewResourceActionRunCommand(cmdCtx)
    * NewResourceHealthCommand(cmdCtx)

## `func NewResourceIgnoreDifferencesCommand(cmdCtx commandContext) *cobra.Command {`
* `argocd admin settings resource-overrides ignore-differences RESOURCE_YAML_PATH`
  * render fields / excluded -- from -- diffing
    * == specified | 'argocd-cm' ConfigMap's `resource.customizations.ignoreDifferences`
* _Examples:_
  ```
  argocd admin settings resource-overrides ignore-differences ./deploy.yaml --argocd-cm-path ./argocd-cm.yaml
  ```

## `func NewResourceIgnoreResourceUpdatesCommand(cmdCtx commandContext) *cobra.Command {`
	var ignoreNormalizerOpts normalizers.IgnoreNormalizerOpts
	command := &cobra.Command{
		Use:   "ignore-resource-updates RESOURCE_YAML_PATH",
		Short: "Renders fields excluded from resource updates",
		Long:  "Renders ignored fields using the 'ignoreResourceUpdates' setting specified in the 'resource.customizations' field of 'argocd-cm' ConfigMap",
		Example: `
argocd admin settings resource-overrides ignore-resource-updates ./deploy.yaml --argocd-cm-path ./argocd-cm.yaml`,
		Run: func(c *cobra.Command, args []string) {
			ctx := c.Context()

			if len(args) < 1 {
				c.HelpFunc()(c, args)
				os.Exit(1)
			}

			executeIgnoreResourceUpdatesOverrideCommand(ctx, cmdCtx, args, func(res unstructured.Unstructured, override v1alpha1.ResourceOverride, overrides map[string]v1alpha1.ResourceOverride) {
				gvk := res.GroupVersionKind()
				if len(override.IgnoreResourceUpdates.JSONPointers) == 0 && len(override.IgnoreResourceUpdates.JQPathExpressions) == 0 {
					_, _ = fmt.Printf("Ignore resource updates are not configured for '%s/%s'\n", gvk.Group, gvk.Kind)
					return
				}

				normalizer, err := normalizers.NewIgnoreNormalizer(nil, overrides, ignoreNormalizerOpts)
				errors.CheckError(err)

				normalizedRes := res.DeepCopy()
				logs := collectLogs(func() {
					errors.CheckError(normalizer.Normalize(normalizedRes))
				})
				if logs != "" {
					_, _ = fmt.Println(logs)
				}

				if reflect.DeepEqual(&res, normalizedRes) {
					_, _ = fmt.Printf("No fields are ignored by ignoreResourceUpdates settings: \n%s\n", override.IgnoreResourceUpdates)
					return
				}

				_, _ = fmt.Printf("Following fields are ignored:\n\n")
				_ = cli.PrintDiff(res.GetName(), &res, normalizedRes)
			})
		},
	}
	command.Flags().DurationVar(&ignoreNormalizerOpts.JQExecutionTimeout, "ignore-normalizer-jq-execution-timeout", normalizers.DefaultJQExecutionTimeout, "Set ignore normalizer JQ execution timeout")
	return command
}

## `func NewResourceHealthCommand(cmdCtx commandContext) *cobra.Command {`
	command := &cobra.Command{
		Use:   "health RESOURCE_YAML_PATH",
		Short: "Assess resource health",
		Long:  "Assess resource health using the lua script configured in the 'resource.customizations' field of 'argocd-cm' ConfigMap",
		Example: `
argocd admin settings resource-overrides health ./deploy.yaml --argocd-cm-path ./argocd-cm.yaml`,
		Run: func(c *cobra.Command, args []string) {
			ctx := c.Context()

			if len(args) < 1 {
				c.HelpFunc()(c, args)
				os.Exit(1)
			}

			executeResourceOverrideCommand(ctx, cmdCtx, args, func(res unstructured.Unstructured, _ v1alpha1.ResourceOverride, overrides map[string]v1alpha1.ResourceOverride) {
				gvk := res.GroupVersionKind()
				resHealth, err := healthutil.GetResourceHealth(&res, lua.ResourceHealthOverrides(overrides))
				switch {
				case err != nil:
					errors.CheckError(err)
				case resHealth == nil:
					fmt.Printf("Health script is not configured for '%s/%s'\n", gvk.Group, gvk.Kind)
				default:
					_, _ = fmt.Printf("STATUS: %s\n", resHealth.Status)
					_, _ = fmt.Printf("MESSAGE: %s\n", resHealth.Message)
				}
			})
		},
	}
	return command
}

## `func NewResourceActionListCommand(cmdCtx commandContext) *cobra.Command {`
	command := &cobra.Command{
		Use:   "list-actions RESOURCE_YAML_PATH",
		Short: "List available resource actions",
		Long:  "List actions available for given resource action using the lua scripts configured in the 'resource.customizations' field of 'argocd-cm' ConfigMap and outputs updated fields",
		Example: `
argocd admin settings resource-overrides action list /tmp/deploy.yaml --argocd-cm-path ./argocd-cm.yaml`,
		Run: func(c *cobra.Command, args []string) {
			ctx := c.Context()

			if len(args) < 1 {
				c.HelpFunc()(c, args)
				os.Exit(1)
			}

			executeResourceOverrideCommand(ctx, cmdCtx, args, func(res unstructured.Unstructured, override v1alpha1.ResourceOverride, overrides map[string]v1alpha1.ResourceOverride) {
				gvk := res.GroupVersionKind()
				if override.Actions == "" {
					_, _ = fmt.Printf("Actions are not configured for '%s/%s'\n", gvk.Group, gvk.Kind)
					return
				}

				luaVM := lua.VM{ResourceOverrides: overrides}
				discoveryScript, err := luaVM.GetResourceActionDiscovery(&res)
				errors.CheckError(err)

				availableActions, err := luaVM.ExecuteResourceActionDiscovery(&res, discoveryScript)
				errors.CheckError(err)
				sort.Slice(availableActions, func(i, j int) bool {
					return availableActions[i].Name < availableActions[j].Name
				})

				w := tabwriter.NewWriter(os.Stdout, 0, 0, 2, ' ', 0)
				_, _ = fmt.Fprintf(w, "NAME\tDISABLED\n")
				for _, action := range availableActions {
					_, _ = fmt.Fprintf(w, "%s\t%s\n", action.Name, strconv.FormatBool(action.Disabled))
				}
				_ = w.Flush()
			})
		},
	}
	return command
}

## `func NewResourceActionRunCommand(cmdCtx commandContext) *cobra.Command {`
	var resourceActionParameters []string

	command := &cobra.Command{
		Use:     "run-action RESOURCE_YAML_PATH ACTION",
		Aliases: []string{"action"},
		Short:   "Executes resource action",
		Long:    "Executes resource action using the lua script configured in the 'resource.customizations' field of 'argocd-cm' ConfigMap and outputs updated fields",
		Example: `
argocd admin settings resource-overrides action /tmp/deploy.yaml restart --argocd-cm-path ./argocd-cm.yaml`,
		Run: func(c *cobra.Command, args []string) {
			ctx := c.Context()

			if len(args) < 2 {
				c.HelpFunc()(c, args)
				os.Exit(1)
			}
			action := args[1]

			// Parse resource action parameters
			parsedParams := make([]*applicationpkg.ResourceActionParameters, 0)
			if len(resourceActionParameters) > 0 {
				for _, param := range resourceActionParameters {
					parts := strings.SplitN(param, "=", 2)
					if len(parts) != 2 {
						log.Fatalf("Invalid parameter format: %s", param)
					}
					name := parts[0]
					value := parts[1]
					parsedParams = append(parsedParams, &applicationpkg.ResourceActionParameters{
						Name:  &name,
						Value: &value,
					})
				}
			}

			executeResourceOverrideCommand(ctx, cmdCtx, args, func(res unstructured.Unstructured, override v1alpha1.ResourceOverride, overrides map[string]v1alpha1.ResourceOverride) {
				gvk := res.GroupVersionKind()
				if override.Actions == "" {
					_, _ = fmt.Printf("Actions are not configured for '%s/%s'\n", gvk.Group, gvk.Kind)
					return
				}

				luaVM := lua.VM{ResourceOverrides: overrides}
				action, err := luaVM.GetResourceAction(&res, action)
				errors.CheckError(err)

				modifiedRes, err := luaVM.ExecuteResourceAction(&res, action.ActionLua, parsedParams)
				errors.CheckError(err)

				for _, impactedResource := range modifiedRes {
					result := impactedResource.UnstructuredObj
					switch impactedResource.K8SOperation {
					// No default case since a not supported operation would have failed upon unmarshaling earlier
					case lua.PatchOperation:
						if reflect.DeepEqual(&res, modifiedRes) {
							_, _ = fmt.Printf("No fields had been changed by action: \n%s\n", action.Name)
							return
						}

						_, _ = fmt.Printf("Following fields have been changed:\n\n")
						_ = cli.PrintDiff(res.GetName(), &res, result)
					case lua.CreateOperation:
						yamlBytes, err := yaml.Marshal(impactedResource.UnstructuredObj)
						errors.CheckError(err)
						fmt.Println("Following resource was created:")
						fmt.Println(bytes.NewBuffer(yamlBytes).String())
					}
				}
			})
		},
	}

	command.Flags().StringArrayVar(&resourceActionParameters, "param", []string{}, "Action parameters (e.g. --param key1=value1)")
	return command
}
