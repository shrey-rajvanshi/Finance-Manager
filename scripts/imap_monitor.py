import sys
import imaplib
import email
import datetime
import requests


IMAP_SERVER = 'imap.gmail.com'
EMAIL_ACCOUNT = "shreykant*********@gmail.com"
EMAIL_FOLDER = "Inbox"
PASSWORD = 'heehaa'

#To-Do : 
#      Handle ATM withdrawal alert
#      Handle for other banks

def get_last_read():
	f=open('last_read')
	last_read = f.readline()
	f.close()
	return int(last_read)

def store_last_read(num):
	f=open('last_read','w')
	last_uid=num
	f.write(last_uid)
	f.close()


def process_mail(body):
	#handles transaction alerts for citi bank
	gist = body[body.find('<strong>'):body.find('</strong>')]
	print gist
	amount = int(float(gist[gist.find('Rs ')+3: gist.find(' on ')]))
	store = gist[gist.find(" at ")+4:]
	#send request to my server
	requests.post("http://shreykant.pythonanywhere.com/sub",data={'name':store,'amount':amount})

def process_mailbox(M):
    last_uid= get_last_read()
    rv, data = M.search(None,'From','"CitiAlert.India@citicorp.com"')
    #command = "UID {}:*".format(last_uid)
    #rv, data = M.uid('search', command)
    if rv != 'OK':
        print "No messages found!"
        return
    
    for num in data[0].split():
		if int(num)>last_uid:
			rv, data = M.fetch(num, '(RFC822)')
			if rv != 'OK':
				print "ERROR getting message", num
				return
			msg = email.message_from_string(data[0][1])
			if msg['Subject'] == "Citi Purchase Alert" or msg['Subject'] == "Confirmation of transaction on your Citibank Debit Card":
	        		print "Writing message ", num
				body=""
				if msg.is_multipart():
					body =  msg.get_payload()[0].get_payload()
				else :
					body=msg.get_payload()
				process_mail(body)
    store_last_read(num)

def handle_failure(rv):
	print "ERROR: Unable to open mailbox ", rv

def main():
    M = imaplib.IMAP4_SSL(IMAP_SERVER)
    M.login(EMAIL_ACCOUNT, PASSWORD)
    rv, data = M.select(EMAIL_FOLDER)
    if rv == 'OK':
        print "Processing mailbox: ", EMAIL_FOLDER
        process_mailbox(M)
        M.close()
    else:
	handle_failure(rv)
    M.logout()

if __name__ == "__main__":
    main()

