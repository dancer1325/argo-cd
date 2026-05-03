# Templates

* goal
  * ApplicationSet's `spec.template`

* allows
  * 👀generating Argo CD `Application` resources👀
    * generation -- thanks to -- 
      * RIGHT NOW
        * [fasttemplate](https://github.com/valyala/fasttemplate)
      * FUTURE
        * [Go Template](GoTemplate.md) 

## 's fields 

* `spec.template.spec` == 💡[Application's `spec`](/manifests/crds/application-crd.yaml)💡/
  * can use generator's parameters

* `spec.template.metadata`
  * set Application's metadata
    * _Examples:_ `name`, `labels` or `annotations`

### | Deploy ApplicationSet resources, as part of a Helm chart

* ⚠️if you use Helm to deploy your ApplicationSet resources -> write the template -- as a -- Helm string literal⚠️
  * ❌!= deploy Application❌
  * Reason:🧠ApplicationSet's templating notation == Helm's templating notation
    * == `{{}}`
    * OTHERWISE, throw errorS🧠

## Generator templates

TODO: 
In addition to specifying a template within the `.spec.template` of the `ApplicationSet` resource, 
templates may also be specified within generators
* This is useful for overriding the values of the `spec`-level template.

The generator's `template` field takes precedence over the `spec`'s template fields:

- If both templates contain the same field, the generator's field value will be used.
- If only one of those templates' fields has a value, that value will be used.

Generator templates can thus be thought of as patches against the outer `spec`-level template fields.

```yaml
apiVersion: argoproj.io/v1alpha1
kind: ApplicationSet
metadata:
  name: guestbook
spec:
  generators:
  - list:
      elements:
        - cluster: engineering-dev
          url: https://kubernetes.default.svc
      template:
        metadata: {}
        spec:
          project: "default"
          source:
            targetRevision: HEAD
            repoURL: https://github.com/argoproj/argo-cd.git
            # New path value is generated here:
            path: 'applicationset/examples/template-override/{{ .nameNormalized }}-override'
          destination: {}

  template:
    metadata:
      name: '{{ .nameNormalized }}-guestbook'
    spec:
      project: "default"
      source:
        repoURL: https://github.com/argoproj/argo-cd.git
        targetRevision: HEAD
        # This 'default' value is not used: it is replaced by the generator's template path, above
        path: applicationset/examples/template-override/default
      destination:
        server: '{{ .server }}'
        namespace: guestbook
```

In [this example](https://github.com/argoproj/argo-cd/tree/master/applicationset/examples/template-override), the ApplicationSet controller will generate an `Application` resource using the `path` generated
by the List generator, rather than the `path` value defined in `.spec.template`.

## Template Patch

Templating is only available on string type
* However, some use cases may require applying templating on other types.

Example:

- Conditionally set the automated sync policy.
- Conditionally switch prune boolean to `true`.
- Add multiple helm value files from a list.

The `templatePatch` feature enables advanced templating, with support for `json` and `yaml`.


> [!IMPORTANT]
> `templatePatch` only works when [go templating](../applicationset/GoTemplate.md) is enabled.
> This means that the `goTemplate` field under `spec` needs to be set to `true` for template patching to work.

> [!IMPORTANT]
> The `templatePatch` can apply arbitrary changes to the template
* If parameters include untrustworthy user input, it 
> may be possible to inject malicious changes into the template
* It is recommended to use `templatePatch` only with 
> trusted input or to carefully escape the input before using it in the template
* Piping input to `toJson` should help
> prevent, for example, a user from successfully injecting a string with newlines.
>
> The `spec.project` field is not supported in `templatePatch`
* If you need to change the project, you can use the
> `spec.project` field in the `template` field.

> [!IMPORTANT]
> When writing a `templatePatch`, you're crafting a patch
* So, if the patch includes an empty `spec: # nothing in here`, it will effectively clear out existing fields
* See [#17040](https://github.com/argoproj/argo-cd/issues/17040) for an example of this behavior.
