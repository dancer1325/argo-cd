# TODO:

TODO:

# plugin / WITHOUT Matrix NOR Merge
* [Applicationset](applicationset.yaml)
* [configMap.yaml](configMap.yaml)
  * uses
    * plugin access -- for -- RPC call
* [secret](secretToStoreSensitiveData.yaml)
  * ways
    * "argocd-secret", OR
    * "another-secret"

# HTTP server

* [python plugin](pythonPlugin.pip)
* TODO:
  * steps to deploy as standalone deployment
  * | "/var/run/argo/token", place the token
    ```
    strong-password
    ```

- You only need to implement the calls `/api/v1/getparams.execute`
- You should check that the `Authorization` header contains the same bearer value as `/var/run/argo/token`. Return 403 if not
- The input parameters are included in the request body and can be accessed using the `input.parameters` variable.
- The output must always be a list of object maps nested under the `output.parameters` key in a map.
- `generator.input.parameters` and `values` are reserved keys. If present in the plugin output, these keys will be overwritten by the
  contents of the `input.parameters` and `values` keys in the ApplicationSet's Plugin generator spec.

# matrix generator / PR + plugin generators

* goal
  * ensure that >=1 PR are available
  * generated tag has been properly generated
    * ❌if you ONLY use PR generator -> ONLY a commit hash -> NOT enough❌

* [applicationSet](applicationsetMatrixOfPRAndPlugin.yaml)

* plugin implementation
  * return
    * a set of image digests / given branch
  * TODO: create OR find it

* _Example:_
  * PR generator
    * returns
      * "feature-branch-1"
      * "feature-branch-2"
  * -> plugin generator would request

  ```shell
  # 1) "feature-branch-1"
  curl http://localhost:4355/api/v1/getparams.execute -H "Authorization: Bearer strong-password" -d \
  '{
    "applicationSetName": "fb-matrix",
    "input": {
      "parameters": {
        "branch": "feature-branch-1"
      }
    }
  }'
  
  # 2) "feature-branch-2"
  curl http://localhost:4355/api/v1/getparams.execute -H "Authorization: Bearer strong-password" -d \
  '{
    "applicationSetName": "fb-matrix",
    "input": {
      "parameters": {
        "branch": "feature-branch-2"
      }
    }
  }'
  ```
    * ALLOWED responses   
      * \1)
      ```
      {
        "output": {
          "parameters": [
            {
              "digestFront": "sha256:a3f18c17771cc1051b790b453a0217b585723b37f14b413ad7c5b12d4534d411",
              "digestBack": "sha256:4411417d614d5b1b479933b7420079671facd434fd42db196dc1f4cc55ba13ce"
            }
          ]
        }
      }
      ```
      * \2)
      ```
      {
        "output": {
          "parameters": [
            {
              "digestFront": "sha256:7c20b927946805124f67a0cb8848a8fb1344d16b4d0425d63aaa3f2427c20497",
              "digestBack": "sha256:e55e7e40700bbab9e542aba56c593cb87d680cefdfba3dd2ab9cfcb27ec384c2"
            }
          ]
        }
      }
      ```