import asyncio
import asyncpg
from typing import List, Tuple, Union
from random import sample

def load_common_words() -> List[str]:
    filepath = "common_words.txt"
    with open(filepath) as common_words:
        return common_words.readlines()

def generate_brand_names(words: List[str]) -> List[Tuple[Union[str,]]]:
    return [(words[index],) for index in sample(range(100), 100)]

async def insert_brands(common_words, connection) -> int:
    brands = generate_brand_names(common_words)
    insert_brands = "INSERT INTO brand VALUES(DEFAULT, $1)"
    return await connection.executemany(insert_brands, brands)

async def get_connection():
    connection = await asyncpg.connect(
        host="127.0.0.1",
        port=5430,
        user="postgres",
        database="postgres",
        password="password"
    )
    version = connection.get_server_version()
    print(f"Connected! Version of Postgres {version}")
    return connection

async def main():
    common_words = load_common_words()
    connection = await get_connection()
    await insert_brands(common_words, connection)


asyncio.run(main())