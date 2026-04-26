# ApplicationSet Security

## ONLY admins should create/update/delete ApplicationSets

* how?
  * -- via -- Kubernetes RBAC

* ApplicationSets
  * can 
    * create Applications | arbitrary projects
    * reveal privileged information
      * _Example:_ [git generator](./Generators-Git.md) can
        * read Secrets | Argo CD namespace
        * send them -- to -- arbitrary URLs

![](/docs/assets/applicationset/security/restrictWhoPushesOnApplicationSetSourceOfTruth.png)

## Admins MUST apply appropriate controls -- for -- ApplicationSets' sources of truth

* POSSIBLE risk
  * ApplicationSet / uses a [git generator](./Generators-Git.md)
    * malicious user pushes | source git repository -> generate HIGH number of Applications

![](/docs/assets/applicationset/security/restrictWhoPushesOnApplicationSetSourceOfTruth.png)

### `spec.template.spec.project`

* recommendations
  * hardcode it
  * if it's NOT hardcode it -> admins should control ApplicationSet's generators' sources of truth

* POSSIBLE risk
  * Application | unrestricted Project (_Example:_ `default`),
    * could take control -- , by modifying its RBAC ConfigMap, -- of Argo CD
