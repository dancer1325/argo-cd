https://github.com/argoproj/argo-cd/security/advisories

# how have these files been generated?
* [install gh](https://cli.github.com/)
* | [rooth path](../../)
  * `gh auth login`
  * `gh api repos/argoproj/argo-cd/security-advisories --paginate > argo-cd-advisories.json`
  * `python3 docs/advisories/generate.py`