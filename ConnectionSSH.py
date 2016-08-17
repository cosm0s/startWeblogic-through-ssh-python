import ReadProperties, paramiko

class ConnectionSSH:

    def __init__(self):
        ConfigParser = ReadProperties.ConfigParser()
        self.ssh = None
        self.prop = ConfigParser.read_config()
        self.bufferRecv = 1024

    def get_ssh_connection(self):
        if self.ssh is not None:
            return self.ssh
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            self.ssh.connect(self.prop.get('ssh', 'host'), username=self.prop.get('ssh', 'user'), password=self.prop.get('ssh', 'password'), port=int(self.prop.get('ssh', 'port')))
            return self.ssh
        except paramiko.SSHException:
            #Poner el resto de excepciones
            return -1

    def close(self):
        self.ssh.close()

    def run_command(self, command):
        self.ssh = self.get_ssh_connection()
        if command is not None and self.ssh is not None and self.prop is not None:
            channel = self.ssh.invoke_shell()
            channel.send(command)
            while channel.transport.is_active():
                outputByte = channel.recv(self.bufferRecv)
                yield outputByte.decode(encoding='UTF-8'), channel





