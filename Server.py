import FSGDP
import multiprocessing as mp
import logging
import time

adress_box = {
    "00100101":(13, 15),
    "00100111":(19, 21),
    }

def get_data(pins):
    pin1, pin2 = pins
    Recv = FSGDP.Receiver(pin1, pin2)
    print ("Waiting for response")
    meta, notinuse = Recv.receive()
    to_adress = str(meta[0]).replace("[", "").replace("]", "").replace(", ", "")
    from_adress = str(meta[1]).replace("[", "").replace("]", "").replace(", ", "")
    print (to_adress, from_adress)
    data = Recv.make_hr()
    if to_adress in adress_box:
        print(adress_box[to_adress])
        pin3, pin4 = adress_box[to_adress]
        Sender = FSGDP.Sender(pin3, pin4)
        Sender.adress = from_adress
        Sender.send(data, to_adress)
    FSGDP.close_connection()
        

def main():
    mp.log_to_stderr()
    logger = mp.get_logger()
    logger.setLevel(logging.INFO)
    print (adress_box)
    p1 = mp.Process(target=get_data, args=((16, 18),))
    p2 = mp.Process(target=get_data, args=((22, 24),))
    p1.start()
    p2.start()
    while True:
        if not p1.is_alive():
            p1.terminate()
            time.sleep(0.5)
            p1.start()
            print("New Process:" + str(p1.name))
        if not p2.is_alive():
            p2.terminate()
            time.sleep(0.5)
            p2.start()
            print("New Process:" + str(p2.name))

if __name__ == "__main__":
    main()
