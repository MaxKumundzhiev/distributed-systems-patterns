"""
CB - state machine

CB States
    - CLOSED    - запросы к сервису выполняются нормально
    - OPEN      - когда количество ответов с НЕуспешным статусом > порог - статус становиться OPEN и CB перстает отправлять запросы caller-а к зависящему сервису, вместо сразу блокирует
    - HALF-OPEN - после некоторого времени (delay), CB переходит в состоянии HALF-OPEN и пробует опросить зависящей сервис, при этом все еще приходящие запросы блокируются, если сервис снова работает, CB переходит в CLOSED состояние 

CB Stores
    - total requests
    - failure threshold
    - failued requests - (total_requests / failied_requests)
    - recovery time
"""