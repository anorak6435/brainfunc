#!/usr/bin/env python
from enum import Enum, auto
from typing import Generator, Tuple

# global vars used throughout the compiler
code = None
codeptr = 0

CELLCOUNT = 500
cells = [0] * CELLCOUNT
cellptr = 0

class CMD(Enum):
    INC_CELL = auto()
    DEC_CELL = auto()
    DEC_PTR = auto()
    INC_PTR = auto()

# catch incomming code in interpret function
def interpret(_code : str):
    # loading the code
    global code, cells, codeptr, cellptr
    code = _code
    codeptr = 0
    cells = [0] * CELLCOUNT
    cellptr = 0

    # tokenizing the code
    tokenGen = tokenizer()
    # build tree
    tree = build_tree(tokenGen)
    # execute tree

    executor = Visitor(tree)
    executor.visit()



# tokenizing the incomming source
def tokenizer() -> Generator[Tuple[bool, CMD], None, Tuple[bool, str]]:
    global codeptr
    while codeptr < len(code):
        ch = code[codeptr]
        match ch:
            case "+":
                yield True, CMD.INC_CELL
            case "-":
                yield True, CMD.DEC_CELL
            case "<":
                yield True, CMD.DEC_PTR
            case ">":
                yield True, CMD.INC_PTR
            case _:
                if code[codeptr] in "+-<>[]":
                    raise Exception(f"'{code[codeptr]}' not recognised in tokenizer!")

        codeptr += 1

    if codeptr == len(code):
        # done tokenizing the code
        yield False, "EOF"

# building a parse tree from the source for lolz

def build_tree(gen):
    tree = []

    for has_token, token in gen:
        if has_token:
            match token:
                case CMD.DEC_CELL:
                    tree.append(TreeNode(CMD.DEC_CELL))
                case CMD.INC_CELL:
                    tree.append(TreeNode(CMD.INC_CELL))
                case CMD.DEC_PTR:
                    tree.append(TreeNode(CMD.DEC_PTR))
                case CMD.INC_PTR:
                    tree.append(TreeNode(CMD.INC_PTR))
                case _:
                    raise Exception(f"unrecognised token by treebuilder: {token}")
    return tree


# simple Node
class TreeNode:
    def __init__(self, _name, _data = []):
        self.name : CMD = _name
        self.data : list = _data

    def __repr__(self):
        if len(self.data) > 0:
            return f"(name:{self.name}, data{self.data})"
        else:
            return f"(name:{self.name})"

# executing the parse tree! XD
class Visitor:
    def __init__(self, tree):
        self.tree : list = tree
        if len(self.tree) == 0:
            raise Exception("Visitor cannot have an empty tree! Check the tree builder!")

    def visit(self):
        global cellptr, cells
        tree_index = 0
        while tree_index < len(self.tree):
            match self.tree[tree_index].name:
                case CMD.INC_CELL:
                    cells[cellptr] += 1
                    if cells[cellptr] == 256:
                        cells[cellptr] = 0
                case CMD.DEC_CELL:
                    cells[cellptr] -= 1
                    if cells[cellptr] == -1:
                        cells[cellptr] = 255
                case CMD.DEC_PTR:
                    cellptr -= 1
                    if cellptr == -1:
                        cellptr = CELLCOUNT - 1
                case CMD.INC_PTR:
                    cellptr += 1
                    if cellptr == CELLCOUNT:
                        cellptr = 0
                case _:
                    raise Exception(f"Visitor can't handle node:{self.tree[tree_index]}")
            tree_index += 1


# test some weard thing more manually
if __name__ == "__main__":
    code = "----"
    interpret(code)

    assert cells[0] == 256 - 4, "Run cells did not wrap rigth with decrementing!"
