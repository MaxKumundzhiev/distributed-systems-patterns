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


async def main():
    connection = await get_connection()
    # start transaction
    async with connection.transaction():
        await connection.execute(
            "INSERT INTO brand VALUES(DEFAULT, 'brand_1')"
        )
        await connection.execute(
            "INSERT INTO brand VALUES(DEFAULT, 'brand_2')"
        )
        query = """
        SELECT brand_name FROM brand WHERE brand_name LIKE 'brand%'
        """
        brands = await connection.fetch(query)
        print(brands)
        

asyncio.run(main())