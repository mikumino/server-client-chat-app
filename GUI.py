# Chat client

import tkinter as tk
from tkinter import ttk
import sv_ttk
import socket
import threading
import select

class GUI:
    def __init__(self, mainWindow):
        sv_ttk.set_theme("dark")
        self.mainWindow = mainWindow
        self.mainWindow.title("Chatting Client")

        self.chatBox = tk.Text(self.mainWindow, height=30, width=100)
        self.chatBox.grid(row = 1, column = 0, padx=30, pady=30)
        self.chatBox.config(state=tk.DISABLED, borderwidth=1, wrap=tk.WORD, font=("Intern", 12), padx=10, pady=10)
        
        self.input = ttk.Entry(self.mainWindow,  width=100)
        self.input.grid(row=2, column=0, padx=10, pady=10)
        self.input.bind('<Return>', self.sendMessage)

        self.sendButton = ttk.Button(self.mainWindow, text="Send", command=self.sendMessage)
        
        self.sendButton.config(style='Accent.TButton')
        self.sendButton.grid(row=3, column=0, padx=10, pady=10)

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


    def sendMessage(self, event=None):
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
