from ..form import SearchForm
from django.shortcuts import render
import requests
import json

def google_api_request(words):
    """
    make a search on google books api
    """
    r = requests.get("https://www.googleapis.com/books/v1/volumes?q=" + words)
    parsed = r.json()
    return parsed


def isbn_text_search(words):
    """
    make a search request based on title or authors
    """
    # r = requests.get('https://www.googleapis.com/books/v1/volumes?q='+ words)
    # parsed = r.json()
    parsed_words = google_api_request(words)
    # check if isbn identifier is not null
    for x in parsed_words["items"]:
        if "industryIdentifiers" not in x["volumeInfo"]:
            parsed_words["items"].remove(x)
        else:
            print("No ISBN number found")
    return parsed_words["items"]


def input_cleaner(search_data):
    """
    make a search request based on isbn number
    """
    try:
        if type(int(search_data)):
            res = requests.get(
                "https://www.googleapis.com/books/v1/volumes?q=isbn:" + str(search_data)
            )
            parsed_res = res.json()
            return parsed_res["items"][0]["volumeInfo"]["title"]
    except (ValueError, KeyError) as error:
        print(error)
        return search_data

def search_result(request):
    form = SearchForm(request.GET)
    if form.is_valid():
        data = form.cleaned_data["post"].casefold()
        if data:
            # check if input is isbn number or title
            checked_input = input_cleaner(str(data))
            # search on title
            result = isbn_text_search(str(checked_input))
            request.session["temp_json"] = result
            context = {"form": form, "result": result}
            return render(request, "search_result.html", context)
        else:
            context = {"form": form}
            return render(request, "search_result.html", context)