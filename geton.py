import FSGDP
import multiprocessing as mp
import logging
import time

def get_data(data_in, clock_in, data_out, clock_out):
    Recv = FSGDP.Receiver(data_out, clock_out)
    print ("Waiting for response")
    meta, data = Recv.receive()
    print (meta)
    to_adress = int(meta[0])
    from_adress = int(meta[1])
    print (str(to_adress), str(from_adress))
    data = Recv.make_hr(data)
    Sender = FSGDP.Sender(data_in, clock_in)
    Sender.adress = from_adress
    Sender.send(data, to_adress)
    FSGDP.close_connection()

def main():
    process_list = []
    mp.log_to_stderr()
    logger = mp.get_logger()
    logger.setLevel(logging.INFO)
    print("Processors: " + str(mp.cpu_count()))
    p1 = mp.Process(target=get_data, args=(13, 15, 16, 18,))
    #p2 = mp.Process(target=get_data, args=(19, 21, 22, 24,))
    process_list.append(p1)
    #process_list.append(p2)
    print(process_list)
    for process in process_list:
        process.start()
    while True:
        for process in process_list:
            if not process.is_alive():
                process.terminate()
                time.sleep(0.5)
                process.start()
                print("New Process:" + str(process.name))
        time.sleep(0.5)

if __name__ == "__main__":
    main()
