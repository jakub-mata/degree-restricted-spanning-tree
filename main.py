from argparse import ArgumentParser

import input_handling
import encode
import output_handler


if __name__ == "__main__":
    parser = ArgumentParser()
    parser = ArgumentParser()
    parser.add_argument("-i", "--input", type=str, help="Filename for csv file with input")
    parser.add_argument("-o", "--output", type=str, help="Filename for the output file in cnf format")
    parser.add_argument("-d", "--degree", type=int, help="Max degree of a spanning tree", required=True)
    args = parser.parse_args()

    input_matrix: list[list[int]] = input_handling.parse_csv_file(args.input)
    if not input_handling.validate_input(input_matrix):
        raise AssertionError("Invalid input")

    cnf, vars = encode.encode(input_matrix, args.degree)
    result = output_handler.write_to_file_and_call_solver(args.output, cnf, vars)
    output_handler.print_result(result)
