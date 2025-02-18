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

async def main():
    connection = await asyncpg.connect(
        host="127.0.0.1",
        port=5430,
        user="postgres",
        database="postgres",
        password="password"
    )
    version = connection.get_server_version()
    print(f"Connected! Version of Postgres {version}")


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

asyncio.run(main())