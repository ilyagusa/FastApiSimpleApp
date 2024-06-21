from fastapi import APIRouter, Depends
from auth.base_config import current_user
from .tasks import send_email_report

router = APIRouter(prefix="/report", tags=["report"])


@router.get("/send_mail")
def send_mail(user=Depends(current_user)):
    send_email_report.delay(user.username)

    return {"status": 200, "data": "Письмо отправлено", "details": None}