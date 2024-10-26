"""
Implementation of idempotence key.

- if new request
    - Add {idempotence_key: {"occurred":now, "expire":future}} to idempotence hash map
    - Add {username: password} to users hash map
- if sequential request and idempotence key has not expired
    - return 200
- if sequential request and idempotence key has expired
    - remove idempotence key from hash map
    - return 200
"""

from json import dumps
from datetime import datetime, timedelta

from fastapi import FastAPI, Header, Response, status
from pydantic import BaseModel


server = FastAPI()
idempotences, users = dict(), dict()

class UserCreateRequest(BaseModel):
    username: str
    password: str

@server.post(path="/users")
async def create(
    request: UserCreateRequest, idempotence_key: str = Header(...)
):
    # declare time now
    now = datetime.now()
    # case when a new request occurred
    if idempotence_key not in idempotences:
        future = now + timedelta(days=1)
        # add idempotence into hashmap
        idempotences[idempotence_key] = {"occurred":now, "expire":future}
        # create a user
        users[request.username] = request.password
        return Response(status_code=status.HTTP_201_CREATED)
    # case when a sequential request occurred
    else:
        expire = idempotences[idempotence_key]['expire']
        # sequential request occurred, but idempotence key has not expired yet
        if now < expire:
            return Response(status_code=status.HTTP_200_OK)
        # sequential request occurred, but idempotence key has expired
        else:
            _ = idempotences.pop(idempotence_key)
            return Response(status_code=status.HTTP_200_OK)

@server.get(path="/users")
async def list():
    return Response(status_code=status.HTTP_200_OK, content=dumps(users))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(server, host="0.0.0.0", port=8000)