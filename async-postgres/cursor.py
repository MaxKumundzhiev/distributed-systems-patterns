import asyncio
import asyncpg


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


async def cursor():
    connection = await get_connection()
    query = "SELECT product_id, product_name FROM product;"
    async with connection.transaction():
        async for product in connection.cursor(query):
            print(product)
    await connection.close()

async def move_cursor():
    connection = await get_connection()
    query = "SELECT product_id, product_name FROM product;"
    async with connection.transaction():
        cursor = await connection.cursor(query)
        await cursor.forward(500)
        products = await cursor.fetch(100)
        for product in products:
            print(product)
    await connection.close()


asyncio.run(move_cursor())