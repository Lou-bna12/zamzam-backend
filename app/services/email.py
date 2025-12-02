import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
FROM_EMAIL = "loubnasellam49@gmail.com"  # on peut changer pour un vrai email

def send_email(to_email: str, subject: str, html_content: str):
    """Envoie un email via SendGrid"""

    if not SENDGRID_API_KEY:
        print("❌ ERREUR : SENDGRID_API_KEY manquant dans les variables d'environnement")
        return False

    message = Mail(
        from_email=FROM_EMAIL,
        to_emails=to_email,
        subject=subject,
        html_content=html_content,
    )

    try:
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        response = sg.send(message)
        print(f"📧 Email envoyé à {to_email} — Status {response.status_code}")
        return True

    except Exception as e:
        print("❌ Erreur SendGrid :", e)
        return False

def send_order_confirmation(order, items):
    """Envoie un email automatique après une commande"""

    # 1 — Construire la liste des produits en HTML
    items_html = ""
    for item in items:
        items_html += f"""
        <tr>
            <td style='padding:8px 0; border-bottom:1px solid #eee;'>{item.product.title}</td>
            <td style='padding:8px 0; border-bottom:1px solid #eee;'>{item.quantity}</td>
            <td style='padding:8px 0; border-bottom:1px solid #eee;' align='right'>{item.price} €</td>
        </tr>
        """

    # 2 — Template email
    html_template = f"""
    <html>
    <body style="font-family: Arial; background:#f7f7f7; padding:20px;">
        <div style="max-width:600px; margin:auto; background:white; border-radius:10px; overflow:hidden;">
            <div style="background:#4F46E5; padding:20px; color:white; text-align:center;">
                <h2>Merci pour votre commande !</h2>
            </div>

            <div style="padding:20px;">
                <p>Bonjour,</p>
                <p>Nous avons bien reçu votre commande <strong>#{order.id}</strong>.</p>
                <p>Date : <strong>{order.created_at.strftime("%d/%m/%Y %H:%M")}</strong><br>
                Statut : <strong>{order.status}</strong></p>
            </div>

            <div style="padding:20px;">
                <table width="100%" style="border-collapse:collapse;">
                    <tr>
                        <th align="left">Produit</th>
                        <th align="left">Qté</th>
                        <th align="right">Prix</th>
                    </tr>
                    {items_html}
                </table>
            </div>

            <div style="padding:20px; text-align:right;">
                <h3>Total : {order.total_price} €</h3>
            </div>

            <div style="padding:10px; background:#f3f3f3; text-align:center; font-size:12px; color:#777;">
                © 2025 ZamZam – Merci de votre confiance ❤️
            </div>
        </div>
    </body>
    </html>
    """

    send_email(
        to_email=order.user.email,
        subject=f"Confirmation de commande #{order.id}",
        html_content=html_template
    )

def send_status_notification(order):
    """Envoie un email selon le nouveau statut de la commande"""

    status_messages = {
        "pending": {
            "title": "Votre commande est en attente",
            "message": "Votre commande a bien été reçue et est en attente de traitement."
        },
        "paid": {
            "title": "Votre paiement a été confirmé 💳",
            "message": "Merci ! Votre commande a été payée avec succès."
        },
        "shipped": {
            "title": "Votre commande a été expédiée 📦",
            "message": "Bonne nouvelle ! Votre commande est maintenant en route."
        },
        "delivered": {
            "title": "Votre commande a été livrée 🏁",
            "message": "Votre commande a été livrée. Nous espérons que vous en êtes satisfait !"
        }
    }

    if order.status not in status_messages:
        print(f"⚠️ Statut inconnu : {order.status}")
        return

    subject = status_messages[order.status]["title"]
    message_text = status_messages[order.status]["message"]

    html_template = f"""
    <html>
    <body style="font-family: Arial; background:#f7f7f7; padding:20px;">
        <div style="max-width:600px; margin:auto; background:white; border-radius:10px;">
            
            <div style="background:#4F46E5; padding:20px; color:white; text-align:center;">
                <h2>{subject}</h2>
            </div>

            <div style="padding:20px;">
                <p>Bonjour {order.user.name},</p>
                <p>{message_text}</p>

                <p><strong>Numéro de commande :</strong> #{order.id}</p>
                <p><strong>Statut actuel :</strong> {order.status}</p>
                <p><strong>Date :</strong> {order.created_at.strftime("%d/%m/%Y %H:%M")}</p>
            </div>

            <div style="padding:10px; background:#f3f3f3; text-align:center; font-size:12px; color:#777;">
                © 2025 ZamZam – Merci de votre confiance ❤️
            </div>
        </div>
    </body>
    </html>
    """

    send_email(
        to_email=order.user.email,
        subject=subject,
        html_content=html_template
    )
