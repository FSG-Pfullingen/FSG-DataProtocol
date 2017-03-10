import FSGDP

if __name__ == "__main__":
    Recv = FSGDP.Receiver() # standart pins and timing
    Recv.receive() # Receive until EOL or '\n' is received
    Recv.make_hr() # Print received text to the console
    FSGDP.close_connection()
