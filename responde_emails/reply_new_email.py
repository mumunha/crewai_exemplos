import os.path
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

import base64
from email.mime.text import MIMEText
import seu_email

current_path = os.path.dirname(os.path.abspath(__file__))

your_email = seu_email.your_email

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://mail.google.com/"]


def get_email_address(headers, field_name):
    for header in headers:
        if header['name'].lower() == field_name.lower():
            return header['value']
    return None

def get_email_body(email_content):
    if 'parts' in email_content["payload"]:
        return email_content["payload"]["parts"][0]["body"]["data"]
    elif 'body' in email_content["payload"]:
        return email_content["payload"]["body"]["data"]
    else:
        return None

def connect():
  creds = None

  if os.path.exists(current_path+"/token.json"):
    creds = Credentials.from_authorized_user_file(current_path+"/token.json", SCOPES)
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          current_path+"/credentials.json", SCOPES
      )
      creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open(current_path+"/token.json", "w") as token:
      token.write(creds.to_json())

  return build("gmail", "v1", credentials=creds)


def show_chatty_threads(service):
  new_email_ids = []

  try:

    threads = (
        service.users().threads().list(userId="me").execute().get("threads", [])
    )
    if not os.path.exists(current_path+'/email_ids.csv'):
        with open(current_path+'/email_ids.csv', 'w') as f:
          existing_email_ids = []
        varre="n"
        varre = input("Voce deseja varrer e armazenar todos os emails atuais? (s/N) ")
        if varre.lower() == "s":
          for thread in threads:
            tdata = (
                service.users().threads().get(userId="me", id=thread["id"]).execute()
            )
            email_ids = [msg["id"] for msg in tdata["messages"]]
            for email_id in email_ids:
              existing_email_ids.append(email_id)
          print("Email_ids varridos: ", existing_email_ids)
          with open(current_path+'/email_ids.csv', 'a') as f:
            for email_id in existing_email_ids:
              f.write(email_id + '\n')

    for thread in threads:
      tdata = (
          service.users().threads().get(userId="me", id=thread["id"]).execute()
      )
      nmsgs = len(tdata["messages"])
      # print(tdata["messages"])
      # get all email_ids of each thread
      email_ids = [msg["id"] for msg in tdata["messages"]]
      
      # load email_ids from csv file

      with open(current_path+'/email_ids.csv', 'r') as f:
        existing_email_ids = f.read().splitlines()
      # check if email_ids already exist in csv file and append new_email_ids array
      for email_id in email_ids:
        if email_id not in existing_email_ids:
          new_email_ids.append(email_id)
          existing_email_ids.append(email_id)         

      read_status = [msg["labelIds"] for msg in tdata["messages"]]

      # skip if <3 msgs in thread
      if nmsgs > 0:
        msg = tdata["messages"][0]["payload"]
        subject = ""
        for header in msg["headers"]:
          if header["name"] == "Subject":
            subject = header["value"]
            break
        if subject:  # skip if no Subject line
          print(f"- {subject}, {nmsgs}, {email_ids}, {read_status}")
    
    print("New email_ids: ", new_email_ids)

    # write new_email_ids to csv file
    with open(current_path+'/email_ids.csv', 'a') as f:
      for email_id in new_email_ids:
        f.write(email_id + '\n')
    
    return new_email_ids
  

  except HttpError as error:
    print(f"An error occurred: {error}")
   
def get_info_new_emails(email_id):
    # get thread_id
    thread_id = (
        service.users()
        .messages()
        .get(userId="me", id=email_id)
        .execute()
    )["threadId"]
    
    # get snippet
    snippet = (
        service.users()
        .messages()
        .get(userId="me", id=email_id)
        .execute()
    )["snippet"]


    email_content = (
        service.users()
        .messages()
        .get(userId="me", id=email_id)
        .execute()
      )
    # get subject
    tdata = (
        service.users().threads().get(userId="me", id=thread_id).execute()
    )
    msg = tdata["messages"][0]["payload"]
    subject = ""
    for header in msg["headers"]:
      if header["name"] == "Subject":
        subject = header["value"]
        break

    
    headers = email_content['payload']['headers']
    sender_email = get_email_address(headers, 'From')
    recipient_email = get_email_address(headers, 'To')

    # print (email_content)
    email_body = get_email_body(email_content)
    email_body = base64.urlsafe_b64decode(email_body).decode("utf-8")

    return sender_email, recipient_email, email_id, thread_id, subject, email_body, snippet
  
def create_message(sender, to, message_id, thread_id, subject, message_text):
    message = MIMEText(message_text)
    message['from'] = sender
    message['to'] = to
    message['In-Reply-To'] = message_id
    message['References'] = message_id
    message['subject'] = subject

    return {
        'raw': base64.urlsafe_b64encode(message.as_string().encode()).decode(),
        'threadId':thread_id
    }

def send_message(service, user_id, message):
    message = (service.users().messages().send(userId="me", 
    body=message).execute())
    print('Message Id: %s' % message['id'])
    return message

def create_draft(service, user_id, message):
    draft = {
        'message': message
    }
    draft = service.users().drafts().create(userId=user_id, body=draft).execute()
    print('Draft Id: %s' % draft['id'])
    return draft

def send_email(sender, to, message_id, thread_id, subject, message_text):
    created_message = create_message(sender, to, message_id, thread_id, subject, message_text)
    # send_message(service, 'me', created_message)
    create_draft(service, 'me', created_message)

if __name__ == "__main__":
  service = connect()
  new_email_ids = []
  new_email_ids = show_chatty_threads(service)

  for email_check in new_email_ids:
    sender_email, recipient_email, email_id, thread_id, subject, email_body, summary = get_info_new_emails(email_check)
    

    if your_email not in sender_email:
      print("De: ", sender_email) 
      print("Resumo: ", summary)
      responder = "s"
      responder = input("Deseja responder (S/n)?")

      if responder.lower() == "s":

        # save email_body to file email.txt
        with open(current_path+'/src/agencia_noticias/email.txt', 'w', encoding='utf-8') as f:
            f.write(email_body)
          
        
        os.system("poetry run agencia_noticias")

        print("Feito!")

        # load reply email_body from file email.txt
        with open(current_path+'/resposta.txt', 'r', encoding='utf-8') as f:
            reply = f.read()
        
        
        email_body = "> " + email_body.replace("\n", "\n>")
        email_body = reply + "\n\n"+ email_body
        send_email(recipient_email, sender_email, email_id, thread_id, subject, email_body)



# melhorias - colocar no inicio do email a mensagem padrao do google - On Wed, Sep 15, 2021 at 10:00 AM, <email> wrote: