# Authorization model
* -- based on -- [Apache Casbin](https://casbin.apache.org/)
* [built-in policy](builtin-policy.csv)
* [model](model.conf)

## model
* `obj`
  * -- depend on the -- resource
    * `<project>/<object>`
      * | Applications & Applicationsets & logs & exec (which belong to a project)
    * `<object>`
      * | REST of resources

## built-in policy
* define the roles
  * `role:readonly`
  * `role:admin`

### role 
* `g, role:admin, role:readonly`
  * == `role:admin`    inherits ALL `role:readonly`'s permissions
* `g, admin, role:admin`
  * == `admin` users belongs -- to -- `role:admin`
