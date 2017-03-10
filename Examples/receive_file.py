import FSGDP

if __name__ == "__main__":
    Recv = FSGDP.Receiver() # standart pins and timing
    try:
        Recv.receive(False) # Receive until you press Ctrl^C received
    except KeyboardInterrupt:
        print "Going on!"
    Recv.write_to_file("./example.txt") # Write the Received Data to 'example.txt'
    FSGDP.close_connection()
