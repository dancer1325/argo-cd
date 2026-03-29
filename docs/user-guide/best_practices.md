# Best Practices

## 💡Separate source code repositories & config repository 💡

* Reasons:🧠

  1. clean separation of application code vs. application config
     * enable
       * modify ONLY the manifests / WITHOUT triggering an entire CI build
         * _Example:_ if you change the Deployment spec's number of replicas -> likely you do NOT want to trigger a build

  2. Cleaner audit log
     * NOT mix audit logs

  3. application / built from MULTIPLE Git repositories & deployed as a 1! unit
     * _Example:_ Kafka + ZooKeeper
     * NOT sense to store the manifests | 1 one of the source code repositories

  4. Separation of access
     * people / have got access to source code != people / have got access to the manifests

  5. | automate your CI pipeline & source code + manifest | SAME Git repository, POSSIBLE INFINITE loop🧠

## Leaving room for dynamism

* == ❌NOT manage ALL | Git❌
  * _Example:_ your deployment's replicas number is managed -- by -- [Horizontal Pod Autoscaler](https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale/)
    * -> you do NOT want to track `replicas` | Git

## specify EXTERNAL manifests -- with -- IMMUTABLE Git revisions 

* EXTERNAL
  * != your source code
* OTHERWISE, 
  * ⚠️output would change ⚠️

* _Example:_ manifests point to EXTERNAL repo's HEAD revision & they are updated -> your manifests change without awareness
