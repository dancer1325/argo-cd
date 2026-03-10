# [Go Text Template](https://pkg.go.dev/text/template)

## Introduction

* Go Template
  * == Go Standard -- for -- string templating
  * vs fasttemplate
    * MORE powerful
  * uses
    * by ApplicationSet
  * how to configure?
    * | your ApplicationSet manifest,
      * add `goTemplate: true`
        * == activate this feature
      * add `goTemplateOptions: ["opt1", "opt2", ...]`
        * [options](https://pkg.go.dev/text/template#Template.Option)
          * if 
            * undefined values are specified -> report an error
              * `missingkey=error`
                * recommended one
                * 1 useful one
            * unset parameters -> error

* fasttemplate
  * default templating engine

* ALLOWED functions
  * [Sprig function library](https://masterminds.github.io/sprig/)
    * EXCEPT to: `env`, `expandenv` and `getHostByName`
  * Go Text Template functions
  * `normalize` function
    * any string parameter is normalized -- as a -- valid DNS name 
      * replace invalid characters -- with -- hyphens
      * truncate at 253 characters
    * uses
      * make safe some parameters
        * _Example:_ Application names
  * `slugify` function
    * sanitizes and smart truncates
    * 's arguments
      - first argument
        - OPTIONAL
        - integer -- about the -- maximum length of the slug
      - second argument
        - OPTIONAL
        - boolean / enable smart truncation 
      - last argument
        - OPTIONAL 
        - name / needs -- to be - slugified

## Limitations

TODO: 
Go templates are applied on a per-fieald basis, and only on string fields
* Here are some examples of what is **not** 
possible with Go text templates:

- Templating a boolean field.

        ::yaml
        apiVersion: argoproj.io/v1alpha1
        kind: ApplicationSet
        spec:
          goTemplate: true
          goTemplateOptions: ["missingkey=error"]
          template:
            spec:
              source:
                helm:
                  useCredentials: "{{.useCredentials}}"  # This field may NOT be templated, because it is a boolean field.

- Templating an object field:

        ::yaml
        apiVersion: argoproj.io/v1alpha1
        kind: ApplicationSet
        spec:
          goTemplate: true
          goTemplateOptions: ["missingkey=error"]
          template:
            spec:
              syncPolicy: "{{.syncPolicy}}"  # This field may NOT be templated, because it is an object field.

- Using control keywords across fields:

        ::yaml
        apiVersion: argoproj.io/v1alpha1
        kind: ApplicationSet
        spec:
          goTemplate: true
          goTemplateOptions: ["missingkey=error"]
          template:
            spec:
              source:
                helm:
                  parameters:
                  # Each of these fields is evaluated as an independent template, so the first one will fail with an error.
                  - name: "{{range .parameters}}"
                  - name: "{{.name}}"
                    value: "{{.value}}"
                  - name: throw-away
                    value: "{{end}}"

- Signature verification is not supported for the templated `project` field when using the Git generator.

        ::yaml
        apiVersion: argoproj.io/v1alpha1
        kind: ApplicationSet
        spec:
          goTemplate: true
          template:
            spec:
              project: {{.project}}


## Migration guide

### Globals

All your templates must replace parameters with GoTemplate Syntax:

Example: `{{ some.value }}` becomes `{{ .some.value }}`

### Cluster Generators

By activating Go Templating, `{{ .metadata }}` becomes an object.

- `{{ metadata.labels.my-label }}` becomes `{{ index .metadata.labels "my-label" }}`
- `{{ metadata.annotations.my/annotation }}` becomes `{{ index .metadata.annotations "my/annotation" }}`

### Git Generators

By activating Go Templating, `{{ .path }}` becomes an object
* Therefore, some changes must be made to the Git 
generators' templating:

- `{{ path }}` becomes `{{ .path.path }}`
- `{{ path.basename }}` becomes `{{ .path.basename }}`
- `{{ path.basenameNormalized }}` becomes `{{ .path.basenameNormalized }}`
- `{{ path.filename }}` becomes `{{ .path.filename }}`
- `{{ path.filenameNormalized }}` becomes `{{ .path.filenameNormalized }}`
- `{{ path[n] }}` becomes `{{ index .path.segments n }}`
- `{{ values }}` if being used in the file generator becomes `{{ .values }}`

Here is an example:

```yaml
apiVersion: argoproj.io/v1alpha1
kind: ApplicationSet
metadata:
  name: cluster-addons
spec:
  generators:
  - git:
      repoURL: https://github.com/argoproj/argo-cd.git
      revision: HEAD
      directories:
      - path: applicationset/examples/git-generator-directory/cluster-addons/*
  template:
    metadata:
      name: '{{path.basename}}'
    spec:
      project: default
      source:
        repoURL: https://github.com/argoproj/argo-cd.git
        targetRevision: HEAD
        path: '{{path}}'
      destination:
        server: https://kubernetes.default.svc
        namespace: '{{path.basename}}'
```

becomes

```yaml
apiVersion: argoproj.io/v1alpha1
kind: ApplicationSet
metadata:
  name: cluster-addons
spec:
  goTemplate: true
  goTemplateOptions: ["missingkey=error"]
  generators:
  - git:
      repoURL: https://github.com/argoproj/argo-cd.git
      revision: HEAD
      directories:
      - path: applicationset/examples/git-generator-directory/cluster-addons/*
  template:
    metadata:
      name: '{{.path.basename}}'
    spec:
      project: default
      source:
        repoURL: https://github.com/argoproj/argo-cd.git
        targetRevision: HEAD
        path: '{{.path.path}}'
      destination:
        server: https://kubernetes.default.svc
        namespace: '{{.path.basename}}'
```

It is also possible to use Sprig functions to construct the path variables manually:

| with `goTemplate: false` | with `goTemplate: true` | with `goTemplate: true` + Sprig |
| ------------ | ----------- | --------------------- |
| `{{path}}` | `{{.path.path}}` | `{{.path.path}}` |
| `{{path.basename}}` | `{{.path.basename}}` | `{{base .path.path}}` |
| `{{path.filename}}` | `{{.path.filename}}` | `{{.path.filename}}` |
| `{{path.basenameNormalized}}` | `{{.path.basenameNormalized}}` | `{{normalize .path.path}}` |
| `{{path.filenameNormalized}}` | `{{.path.filenameNormalized}}` | `{{normalize .path.filename}}` |
| `{{path[N]}}` | `-` | `{{index .path.segments N}}` |

## Available template functions

ApplicationSet controller provides:

- all [sprig](http://masterminds.github.io/sprig/) Go templates function except `env`, `expandenv` and `getHostByName`
- `normalize`: sanitizes the input so that it complies with the following rules:
    1. contains no more than 253 characters
    2. contains only lowercase alphanumeric characters, '-' or '.'
    3. starts and ends with an alphanumeric character

- `slugify`: sanitizes like `normalize` and smart truncates (it doesn't cut a word into 2) like described in the [introduction](#introduction) section.
- `toYaml` / `fromYaml` / `fromYamlArray` helm like functions


## Examples

### Fallback value -- for -- unset parameters

* use cases
  * | some generators,
    * parameter of a certain name might NOT ALWAYS be populated
      * _Example:_ values generator OR git files generator

, so you need to avoid looking up a property
that doesn't exist


* use template functions / do the lookup -- with a -- default 
  * _Example:_ `dig`
* if you want unset parameters / fallback 0 ->
  * remove `goTemplateOptions: ["missingkey=error"]` OR
  * set `goTemplateOptions: ["missingkey=invalid"]`
