# Designing Rate Limiter
Rate limiter is meant to be used in network systems for managing the speed of transfering the data from a client to a server. In the world of HTTP it is meant to limit the amount of requests, which user might send for the certain period of time. If the limit is exceeded, all the next requests are supposed to be blocked. There is a dedicated `429 HTTP status` code, which states - too many requests.

## User-wise cases:
- user can create not grater than 2 messages per second;
- from one IP address it is allowed to create not grater than 10 profiles per day;

## System-wise cases:
- Prevention of lack of system resources, issues due to DoS attack;
    - i.e. Twitter limits no more 300 tweets for 3 hours
    - i.e. API Google limits no more 300 write requests per 1 hour
- Saving budget, limiting exhausting requests, freeing up more resources for high priority requests;
- Prevention of overloading servers. To do so, rate limiters might filter out low priority requests;

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

![Screenshot 2024-12-20 at 15 23 14](https://github.com/user-attachments/assets/eec25e82-453d-4e70-9bc1-624f8710e586)


