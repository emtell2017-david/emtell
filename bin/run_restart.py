"""

python nlp/bin/run_restart.py  --vocab_file ctakes_vocabs.txt --save_dir nlp/checkpoint --root /home/lca80/Desktop/data/emtell/PMC/txt --prefixes_dir prefixes_tokens_count.txt --span 0:8
python nlp/bin/run_restart.py  --vocab_file ctakes_vocabs.txt --save_dir checkpoint --prefixes_dir prefixes_tokens_count.txt --span 34:55

"""
import os
import sys
import argparse

current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

from helper import clean_checkpoint

def main(args):
    (s, e) = args.span.split(":")
    s, e = int(s), int(e)
    with open(args.prefixes_dir, "r") as fd:
        prefixes = fd.read().split('\n')

    for prefix in prefixes[s:e]:
        if prefix == "":
            continue
        if prefix[:5] == "total":
            continue
        prefix = os.path.join(args.root, prefix.split()[0]) + "/*"
        run_str = "python nlp/bin/restart.py --train_prefix=%s --vocab_file %s --save_dir %s --n_gpus %d"%(prefix, args.vocab_file, args.save_dir, args.n_gpus)

        print(run_str)
        os.system(run_str)
        clean_checkpoint(args.save_dir)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--save_dir', default='checkpoint', help='Location of checkpoint files')
    parser.add_argument('--vocab_file', default='vocabs.txt', help='Vocabulary file')
    parser.add_argument('--root', default='/shared/dropbox/ctakes_conll/tokenized_text', help='data root')
    parser.add_argument('--prefixes_dir', default='prefixes_tokens_count.txt', help='prefixes_dir')
    parser.add_argument('--n_gpus', type=int, default=2)
    parser.add_argument('--span', type=str, default='0:1')

    args = parser.parse_args()
    main(args)
