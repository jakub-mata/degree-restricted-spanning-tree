from argparse import ArgumentParser

def parse_file(filename: str):
    pass
    


if __name__ == "__main__":
    parser = ArgumentParser()
    parser = ArgumentParser()
    parser.add_argument("filename", type=str, help="Filename with input in cnf")
    parser.add_argument("-d", "--degree", type=int, help="Max degree of a spanning tree")
    args = parser.parse_args()

    parse_file(args.filename)
