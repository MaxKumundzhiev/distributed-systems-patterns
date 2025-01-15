# Key Concepts
- queue - placeholder for the messages (commonly FIFO order)
- producer - stands for writing a message to the queue
- broker - stands for picking a message from the queue and routing it to the subscriber
- consumer - stands for reading a message


## RabbitMQ
RabbitMQ is a implementation of `tasks` queue. RabbitMQ works on `AMQP` protocol.


## Run components
*Spin up RabbitMQ with manager*
```bash
$ docker compose up -d
```

*Spin up publisher*
```bash
$ python publisher.py
```

*Spin up consumer*
```bash
$ python consumer.py
```