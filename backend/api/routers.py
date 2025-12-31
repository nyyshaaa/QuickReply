from fastapi import APIRouter
from backend.api.__init__ import version_prefix
from backend.app.chat_assist.routes import chat_assit_router



public_routers = APIRouter(prefix=version_prefix)

public_routers.include_router(chat_assit_router, prefix="/chat",tags=["chat-assit"])

#--------------------------------------------------------------------------------------------------------

admin_routers = APIRouter(prefix=f"{version_prefix}/admin")
