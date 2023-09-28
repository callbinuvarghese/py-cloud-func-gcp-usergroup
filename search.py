from urllib.parse import urlencode

def search_transitive_groups(service, member, page_size):
  try:
    groups = []
    next_page_token = ''
    while True:
      query_params = urlencode(
        {
          "query": "member_key_id == '{}' && 'cloudidentity.googleapis.com/groups.discussion_forum' in labels".format(member),
          "page_size": page_size,
          "page_token": next_page_token
        }
      )
      request = service.groups().memberships().searchTransitiveGroups(parent='groups/-')
      request.uri += "&" + query_params
      response = request.execute()

      if 'memberships' in response:
        groups += response['memberships']

      if 'nextPageToken' in response:
        next_page_token = response['nextPageToken']
      else:
        next_page_token = ''

      if len(next_page_token) == 0:
        break;

    return groups
  except Exception as e:
    print(e)
