import argparse
from pathlib import Path, PurePath
import pandas as pd
import re

import logging
logger = logging.getLogger('root')
logger.setLevel(logging.DEBUG)

LOG_FILE = 'parsing.log'
handler = logging.FileHandler(LOG_FILE, encoding='utf-8')
formatter = logging.Formatter('%(asctime)s : %(levelname)s : %(module)s / %(funcName)s : %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


def read_file(file_path: Path, parser: str):
    """"""
    logging.debug(f'start parsing {file_path}')
    _row_ok = 0
    result = []
    try:
        parser = globals()[parser]
    except:
        raise Exception(f'{parser} function is not found')

    with file_path.open('r') as _f:
        _suffix = PurePath(file_path).suffix
        if _suffix in ('.xls', '.xlsx'):
            workbook = pd.read_excel(file_path)
            for _row in workbook.values:
                _result = parser(_row)
                if _result:
                    result.append(_result)
                    _row_ok+=1

    msg = f'file {file_path} : {_row_ok}'
    logger.info(msg)
    print(f'==> {msg}')
    return result


def write_file(data: list, file_path: str, format: str, write_mode='w'):
    """"""
    _suffix = PurePath(file_path).suffix
    if _suffix != format:
        file_path = f'{file_path}.{format}'
    _file = Path(file_path)
    _file.parent.mkdir(parents=True, exist_ok=True)
    msg = f'writing to file {_file}'
    logger.info(msg)
    print(f'==> {msg}')

    df = pd.DataFrame.from_records(data)

    if format == 'csv':
        df.to_csv(_file, index=False, header=False, mode=write_mode)
    else:
        raise TypeError(f'{format} output file type is not supported')

def parser_rule_1(row: list):
    """
    list parsing for email
    :param row: element #1 - name, #8 - email
    :return: (name, email)
    """
    return_ = ()
    if row[2] and isinstance(row[8], str) and re.search('@', row[8]):
        # print(f'{row[2]} : {row[8].lower()}')
        return_ = (row[2], row[8].lower())
    return return_

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-if', '--input_file', type=str, default='', help='path to input file')
    parser.add_argument('-id', '--input_dir', type=str, default='.',
                        help='path to directory where input files are located')
    parser.add_argument('-of', '--output_file', type=str, help='path to output file')
    parser.add_argument('-od', '--output_dir', type=str,
                        help='path to a directory where output files will be located with the same names as input ones')

    parser.add_argument('-off', '--output_file_format', type=str, default='csv', help='output file format: csv')
    parser.add_argument('-pl', '--parse_rule', type=str, default='parser_rule_1', help='rule name for parse input file')

    args = parser.parse_args()
    if args.input_file:
        try:
            _file = Path(args.input_file)
            result = read_file(_file, args.parse_rule)
            if args.output_file:
                write_file(result, args.output_file, args.output_file_format, write_mode='a')
            elif args.output_dir:
                write_file(result, f'{Path(args.output_dir, PurePath(args.input_file).stem)}', args.output_file_format)

        except Exception as e:
            raise Exception(f'reading file is failed: {e}')

    else:
        try:
            _path = Path(args.input_dir)
            for _file in _path.glob('*'):
                if _file.is_file():
                    result = read_file(_file, args.parse_rule)
                    if args.output_file:
                        write_file(result, args.output_file, args.output_file_format, write_mode='a')
                    elif args.output_dir:
                        write_file(result, f'{Path(args.output_dir, PurePath(_file).stem)}', args.output_file_format)

        except Exception as e:
            raise Exception(f'reading file is failed: {e}')


if __name__ == '__main__':
    main()
