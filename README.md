# ua_defence

transform input file to output file
> python ./main.py  --input_file input_file --output_file output_file

transform files from input_dir to output dir with the same file names as input ones
> python ./main.py  --input_dir input_dir --output_dir output_dir_results

transform files from input_dir to one output file
> python ./main.py  --input_dir input_dir --output_file output_dir_results/all_in_one

    > python ./main.py --help

    usage: main.py [-h] [-if INPUT_FILE] [-id INPUT_DIR] [-of OUTPUT_FILE] [-od OUTPUT_DIR] [-off OUTPUT_FILE_FORMAT] [-pl PARSE_RULE]

    options:
      -h, --help            show this help message and exit
      -if INPUT_FILE, --input_file INPUT_FILE
                            path to input file
      -id INPUT_DIR, --input_dir INPUT_DIR
                            path to directory where input files are located
      -of OUTPUT_FILE, --output_file OUTPUT_FILE
                            path to output file
      -od OUTPUT_DIR, --output_dir OUTPUT_DIR
                            path to a directory where output files will be located with the same names as input ones
      -off OUTPUT_FILE_FORMAT, --output_file_format OUTPUT_FILE_FORMAT
                            output file format: csv
      -pl PARSE_RULE, --parse_rule PARSE_RULE
                            rule name for parse input file
