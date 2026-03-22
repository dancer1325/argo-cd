# Open Container Initiative (OCI)

* [documentation](https://opencontainers.org/)
* OCI images
  * uses
    * -- as -- [application source](application_sources.md)
  * 👀types👀
    * plain manifests (YAML, Kustomize, Jsonnet, ...)
    * helm charts

## Declarative

* | "Application.yaml",
  * `spec.source.repoURL: oci://registryName/imageName`
    * == OCI image repository URL  
  * `spec.source.targetRevision`
    * == desired image tag OR digest
  * `spec.source.path`
    * == relative path -- from the -- `spec.source.repoURL`
      * if it's
        * | root path -> `.`
        * OCI Helm charts -> ALWAYS `.`

## OCI Repositories special cases

* if you need credentials -- for a -- OCI repository ->
  * you need to create a repository credential / type `oci`
```shell
  # Add a private HTTPS OCI repository named 'stable'
  argocd repo add oci://registry-1.docker.io/bitnamicharts/nginx --type oci --name stable --username test --password test 
```

TODO:
In the case of Helm repositories there is another way to use OCI credentials with Helm
```shell
  # Add a private HTTPS OCI Helm repository named 'stable'
  argocd repo add registry-1.docker.io/bitnamicharts/nginx --type helm --name stable --username test --password test --enable-oci
```

> [!NOTE]
> The repository URL should not contain the OCI scheme prefix `oci://`.
> Also the path should be removed from the repository URL and should be defined instead in the `path` attribute.

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: my-custom-image
  namespace: argocd
spec:
  project: default
  source:
    path: bitnamicharts/nginx
    repoURL: registry-1.docker.io
    targetRevision: 1.16.1
  destination:
    server: "https://kubernetes.default.svc"
    namespace: my-namespace
```

> [!NOTE]
> Keep in mind that this only applies when using a Helm repository credential. 

## Usage Guidelines

First off, you'll need to have a repository that is OCI-compliant
* As an example, DockerHub, ECR, GHCR and GCR all fit 
the bill.

Secondly, Argo CD expects an OCI image to contain a single layer
* It also expects an OCI image to have a media type which 
is accepted by the Argo CD repository server
* By default, Argo CD accepts one of the following media types for the image 
layer:

* `application/vnd.oci.image.layer.v1.tar+gzip`
* `application/vnd.cncf.helm.chart.content.v1.tar+gzip`

Custom media types can be configured by setting the `ARGOCD_REPO_SERVER_OCI_LAYER_MEDIA_TYPES` environment variable 
in the repo-server deployment.

To create an OCI artifact compatible with Argo CD, there are a multitude of tools to choose from
* For this example we'll
use [ORAS](https://oras.land/)
* Navigate to the directory where your manifests are located and run `oras push`.

```shell
oras push <registry-url>/guestbook:latest .
```

ORAS will take care of packaging the directory to a single layer and setting the `mediaType` to 
`application/vnd.oci.image.layer.v1.tar+gzip`.

You can also package your OCI image using a compressed archive.

```shell
# Create a tarball of the directory containing your manifests. If you are not in the current directory, please ensure 
# that you are setting the correct parent of the directory (that is what the `-C` flag does).
tar -czvf archive.tar.gz -C manifests .
```

Then, you can push the archive to your OCI registry using ORAS:

```shell
# In the case of tarballs, you currently need to set the media type manually. 
oras push <registry-url>/guestbook:latest archive.tar.gz:application/vnd.oci.image.layer.v1.tar+gzip
```

## OCI Metadata Annotations

Argo CD can display standard OCI metadata annotations, providing additional context and information about your OCI 
images directly in the Argo CD UI.

### Supported Annotations

Argo CD recognizes and displays the following standard OCI annotations:

* `org.opencontainers.image.title`
* `org.opencontainers.image.description`
* `org.opencontainers.image.version`
* `org.opencontainers.image.revision`
* `org.opencontainers.image.url`
* `org.opencontainers.image.source`
* `org.opencontainers.image.authors`
* `org.opencontainers.image.created`

Using the previous example with ORAS, we can set annotations which Argo CD can make use of:

```shell
oras push -a "org.opencontainers.image.authors=some author" \
          -a "org.opencontainers.image.url=http://some-url" \
          -a "org.opencontainers.image.version=some-version" \
          -a "org.opencontainers.image.source=http://some-source" \
          -a "org.opencontainers.image.description=some description" \
          <registry-url>/guestbook:latest .
```
