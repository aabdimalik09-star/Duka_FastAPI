import mailtrap

# token mailtrap

token="46aaee323673497e0739b25bef7a8d30"

def email(to,subject,message):
    mail=mailtrap.Mail(
        sender=mailtrap.Address(email="hello@demomailtrap.co", name="FLASK_API"),
        to=[mailtrap.Address(email=to)],
        subject=subject,
        text=message,
        category="mailtrap integration test"
    )
    client=mailtrap.MailtrapClient(token=token)
    response=client.send(mail)

    print("this is mailtrap---------")
    print(response)

#email("aabdimalik09@gmail.com","Testing API","I'M testing my API")    