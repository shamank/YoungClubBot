import smtplib



from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from config import email, email_password

def send_email(TO, msg):

    # server = smtplib.SMTP_SSL('smtp.mail.yahoo.com', 465)
    server = smtplib.SMTP_SSL('smtp.yandex.ru', 465)

    # server.starttls()
    # print("server.starttls()")

    server.login(email, email_password)
    server.sendmail(email, TO, msg)


    server.quit()
    print("server.quit()")

def generate_reg_mail(TO, code):
    msg = MIMEMultipart('alternative')
    msg['Subject'] = "Подтверждение почты | БОТ"
    msg['From'] = email
    msg['To'] = TO

    html = f"""
    <html>
        <body>
            <p>Здравствуйте!</p>
            <p>Код подтверждения: {code}</p>
        </body>
    </html>
    """
    part2 = MIMEText(html, 'html')
    msg.attach(part2)

    return msg.as_string()