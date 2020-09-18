import base64
import mimetypes
import os
import pickle
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from apiclient import errors
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


def gmail_auth(gmail_json, auth_port, auth_hostname):
  creds = None

  SCOPES = [
    'https://www.googleapis.com/auth/gmail.readonly',
    'https://www.googleapis.com/auth/gmail.compose'
    # Add other requested scopes.
  ]

  # The file token.pickle stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
  if os.path.exists('gmail_token.pickle'):
    with open('gmail_token.pickle', 'rb') as token:
      creds = pickle.load(token)
  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(gmail_json, SCOPES)
      creds = flow.run_local_server(port=auth_port, host=auth_hostname)
      # Save the credentials for the next run
      with open('gmail_token.pickle', 'wb') as token:
        pickle.dump(creds, token)

  service = build('gmail', 'v1', credentials=creds)
  return service


def send_message(service, user_id, message):
    """Send an email message.

    Args:
      service: Authorized Gmail API service instance.
      user_id: User's email address. The special value "me"
      can be used to indicate the authenticated user.
      message: Message to be sent.

    Returns:
      Sent Message.
    """
    try:
        message = (service.users().messages().send(userId=user_id, body=message).execute())
        print('Message Id: %s' % message['id'])
        return message
    except errors.HttpError as error:
        print('An error occurred: %s' % error)
        return None

"""Generates and submits an email as a draft.
"""


def CreateDraft(service, user_id, message_body):
  """Create and insert a draft email. Print the returned draft's message and id.

  Args:
    service: Authorized Gmail API service instance.
    user_id: User's email address. The special value "me"
    can be used to indicate the authenticated user.
    message_body: The body of the email message, including headers.

  Returns:
    Draft object, including draft id and message meta data.
  """
  try:
    message = {'message': message_body}
    draft = service.users().drafts().create(userId=user_id, body=message).execute()

    print('Draft id: %s\nDraft message: %s' % (draft['id'], draft['message']))

    return draft
  except errors.HttpError as error:
    print('An error occurred: %s' % error)
    return None


def CreateMessage(sender, to, subject, message_text, cc=None, bcc=None):
  """Create a message for an email.

  Args:
    sender: Email address of the sender.
    to: Email address of the receiver.
    subject: The subject of the email message.
    message_text: The text of the email message.

  Returns:
    An object containing a base64url encoded email object.
  """
  message = MIMEText(message_text, 'html')
  # message = MIMEText(message_text, _charset="UTF-8")
  message['to'] = to
  if cc:
    message['cc'] = cc
  if bcc:
    message['bcc'] = bcc
  message['from'] = sender
  message['subject'] = subject
  raw = base64.urlsafe_b64encode(message.as_bytes())
  raw = raw.decode()
  return {'raw': raw}
  # return {'raw': base64.urlsafe_b64encode(message.as_string())}


def CreateMessageWithAttachment(sender, to, subject, message_text, file_dir,
                                filename):
  """Create a message for an email.

  Args:
    sender: The email address of the sender.
    to: The email address of the receiver.
    subject: The subject of the email message.
    message_text: The text of the email message.
    file_dir: The directory containing the file to be attached.
    filename: The name of the file to be attached.

  Returns:
    An object containing a base64url encoded email object.
  """
  message = MIMEMultipart()
  message['to'] = to
  message['from'] = sender
  message['subject'] = subject

  msg = MIMEText(message_text)
  message.attach(msg)

  path = os.path.join(file_dir, filename)
  content_type, encoding = mimetypes.guess_type(path)

  if content_type is None or encoding is not None:
    content_type = 'application/octet-stream'
  main_type, sub_type = content_type.split('/', 1)
  if main_type == 'text':
    fp = open(path, 'rb')
    msg = MIMEText(fp.read(), _subtype=sub_type)
    fp.close()
  elif main_type == 'image':
    fp = open(path, 'rb')
    msg = MIMEImage(fp.read(), _subtype=sub_type)
    fp.close()
  elif main_type == 'audio':
    fp = open(path, 'rb')
    msg = MIMEAudio(fp.read(), _subtype=sub_type)
    fp.close()
  else:
    fp = open(path, 'rb')
    msg = MIMEBase(main_type, sub_type)
    msg.set_payload(fp.read())
    fp.close()

  msg.add_header('Content-Disposition', 'attachment', filename=filename)
  message.attach(msg)

  return {'raw': base64.urlsafe_b64encode(message.as_string())}

def gmail_message(sender, subject, to, contents, gmail_json, auth_hostname, auth_port, cc=None):
  print("Gmailing email")
  service = gmail_auth(gmail_json, auth_hostname=auth_hostname, auth_port=auth_port)
  message = CreateMessage(sender=sender, subject=subject, to=to,
                          message_text=contents, cc=cc)
  send_message(service, 'me', message)

def main():
  print("Running")
  service = gmail_auth()
  print(service)
  message = CreateMessage(sender="Czas na Przygode", subject="Wiadomość testowa2 ", to="zefir@ava.waw.pl", message_text="Jakaś tam zawartość/n/nI podpis")
  print(message)
  send_message(service, 'me', message)

if __name__ == '__main__':
  main()