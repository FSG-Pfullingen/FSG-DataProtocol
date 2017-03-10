import FSGDP

if __name__ == "__main__":
    Sender = FSGDP.Sender() # standart pins and timing
    Sender.send() #Prompt some text to send
    FSGDP.close_connection()
