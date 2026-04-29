# List Generator

* List generator
  * [data structure](/manifests/crds/applicationset-crd.yaml)'s `spec.generators[*].list`
    * `.elements`
      * == key/value []
    * `.elementsYaml`
      * == YAML string / key/value []
      * uses
        * list generator | Matrix generator
    * `.template`
      * override default ApplicationSet `spec.template`
  * generates parameters -- based on an -- arbitrary list of key/value pairs
    * Reason of arbitrary:🧠| ApplicationSet v0.1.0-, ONLY enable to specify | `list.elements[*]`
      * `url`
      * `cluster`
        * requirements
          * ⚠️ALREADY predefined | Argo CD⚠️
            * == ❌ApplicationSet controller does NOT create clusters | Argo CD❌ 
      * `values` 🧠 
    * requirements
      * string values

* _Example:_ [here](/applicationset/examples/list-generator)

## DYNAMICALLY generated elements

* -- through -- [matrix generator](Generators-Matrix.md) OR [merge generator](Generators-Merge.md)

* steps
  * PREVIOUS generator, generate parameters  
  * list generator use PREVIOUSLY generated parameters
