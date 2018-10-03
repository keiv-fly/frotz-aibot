from subprocess import Popen, PIPE, STDOUT, check_output, CREATE_NEW_CONSOLE
from lib.InputStreamChunker import InputStreamChunker
from time import sleep

def get_data():
    l_data = []
    ch.data_available.wait(0.5)
    sleep(0.1)
    ch.data_unoccupied.clear()
    while ch.data:
        l_data.append(ch.data.pop(0)[:-1])
    ch.data_available.clear()
    ch.data_unoccupied.set()
    return b"\n".join(l_data).decode(encoding="utf-8")

def send_data(data):
    _ = p.stdin.write(data.encode() + b"\n")
    _ = p.stdin.flush()
    return get_data()

ch = InputStreamChunker([b"\n"])  #('\x04')
ch.daemon = True
ch.start()

p = Popen([r'cmd /c dfrotz\dfrotz.exe -m games\Advent.z5'], stdout=ch.input,
          stdin=PIPE, stderr=STDOUT, shell=True)


print(get_data())
print(send_data("n"))

print(send_data("look"))

