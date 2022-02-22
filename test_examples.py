#!/usr/bin/env python
import run

def test_hello_world(capsys):
    code = "++++++++[>++++[>++>+++>+++>+<<<<-]>+>+>->>+[<]<-]>>.>---.+++++++..+++.>>.<-.<.+++.------.--------.>>+.>++."
    run.interpret(code)
    out, err = capsys.readouterr()
    assert out == "Hello World!\n", f"Expected Hello World!\n but got'{out}'"


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

def test_inmemory_countdown():
    code = "+++++>++++>+++>++>+"
    run.interpret(code)

    assert ( run.cells[0] == 5 and
               run.cells[1] == 4 and
               run.cells[2] == 3 and
               run.cells[3] == 2 and
               run.cells[4] == 1 ), f"Not all cells where incremented properly: '{run.cells[0:5]}'"

def test_basic_output(capsys):
    code = "++++++++++++++++++++++++++++++++++++++++++++++++.+.+.+.+.+.>++++++++++."
    run.interpret(code)

    out, err = capsys.readouterr()

    assert out == "012345\n", "Did not print the right unicode values!"

def test_basic_loop_abc_print(capsys):
    code = "+++++[->+++++++++++++<]>.>>++++++++++."
    run.interpret(code)

    out, err = capsys.readouterr()

    assert out == "A\n", f"Simple loop found '{out}' instead of 'A\n'"

def test_complexer_hello_world(capsys):
    code = """>++++++++[-<+++++++++>]<.>>+>-[+]++>++>+++[>[->+++<<+++>]<<]>-----.>->
+++..+++.>-.<<+[>[+>+]>>]<--------------.>>.+++.------.--------.>+.>+."""
    run.interpret(code)

    out, err = capsys.readouterr()

    assert out == "Hello World!\n", "It is not the Hello World! you expected!"

def test_basic_move_value(capsys):
    code = "+++++[->+++++++++++++<]>   >>[-]<<[->>+<<] >> ."
    run.interpret(code)

    out, err = capsys.readouterr()

    assert out == "A", "The A value was unsuccesfully moved!"
