from src.genom_compare import GenomCompare
from src.config_parser import ConfigParser
from src.errors import ConfigError, InvalidSeqLengthError
from src.utils import load_fasta

import argparse
import logging
import json
import sys



def parse_args():
    parser = argparse.ArgumentParser(description='TODO')
    parser.add_argument('-a', dest='seq1_path', required=True, help='path to first sequence')
    parser.add_argument('-b', dest='seq2_path', required=True, help='path to second sequence')
    parser.add_argument('-c', dest='config_path', required=True, help='path to config file')
    parser.add_argument('-o', dest='output_path', required=True, help='path to output file')

    args = parser.parse_args()
    return args


if __name__ == '__main__':
    args = parse_args()
    parser = ConfigParser()

    try:
        config = parser.load_config(args.config_path)
    except json.JSONDecodeError, ConfigError as e:
        logging.error(e)
        sys.exit(1)

    comparer = GenomCompare(same=config['SAME'], diff=config['DIFF'], gp=config['GP'], \
                            max_paths=config['MAX_NUMBER_PATHS'], max_seq_len=config['MAX_SEQ_LENGTH'])

    seq1 = load_fasta(args.seq1_path)
    seq2 = load_fasta(args.seq2_path)
    
    try:
        score, saved_paths = comparer.run_save(seq1, seq2, 'tmp.txt')
    except InvalidSeqLengthError as e:
        logging.error(e)
        sys.exit(1)

    print(f'Score: {score}\nPaths written: {saved_paths}')


    # TODO
    # complicated tests