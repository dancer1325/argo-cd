# Plugins

* goal
  * how to write plugins -- for -- `argocd` CLI tool

* Plugins or ArgoCD plugins
  * [original proposal](../proposals/argocd-cli-pluin.md) 
  * == standalone executable file /
    * 's name: "argocd-"
  * allow
    * ⭐️extend `argocd` CLI -- with -- NEW sub-commands⭐️
      * == add custom features / NOT included by `argocd`
  * how to install?
    * move its executable file | ANY directory / included | your PATH
      * ⚠️include it as absolute path⚠️
        * _Example:_
          * (right) `export PATH="/usr/local/bin:/home/user/bin:$PATH"`
          * (wrong) `export PATH="./bin:../tools:$PATH"`
  * how does it work?
    * if you use `argocd my-plugin arg1 arg2 --flag1` -> Argo CD looks for "argocd-my-plugin" executable | your PATH

## Limitations

TODO:
1. It is currently not possible to create plugins that overwrite existing
`argocd` commands. For example, creating a plugin such as `argocd-version`
will cause the plugin to never get executed, as the existing `argocd version`
command will always take precedence over it. Due to this limitation, it is
also not possible to use plugins to add new subcommands to existing `argocd` commands.
For example, adding a subcommand `argocd cluster upgrade` by naming your plugin
`argocd-cluster` will cause the plugin to be ignored.

2. It is currently not possible to parse the global flags set by `argocd` CLI. For example, 
if you have set any global flag value such as `--logformat` value to `text`, the plugin will
not parse the global flags and pass the default value to the `--logformat` flag which is `json`.
The flag parsing will work exactly the same way for existing `argocd` commands which means executing a
existing argocd command such as `argocd cluster list` will correctly parse the flag value as `text`.

## Conditions for an `argocd` plugin

Any binary that you would want to execute as an `argocd` plugin need to satisfy the following three conditions:

1. The binary should start with `argocd-` as the prefix name. For example,
   `argocd-demo-plugin` or `argocd-demo_plugin` is a valid binary name but not
   `argocd_demo-plugin` or `argocd_demo_plugin`.
2. The binary should have executable permissions otherwise it will be ignored.
3. The binary should reside anywhere in the system's absolute PATH.

## Writing `argocd` plugins

### Naming a plugin

An Argo CD plugin’s filename must start with `argocd-`. The subcommands implemented
by the plugin are determined by the portion of the filename after the `argocd-` prefix.
Anything after `argocd-` will become a subcommand for `argocd`.

For example, A plugin named `argocd-demo-plugin` is invoked when the user types:
```bash
argocd demo-plugin [args] [flags]
```

The `argocd` CLI determines which plugin to invoke based on the subcommands provided.

For example, executing the following command:
```bash
argocd my-custom-command [args] [flags]
```
will lead to the execution of plugin named `argocd-my-custom-command` if it is present in the PATH.

### Writing a plugin

A plugin can be written in any programming language or script that allows you to write command-line commands.

A plugin determines which command path it wishes to implement based on its name.

For example, If a binary named `argocd-demo-plugin` is available in your system's absolute PATH, and the user runs the following command:

```bash
argocd demo-plugin subcommand1 --flag=true
```

Argo CD will translate and execute the corresponding plugin with the following command:

```bash
argocd-demo-plugin subcommand1 --flag=true
```

Similarly, if a plugin named `argocd-demo-demo-plugin` is found in the absolute PATH, and the user invokes:

```bash
argocd demo-demo-plugin subcommand2 subcommand3 --flag=true
```

Argo CD will execute the plugin as:

```bash
argocd-demo-demo-plugin subcommand2 subcommand3 --flag=true
```

### Example plugin
```bash
#!/bin/bash

# Check if the argocd CLI is installed
if ! command -v argocd &> /dev/null; then
    echo "Error: Argo CD CLI (argocd) is not installed. Please install it first."
    exit 1
fi

if [[ "$1" == "version" ]]
then
    echo "displaying argocd version..."
    argocd version
    exit 0
fi


echo "I am a plugin named argocd-foo"
```

### Using a plugin

To use a plugin, make the plugin executable:
```bash
sudo chmod +x ./argocd-foo
```

and place it anywhere in your `PATH`:
```bash
sudo mv ./argocd-foo /usr/local/bin
```

You may now invoke your plugin as a argocd command:
```bash
argocd foo
```

This would give the following output
```bash
I am a plugin named argocd-foo
```

All args and flags are passed as-is to the executable:
```bash
argocd foo version
```

This would give the following output
```bash
DEBU[0000] command does not exist, looking for a plugin... 
displaying argocd version...
2025/01/16 13:24:36 maxprocs: Leaving GOMAXPROCS=16: CPU quota undefined
argocd: v2.13.0-rc2+0f083c9
  BuildDate: 2024-09-20T11:59:25Z
  GitCommit: 0f083c9e58638fc292cf064e294a1aa53caa5630
  GitTreeState: clean
  GoVersion: go1.22.7
  Compiler: gc
  Platform: linux/amd64
argocd-server: v2.13.0-rc2+0f083c9
  BuildDate: 2024-09-20T11:59:25Z
  GitCommit: 0f083c9e58638fc292cf064e294a1aa53caa5630
  GitTreeState: clean
  GoVersion: go1.22.7
  Compiler: gc
  Platform: linux/amd64
  Kustomize Version: v5.4.3 2024-07-19T16:40:33Z
  Helm Version: v3.15.2+g1a500d5
  Kubectl Version: v0.31.0
  Jsonnet Version: v0.20.0
```

## Distributing `argocd` plugins

If you’ve developed an Argo CD plugin for others to use,
you should carefully consider how to package, distribute, and
deliver updates to ensure a smooth installation and upgrade process
for your users.

### Native / platform specific package management

You can distribute your plugin using traditional package managers,
such as `apt` or `yum` for Linux, `Chocolatey` for Windows, and `Homebrew` for macOS.
These package managers are well-suited for distributing plugins as they can
place executables directly into the user's PATH, making them easily accessible.

However, as a plugin author, choosing this approach comes with the responsibility of
maintaining and updating the plugin's distribution packages across multiple platforms
for every release. This includes testing for compatibility, ensuring timely updates,
and managing versioning to provide a seamless experience for your users.

### Source code

* recommendation
  * publish the source code of your plugin | Git repository

* steps to use it by rest
  * fetch the code,
  * if the plugin requires compiling -> set up a suitable build environment
  * manually deploy it
