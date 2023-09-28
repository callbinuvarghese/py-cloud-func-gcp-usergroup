import functions_framework
import search
import google.cloud.logging
import logging
import googleapiclient.discovery
import google.auth
import google.auth.transport.requests


# Imports the Cloud Logging client library
import google.cloud.logging

# Instantiates a client
client = google.cloud.logging.Client()

# Retrieves a Cloud Logging handler based on the environment
# you're running in and integrates the handler with the
# Python logging module. By default this captures all logs
# at INFO level and higher
client.setup_logging()


@functions_framework.http
def get_usergroups(request):
    """HTTP Cloud Function.
    Args:
        user name of the user in gcp
    Returns:
        user groups that the person is a member of
    Note:
       testing 
    """

    client = google.cloud.logging.Client()
    client.setup_logging()
    logging.info('Received function call usergroups_get')
    username = request.args.get('username')
    logging.info(f'usergroups_get username={username}')

    # getting the credentials and project details for gcp project
    userscope="https://www.googleapis.com/auth/cloud-platform"
    credentials, your_project_id = google.auth.default(scopes=[f"{userscope}"])
    logging.info(f'usergroups_get got creds for userscope={userscope}')


    #getting request object
    auth_req = google.auth.transport.requests.Request()
    logging.info(f'usergroups_get auth_req got')

    logging.info(f"credentials valid={credentials.valid}") # prints False
    credentials.refresh(auth_req) #refresh token
    logging.info(f"credentials refreshed")

    #cehck for valid credentials
    logging.info(f"usergroups_get credentials.valid={credentials.valid}")  # prints True
    logging.info(f"usergroups_get credentials.token={credentials.token}") # prints token
    logging.info(f"usergroups_get project_id={your_project_id}")

    logging.info(f"usergroups_get getting discovery service");
    service = googleapiclient.discovery.build('cloudidentity', 'v1')

    logging.info(f"usergroups_get calling search transitive with limit of 50")
    # Return results with a page size of 50
    groups = search.search_transitive_groups(service, 'binu.b.varghese@accenture.com', 50)

    return groups