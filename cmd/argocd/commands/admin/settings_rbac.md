# var resourceMap = map[string]string{
	"account":         rbac.ResourceAccounts,
	"app":             rbac.ResourceApplications,
	"apps":            rbac.ResourceApplications,
	"application":     rbac.ResourceApplications,
	"applicationsets": rbac.ResourceApplicationSets,
	"cert":            rbac.ResourceCertificates,
	"certs":           rbac.ResourceCertificates,
	"certificate":     rbac.ResourceCertificates,
	"cluster":         rbac.ResourceClusters,
	"extension":       rbac.ResourceExtensions,
	"gpgkey":          rbac.ResourceGPGKeys,
	"key":             rbac.ResourceGPGKeys,
	"log":             rbac.ResourceLogs,
	"logs":            rbac.ResourceLogs,
	"exec":            rbac.ResourceExec,
	"proj":            rbac.ResourceProjects,
	"projs":           rbac.ResourceProjects,
	"project":         rbac.ResourceProjects,
	"repo":            rbac.ResourceRepositories,
	"repos":           rbac.ResourceRepositories,
	"repository":      rbac.ResourceRepositories,
}
* == map(shorthand resource names, RBAC counterparts)

# var validRBACResourcesActions = map[string]actionTraitMap{
	rbac.ResourceAccounts:        accountsActions,
	rbac.ResourceApplications:    applicationsActions,
	rbac.ResourceApplicationSets: defaultCRUDActions,
	rbac.ResourceCertificates:    defaultCRDActions,
	rbac.ResourceClusters:        defaultCRUDActions,
	rbac.ResourceExtensions:      extensionActions,
	rbac.ResourceGPGKeys:         defaultCRDActions,
	rbac.ResourceLogs:            logsActions,
	rbac.ResourceExec:            execActions,
	rbac.ResourceProjects:        defaultCRUDActions,
	rbac.ResourceRepositories:    defaultCRUDActions,
}
* ALLOWED RBAC resources

# `func NewRBACCommand() *cobra.Command {`
* `argocd admin settings rbac COMMAND`
  * validate & test RBAC configuration
  * ALLOWED `COMMAND`
    * [`NewRBACCanCommand()`](#func-newrbaccancommand-cobracommand-)
    * [`NewRBACValidateCommand()`](#func-newrbacvalidatecommand-cobracommand-)

## `func NewRBACCanCommand() *cobra.Command {`
* `argocd admin settings rbac can ROLE/SUBJECT ACTION RESOURCE [SUB-RESOURCE] [FLAGS]`
  * check if a role OR subject has RBAC permissions -- to -- do something 
  * ALLOWED FLAGS
    * `policy-file`
      * == path -- to the -- policy file to use
      * by default,
        * ""
    * `default-role`
      * == name -- of the -- default role to use
      * by default,
        * ""
    * `use-builtin-policy`
      * whether to also use builtin-policy
      * by default,
        * `true`
    * `strict`
      * whether to perform strict check | action & resource names
      * by default,
        * `true`
    * `quiet` / `-q`
      * quiet mode
        * == ❌NOT print results | stdout❌
      * by default,
        * `false`
* _Example:_ 
	```
	# Check whether role some:role has permissions to create an application in the
	# 'default' project, using a local policy.csv file
	argocd admin settings rbac can some:role create application 'default/app' --policy-file policy.csv
	
	# Policy file can also be K8s config map with data keys like argocd-rbac-cm,
	# i.e. 'policy.csv' and (optionally) 'policy.default'
	argocd admin settings rbac can some:role create application 'default/app' --policy-file argocd-rbac-cm.yaml
	
	# If --policy-file is not given, the ConfigMap 'argocd-rbac-cm' from K8s is
	# used. You need to specify the argocd namespace, and make sure that your
	# current Kubernetes context is pointing to the cluster Argo CD is running in
	argocd admin settings rbac can some:role create application 'default/app' --namespace argocd
	
	# You can override a possibly configured default role
	argocd admin settings rbac can someuser create application 'default/app' --default-role role:readonly
	```

## `func NewRBACValidateCommand() *cobra.Command {`
* `argocd admin settings rbac validate [--policy-file POLICYFILE] [--namespace NAMESPACE]`
  * validate if RBAC policy is SYNTACTICALLY correct
  * requirements
    * `[--policy-file POLICYFILE]` OR `[--namespace NAMESPACE]`
      * ONE of those
  * `POLICYFILE`
    * == path -- to the -- policy file / use
    * by default,
      * ""
    * ALLOWED files
      * local file OR
      * K8s ConfigMap | provided namespace
    * ALLOWED formats
      * CSV OR
      * K8s ConfigMap format
  * `NAMESPACE`
    * == namespace | get argo rbac configmap
* _Example:_
	```
	# Check whether a given policy file is valid using a local policy.csv file.
	argocd admin settings rbac validate --policy-file policy.csv
	
	# Policy file can also be K8s config map with data keys like argocd-rbac-cm,
	# i.e. 'policy.csv' and (optionally) 'policy.default'
	argocd admin settings rbac validate --policy-file argocd-rbac-cm.yaml
	
	# If --policy-file is not given, and instead --namespace is giventhe ConfigMap 'argocd-rbac-cm'
	# from K8s is used.
	argocd admin settings rbac validate --namespace argocd
	```
