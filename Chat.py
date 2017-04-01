import FSGDP


def main():
    Recv = FSGDP.Receiver()
    sender = FSGDP.Sender()
    desc = input("Start chat or join chat [s/j]")
    if desc == "s":
        adress = input("Adress[8-bit]:")
        message_back = input("Message:")
        sender.send_string(message_back, adress)
    while True:
        Recv.daten = []
        print ("Incoming Message:")
        meta, data = Recv.receive()
        Recv.make_hr()
        message_back = input("Message:")
        meta = meta[1]
        meta = str(meta).replace("[", "")
        meta = str(meta).replace("]", "")
        meta = str(meta).replace(",", "")
        meta = str(meta).replace(" ", "")
        print (meta)
        sender.send_string(message_back, meta)

if __name__ == '__main__':
    main()
