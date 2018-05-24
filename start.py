from lexial import Parser
from setting import *

def main():
    parse = Parser()
    with open(FILE, 'r', encoding='utf-8') as f:
        text = f.read()
    Input = parse.parser(text)
    print(Input)

if __name__ == '__main__':
    main()
