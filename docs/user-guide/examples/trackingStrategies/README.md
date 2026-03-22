# Tracking Strategies

TODO: 

## Helm

### Pin to a version

* [here](applicationWithHelmAsApplicationSource.yaml)'s 1.

### Track patches

* [here](applicationWithHelmAsApplicationSource.yaml)'s 2.

### Track minor releases

* [here](applicationWithHelmAsApplicationSource.yaml)'s 3.

### Use the latest

* [here](applicationWithHelmAsApplicationSource.yaml)'s 4.

### Use the latest including pre-releases

* [here](applicationWithHelmAsApplicationSource.yaml)'s 5.

## Git

### HEAD / Branch Tracking

* [here](applicationWithGitAsApplicationSource.yaml)'s 1.

### Pin to a version

* [here](applicationWithGitAsApplicationSource.yaml)'s 2.

### Track patches

* [here](applicationWithGitAsApplicationSource.yaml)'s 3.

### Track minor releases

* [here](applicationWithGitAsApplicationSource.yaml)'s 4.

### Use the latest

* [here](applicationWithGitAsApplicationSource.yaml)'s 5.

### Tag Tracking: Use the latest including pre-releases

* [here](applicationWithGitAsApplicationSource.yaml)'s 6.

### Handling Ambiguous Git References

TODO: 
**File:** [git-qualified-refs.yaml](./git-qualified-refs.yaml)

**Problem:** When both a branch and tag have the same name:
```bash
refs/heads/release-1.0 -> commit B
refs/tags/release-1.0  -> commit A
```

**Solution 1: Explicit branch reference**
```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: myapp-branch-explicit
spec:
  source:
    repoURL: https://github.com/myorg/myapp
    targetRevision: refs/heads/release-1.0  # Explicit branch
    path: manifests/
```

**Solution 2: Explicit tag reference**
```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: myapp-tag-explicit
spec:
  source:
    repoURL: https://github.com/myorg/myapp
    targetRevision: refs/tags/release-1.0  # Explicit tag
    path: manifests/
```
