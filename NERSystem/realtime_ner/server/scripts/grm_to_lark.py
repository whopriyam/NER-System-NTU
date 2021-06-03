#!/usr/bin/env python3

import os
import re

COMMENT_RE = r'#.*'
SYMBOL_DECL_RE = r'^[a-zA-Z-_]+\s*=\s*SymbolTable.*$'
SYMBOL_TOKEN_RE = r'(".+?")\.[a-zA-Z-_]+'
PROB_RE = r'<0?\.[0-9]+>'
DECL_EQL_RE = r'(\S+\s*)='
EXPORT_RE = r'^export\s*(\S+)'
END_SEMICOLON_RE = r';$'
ALL_CHAR_NOT_IN_QUOTE_RE = r'\b(?<!")(\w+)(?!")\b'


def grm_to_lark(filein, fileout):
    in_lines = []
    out_lines = []
    with open(filein) as fin:
        in_lines = fin.readlines()

    for line in in_lines:
        # order is important
        line = re.sub(COMMENT_RE, '', line)
        line = re.sub(SYMBOL_DECL_RE, '', line)
        line = re.sub(ALL_CHAR_NOT_IN_QUOTE_RE,
                      lambda match: match.group(1).lower(), line)
        line = re.sub(SYMBOL_TOKEN_RE, r'\1', line)
        line = re.sub(PROB_RE, '', line)
        line = re.sub(DECL_EQL_RE, r'\1:', line)

        export_match = re.search(EXPORT_RE, line)
        if export_match:
            out_lines.insert(0, f'start: {export_match.group(1)}\n')
            line = re.sub(EXPORT_RE, r'\1', line)

        # remove white spaces
        line = line.strip()
        # strip semicolon after removing trailing whitespace
        line = re.sub(END_SEMICOLON_RE, '', line)
        # add back newline at the end for readability
        if line:
            line += '\n'

        out_lines.append(line)

    out_lines.append(r'%import common.WS' + '\n')
    out_lines.append(r'%ignore WS')

    with open(fileout, mode='w') as fout:
        fout.writelines(out_lines)


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('filein', type=str)
    parser.add_argument('fileout', type=str)

    args = parser.parse_args()
    filein = args.filein
    fileout = args.fileout

    outdir = os.path.dirname(fileout)
    if outdir and not os.path.isdir(outdir):
        os.mkdir(outdir)

    grm_to_lark(filein, fileout)
