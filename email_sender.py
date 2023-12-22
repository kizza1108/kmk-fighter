import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def Send_email(mail_to, password):
    try:
        # setting email id, pass, subject, from , to and setting body msg
        email_id = 'kizzapass@gmail.com'
        email_pass = 'yjysomgntqtexhah'
        email_msg = MIMEMultipart()
        email_msg['Subject'] = 'KMK-Fighting account Reset Password.'
        email_msg['From'] = email_id
        email_msg['To'] = mail_to
        email_msg.attach(MIMEText("Your reset password request has been accepted Successfully."
                                  "\n\nYour  password reset code is '" + password +
                                  "'\n\nThis email is auto generated so kindly don't reply on it", 'plain'))

        with smtplib.SMTP('smtp.gmail.com', port=587) as smtp:
            # start TLS for security
            smtp.starttls()
            smtp.ehlo()
            # login in email
            smtp.login(email_id, email_pass)
            msg = email_msg.as_string()
            # send email
            smtp.sendmail(email_id, mail_to, msg)
            # quit server
            smtp.quit()

        return ["Password Reset Successfully...", True]
    except Exception as e:
        print(str(e))
        return [str(e), False]
