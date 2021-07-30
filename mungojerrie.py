#!/usr/bin/env python

import sys
import argparse
import subprocess
import tempfile
import pathlib

mungojerrie_path = "mungojerrie/build/mungojerrie"

def main():
    args = sys.argv[1:]
    
    try:
        sep_idx = args.index("--")
    except ValueError:
        raise ValueError("Must use '--' to provide arguments to mungojerrie")

    args, mungojerrie_args = args[:sep_idx], args[sep_idx+1:]
    model_path = mungojerrie_args[0]

    parser = argparse.ArgumentParser()
    parser.add_argument('-m','--model-params', nargs='+', 
        help='Substitute variables in .prism model', dest="model_params", required=False)

    args = parser.parse_args(args)
    model_params = args.model_params
    model_params = dict(x.split("=") for x in model_params)

    with tempfile.NamedTemporaryFile(mode='w+') as tmp:
        model_str = pathlib.Path(model_path).read_text()
        model_str = model_str.format(**model_params)
        tmp.write(model_str)
        tmp.flush()
        return subprocess.check_call([mungojerrie_path, tmp.name] + mungojerrie_args[1:])


if __name__ == '__main__':
    main()