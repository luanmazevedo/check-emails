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
	#Checking if there are emails
	if data[0] == '':
#		print("No email")
		subprocess.call(["/home/luan/mail/log.sh", "\"No email\""])
		mail.close()
		mail.logout()
		exit()
	else: 
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
				#Getting only "FROM" without the full name
				aux = str(mail_from)
				a = aux.split('<')
				if a >= 0:
					aux1 = aux.split('<')
					print(aux1)
					aux2 = aux1[1].split('>')
					print(aux2)
					aux3 = aux2[0]
					print(aux3)
					arg1 = str(mail_sub)
					arg2 = aux3
				else:
					arg1 = str(mail_sub)
					arg2 = str(mail_from)
				exit_code = subprocess.call(["/home/luan/mail/teste.sh", arg1, arg2])
				#Checking if the shell script executed successful
				if exit_code == 0:
#					print("Script executed successful")
				else:
#					print("Script failed")
					subprocess.call(["/home/luan/mail/log.sh", "\"Script failed\""])
					exit()
	#Delete emails
	for i in range(last_id,first_id-1, -1):
		typ, data = mail.fetch(i, '(RFC822)') 
		mail.store(i, '+FLAGS', '(\\Deleted)')
	mail.expunge()
	#Close the mailbox
	mail.close()
	#Logout the mailbox
	mail.logout()
	subprocess.call(["/home/luan/mail/log.sh", "\"Script executed successful\""])
