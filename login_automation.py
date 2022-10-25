from paramiko import SSHClient
import sys


client = SSHClient()
client.load_system_host_keys()
client.load_host_keys("/home/deji/.ssh/known_hosts")

client.connect("brz-avmrn1-01.amer.thermo.com", username="dpn", password="ZPfc4ZzJ0P1k")
stdin, stdout, stderr = client.exec_command('change-passwords')

# stdin.write('no\n')
# stdin.write('yes\n')
# stdin.flush()
#
# stdin.write('"abc123"\n')
# stdin.write('"abc123"\n')
# stdin.flush()

stdin.channel.send('no\n')
stdin.channel.send('yes\n')
stdin.channel.send('"abc123"\n')
stdin.channel.send('"93a38UCzq5lX"\n')
stdin.channel.send('"93a38UCzq5lX"\n')
stdin.flush()


#print(f'STDOUT: {stdout.read().decode("utf8")}')
#print(f'STDERR: {stderr.read().decode("utf8")}')
#print(f'Return code: {stdout.channel.recv_exit_status()}')

stdin.channel.close()
#stdout.close()
#stderr.close()

#sys.stdout.write(stdout.read().decode())
#sys.stderr.write(stderr.read().decode())

for line in stdout.xreadlines():
     sys.stdout.write(line)

# for line in stderr.xreadlines():
#     sys.stderr.write(line)

client.close()

