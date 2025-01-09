import json

import requests
from flask import Flask, render_template

# TODO: Read Public List of Authors From Api
# TODO: Select From List of Authors With Searchable Table With Paging
# https://openlibrary.org/dev/docs/api/search
# TODO: Open New Page With All Author's books

author_name = "a"
author_search_endpoint = "https://openlibrary.org/search/authors.json"
author_search_params = {"q": author_name}

author_key = None
author_works_endpoint = f"https://openlibrary.org/authors/{author_key}/works.json"
works_limit = None
works_offset = None
author_works_params = {"limit": works_limit, "offset": works_offset}

# test_response = requests.get(url=author_search_endpoint, params=author_search_params)
# test_response.raise_for_status()
# test_data = test_response.json()
# test_json = json.dumps(test_data, indent=2)
# print(test_data["numFound"])
#
# with open("test.json", "w") as outfile:
#     outfile.write(test_json)

with open("test.json", "r") as test_file:
    test_data = json.load(test_file)

test_data_author_list = test_data["docs"]
author_list = []

for author_item in test_data_author_list:
    author_data = {
        "name": author_item["name"],
        "key": author_item["key"],
        "top_work": author_item["top_work"],
    }
    print(author_data["name"])
    author_list.append(author_data)

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html", authors=author_list)

if __name__ == "__main__":
    app.run(debug=True)
