# Web scraper api

This api has endpoints that send twwets and news headlines of a ticker as the response.
By default, it returns 40 and 80 rows respectively, due to the time intensive web scraping.

## End points

test endpoint - http://127.0.0.1:8000
sample tweets - http://127.0.0.1:8000/tweets-example/
get tweets - http://127.0.0.1:8000/tweets/?ticker=tsla
get news - http://127.0.0.1:8000/news/?ticker=tsla
api docs(swagger ui) - http://127.0.0.1:8000/docs

## Steps to run

1. clone the repository
2. `virtualenv venv` to create a virtual environment
3. `source venv/Scripts/activate` to activate the virtual environment
4. `pip install -r requirements.txt`
5. Run the app using `python -m uvicorn main:app --reload`