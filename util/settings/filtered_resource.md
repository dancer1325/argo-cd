# `type FilteredResource struct {`
* ``APIGroups []string `json:"apiGroups,omitempty"``
  * / EACH string
    * == glob / match the API group
      * ⚠️if you write an INVALID glob -> WHOLE rule is ignored⚠️
* ``Kinds     []string `json:"kinds,omitempty"``
  * / EACH string
    * == kind
* ``Clusters  []string `json:"clusters,omitempty"``
  * / EACH string
    * == glob / match the cluster URL
      * ⚠️if you write an INVALID glob -> WHOLE rule is ignored⚠️
* ⚠️requirements⚠️
  * match ALL properties
