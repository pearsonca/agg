#!/usr/bin/python
import sys

interval = 7
data_buffer = []
agg_fun = sum
num_fun = []
sep = ' '

filenames = sys.argv[1:]
if not filenames:
    filenames = ["/dev/stdin"]

for filename in filenames:
    f = open(filename)

    counter = 0
    for line in f:
        parts = line.strip().split(sep)
        if len(data_buffer) == 0:
            for p in parts:
                if p.find('.') == -1: # it doesn't look like a float
                    num_fun.append(int)
                else:
                    num_fun.append(float)
            data_buffer = [num_fun[i](parts[i]) for i in range(len(parts))]
        else:
            data_buffer = [agg_fun([data_buffer[i], num_fun[i](parts[i])]) for i in range(len(parts))]
        counter += 1
        if counter == interval:
            print sep.join(map(str, data_buffer))
            data_buffer = []
            counter = 0
