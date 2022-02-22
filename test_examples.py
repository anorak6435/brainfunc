#!/usr/bin/env python
import run

#def  test_hello_world(capsys):                                                                                           #
    # code = "++++++++[>++++[>++>+++>+++>+<<<<-]>+>+>->>+[<]<-]>>.>---.+++++++..+++.>>.<-.<.+++.------.--------.>>+.>++." #
    # run.interpret(code)                                                                                                 #
    #                                                                                                                     #
    # out, err = capsys.readouterr()                                                                                      #
    #
    #assert out == "Hello World!\n", f"Expected Hello World! but got'{out}'"


def test_increment_cell():
    code = "++++"
    run.interpret(code)

    mycell = [0] * run.CELLCOUNT

    mycell[0] = 4

    assert run.cells == mycell, "Could probably not find that the '4' in first cell"

def test_decrement_cell():
    code = "----"
    run.interpret(code)

    assert run.cells[0] == 256 - 4, f"Run cells did not wrap rigth with decrementing! {run.cells[0]}"

def test_increment_ptr():
    code = ">>>>"
    run.interpret(code)

    assert run.cellptr == 4, "Unsuccesfully incremented the cell pointer"


def test_decrement_ptr():
    code = "<<<<"
    run.interpret(code)

    assert run.cellptr == run.CELLCOUNT - 4, f"Unexpected value in wrapping cellptr to the end of the list"