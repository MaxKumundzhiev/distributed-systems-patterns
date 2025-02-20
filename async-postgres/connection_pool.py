import asyncio
import asyncpg
from datetime import datetime

from statements import GET_PRODUCTS as product_query

async def query_product(pool):
    async with pool.acquire() as connection:
        start = datetime.now()
        await connection.fetchrow(product_query)
        end = datetime.now()
        print(f"query done for {end-start}")
        return 


async def main():
    async with asyncpg.create_pool(host='127.0.0.1',
                                   port=5430,
                                   user='postgres',
                                   password='password',
                                   database='postgres',
                                   min_size=6,
                                   max_size=6) as pool:
        queries = [query_product(pool) for _ in range(10000)]
        await asyncio.gather(*queries)


asyncio.run(main())