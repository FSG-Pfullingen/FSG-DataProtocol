from FSGDP import Receiver, close_connection
from multiprocessing import Pool

if __name__ == '__main__':
    recv1 = Receiver()
    #recv2 = Receiver(22, 24)
    with Pool(processes=1) as pool:
        result1 = pool.apply_async(recv1.receive)
        #result2 = pool.apply_async(recv2.receive)
    print (result1.get())
    
