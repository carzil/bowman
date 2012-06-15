class Command():
    def __init__(self, world):
        self.world = world

    def register(self):
        pass

    def handle(self, args):
        pass

class Admin():
    def __call__(self, *args, **kwargs):
        self.client_sock, self.client = self.sock.accept()
        self.client_sock.send(b"hello")
        while not self.auth():
            self.client_sock, self.client = self.sock.accept()
            self.client_sock.send(b"hello")
        self.run()

    def __init__(self, server_sock, passwd):
        self.password = passwd
        self.sock = server_sock

    def get_pack(self):
        pack = self.client_sock.recv(1)
        while pack[-1:] != "\xff":
            pack += self.client_sock.recv(1)
        pack = pack[:-1]
        pack =str(pack, "utf-8")
        return pack

    def auth(self):
        password = self.get_pack()
        if self.password != password:
            self.client_sock.close()
            return False
        else:
            return True

    def run(self):
        command = self.client_sock.recv(1)
        while command[-1:] != "\xff":
            command += self.client_sock.recv(1)
