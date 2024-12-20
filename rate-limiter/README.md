# Designing Rate Limiter
Rate limiter is meant to be used in network systems for managing the speed of transfering the data from a client to a server. In the world of HTTP it is meant to limit the amount of requests, which user might send for the certain period of time. If the limit is exceeded, all the next requests are supposed to be blocked.

## User-wise cases:
- user can create not grater than 2 messages per second;
- from one IP address it is allowed to create not grater than 10 profiles per day;

## System-wise cases:
- Prevention of lack of system resources, issues due to DoS attack;
    - i.e. Twitter limits no more 300 tweets for 3 hours
    - i.e. API Google limits no more 300 write requests per 1 hour
- Saving budget, limiting exhausting requests, freeing up more resources for high priority requests;
- Prevention of overloading servers. To do so, rate limiters might filter out low priority requests;





