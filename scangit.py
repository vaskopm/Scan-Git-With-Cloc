import os, smtplib, email, requests,io
from zipfile import ZipFile
from smtplib import SMTPException
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email import encoders
from email.mime.base import MIMEBase
import getpass
import shutil
from sys import platform

#Create input folder
inputFolder = "InputFolder"
if not (os.path.exists(inputFolder)):
    os.mkdir(inputFolder)
    print(inputFolder + "Created!")

#Get zip folder from gitub and extract it
zipUrl = input("Zip repository url download: ")
req = requests.get(zipUrl, stream=True)
zip = ZipFile(io.BytesIO(req.content))
zip.extractall(inputFolder)
print('Files extracted!')

#Run cloc
file_result = "result.txt"
if platform == "win32":
    os.system("cloc.exe InputFolder --out=" + file_result)
else:
    os.system("cloc InputFolder --out=" + file_result)

#Send email with result file
sender = 'sender-email'
serverPassw = getpass.getpass("SMTP Server password: ")
receiver = input("Receiver email: ")

try:
    server = smtplib.SMTP('your-smtp-server', 587) #587 - port number
    message = MIMEMultipart()
    message["From"] = sender
    message["To"] = receiver
    message["Subject"] = "Cloc Results"
    message.attach(MIMEText("We are sending you an attachment file with your cloc results.", "plain"))
    with open(file_result, "rb") as attachment:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())
    encoders.encode_base64(part)
    part.add_header("Content-Disposition",f"attachment; filename= {file_result}")
    message.attach(part)
    text = message.as_string()
    server.starttls()
    server.login(sender, serverPassw)
    server.sendmail(sender, receiver, text)
    server.quit()
    print("Successfully sent email")
except SMTPException:
   print ("Error: unable to send email")

#Delete input folder
shutil.rmtree(inputFolder)

print("The script was successfully executed.")


