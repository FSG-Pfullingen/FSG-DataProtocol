import FSGDP

if __name__ == "__main__":
    Recv = FSGDP.Receiver() # standart pins and timing
    Recv.receive() # Receive until EOL or '\n' is received
    Recv.write_to_file("./example.txt") # Write the Received Data to 'example.txt'
    FSGDP.close_connection()
