"""
How it works

You do have a tokens bucket, with predifined bucket capacity for tokens. Tokens might be added and removed from bucket. 
When bucket has a capacity to add a token - its added, otherwise, token is discarded.

Every request consumes 1 token. When income request, we check, do we have enough tokens to process request.
If there are enough tokens - we remove token one by one from bucket and request is forwared further.
Otherwise we decline a request.

Whats neccessary to be defined overall:
    - bucket capacity
    - amount of tokens bucket is "filled" per which interval
    - amount of tokens a request consumes
    - rate limit threshold

On top, important to remember, it might be > 1 bucket. 
Examples: 
1. if user publishes 1 message per second, adds 150 friends during a day and likes 5 messages per seconds - 
we might consider 3 dedicated rate limiting buckets per each "action";

2. if its required to filter requests depending on IP-address, each IP-address might require dedicated bucket;
3. if system allows not grater than 10.000 RPS, it might require global bucket for all the requests.


Problem:
Assume, the system is meant to process no more than 10.000 requests per minute.
You are challenged to design and code a data structure, which will reproduce rate limiting functionalities. 
If rate limit occurred all other requests might be blocked (rejected).

Input parameters for:
    bucket size: int - max tokens amount, which bucket can hold
    refill frequency per second: int - amount of tokens, which are added to the bucket at every second
"""

import asyncio
import random
from loguru import logger


class TokenBucketRateLimiter:
    def __init__(self, max_capacity: int, refill_delay: int):
        self.max_capacity = max_capacity
        self.refill_delay = refill_delay
        self.counter_at_the_moment = max_capacity  # Start with a full bucket
        self.lock = asyncio.Lock()  # Ensure thread safety for counter updates
    
    async def refill(self):
        """Refill bucket periodically."""
        while True:
            await asyncio.sleep(self.refill_delay)
            async with self.lock:
                if self.counter_at_the_moment < self.max_capacity:
                    remaining = self.max_capacity - self.counter_at_the_moment
                    self.counter_at_the_moment += remaining
                    logger.info(f'Refilled: {remaining} tokens added. Total: {self.counter_at_the_moment}')
    
    async def worker(self, task_id: int):
        """Simulates a worker processing a request."""
        async with self.lock:
            if self.counter_at_the_moment > 0:
                self.counter_at_the_moment -= 1
                logger.info(f'Task {task_id}: Forwarded. Tokens left: {self.counter_at_the_moment}')
            else:
                logger.warning(f'Task {task_id}: Declined. Tokens left: {self.counter_at_the_moment}')

async def simulate_rate_limiter():
    # Parameters
    max_capacity = 10
    refill_delay = 5  # seconds
    rate_limiter = TokenBucketRateLimiter(max_capacity, refill_delay)
    
    # Run refill in the background
    asyncio.create_task(rate_limiter.refill())
    
    # Generate random tasks
    task_id = 0
    while True:
        await asyncio.sleep(random.uniform(0.2, 0.5))  # Random delay between tasks
        asyncio.create_task(rate_limiter.worker(task_id))
        task_id += 1

# Run the simulation
if __name__ == "__main__":
    asyncio.run(simulate_rate_limiter())
