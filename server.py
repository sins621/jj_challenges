import json

import requests
from flask import Flask

# TODO: Read Public List of Authors From Api
# TODO: Select From List of Authors With Searchable Table With Paging
# https://openlibrary.org/dev/docs/api/search
# TODO: Open New Page With All Author's books

author_name = "Bradly"
author_search_endpoint = "https://openlibrary.org/search/authors.json"
author_search_params = {"q": author_name}

author_key = None
author_works_endpoint = f"https://openlibrary.org/authors/{author_key}/works.json"
works_limit = None
works_offset = None
author_works_params = {"limit": works_limit, "offset": works_offset}

test_response = requests.get(url=author_search_endpoint, params=author_search_params)
test_response.raise_for_status()
test_data = test_response.json()
test_json = json.dumps(test_data, indent=2)
print(test_data["numFound"])

with open("test.json", "w") as outfile:
    outfile.write(test_json)
