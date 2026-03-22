# Commit Server

* Argo CD Commit Server
  * provides
    * | hydrated manifests, push access -- to -- git repositories 
  * exposes
    * [gRPC service](/commitserver/commit/commit.proto) /
      * accepted requests: push hydrated manifests -- to a -- git repository
