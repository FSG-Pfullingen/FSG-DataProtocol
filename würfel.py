import random
import FSGDP
sender=FSGDP.Sender()
recv=FSGDP.Receiver()

print("Wilkommen zum Wuerfelspiel!")
yn=raw_input("Einladung senden [y/n]")
if yn=="n":
	while True:
		recv.receive()
		data=recv.make_hr()
		yn=raw_input("Einladung akzeptieren [y/n]")
		if yn=="y":
			if data==("Einladung"):
				break
		elif yn=="y":
			print("")
		else:
			print("error")
		
else:
	adress=raw_input("Adresse eingeben")
	sender.send_string("Einladung", adress)
	
while True:
	runde=0
	while 10>=runde:
		print ("Wuerfeln......")
		print (random.randint(1, 6))
		runde=runde+1
	zahl=str(random.randint(1, 6))
	sender.send(zahl, adress)
	
	
	recv.receive()
	data=recv.make_hr()
	if data>zahl:
		print ("Du hast verloren")
	elif data<zahl:
		print ("Du hast gewonnen")
	elif data==zahl:
		print ("Unentschieden")
	else:
		print ("error")
	
