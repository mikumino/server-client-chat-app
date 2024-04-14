# Chat client

import tkinter as tk
import socket
import threading
import select


class GUI:
    def __init__(self, mainWindow):
        self.mainWindow = mainWindow
        self.mainWindow.title("Chatting Client")

        self.chatBoxLabel = tk.Label(self.mainWindow, text="Chat Box", font="Intern")
        self.chatBoxLabel.grid(row=0, column=0, padx=10, pady=0)
        self.chatBox = tk.Text(self.mainWindow, height=30, width=100)
        self.chatBox.grid(row = 1, column = 0, padx=10, pady=10)
        self.chatBox.config(borderwidth=2, state=tk.DISABLED)
        

    #I don't get why it won't get bigger, messed with width, the grid, no dice.
        self.input = tk.Entry(self.mainWindow,  width=50, bg="#b59ad1")
        self.input.grid(row=2, column=0, padx=20, pady=20)
        self.input.config(borderwidth=3)

        self.send = tk.Button(self.mainWindow, text="Send", bg="#5f77b4", command=self.send)
        self.send.grid(row=3, column=0, padx=10, pady=10)

        #We can remove this later or leave it in, it's this while im testing it though
        self.host = 'localhost'  
        self.port = 9009 
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.settimeout(2)
        try:
            self.s.connect((self.host, self.port))
        except:
            print('Unable to connect')
            exit()

        # Start the thread to receive messages
        threading.Thread(target=self.receive, daemon=True).start()
        self.message("Hostname: localhost      Port: 9009\n")
        self.message("Connected to remote host. You can start sending messages")
        

    def message(self, text):
        self.chatBox.config(state=tk.NORMAL)
        self.chatBox.insert(tk.END, text+'\n')
        self.chatBox.config(state=tk.DISABLED)
        self.chatBox.see(tk.END)


    def send(self):
        msg = self.input.get()
        if msg:
            try:
                self.s.send(msg.encode('utf-8'))
                self.message(f'[Me]  {msg}')
                self.input.delete(0, tk.END)
            except:
                self.message('Failed to send message.')


    def receive(self):
        while True:
            socket_list = [self.s]
            read_sockets, write_sockets, error_sockets = select.select(socket_list, [], [])
            self.message('read_sockets: ' + str(read_sockets))
            if read_sockets:
                data = self.s.recv(4096)
                if not data:
                    self.message('\nDisconnected from chat server')
                    exit()
                else:
                    self.message(data.decode('utf-8'))


def main():
    root = tk.Tk()
    client = GUI(root)
    root.mainloop()

main()
