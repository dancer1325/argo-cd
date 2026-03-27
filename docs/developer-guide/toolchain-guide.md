# Development Toolchain

* goal
  * ways to set your [developer environment](development-environment.md)
    * [local](#local)
    * [virtualized](#virtualized)

* prerequisites
  * [Development Environment](development-environment.md)

* _Example:_ MOST relevant [Makefile targets](/Makefile) provide -- for the -- 2 variants
  * `make test`
    * run unit tests | Docker container (== virtualized toolchain)
  * `make test-local`
    * run unit tests | your local system (== local toolchain)

## local vs virtualized

```
LOCAL TOOLCHAIN                    VIRTUALIZED TOOLCHAIN
─────────────────                  ────────────────────

Your Machine:                      Your Machine:
├─ Go 1.26 ✅                      └─ Docker ✅
├─ Node.js ✅
├─ yarn ✅
├─ kubectl ✅
├─ helm ✅                         💡When you run make:💡
├─ kustomize ✅                    1. Creates temp container
├─ goreman ✅                      2. Mounts your code
├─ Git LFS ✅                      3. Runs command inside
├─ GnuPG v2 ✅                     4. Deletes container
└─ ...
                                   Pros:
When you run make:                 ✅ Consistent environment
→ Runs directly on your OS         ✅ NO tool installation
→ Fast iteration                   ✅ == production (containers)
→ IDE debugger works               ✅ repeatable

Pros:                             Cons:
✅ Faster execution                ❌ Slower
✅ Better for debugging            ❌ | install local k8s, requires K8s IP config

Cons:
❌ Complex setup
❌ "Works on my machine"
```

## local

* local toolchain
  * ==💡install the [development environment](development-environment.md) | your local machine💡
  * use cases
    * macOS hosts
      * Reason:🧠Docker & Linux kernel run | VM🧠

* install ADDITIONAL tools
  * `make install-tools-local`
    * install required dependencies & build-tools
      * by default, | "/usr/local/bin"
        * if you want to change the target location -> BEFORE run the script, set `BIN` environment

          ```shell
          BIN=PathInWhichRunScript make install-tools-local
          ```

## virtualized

* virtualized toolchain
  * == 💡| containers, 
    * run ALL
      * install the development environment
      * run the build & programs💡
  * local (== | your machine) mounts / content can be modified
    * `~/go/src`
      * == your Go workspace's source directory
    * `~/.cache/go-build`
      * == your Go build cache
    * `~/.kube`
      * == your Kubernetes client configuration

* requirements
  * Kubernetes API server 
    * ⚠️MUST listen |  
      * your local machine's network interface OR
      * VM's network interface⚠️
    * ❌NOT MUST listen |
      * `127.0.0.1` NOR
      * `localhost`❌
  * [Kubernetes client configuration](https://kubernetes.io/docs/concepts/configuration/organize-cluster-access-kubeconfig/)
    * _Example:_ default "~/.kube/config"
    * ❌MUST NOT use an API URL / points -- to --
      * `localhost`
      * `127.0.0.1`
      * `0.0.0.0`❌

### known issues | macOS

* [here](mac-users.md)

### Docker privileges

* Docker privileges
  * enable you to,
    * interact -- with -- Docker daemon

* recommendations
  * ❌NOT work -- as the -- root user❌
  * if your user does NOT have permissions to talk to the Docker daemon (== ❌`docker` NOT work❌) -> use `sudo`

    ```
    # way1: set SUDO=sudo 
    SUDO=sudo make sometarget
    
    # way2: export sudo permanently
    export SUDO=sudo
    ```

### using Podman

* steps
  * BEFORE running any `make` command,

    ```
    DOCKER=podman make start
    ```

### Build the required Docker image

* `make test-tools-image`
  * [Dockerfile](/test/container/Dockerfile) used to build these images

### Configure your K8s cluster for connection from the build container

#### [K3d](https://k3d.io/stable/)

* approach
  * Kubernetes run | docker container

TODO: 
* you're dealing with docker's internal networking rules when using k3d
* A typical Kubernetes cluster running on your local machine is part of the same network that you're on, so you can access it using **kubectl**
* However, a Kubernetes cluster running within a docker container (in this case, the one launched by make) cannot access 0.0.0.0 
from inside the container itself, when 0.0.0.0 is a network resource outside the container itself (and/or the container's network)
* This is the cost of a fully self-contained, disposable Kubernetes cluster.

The configuration you will need for Argo CD virtualized toolchain:

1
* For most users, the following command works to find the host IP address.

    * If you have perl

       ```pl
       perl -e '
       use strict;
       use Socket;

       my $target = sockaddr_in(53, inet_aton("8.8.8.8"));
       socket(my $s, AF_INET, SOCK_DGRAM, getprotobyname("udp")) or die $!;
       connect($s, $target) or die $!;
       my $local_addr = getsockname($s) or die $!;
       my (undef, $ip) = sockaddr_in($local_addr);
       print "IP: ", inet_ntoa($ip), "\n";
       '
       ```

    * If you don't

      * Try `ip route get 8.8.8.8` on Linux
      * Try `ifconfig`/`ipconfig` (and pick the ip address that feels right -- look for `192.168.x.x` or `10.x.x.x` addresses)

    Note that `8.8.8.8` is Google's Public DNS server, in most places it's likely to be accessible and thus is a good proxy for "which outbound address would my computer use", but you can replace it with a different IP address if necessary.

    Keep in mind that this IP is dynamically assigned by the router so if your router restarts for any reason, your IP might change.

2
* Edit your ~/.kube/config and replace 0.0.0.0 with the above IP address, delete the cluster cert and add `insecure-skip-tls-verify: true`

3
* Execute a `kubectl version` to make sure you can still connect to the Kubernetes API server via this new IP
* 

#### Minikube

By default, minikube will create Kubernetes client configuration that uses authentication data from files
* This is incompatible with the virtualized toolchain
* So if you intend to use the virtualized toolchain, you have to embed this authentication data into the client configuration
* To do so, start minikube using `minikube start --embed-certs`
* Please also note that minikube using the Docker driver is currently not supported with the virtualized toolchain, 
because the Docker driver exposes the API server on 127.0.0.1 hard-coded.

### Test connection from the build container to your K8s cluster

You can test whether the virtualized toolchain has access to your Kubernetes cluster 
by running `make verify-kube-connect` which will run `kubectl version` inside the Docker container used for running all tests.


If you receive an error similar to the following:

```
The connection to the server 127.0.0.1:6443 was refused - did you specify the right host or port?
make: *** [Makefile:386: verify-kube-connect] Error 1
```

you should edit your `~/.kube/config` and modify the `server` option to point
to your correct K8s API (as described above).

