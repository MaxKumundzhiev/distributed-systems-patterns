"""
How it works
Tokens bucket algorithm + FIFO queue

- once incoming request, system checks, if a queue is full. Request is added to the queue if queue has a place. otherwise discarded.
- requests are pulled from queue and are processed after equal periods of time.
"""


import asyncio
import random
from loguru import logger


class LeakingBucketRateLimiter:
    def __init__(self, bucket_max_capacity: int, bucket_refill_delay: int, queue_max_capacity: int, queue_pulling_time: int):
        self.bucket_max_capacity = bucket_max_capacity
        self.bucket_refill_delay = bucket_refill_delay
        self.tokens_counter_at_the_moment = bucket_max_capacity  # Start with a full bucket
        self.bucket_lock = asyncio.Lock()  # Ensure thread safety for counter updates
        self.queue = asyncio.Queue(maxsize=queue_max_capacity)
        self.queue_pulling_time = queue_pulling_time

    async def tokens_refill(self):
        """Refill bucket periodically."""
        while True:
            await asyncio.sleep(self.bucket_refill_delay)
            async with self.bucket_lock:
                if self.tokens_counter_at_the_moment < self.bucket_max_capacity:
                    remaining = self.bucket_max_capacity - self.tokens_counter_at_the_moment
                    self.tokens_counter_at_the_moment += remaining
                    logger.info(f"Refilled: {remaining} tokens added. Total: {self.tokens_counter_at_the_moment}")

    async def add_task_to_queue(self, task_id: int):
        """Attempts to add a task to the queue."""
        try:
            await self.queue.put(task_id)
            logger.info(f"Task {task_id} added to the queue.")
        except asyncio.QueueFull:
            logger.warning(f"Task {task_id} dropped due to a full queue.")

    async def process_queue(self):
        """Process tasks in the queue at a steady rate."""
        while True:
            await asyncio.sleep(self.queue_pulling_time)
            if not self.queue.empty():
                task_id = await self.queue.get()
                logger.info(f"Processing task {task_id} from the queue.")
            else:
                logger.info("Queue is empty.")

    async def worker(self, task_id: int):
        """Simulates a worker processing a request."""
        async with self.bucket_lock:
            if self.tokens_counter_at_the_moment > 0:
                self.tokens_counter_at_the_moment -= 1
                logger.info(f"Task {task_id}: Forwarded. Tokens left: {self.tokens_counter_at_the_moment}")
                await self.add_task_to_queue(task_id)
            else:
                logger.warning(f"Task {task_id}: Declined. Tokens left: {self.tokens_counter_at_the_moment}")

async def simulate_rate_limiter():
    # Parameters
    bucket_max_capacity = 10          # Large enough to allow tasks to pass to the queue
    bucket_refill_delay = 5           # Refill delay remains moderate
    queue_max_capacity = 3            # Small queue capacity to hit full state
    queue_pulling_time = 3  

    rate_limiter = LeakingBucketRateLimiter(
        bucket_max_capacity=bucket_max_capacity,
        bucket_refill_delay=bucket_refill_delay, 
        queue_max_capacity=queue_max_capacity,
        queue_pulling_time=queue_pulling_time
    )

    # Run background tasks
    asyncio.create_task(rate_limiter.tokens_refill())
    asyncio.create_task(rate_limiter.process_queue())

    # Generate random tasks
    task_id = 0
    while True:
        await asyncio.sleep(random.uniform(0.1, 0.2))  # Random delay between tasks
        asyncio.create_task(rate_limiter.worker(task_id))
        task_id += 1

if __name__ == "__main__":
    asyncio.run(simulate_rate_limiter())
