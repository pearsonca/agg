#!/usr/bin/python
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

    def clean_break(line):
        return line.strip().split(input_args.separator)

    def output(data_buffer):
        print(input_args.separator.join(map(str, data_buffer)))

    def headline(filename):
        if (input_args.verbose):
            print(filename)

    def parse_head(file):
        line = file.readline()
        ## TODO parse header info here if option set
        parts = clean_break(line)
        num_fun = [ (float if p.find('.') != -1 else int) for p in parts]  # look for E as well?
        buffer = [ f(y) for f, y in zip(num_fun, parts)]
        return buffer, num_fun

    def parse_line(l, buffer, item_parser, agg):
        return [agg([b, nf(p)]) for p, nf, b in zip(clean_break(l), item_parser, buffer)]

    for filename in input_args.filenames:
        headline(filename)
        with open(filename,'r') as f:
            ## TODO: get the first line, handle it as as special case
            data_buffer, number_parser = parse_head(f)
            counter = 1
            for line in f:
                parts = clean_break(line)
                data_buffer = parse_line(line, data_buffer, number_parser, agg_fun)
                counter += 1
                if counter == interval:
                    output(data_buffer)
                    data_buffer = []
                    counter = 0
            if counter != 0:
                print("partial aggregation:",counter,"lines.")
                output(data_buffer)