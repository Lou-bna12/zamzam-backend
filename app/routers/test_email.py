from fastapi import APIRouter
from app.services.email import send_email

router = APIRouter(prefix="/test-email", tags=["Email"])

@router.get("/")
def test_email():
    send_email(
        to_email="tonEmail@gmail.com",
        subject="Test ZamZam",
        html_content="<h1>Email ZamZam Fonctionnel 🎉</h1><p>Ceci est un test.</p>"
    )
    return {"message": "Email envoyé si tout est bon 👌"}
