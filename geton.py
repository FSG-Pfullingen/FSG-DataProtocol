import FSGDP
import multiprocessing as mp
import time

# Multiprocessing: https://docs.python.org/2/library/multiprocessing.html#exchanging-objects-between-processes

def get_data((data_out, clock_out, data_in, clock_in), queue):
    Recv = FSGDP.Receiver(data_in, clock_in)
    print ("Waiting for response")
    meta, data = Recv.receive()
    print (meta)
    to_adress = int(meta[0])
    from_adress = int(meta[1])
    print (str(to_adress), str(from_adress))
    data = Recv.make_hr(data)
    queue.put((to_adress, from_adress, data))
    Sender = FSGDP.Sender(data_out, clock_out)
    Sender.adress = from_adress
    Sender.send(data, to_adress)
    FSGDP.close_connection()

def open_interface(pin_list, q):
    print("Processors: " + str(mp.cpu_count()))
    process_list = []
    for pins in pin_list:
        print (pins)
        process = mp.Process(target=get_data, args=(pins, q,))
        process_list.append(process)
        process.start()
    return process_list

def renew_process(input_list):
    for process in input_list:
        if not process.is_alive():
            process.terminate()
            time.sleep(1)
            process.start()
            print("New Process:" + str(process.name))

def main():
    Pinout = [(13, 15, 16, 18), (19, 21, 22, 24)] # (data_out, clock_out, data_in, clock_in)
    process_list = open_interface(Pinout)
    q = mp.Queue()
    while True:
        renew_process(process_list, q)
        print("In Queue: ", str(q.get()))
        time.sleep(0.5)

if __name__ == "__main__":
    main()
