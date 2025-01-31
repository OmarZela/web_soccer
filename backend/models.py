from twilio.rest import Client

def send_whatsapp_message(name, position):
    account_sid = 'AC7b47792bd91f07a13f2edea73a1b85e0'
    auth_token = 'a4aad9f4118b0ca6ff7bef069fd955c3'
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        body=f"Hola {name}, confirma tu asistencia para la posición {position}: [Enlace de confirmación]",
        from_='whatsapp:+14155238886',  # Número de Twilio
        to='whatsapp:+51926918702'     # Número del jugador
    )