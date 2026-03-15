* **declarative paradigm**
  * == define **WHAT** (== desired state)
    * ArgoCD handles HOW to achieve it
    * NO require MANUAL steps
* **imperative paradigm**
  * == define **HOW** (== steps)

# ArgoCD is Declarative

## 1. deploy an application | Kubernetes cluster

### declarative

* steps
  * [install Argo CD](/docs/operator-manual/installation.md)
  * `kubectl apply -f simple-application.yaml`

### imperative

* steps
  ```bash
  git clone https://github.com/argoproj/argocd-example-apps.git
  cd argocd-example-apps/guestbook
  
  # 1. EACH file
  kubectl apply -f guestbook-ui-deployment.yaml
  kubectl apply -f guestbook-ui-svc.yaml
  
  # 2. recursively ALL | this path 
  kubectl apply -R -f .
  ```

## 2. continuous reconciliation status check

* goal
  * check desired state (| Git) == live state (| cluster)

### declarative

* declared | [Argo CD's Application](simple-application.yaml)

  ```yaml
  spec:
    source:
      repoURL: https://github.com/myorg/myapp.git
      targetRevision: main
  ```

* handled INTERNAL & AUTOMATICALLY -- by -- Argo CD

  ```
  1. Argo CD 
    1.1 reads desired state | Git
    1.2 reads live state | cluster
    1.3 compares states
  ```

### imperative

* YOU need to MANUALLY check
  * YOU can try to be noticed -- via -- CUSTOM script
    ```bash
    # You must write and run this loop yourself
    while true; do
      git pull origin main >/dev/null 2>&1

      CURRENT_COMMIT=$(git rev-parse HEAD)
      LAST_COMMIT=$(cat .last-deployed-commit 2>/dev/null || echo "")

      # Check for changes
      if [[ "$CURRENT_COMMIT" != "$LAST_COMMIT" ]]; then
        echo "[$(date)] 🔄 Changes detected: $LAST_COMMIT -> $CURRENT_COMMIT"
        echo "Applying manifests..."
        kubectl apply -f manifests/
        echo "$CURRENT_COMMIT" > .last-deployed-commit
        echo "✅ Deployment complete"
      fi

      sleep 180  # Poll every 3 minutes
    done
    ```

## 3. Automated Sync

* goal
  * desired state (| Git) == live state (| cluster)

### declarative

* declared | [Argo CD's Application](application-with-sync-policy.yaml)

  ```yaml
  syncPolicy:
    automated: {}
  ```

* handled INTERNAL & AUTOMATICALLY -- by -- Argo CD

  ```
  1. Argo CD 
    1.1 reads desired state | Git
    1.2 reads live state | cluster
    1.3 compares states
    1.4 if there ar differences -> AUTOMATICALLY sync
  ```

### imperative

* YOU need to MANUALLY trigger it
  * YOU can try -- via -- CUSTOM script

```bash
git pull origin main

if [[ $(git rev-parse HEAD) != $(cat .last-commit) ]]; then
  echo "New commit detected, syncing..."
  
  # 1. trigger the sync
  kubectl apply -f manifests/
fi
```

## 4. Customize Sync processes

* goal
  * customize sync processes

### declarative

* declared | [Argo CD's Application](application-with-sync-policy.yaml)

  ```yaml
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
      allowEmpty: false
  
    syncOptions:
      - CreateNamespace=true
      - PruneLast=true
      - ApplyOutOfSyncOnly=true
  
    retry:
      limit: 5
      backoff:
        duration: 5s
        factor: 2
        maxDuration: 3m
  ```

* handled INTERNAL & AUTOMATICALLY -- by -- Argo CD

  ```
  1. Argo CD 
    1.1 reads desired state | Git
    1.2 reads live state | cluster
    1.3 compares states
    1.4 if there ar differences -> AUTOMATICALLY sync
  ```

### imperative

* YOU need to MANUALLY trigger it
  * YOU can try -- via -- TRICKY & large CUSTOM script
