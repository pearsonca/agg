#!/usr/bin/python
import sys

from argparse import ArgumentParser

if __name__ == "__main__":
    parser = ArgumentParser(description="agg: a command line utility for aggregating lines of output.")
    parser.add_argument("filenames", metavar="N", nargs="+", help="paths to files for aggregation", default="/dev/stdin", type=str)
    parser.add_argument("-s", dest="separator", help="separator string", default=" ", type=str)
    parser.add_argument("-i", dest="interval", help="aggregation interval", default=7, type=int)
    parser.add_argument("-v", dest="verbose", action='store_true', help="verbose mode.")
    ## parser.add_argument("-r", help="should separator be treated as a regular expression?", default=False, type=bool)
    ## parser.add_argument("-c", help="do the inputs have a header line?", default=False, type=bool)
    input_args = parser.parse_args()
    print(input_args)
    interval = input_args.interval
    data_buffer = []
    agg_fun = sum
    num_fun = []

    def clean_break(line):
        return line.strip().split(input_args.separator)

    def output(data_buffer):
        print(input_args.separator.join(map(str, data_buffer)))

    def headline(filename):
        if (input_args.verbose):
            print(filename)

    for filename in input_args.filenames:
        headline(filename)
        f = open(filename)
        ## TODO: get the first line, handle it as as special case
        counter = 0
        for line in f:
            parts = clean_break(line)
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
                output(data_buffer)
                data_buffer = []
                counter = 0
        if counter != 0:
            print("partial aggregation:",counter,"lines.")
            output(data_buffer)