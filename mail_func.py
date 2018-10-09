import mail_param
import imaplib
import email
import subprocess

#Read mailbox
def read_email():
	mail = imaplib.IMAP4_SSL(mail_param.SRV, mail_param.PORT)
	mail.login(mail_param.MAIL, mail_param.PWD)
	#Select mailbox
	mail.select('inbox')

	#Search all emails in mailbox
	type, data = mail.search(None, 'ALL')
	mail_ids = data[0]

	#list of mail ids
	id_list = mail_ids.split()
	first_id = int(id_list[0])
	last_id = int(id_list[-1])

	#Fetch the emails on id list 
	for i in range(last_id,first_id-1, -1):
		typ, data = mail.fetch(i, '(RFC822)')

		#Select data of fetched email
		for response_part in data:
			if isinstance(response_part, tuple):
				msg = email.message_from_string(response_part[1])
				mail_from = msg['from']
				mail_sub = msg['subject']
				arg = str(mail_sub)
				exit_code = subprocess.call(["/home/luan/mail/teste.sh", arg])
				#Checking if the shell script executed successful
				if exit_code == 0:
					print("Script executed successful")
				else:
					print("Script failed")
	#Delete emails
	for i in range(last_id,first_id-1, -1):
		typ, data = mail.fetch(i, '(RFC822)') 
		mail.store(i, '+FLAGS', '(\\Deleted)')
	mail.expunge()
	#Close the mailbox
	mail.close()
	#Logout the mailbox
	mail.logout()
