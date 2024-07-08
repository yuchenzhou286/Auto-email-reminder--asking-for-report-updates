import configparser
from email.message import EmailMessage
import os
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from email.message import EmailMessage
import base64

# Load configuration
config = configparser.ConfigParser()
config.read('config.ini')

# email_name = {
#     'nsimet@hirecsg.com' : 'Nicole',
#     'ryan@ibexlegal.com' : 'Ryan',
#     'adam@krauseandkinsman.com' : 'Adam',
#     'bryan@krauseandkinsman.com' : 'Bryan',
#     'schery@krauseandkinsman.com' : 'Schery',
#     'rwindsor@motleyrice.com' : 'Rachel',
#     'cscott@motleyrice.com' : 'Carmen',
#     'ffitzpatrick@motleyrice.com' : 'Fidelma',
#     'dbias@ntrial.com' : 'Drew',
#     'lroundtree@ntrial.com' : 'Lauren',
#     'madisyn.zadjeika@klinespecter.com' : 'Madi',
#     'priscilla.jimenez@klinespecter.com' : 'Priscill',
#     'plyons@ashcraftlaw.com' : 'Patrick',
#     'hcharm@wagstafflawfirm.com' : 'Hillel',
#     'nnelson@parawolf.com' : 'Nancy',
#     'treven@elglaw.com' : 'Treven',
# }

# cc_email = {
#     '247' : ['mia.ye@bridgelegal.com', 'meghan@bridgelegal.com', 'evanatkinson@baypointadvisors.com'],
#     '252' : ['mia.ye@bridgelegal.com', 'meghan@bridgelegal.com'],
# }


#########################################################

email_name = {
    '737791989@qq.com' : 'Adam',
    'xxhgoodluck@gmail.com' : 'Xuhan',
    'xuhanxie@outlook.com' : 'xxh'
}

cc_email = {
    '247' : ['xuhanxie@outlook.com']
}

#########################################################

# If modifying these SCOPES, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.send']

def service_gmail():
    creds = None
    # The file token.json stores the user's access and refresh tokens,
    # and is created automatically when the authorization flow completes for the first time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return build('gmail', 'v1', credentials=creds)

def create_message(sender, to, subject, message_text, cc=None, file=None):
    message = EmailMessage()
    message.set_content(message_text)
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject

    # Add cc if provided
    if cc and isinstance(cc, list):
        message['cc'] = ', '.join(cc)
    elif cc:
        message['cc'] = cc
    # if you want to add the attachment to the message, remember passing file to this function
    if file:
        with open(file, 'rb') as f:
            file_data = f.read()
            file_name = os.path.basename(file)
        message.add_attachment(file_data, maintype='application', subtype='octet-stream', filename=file_name)
    raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
    return {'raw': raw_message}

def send_message(service, user_id, message, receiver):
    try:
        message = (service.users().messages().send(userId=user_id, body=message).execute())
        print('Message Id: %s' % message['id'])
        print('Successfully sent email to {fr}'.format(fr=receiver))
        return message
    except Exception as error:
        print(f'An error occurred: {error}')
        return None

def send(matter_type, email_list, org_id):
    sender_email = config['email']['my_email']
    receiver_emails = ', '.join(email_list)
    # Generate a string of first names
    first_names = [email_name[receiver_email] if receiver_email in email_name else "" for receiver_email in email_list]
    first_names_string = ", ".join(first_names[:-1]) + " and " + first_names[-1] if len(first_names) > 1 else first_names[0]

    cc = cc_email[str(org_id)] if str(org_id) in cc_email else None
    
    # Customize your email subject here
    subject = "Request for updating " + str(matter_type) + " reports"

    # Customize your email body here
    org = ""
    if org_id == 247:
        org = "Bay Point"
    elif org_id == 252:
        org = "Neeley"

    body = (
        "Hi {fn},\n\n"
        "Hope all is well!\n\n"
        "I am Cindy from Bridge Legal. Can you please send us an updated case status report for all of {fo} {fc} cases? "
        "If you are able to provide this information by the end of this week or early next week, we would greatly appreciate it!\n\n"
        "Hope you have a good week!\n\n"
        "Best,\n"
        "Cindy"
    ).format(fn=first_names_string, fo=org, fc=matter_type)

    # Create and send the email
    gmail_service = service_gmail()
    email_message = create_message(sender_email, receiver_emails, subject, body, cc=cc)
    send_message(gmail_service, 'me', email_message, receiver=receiver_emails)