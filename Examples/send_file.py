import FSGDP

if __name__ == "__main__":
    Sender = FSGDP.Sender() # standart pins and timing
    Sender.send_file("./FSGDP.py") # Send the file 'example.txt'
    FSGDP.close_connection()
