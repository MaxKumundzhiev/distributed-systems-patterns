import asyncio
import asyncpg

from asyncpg.transaction import Transaction


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


async def manual_transaction():
    connection = await get_connection()
    transaction: Transaction = connection.transaction()
    await transaction.start()
    try:
        await connection.execute("INSERT INTO brand VALUES(DEFAULT, 'brand_1')")
        await connection.execute("INSERT INTO brand VALUES(DEFAULT, 'brand_2')")
    except asyncpg.PostgresError:
        print("issue, transaction rollback")
        await transaction.rollback()
    else:
        print("good, transaction committing")
        await transaction.commit()
    query = """
    SELECT brand_name FROM brand WHERE brand_name LIKE 'brand%'
    """
    brands = await connection.fetch(query)
    print(f'query res: {brands}')
    await connection.close()


asyncio.run(manual_transaction())
