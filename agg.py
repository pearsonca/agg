#!/usr/bin/python
from argparse import ArgumentParser

if __name__ == "__main__":
    parser = ArgumentParser(description="agg: a command line utility for aggregating lines of output.")
    parser.add_argument("filenames", metavar="N", nargs="*", help="paths to files for aggregation", default=["/dev/stdin"], type=str)
    parser.add_argument("-s", dest="separator", help="separator string", default=" ", type=str)
    parser.add_argument("-v", dest="verbose", action='store_true', help="verbose mode.")
    #parser.add_argument("-w", dest="warnings", action='store_true', help="check for and display warnings.")

    interval_group = parser.add_mutually_exclusive_group()
    interval_group.add_argument("-i", dest="interval", help="aggregation interval", default=7, type=int)
    interval_group.add_argument("-d", nargs='+',
        dest="interval", help="special aggregation interval.", default="week", choices=['week','month','year'])
    ## parser.add_argument("-r", help="should separator be treated as a regular expression?", action="store_true")
    parser.add_argument("-c", dest="header", help="do the inputs have a header line?", action="store_true")
    input_args = parser.parse_args()
    if input_args.verbose:
        print("using parsing arguments: %s" % input_args)
    interval = input_args.interval
    agg_fun = sum

    def clean_break(line):
        return line.strip().split(input_args.separator)

    def output(data_buffer):
        print(input_args.separator.join(map(str, data_buffer)))

    def headline(filename, header):
        if (input_args.verbose):
            print("file: %s - cols:" % filename)
            print(" ".join(header))

    def parse_head(file):
        ## TODO parse header info here if option set
        parts = clean_break(file.readline())
        if input_args.header:
            header = parts
            parts = clean_break(file.readline())
        else:
            header = ["col%d"%i for i in range(len(parts))]
        num_fun = [ (float if p.find('.') != -1 else int) for p in parts]  # look for E as well?
        buffer = [ f(y) for f, y in zip(num_fun, parts)]
        if input_args.verbose:
            print("detected number formats: %s" % num_fun)
        return buffer, num_fun, header

    def parse_line(l, buffer, item_parser, agg):
        return [agg([b, nf(p)]) for p, nf, b in zip(clean_break(l), item_parser, buffer)]

    for filename in input_args.filenames:
        with open(filename,'r') as f:
            data_buffer, number_parser, header = parse_head(f)
            headline(filename, header)
            counter = 1
            for line in f:
                parts = clean_break(line)
                data_buffer = parse_line(line, data_buffer, number_parser, agg_fun)
                counter += 1
                if counter == interval:
                    output(data_buffer)
                    data_buffer = [nf() for nf in number_parser]
                    ## TODO need appropriate init value for aggregation function - e.g., 0 doesn't work w/ prod
                    counter = 0
            if counter != 0:
                print("partial aggregation on %d lines:" % counter)
                output(data_buffer)