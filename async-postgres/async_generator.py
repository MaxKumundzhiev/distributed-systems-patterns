import asyncio

async def positive_integers(until: int):
  for integer in range(until):
    asyncio.sleep(1)
    yield integer

async def main():
  async_gen = positive_integers(until=5)
  async for int_ in async_gen:
    print(int_)

asyncio.run(main())