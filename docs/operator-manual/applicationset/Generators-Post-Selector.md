# Post Selector all generators

* `spec.generators[*].selector`
  * allows post-filter `ApplicationSet` results
  * `.matchLabels`
    * follow the [Kubernetes common labelSelector format](https://kubernetes.io/docs/concepts/overview/working-with-objects/labels/#label-selectors) 
    * == map of `key:value` pairs
  * `.matchExpressions`
    * MORE powerful

    ```
    - key: <SOME_KEY>
      operator: <CHOOSE_VALID_OPERATOR> 
      values:
        - <SOME_VALUE>
    - ...
    ```
    * `<CHOOSE_VALID_OPERATOR>`
      * `In` OR `NotIn` OR `Exists` OR `DoesNotExist`
    * `<SOME_VALUE>`
      * ⚠️if you use `In` OR `NotIn` -> MUST be NON-empty⚠️ 
