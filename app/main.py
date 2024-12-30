from fastapi import FastAPI, Query, Path
from fastapi.responses import RedirectResponse

from typing import Union
from typing_extensions import Annotated

from .db.database import Database
from .db.redis_cache import RedisCache
from .uid_generator import UniqueIDGenerator
from .utils import create_url_from_uid

app = FastAPI()

# A unique ID generator for this machine/process
generator = UniqueIDGenerator()


@app.post("/shorten/")
async def shorten_url(long_url: Annotated[str, Query(min_legnth=10, max_length=2000)]):

    # check if url in cache
    redis_cache = RedisCache()
    response = redis_cache.get(long_url)

    # check if url in database
    db_instance = Database()
    response = db_instance.get_data_by_long_url(long_url)

    if len(response) > 0:
        return {"short_url": response[0][2]}

    # create a new url entry
    new_entry = create_url_from_uid(generator.get_unique_id(), long_url)
    db_instance.insert_new_entry(new_entry)

    # load into cache
    redis_cache.set(new_entry["short_url"], new_entry["long_url"])
    redis_cache.set(new_entry["long_url"], new_entry["short_url"])

    return {"short_url": new_entry["short_url"]}


@app.get("/fetch/{short_url}")
def fetch_long_url(short_url: Annotated[str, Path(min_legnth=5, max_length=25)]):
    # search for short_url in cache
    redis_cache = RedisCache()
    response = redis_cache.get(short_url)
    if response is not None:
        # use 301 permanent redirect to let users' browser cache long_url
        return RedirectResponse(response.decode("utf-8"), status_code=301)

    # search for short_url in SQL
    db_instance = Database()
    response = db_instance.get_data_by_short_url(short_url)

    # short_url not found
    if not response:
        raise ValueError

    # bring result to cache
    fetched_short, fetched_long = response[0][2], response[0][1]
    redis_cache.set(fetched_short, fetched_long)

    # use 301 permanent redirect to let users' browser cache long_url
    return RedirectResponse(fetched_long.decode("utf-8"), status_code=301)
