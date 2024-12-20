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


class TokenBucket:
    def __init__(
        self, bucket_size: int, refill_frequency_per_second: int
    ) -> None:
        self.__size = bucket_size
        self.__frequency = refill_frequency_per_second
        self.__tokens = ...
    
    def refill_bucket(self) -> None:
        ...
    
    def forward_reques(self):
        ...
    
    def decline_request(self):
        ...
    
    def process_request(self):
        ...