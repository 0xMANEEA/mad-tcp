#!/usr/bin/env python

from time import time as epoch, sleep
from os import environ, popen
from datetime import timedelta
import sys

STDIN   =   0
STDOUT  =   1
STDERR  =   2

s = {
    "B"         : "",   # Bold
    "I"         : "",   # Italic
    "U"         : "",   # Underline
    "L"         : "",   # Blink
    "H"         : "",   # Highlight
    "r"         : "",   # Red
    "g"         : "",   # Green
    "y"         : "",   # Yellow
    "b"         : "",   # Blue
    "p"         : "",   # Purple
    "c"         : "",   # Cyan
    "w"         : "",   # White
    "|"         : "",   # Clear Screen
    "_"         : "",   # Clear Line
    "R"         : ""    # Reset Style
}

if popen("uname").read() == "Linux\n" or popen("uname").read() in "Darwin\n":
    environ["TERM"] =   "xterm-256color"    
    s["B"]     =   "\033[1m"           # Bold
    s["I"]     =   "\033[3m"           # Italic
    s["U"]     =   "\033[4m"           # Underline
    s["L"]     =   "\033[5m"           # Blink
    s["H"]     =   "\033[7m"           # Highlight
    s["r"]     =   "\033[91m"          # Red
    s["g"]     =   "\033[92m"          # Green
    s["y"]     =   "\033[93m"          # Yellow
    s["b"]     =   "\033[94m"          # Blue
    s["p"]     =   "\033[95m"          # Purple
    s["c"]     =   "\033[96m"          # Cyan
    s["w"]     =   "\033[97m"          # White
    s["|"]     =   "\033[H\033[2J"     # Clear Screen
    s["_"]     =   "\033[1K\033[9999D" # Clear Line
    s["R"]     =   "\033(B\033[m"      # Reset Style

def out(text, time=0, clear=False, clear_line=False, start=" ", end="\n", sd="`", ed="`", keep_style=False, ret=False):
    text = style(text, clear, clear_line, start, end, sd, ed, keep_style)
    for i in text:
        write(i)
        sleep(time)

def err(text, time=0, clear=False, clear_line=False, start=" ", end="\n", sd="`", ed="`", keep_style=False, ret=False):
    text = s["B"] + s["L"] + s["r"] + "[!]" + s["R"] + " " + text
    text = style(text, clear, clear_line, start, end, sd, ed, keep_style)
    if ret:
        return text
    for i in text:
        write(i, stream=STDERR)
        sleep(time)

def style(text, clear, clear_line, start, end, sd, ed, keep_style):
    text = start + text + end
    if not keep_style:
        text += s['R']

    if clear:
        text = s['|'] + text
    elif clear_line:
        text = s['_'] + text

    # Apply the s
    for style in s.keys():
        text = text.replace(sd + style + ed, s[style])

    return text

def write(text, stream=STDOUT):
    if stream == STDOUT:
        sys.stdout.write(text)
        sys.stdout.flush()
    elif stream == STDERR:
        sys.stderr.write(text)
        sys.stderr.flush()

def progress_bar(ratio, columns=0, time=-1, ret=False):
    if columns == 0:
        rows, columns = popen("stty size").read().split()
    columns = int(columns) / 2
    bar = '[%4.1f%%] ' % (ratio*100) + s['B']
    if ratio > 0.7:
        bar += s['g']
    elif ratio > 0.2:
        bar += s['y']
    else:
        bar += s['r']
    bar += '['
    for i in range(int((columns-2)*ratio)):
        bar += '='
    for i in range(int((columns-2) * (1-ratio))):
        bar += ' '
    bar += ']' + s['R']

    if time is not -1:
        try:
            bar += s['B'] + ' [ ' + s['R'] + 'Estimated time left: ' + s['B'] + str(timedelta(seconds = (epoch() - time) / ratio - (epoch() - time))).split('.')[0] + ' ]' + s['R']
        except:
            pass

    if ret:
        return bar

    write(bar+'\n')

if __name__ == "__main__":
    # Use case

    progress_bar(1)
    exit(0)

    sample = "`L``B``H`[!]`R` Lorem ipsum dolor sit amet, consectetur adipiscing elit."

    out("AAA")

    out(sample, time=0.01, end="", clear=True)

    sleep(1)

    err(sample, time=0.01, clear_line=True)
    out(sample, time=0.01)
    out(sample, time=0.01)
    out(sample, time=0.01)
    err(sample, time=0.01)

    sleep(2)
