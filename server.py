import json

import requests
from flask import Flask, redirect, render_template, request

# TODO: Read Public List of Authors From Api
# TODO: Select From List of Authors With Searchable Table With Paging
# https://openlibrary.org/dev/docs/api/search
# TODO: Open New Page With All Author's books


author_key = None
author_works_endpoint = f"https://openlibrary.org/authors/{author_key}/works.json"
works_limit = None
works_offset = None
author_works_params = {"limit": works_limit, "offset": works_offset}

with open("test.json", "r") as test_file:
    test_data = json.load(test_file)

test_data_author_list = test_data["docs"]


def get_openl_authors(author_name):
    author_name = author_name
    author_search_endpoint = "https://openlibrary.org/search/authors.json"
    author_search_params = {"q": author_name}
    response = requests.get(url=author_search_endpoint, params=author_search_params)
    response.raise_for_status()
    data = response.json()
    return data["docs"]


def author_json_to_list_of_dicts(author_list_data, items_per_page):
    author_list = []

    for author_item in author_list_data:
        author_data = {
            "name": author_item["name"],
            "key": author_item["key"],
            "top_work": author_item["top_work"],
        }
        author_list.append(author_data)

    author_list = [
        author_list[items_per_page * i : items_per_page * (i + 1)]
        for i in range(len(author_list) // items_per_page + 1)
    ]
    return author_list


items_per_page = 20
authors = author_json_to_list_of_dicts(test_data_author_list, items_per_page)
page = 0

app = Flask(__name__)


@app.route("/")
def home():
    return redirect("/author_search")


@app.route("/author_search")
def author_search():
    global authors, page
    return render_template(
        "author_search.html", authors=authors[page], page=page, list_length=len(authors)
    )


@app.route("/next_page")
def next_page():
    global page
    page += 1
    return redirect("author_search")


@app.route("/prev_page")
def prev_page():
    global page
    page -= 1
    return redirect("author_search")


@app.route("/author_search", methods=["POST"])
def search_author():
    global authors, page, items_per_page
    authors = author_json_to_list_of_dicts(
        get_openl_authors(request.form["author_name"]), items_per_page=items_per_page
    )
    page = 0
    return redirect("author_search")


if __name__ == "__main__":
    app.run(debug=True)
