#!/bin/sh

# $ARGOCD_APP_PARAMETERS
#   == JSON / has ALL parameters
ARGUMENTS=$(echo "$ARGOCD_APP_PARAMETERS" | jq -r '.[] | select(.name == "values-files").array | .[] | "--values=" + .')

# $ARGOCD_APP_PARAMETERS
#   == JSON / has ALL parameters
PARAMETERS=$(echo "$ARGOCD_APP_PARAMETERS" | jq -r '.[] | select(.name == "helm-parameters").map | to_entries | map("\(.key)=\(.value)") | .[] | "--set=" + .')

# NEXT command
#   == helm template <PASSING_ARGUMENTS_PARAMETERS>
echo ". $ARGUMENTS $PARAMETERS" | xargs helm template
