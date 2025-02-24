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


async def succ_transaction():
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
        

async def fail_transaction():
    connection = await get_connection()
    async with connection.transaction():
        try:
            insert_brand = "INSERT INTO brand VALUES(9999, 'big_brand')"
            await connection.execute(insert_brand)
            await connection.execute(insert_brand)
        except Exception as e:
            print(f"issue executing insert stmt: {e}")
        finally:
            query = """
            SELECT brand_name FROM brand WHERE brand_name LIKE 'brand%';
            """
            brands = await connection.fetch(query)
            print(f"query res: {brands}")
            await connection.close()


asyncio.run(fail_transaction())