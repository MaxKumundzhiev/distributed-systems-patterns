# Designing Rate Limiter
Rate limiter is meant to be used in network systems for managing the speed of transfering the data from a client to a server. In the world of HTTP it is meant to limit the amount of requests, which user might send for the certain period of time. If the limit is exceeded, all the next requests are supposed to be blocked. There is a dedicated `429 HTTP status` code, which states - too many requests.

Rate Limiting might be applied on 7 diifferent levels of OSI (HTTP is 7th level, or IP is 3rd level).

## User-wise cases:
- user can create not grater than 2 messages per second;
- from one IP address it is allowed to create not grater than 10 profiles per day;

## System-wise cases:
- Prevention of lack of system resources, issues due to DoS attack;
    - i.e. Twitter limits no more 300 tweets for 3 hours
    - i.e. API Google limits no more 300 write requests per 1 hour
- Saving budget, limiting exhausting requests, freeing up more resources for high priority requests;
- Prevention of overloading servers. To do so, rate limiters might filter out low priority requests;


## Rate limiter algorithms
Implementaion of rate limiter might be done in various ways, where each has its pros and cons. Here's list of most popular ones:
- token bucket
- leaking bucket
- fixed window counter
- sliding window log
- sliding window counter

## Where to place rate limiter?
Commonly there are 3 main options:
1. place on a client side
```text
Note
Client side is not the most `safe` place to put a rate limiter, because clients requests might be easily forged by attackes. 
Moreover, someone else might be challanged to develop a client side.
```
2. place on a server side
```text
Note
common practice
```
![Screenshot 2024-12-20 at 15 20 23](https://github.com/user-attachments/assets/031173ae-79fb-4ea7-8f81-e84b69b28ac3)


3. place between a client and a server (aka gateway)
```text
Note
common practice
```

![Screenshot 2024-12-20 at 15 26 48](https://github.com/user-attachments/assets/1912c5d8-ed10-4e28-aefb-89fb0f50f25d)

## General Architecture
We concluded rate limiter is always about utilize an algorithm which composes some counter. The question now - `where to store` a counter. Due to data base is commonly too slow, we might use cache a storage, i.e. Redis, which supports features as `INCR` - increments the stored counter and `EXPIRE` - set a duration for the counter.

<img width="541" alt="Screenshot 2024-12-28 at 20 15 54" src="https://github.com/user-attachments/assets/b04dce85-b8d0-455b-8efb-2e70a0b35df2" />

1. client sends request to the gateway (rate limiter)
2. gateway (rate limiter) get counter from certain bucket from cache and checks the limit
    - if limit exceeds - request declines
    - if limit accepatble, request is redirected to the servers, in the meantime, counter is incremented and sent to the cache


## Rate Limiter in distributed environment
When developing rate limiter for disrtibuted environment, u commonly face 2 main issues:
1. race condition - resolved by `locking`
2. difficulty of syncronization - resolved by `centralized storage`
<img width="845" alt="Screenshot 2024-12-28 at 20 48 25" src="https://github.com/user-attachments/assets/9fb0b67f-6b8e-4b6b-8cd0-be7d1ca395f6" />
