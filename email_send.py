# Import smtplib for the actual sending function
import smtplib
def alert_user(coin,email,password):
    server = smtplib.SMTP_SSL('smtp.gmail.com',465)
    server.login(email,password)
    msg_text = "Its time to sell "+coin
    server.sendmail(email,email,msg_text)
    server.quit()