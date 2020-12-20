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

#Initial data
username = input("Github username: ")
repo = input("Repository name: ")
sendEmail = int(input("Send results by email? 1 - Yes; 2 - No: "))

#Create input folder
inputFolder = "InputFolder"
if not (os.path.exists(inputFolder)):
    os.mkdir(inputFolder)

#Get zip folder from gitub and extract it
print("Downloading Repo...")
zipUrl = "https://api.github.com/repos/" + username + "/" + repo + "/zipball"
req = requests.get(zipUrl, stream=True)
zip = ZipFile(io.BytesIO(req.content))
zip.extractall(inputFolder)
print('Files extracted!')

#Run cloc
if sendEmail==1:
    print("Reading and generating file result...")
    file_result = "result.txt"
    if platform == "win32":
        os.system("cloc.exe InputFolder --out=" + file_result)
    else:
        os.system("cloc InputFolder --out=" + file_result)

    #Send email with result file
    sender = 'xxxxxxxxx' #sender = email sender
    serverPassw = "xxxxxxxxx" #serverPassw = email server/sender password
    receiver = input("Your email: ") 
    print("Sending email...")

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587) #server = smtplib.SMTP('your-smtp-server', port-number)
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

else:
    print("Reading files...")
    if platform == "win32":
        os.system("cloc.exe InputFolder")
    else:
        os.system("cloc InputFolder")

#Delete input folder
shutil.rmtree(inputFolder)

print("The script was successfully executed.")


