from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate
from email import encoders
import smtplib
import os


def send_mail(send_from, send_to, subject, text, files, server, port, username, password):
    msg = MIMEMultipart()

    # header
    msg['From'] = send_from
    msg['To'] = COMMASPACE.join(send_to)
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject

    # add body of message
    msg.attach(MIMEText(text))

    # attach files
    for f in files:
        with open(f, 'rb') as attach_file:
            part = MIMEApplication(
                attach_file.read(),
                Name = os.path.basename(f)
            )
            part['Content-Disposition'] = 'attachment; filename=%s' % os.path.basename(f)
            msg.attach(part)

    smtp = smtplib.SMTP(server, port)
    smtp.ehlo()
    smtp.starttls()
    smtp.login(username, password)
    smtp.sendmail(send_from, send_to, msg.as_string())
    smtp.quit()


if __name__ == "__main__":

    from _credentials import username, password, server, smtp_port

    for module_code in ['CMT112']:

        data_directory = os.path.join(os.getcwd(), 'dist', module_code)
        docs_directory = os.path.join(os.getcwd(), 'documents')
        files = [os.path.join(data_directory, f) for f in os.listdir(data_directory)]
        files.extend([os.path.join(docs_directory, f) for f in os.listdir(docs_directory)])

        mail_from = "ChorleyMJ@cardiff.ac.uk"
        mail_to = ["martin.chorley@gmail.com"]
        subject = "Module Review 2016/17"
        message = "Dear %s,\n\nPlease find attached the documents for this years module review for module %s. Attached to this email you will find:\n\n\tAn up to date copy of the module description\n\tA pre-filled (where possible) module tracking form\n\tA copy of last years student feedback for the module\n\tAn assessment report showing correlations between student marks for all assessments in the module and student's overall marks for the year\n\tA document containing guidance notes for the review process.\n\nPlease read the guidance notes carefully and review your module description for the coming 17/18 academic year accordingly, completing and updating the tracking form as necessary. Once complete, the module description and tracking form should be placed on the shared drive in 'School Administration/Teaching Administration/2016-17/Module Description Review/%s'.\n\nALL MODULE REVIEWS SHOULD BE COMPLETE BY 9AM, MONDAY JANUARY 30TH.\n\nIf you have any questions, please get in touch\n\nThanks,\nMartin'" % ("Martin", module_code, module_code)

        send_mail(mail_from, mail_to, subject, message, files, server, smtp_port, username, password)
