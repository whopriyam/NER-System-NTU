#!/usr/bin/env python3

import os
import re
import csv

ATC_UNIT_REGEX = r'^\(\(FROM\s+(?P<from>[A-Za-z0-9_-]+)\)\s*(?:\(NUM\s+[A-Za-z0-9_-]+\)\s*)?\(TO\s+(?P<to>[A-Za-z0-9_-]+\s*)\)\s*\(TEXT\s+(?P<text>[^)]+)\)\s*\(TIMES\s+(?P<time_start>[0-9\.]+)\s+(?P<time_end>[0-9\.]+)\s*\)(?:\s*\(COMMENT\s+\"(?P<comment>[^)]+)\"\))?\)'


def convert_to_dicts(filename):
    atc_text = ''
    with open(filename) as opened_file:
        atc_text = opened_file.read()

    dicts = []
    for match in re.finditer(ATC_UNIT_REGEX, atc_text,
                             re.MULTILINE | re.DOTALL):
        dicts.append({
            'from':
            match.group('from'),
            'to':
            match.group('to'),
            'text':
            re.sub(
                r'\s+',
                ' ',
                match.group('text').replace('\"', '').lower(),
            ),
            'time_start':
            match.group('time_start'),
            'time_end':
            match.group('time_end'),
            'comment':
            re.sub(
                r'\s+',
                ' ',
                (match.group('comment') or '').replace('\"', '').lower(),
            )
        })

    return dicts


def write_to_csv(dicts, filename):
    with open(filename, 'w') as csv_file:
        field_names = [
            'from', 'to', 'text', 'time_start', 'time_end', 'comment'
        ]
        writer = csv.DictWriter(csv_file, fieldnames=field_names)

        writer.writeheader()
        for row in dicts:
            writer.writerow(row)


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        'in_path',
        type=str,
        help='Path to input directory containing ATC text files')
    parser.add_argument(
        'out_path',
        type=str,
        help='Path to output directory for processed csv files')
    parser.add_argument(
        '-c', '--combined', action='store_true', help='output a combined csv')

    args = parser.parse_args()
    in_path = args.in_path
    out_path = args.out_path
    combined = args.combined

    try:
        if not os.path.isdir(out_path):
            os.mkdir(out_path)

        combined_content = []
        for filename in os.listdir(in_path):
            out_filename, _ = os.path.splitext(filename)

            content = convert_to_dicts(os.path.join(in_path, filename))
            write_to_csv(content, os.path.join(out_path,
                                               out_filename + '.csv'))
            combined_content += content

            print(f'Processed {filename}')

        if (combined):
            write_to_csv(combined_content,
                         os.path.join(out_path, 'combined.csv'))
    except FileNotFoundError:
        parser.error(f'input path {in_path} does not exist')
