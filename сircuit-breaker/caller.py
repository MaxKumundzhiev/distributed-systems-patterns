from time import time 
from uuid import UUID, uuid4

from fastapi import FastAPI
from pydantic import BaseModel, Field


class Request(BaseModel):
    callee_identifier: str


class Response(BaseModel):
    callee_identifier: str
    request_id: UUID
    request_at: int
    status_code: int
    circuit_breaker_status: str
    circuit_breaker_details: dict


server = FastAPI(title="caller")

@server.post("/", response_model=Response)
async def post_to_callee(request: Request):
    return Response(
        **request.model_dump(),
        request_id=uuid4(),
        request_at=int(time()),
        status_code=200,
        circuit_breaker_status="CLOSED",
        circuit_breaker_details={}
    )
