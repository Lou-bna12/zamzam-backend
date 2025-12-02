from app.core.firebase_config import messaging

def send_push_notification(token: str, title: str, body: str):
    """
    Envoie une notification push FCM à un mobile
    """
    message = messaging.Message(
        notification=messaging.Notification(
            title=title,
            body=body
        ),
        token=token
    )

    response = messaging.send(message)
    return response
