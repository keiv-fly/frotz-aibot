from subprocess import Popen, PIPE, STDOUT, check_output
from lib.InputStreamChunker import InputStreamChunker
from time import sleep
import pandas as pd
from collections import OrderedDict

p = ""
ch = ""


def loc_parse(loc_str):
    lines = loc_str.split("\n")
    title = lines[2].strip()
    desc = "\n".join([line.strip() for line in lines[3:]])
    return title, desc


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


def start():
    ch = InputStreamChunker([b"\n"])  # ('\x04')
    ch.daemon = True
    ch.start()
    p = Popen([r'cmd /c dfrotz\dfrotz.exe -m games\Advent.z5'], stdout=ch.input,
              stdin=PIPE, stderr=STDOUT, shell=True)
    return p, ch


def restart():
    global p,ch
    p.terminate()
    del ch
    p,ch = start()
    return p, ch


def look(loc_list, move, move_title, move_desc):
    title, desc = loc_parse(send_data("look"))
    loc_it = OrderedDict({
        "move": move,
        "title": title,
        "desc": desc,
        "move_title":move_title,
        "move_desc":move_desc
    })
    loc_list.append(loc_it)


def parse_move_response(s):
    lines = s.split("\n")
    move_title = lines[2]
    move_desc = "\n".join(lines[3:])
    return move_title, move_desc

p, ch = start()

loc_list = []

restart()
get_data()
look(loc_list, "start","","")
moves = ["n","s","w","e", "n","s"]
for move in moves:
    move_title, move_desc = parse_move_response(send_data(move))
    look(loc_list, move, move_title, move_desc)

restart()
get_data()
look(loc_list, "start","","")
moves = ["w","w","w"]
for move in moves:
    move_title, move_desc = parse_move_response(send_data(move))
    look(loc_list, move, move_title, move_desc)
dfl = pd.DataFrame(loc_list)
print(dfl)

send_data("")

help_s = send_data("HELP")
print(send_data("n"))

print(send_data("look"))

