import requests

API_KEY = "AIzaSyCfBps98EOqAIPXTrzLhP1I3IfbK_m3H10"      # <-- replace
CSE_ID = "c0dc676620d844c89"        # <-- replace

def get_first_image_src(query):
    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "q": query,
        "cx": CSE_ID,
        "key": API_KEY,
        "searchType": "image",
        "num": 1
    }

    res = requests.get(url, params=params).json()

    if "items" in res:
        return res["items"][0]["link"]   # direct image URL

    return None


if __name__ == "__main__":
    text = input("Search query: ")
    img_url = get_first_image_src(text)

    if img_url:
        print("First image URL:", img_url)
    else:
        print("No image found.")
