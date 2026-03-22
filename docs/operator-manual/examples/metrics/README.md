# Application Controller Metrics

## Expose Application labels -- as -- Prometheus metrics

* [argoCDApplicationControllerExposingApplicationLabels.yaml](argoCDApplicationControllerExposingApplicationLabels.yaml)
* the metric would look like

    ```
    # TYPE argocd_app_labels gauge
    argocd_app_labels{label_business_unit="bu-id-1",label_team_name="my-team",name="my-app-1",namespace="argocd",project="important-project"} 1
    argocd_app_labels{label_business_unit="bu-id-1",label_team_name="my-team",name="my-app-2",namespace="argocd",project="important-project"} 1
    argocd_app_labels{label_business_unit="bu-id-2",label_team_name="another-team",name="my-app-3",namespace="argocd",project="important-project"} 1
    ```

## Expose Application conditions -- as -- Prometheus metrics

* [argoCDApplicationControllerExposingApplicationConditions.yaml](argoCDApplicationControllerExposingApplicationConditions.yaml)
* the metric would look like

    ```
    # TYPE argocd_app_condition gauge
    # TODO: check the label format
    argocd_app_condition{condition="OrphanedResourceWarning",name="my-app-1",namespace="argocd",project="important-project"} 1
    argocd_app_condition{condition="SharedResourceWarning",name="my-app-2",namespace="argocd",project="important-project"} 1
    ```

## Expose Cluster labels -- as -- Prometheus metrics

* [argoCDApplicationControllerExposingClusterLabels.yaml](argoCDApplicationControllerExposingClusterLabels.yaml)
* the metric would look like

  ```
  # TYPE argocd_cluster_labels gauge
  argocd_cluster_labels{label_environment="dev",label_team_name="team1",name="cluster1",server="server1"} 1
  argocd_cluster_labels{label_environment="staging",label_team_name="team2",name="cluster2",server="server2"} 1
  argocd_cluster_labels{label_environment="production",label_team_name="team3",name="cluster3",server="server3"} 1
  ```


# TODO: