import firebase_admin
from firebase_admin import credentials, messaging

# Configuration sécurisée Firebase Admin SDK
firebase_credentials = {
    "type": "service_account",
    "project_id": "zamzam-notifications",
    "private_key_id": "NOT_USED_HERE",
    "private_key": """-----BEGIN PRIVATE KEY-----
MIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQDT64JhbvKR304L
Qcb8jDtuZCHfC87oaTUCtinBqHA6z5piK7jslIff1pOsGt6ZYlebWwsqmpVvNER/
3DYAPvJ0l+YBlJ2jeNb5MqeFZ/0+rhGcNHpE9oWlx9Vo6w9mem1vfOfyWjVbYg/U
Iq+bxBbeMKo/ZKs0Bi77KhlazEU2xZviZwRDz8FMtFYQivFPkOdJfC0Y3eGfiiL/
+mNlgA1+nAnQrmP/1j+j7LsYQvm1GuRhUlTTHopmsKdXwb4QFwWMY8TuyRkNMQLp
+HFBbfpJEb1OPEOWJhKYa0sjpWbMyTZigA4l0xVJUWXxsAAfLe2rt7+txnAGxO/5
qKwdNq7HAgMBAAECggEAHmV0h+AqN9p1RG+/XcBe0pMsjo8QMvggK+Q6sgskad3B
hvI+2I7nZvz3+ngc1JhX+NxtX24udUsPG4iCUF+3AW/mLvTaSt/NdI9GRarS7AIm
BtHkyxknC058oaC8TpZ3NZtks4zVLryD3l7JRx4wVNdbHAj8S36AOki2u/YlDq60
4jdp5fsGlcYqdeMEU8SdL83ChVEDIB0QFwSJPmgIJ+UhhpCIVVIsxP91n0X8D2fC
RrC5m0DzkhCt10MUHJcZcCiq6TKedC5Ur/fzgH8yahiDzQ8ZldLbPP1zhH8TTn13
NngT5Fmi9zxiLDzGLgTbK9rZpMdA+kHDf3gPP4/5bQKBgQDwGpEslLuliLznT8Us
gHn2l90237lFszaenLVNEp35/EtWzZYh3erOeTV5am14eKM1j4t8wbRYHqOu6/iu
/uXEC0N8i09+h/CATjKAs7rAMMfhIionBI++/p9pcZhk0/J870fdouCFXPyL9w9f
g9dPp6YeKdq3t/FEGBm9hsLxiwKBgQDh80PG18NU+Zwcs49yFEmCdrUGmPtGT5+t
6F2tMK8SEntc4EeUVPgCBHgaa4kYtlaMXtCUvPiXhGg0k7iXLQdHc9L8y+IUvbjb
3zfG2MOVRiEKLTxD5WLvZik0zyk0T7z5Xnf7vUfwnD3dQwwm+m/cs6lEdZN2byaq
9mGgqPunNQKBgQCP6Fx6y+psHLicK0OSmK6BDiSYbx8sl211Q5emyjHFU2IUdMQ3
KDtD5YIXc6KJQkUQJSkFbVQaPML+ZJB40m4EQnwAeb77p56OSFAcs5yK9LHYThHV
sPY3E4WYPW2JgT8lgoUgYi8Pv9veSAX+yZaTN3hpO8zLsIP6vDcxUUQmYQKBgHmY
ld/7m5YuYnIbu9Wzzz+TrKYpTAixrwhDJa6fpYe/RH5eAId2FqXXS99EAdq3ven6
2JtC+zFnQ0EQQmWxCNrOHTyIaFmrJEHHZdfwLYk23W8Bmw4a81xMiV5vIgiR5Ov6
h+2FFqMJIk3h2DddzTdjxHMgJ0S0WoXk4/M3HX8FAoGBAKiJ2jtvBHodcRGzuec9
5bUOt2P9HxkUP8aeagzC2JODNCU78gGK3inTLfTX7S5KuOdkMPsq4i7jMeSawDpz
Yp2wn5RQVkCGu2h8brwJGQB1MKO5LmT88jkpszE1/P/M/pXMby4DEr3YE0n2IN+y
hGhYmsZgJgV2DM35bPJyRhJg
-----END PRIVATE KEY-----""",
    "client_email": "firebase-adminsdk-fbsvc@zamzam-notifications.iam.gserviceaccount.com",
    "client_id": "NOT_USED_HERE",
    "token_uri": "https://oauth2.googleapis.com/token"
}

cred = credentials.Certificate(firebase_credentials)

try:
    firebase_admin.initialize_app(cred)
except ValueError:
    # Already initialized
    pass
