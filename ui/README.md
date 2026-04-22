# Argo CD Web UI

<img src="https://github.com/argoproj/argo-cd/blob/master/ui/src/assets/images/argo.png?raw=true" alt="Argo Image" width="600" />

## Getting started
### requirements
* install [NodeJS](https://nodejs.org/en/download/) and [Yarn](https://yarnpkg.com)
  * | macOS, run SIMPLY `brew install node yarn`

### how to install?
* `yarn install` 

### how to start webpack dev UI server?
* `yarn start`

### how to build? 
* `yarn build`
  * create static resources | "./dist"

### how to build a Docker image?
* `IMAGE_NAMESPACE=yourimagerepo IMAGE_TAG=latest yarn docker`
  * if you want to push | Docker registry -> run `IMAGE_NAMESPACE=yourimagerepo IMAGE_TAG=latest DOCKER_PUSH=true yarn docker`

## Pre-commit Checks

TODO: 
Make sure your code passes the lint checks:

```bash
yarn lint --fix
```

If you are using VSCode, add this configuration to `.vscode/settings.json` in the root of this repository to identify and fix lint issues automatically before you save file.

Install [Eslint Extension](https://marketplace.visualstudio.com/items?itemName=dbaeumer.vscode-eslint) in VSCode.

`.vscode/settings.json`

```json
{
  "eslint.format.enable": true,
    "editor.codeActionsOnSave": {
        "source.fixAll.eslint": "always"
    },
    "eslint.workingDirectories": [
        {
            "directory": "./ui",
            "!cwd": false
        }
    ],
    "eslint.useFlatConfig": true
}
```
