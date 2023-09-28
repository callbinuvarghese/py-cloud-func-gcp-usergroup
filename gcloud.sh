export PROJECT_ID=$(gcloud config get-value project)
export PROJECT_NUMBER=$(gcloud projects describe $PROJECT_ID --format='value(projectNumber)')
export PROJECT_NAME=$(gcloud projects describe $PROJECT_ID --format='value(name)')
export REGION=us-east1

export _SA_EMAIL="${PROJECT_NUMBER}-compute@developer.gserviceaccount.com"
export _CUSTOM_ROLE="custom.searchTransitiveGroups"

echo "PROJECT_ID:${PROJECT_ID}"
echo "PROJECT_NUMBER:${PROJECT_NUMBER}"
echo "PROJECT_NAME:${PROJECT_NAME}"
echo "REGION:${REGION}"

echo "_SA_EMAIL:${_SA_EMAIL}"
echo "_CUSTOM_ROLE:${_CUSTOM_ROLE}"

# Enable the API Service for Cloud Identity
gcloud services enable cloudidentity.googleapis.com

echo "Creating a new Custom role ${_CUSTOM_ROLE}"
gcloud iam roles create ${_CUSTOM_ROLE} --project=${PROJECT_ID} --file=custom-role.yaml
exit

echo "Adding the service account:${_SA_EMAIL} Custom role ${_CUSTOM_ROLE}"
gcloud projects add-iam-policy-binding ${PROJECT_ID} \
    --member="serviceAccount:${_SA_EMAIL}" \
    --role="projects/${PROJECT_ID}/roles/${CUSTOM_ROLE}"

# Build cloud function
gcloud functions deploy py-get-usergrps \
--gen2 \
--runtime=python311 \
--region=$REGION \
--source=. \
--entry-point=get_usergroups \
--trigger-http \
--allow-unauthenticated

# Test using curl
curl -m 70 -X POST https://us-east4-acn-highmark-health-odh.cloudfunctions.net/py-get-usergrps \
-H "Authorization: bearer $(gcloud auth print-identity-token)" \
-H "Content-Type: application/json" \
-d '{
  "name": "Hello World"
}'