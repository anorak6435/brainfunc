#!/usr/bin/env python
from enum import Enum, auto
from typing import Generator, Tuple
import sys

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
    PRINT = auto()
    LOOP = auto()
    END_LOOP = auto()

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
            case ".":
                yield True, CMD.PRINT
            case "[":
                yield True, CMD.LOOP
            case "]":
                yield True, CMD.END_LOOP
            case _:
                if code[codeptr] in "+-<>[].,":
                    raise Exception(f"'{code[codeptr]}' not recognised in tokenizer!")

        codeptr += 1

    if codeptr == len(code):
        # done tokenizing the code
        yield False, "EOF"

# building a parse tree from the source for lolz

def build_tree(gen, inloop=False):
    tree = []
    inloop = inloop
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
                case CMD.PRINT:
                    tree.append(TreeNode(CMD.PRINT))
                case CMD.LOOP:
                    children = build_tree(gen, True) # get the commands inside the '['  ']' as children
                    tree.append(TreeNode(CMD.LOOP, children))
                case CMD.END_LOOP:
                    if inloop:
                        tree.append(TreeNode(CMD.END_LOOP))
                        return tree
                    else:
                        raise Exception(f"On reaching '{token}' we found that we are not in a loop!")
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
                case CMD.PRINT:
                    print(chr(cells[cellptr]), end="")
                case CMD.LOOP:
                    # if the current cell is 0 jump over the loop
                    if cells[cellptr] != 0:
                        # not zero so go though the values in loop
                        loop_visit = Visitor(self.tree[tree_index].data)
                        loop_visit.visit()
                    # else the code continues
                case CMD.END_LOOP:
                    # if the byte at datapointer is non-zero repeat this tree of commands
                    if cells[cellptr] != 0:
                        tree_index = -1
                case _:
                    raise Exception(f"Visitor can't handle node:{self.tree[tree_index]}")
            tree_index += 1


# test some weard thing more manually
if __name__ == "__main__":
    if len(sys.argv) == 2:
        with open(sys.argv[1], "r") as f:
            code = f.read()
            interpret(code)
    else:
        raise Exception("Please add the filename inside the command line arguments!")
