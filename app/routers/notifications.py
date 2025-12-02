from fastapi import APIRouter
from pydantic import BaseModel
from app.services.notifications import send_push_notification

router = APIRouter(prefix="/notifications", tags=["Notifications"])

class NotificationRequest(BaseModel):
    token: str
    title: str
    body: str

@router.post("/send")
def send_notification(data: NotificationRequest):
    res = send_push_notification(data.token, data.title, data.body)
    return {"status": "sent", "response": res}
