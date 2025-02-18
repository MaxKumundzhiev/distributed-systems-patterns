import asyncio
import asyncpg

from statements import (
    CREATE_PRODUCT_TABLE,
    CREATE_BRAND_TABLE,
    CREATE_PRODUCT_COLOR_TABLE,
    CREATE_PRODUCT_SIZE_TABLE,
    CREATE_SKU_TABLE,
    SIZE_INSERT,
    COLOR_INSERT
)

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


async def creation():
    connection = await get_connection()

    statements = [
        CREATE_BRAND_TABLE,
        CREATE_PRODUCT_TABLE,
        CREATE_PRODUCT_SIZE_TABLE,
        CREATE_PRODUCT_COLOR_TABLE,
        CREATE_SKU_TABLE,
        SIZE_INSERT,
        COLOR_INSERT
    ]
    print("creating db tables")
    for statement in statements:
        status = await connection.execute(statement)
        print(status)
    print("db tables created")
    await connection.close()


async def insert_and_fetch():
    from asyncpg import Record
    from typing import List

    connection = await get_connection()
    await connection.execute("INSERT INTO brand VALUES(DEFAULT, 'Levis')")
    await connection.execute("INSERT INTO brand VALUES(DEFAULT, 'Seven')")

    brand_query = "SELECT brand_id, brand_name FROM brand;"
    result: List[Record] = await connection.fetch(brand_query)
    for brand in result:
        print(f"id {brand['brand_id']}, name: {brand['brand_name']}")
    await connection.close()

asyncio.run(insert_and_fetch())