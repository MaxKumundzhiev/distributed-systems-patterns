# Idempotence
**important**
Idempotency of an API is determined by the changes it makes to the system, not the response it provides.

Idempotency is a property of API design that ensures that making the same request multiple times produces the same result as making it once. In other words, no matter how many times an idempotent API endpoint is invoked with the same set of parameters, the outcome remains unchanged after the first successful request.

In the context of API designing, idempotency is crucial to prevent unintended side effects and ensure the predictability and reliability of the API. It allows clients to safely retry requests without causing any data duplication, overwriting, or other unwanted effects.

**To better understand the above statement, consider this example:**

- Consider an API endpoint that is designed to sign up a new user account in a web application. If this API is idempotent, it means that no matter how many times the API is called with the same input data (e.g., the same email and password), it will create the user account only once, and any subsequent invocations will have no further effect.

- The API may return a successful response (e.g., status code 200) for the first request and subsequent requests, indicating that the user account already exists, but the system state remains unchanged.

- The idempotency is evaluated based on the side effect of creating the user account, not the response message.


# How to Implement Idempotency in API Design?
- Assign unique identifiers: Use UUIDs or other unique identifiers for each request to track and identify requests.

- Idempotent HTTP methods: Design APIs using idempotent HTTP methods like GET, PUT, and DELETE. These methods ensure that multiple identical requests have the same effect as a single request.

- Expiration time for idempotency keys: Set a reasonable expiration time for idempotency keys to ensure they are valid only for a certain period.

- Response codes and headers: Utilize appropriate HTTP status codes (e.g., 200, 201, 204) and headers (e.g., ETag, Last-Modified) to indicate idempotency and successful processing.

# What are Idempotency Keys?
- Before making an API call, the client requests a random ID from the server, which acts as the idempotency key | Before making an API call the client generates a random ID, which acts as an idempotency key.

- The client includes this key in all future requests to the server. The server stores the key and request details in its database.

- When the server receives a request, it checks if it has already processed the request using the idempotency key.

- If it has, the server ignores the request. If not, it processes the request and removes the idempotency key, ensuring processing is done only once.