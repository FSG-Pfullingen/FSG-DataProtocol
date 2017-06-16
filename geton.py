import FSGDP
import multiprocessing as mp
import time

# Multiprocessing: https://docs.python.org/2/library/multiprocessing.html#exchanging-objects-between-processes

MY_ADRESS = 32

def get_data(data_in, clock_in, queue):
    print ("Receive Pins: " + str(data_in) + ", " + str(clock_in))
    global MY_ADRESS
    Recv = FSGDP.Receiver(data_in, clock_in)
    print ("Waiting for response")
    meta, data = Recv.receive()
    print (meta)
    to_adress = int(meta[0])
    from_adress = int(meta[1])
    print (str(to_adress), str(from_adress))
    if to_adress == MY_ADRESS:
        Recv.make_hr(data)
    else:
        data = Recv.make_hr(data)
        queue.put((to_adress, from_adress, data))

def UI(queue):
    global MY_ADRESS
    adress = input("Adress: ")
    data = input("Message: ")
    print ("Sending " + data + " to " + adress)
    queue.put(int(adress), MY_ADRESS, data)

def send_data(data_out, clock_out, queue):
    print ("Send Pins: " + str(data_out) + ", " + str(clock_out))
    things_to_send = []
    while things_to_send == []:
        things_to_send = queue.get()
    for item in thins_to_send:
        to_adress, from_adress, data = item
        Sender = FSGDP.Sender(data_out, clock_out)
        Sender.adress = from_adress
        Sender.send(data, to_adress)
        FSGDP.close_connection()

def open_interface(input_args, q):
    print("Processors: " + str(mp.cpu_count()))
    process_list = []
    process = mp.Process(target=get_data, args=(input_args["input"][0], input_args["input"][1], q,))
    process_list.append(process)
    process.start()
    process = mp.Process(target=send_data, args=(input_args["output"][0], input_args["output"][1], q, ))
    process_list.append(process)
    process.start()
    #process = mp.Process(target=UI, args=(q,))
    #process_list.append(process)
    #process.start()
    return process_list

def renew_process(input_list):
    for process in input_list:
        if not process.is_alive():
            process.terminate()
            time.sleep(1)
            process.start()
            print("New Process:" + str(process.name))

def main():
    input_args = {"input":[16, 18], "output":[13, 15]} # (data_out, clock_out, data_in, clock_in)
    q = mp.Queue()
    process_list = open_interface(input_args, q)
    while True:
        renew_process(process_list)
        print("In Queue: ", str(q.get()))
        time.sleep(0.5)

if __name__ == "__main__":
    main()
