import json

import requests
from flask import Flask, redirect, render_template

# TODO: Read Public List of Authors From Api
# TODO: Select From List of Authors With Searchable Table With Paging
# https://openlibrary.org/dev/docs/api/search
# TODO: Open New Page With All Author's books


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


def search_authors(author_name):
    author_search_endpoint = "https://openlibrary.org/search/authors.json"
    author_search_params = {"q": author_name}
    response = requests.get(url=author_search_endpoint, params=author_search_params)
    response.raise_for_status()
    data = response.json()
    return data["docs"]


def get_list_of_author_dicts(author_list_data):
    author_list = []

    for author_item in author_list_data:
        author_data = {
            "name": author_item["name"],
            "key": author_item["key"],
            "top_work": author_item["top_work"],
        }
        author_list.append(author_data)

    author_list = [
        author_list[10 * i : 10 * (i + 1)] for i in range(len(author_list) // 10 + 1)
    ]
    return author_list


app = Flask(__name__)


@app.route("/")
def home():
    return redirect("/author_search/a/0")


@app.route("/author_search/<author_name>/<int:page>", methods=["GET", "POST"])
def author_search(author_name, page):
    return render_template(
        "author_search.html",
        authors=get_list_of_author_dicts(search_authors(author_name)),
        page=page,
    )


@app.route("/search_author")
def search_author():
    return ""


if __name__ == "__main__":
    app.run(debug=True)
