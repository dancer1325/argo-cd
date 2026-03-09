# Authentication and Authorization

* separated | code base

## Logical layers

* | Argo CD API server, 
  * 4 DIFFERENT logical layers
    - **HTTP**
      - groups the *logical elements* / handle HTTP requests
      - 1! HTTP server / 
        - port: 8080
        - dispatch -- , based on request headers, to the -- proper server
          - gRPC
          - standard HTTP
    - [**gRPC**](https://grpc.io/)
      - groups the logical elements / responsible for: gRPC implementation
    - **AuthN**
      - responsible for: authentication
    - **AuthZ**
      - responsible for: authorization

![Argo CD Architecture](../../assets/argocd-arch-authn-authz.jpg)

## Logical elements

* | PREVIOUS diagram,
  * identified -- by -- numbers

* ALLOWED types
  * code base's 
    * object
    * function
    * component

1. [**Cmux**](https://github.com/soheilhy/cmux)
   * == library /
     * provide a 
       * connection / multiplexer capability 
     * allows
       * | 1 port, handle
         * standard HTTP requests
         * gRPC requests
     * responsible for
       * dispatch incoming requests -- , based on request headers, to the -- proper server
         * if the request version = `http1.x` -> dispatch -- to the -- *http mux*
         * if the request version = `http2` & contains the header `content-type: application/grpc` -> delegate -- to the -- *gRPC Server*

1. **HTTP mux**
   * == [standard HTTP multiplexer](https://pkg.go.dev/net/http#ServeMux) / handle NON gRPC requests
     * responsible for 
       * serving a unified REST API 
         * -- to the -- web UI
         * == expose ALL gRPC & non-gRPC services

1. **gRPC-gateway**
   * == [grpc-gateway library](https://github.com/grpc-ecosystem/grpc-gateway) /
     * translate internal gRPC services
     * expose internal gRPC services -- as a -- REST API
       * -> being accessible | Web UI
   * MOST Argo CD'S API services
     * implemented in gRPC

1. **gRPC Server**
   * == internal gRPC Server
     * responsible for
       * handling gRPC requests

1. **AuthN**
   * registered -- as a -- gRPC interceptor
     * Reason:🧠triggered / EACH gRPC request🧠 
   * responsible for
     * invoking the authentication logic

1. **Session Manager**
   * == object 
     * responsible for
       * managing Argo CD API server session
         * == validate the authentication token / provided | request
         * if Argo CD is configured -- to -- use an external AuthN provider -> delegate the validation to it

1. **AuthN Provider**
   * == pluggable component /
     * provide
       * authentication functionality  
         * _Examples:_login, token verification process
   * [MORE](../../operator-manual/user-management/index.md)

1. **Service Method**
   * == method / 
     * implement the business logic (core functionality) requested
       * _Example of business logic:_ `List Applications` 
     * responsible for
       * validate -- , by invoking the RBAC enforcement function, -- if the authenticated user has permission to execute this method

1. **RBAC**
   * == functions /
     * verify if the user has permission -- to -- execute a specific action | Argo CD
       * validate the incoming request action vs predefined RBAC rules
   * RBAC rules
     * ways to be configured
       * | Argo CD API server
       * | Argo CD `Project` CRD

1. [**Casbin**](https://casbin.org/)
   * == library / enforce RBAC rules

1. **AuthN Middleware**
   * == [HTTP Middleware](https://go.dev/wiki/LearnServerProgramming#middleware)
   * uses
     * verify the token -- for -- HTTP services / NOT implemented as gRPC

1. **HTTP Handler**
   * responsible for
     * invoking the business logic (core functionality) requested
       * _Example:_ `List Applications`
     * validate -- , by invoking the RBAC enforcement function, -- if the authenticated user has permission to execute this business logic
