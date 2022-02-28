#!/usr/bin/env python
import run
import sys
from io import StringIO

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

# def test_char_in_test(monkeypatch):

    # def inner_func(): # if the official implementation did not have the \n I would use this
    #     str_test = ""
    #     count = 5
    #     while count > 0:
    #         c = sys.stdin.read(1)
    #         str_test += c
    #         count -= 1
    #     return str_test

    # string_input = StringIO("hello")
    # monkeypatch.setattr('sys.stdin', string_input)

    # assert inner_func() == "hello", "Expected the string hello in characters!"

def test_simple_yes_no(monkeypatch):

    def inner_func():
        return input()

    # the testing input given to a function with the input called.
    # This will be encountered in the interpreter.
    string_input = StringIO("y\n")
    monkeypatch.setattr('sys.stdin', string_input)

    assert inner_func() == "y", "Not expected the input function return!"


def test_rot_13_input_test(capsys, monkeypatch):

    code = """-,+[           Read first character and start outer character reading loop
    -[                       Skip forward if character is 0
        >>++++[>++++++++<-]  Set up divisor (32) for division loop
                               (MEMORY LAYOUT: dividend copy remainder divisor quotient zero zero)
        <+<-[                Set up dividend (x minus 1) and enter division loop
            >+>+>-[>>>]      Increase copy and remainder / reduce divisor / Normal case: skip forward
            <[[>+<-]>>+>]    Special case: move remainder back to divisor and increase quotient
            <<<<<-           Decrement dividend
        ]                    End division loop
    ]>>>[-]+                 End skip loop; zero former divisor and reuse space for a flag
    >--[-[<->+++[-]]]<[         Zero that flag unless quotient was 2 or 3; zero quotient; check flag
        ++++++++++++<[       If flag then set up divisor (13) for second division loop
                               (MEMORY LAYOUT: zero copy dividend divisor remainder quotient zero zero)
            >-[>+>>]         Reduce divisor; Normal case: increase remainder
            >[+[<+>-]>+>>]   Special case: increase remainder / move it back to divisor / increase quotient
            <<<<<-           Decrease dividend
        ]                    End division loop
        >>[<+>-]             Add remainder back to divisor to get a useful 13
        >[                   Skip forward if quotient was 0
            -[               Decrement quotient and skip forward if quotient was 1
                -<<[-]>>     Zero quotient and divisor if quotient was 2
            ]<<[<<->>-]>>    Zero divisor and subtract 13 from copy if quotient was 1
        ]<<[<<+>>-]          Zero divisor and add 13 to copy if quotient was 0
    ]                        End outer skip loop (jump to here if ((character minus 1)/32) was not 2 or 3)
    <[-]                     Clear remainder from first division if second division was skipped
    <.[-]                    Output ROT13ed character from copy and clear it
    <-,+                     Read next character
    ]"""

    string_input = StringIO("u\nr\ny\ny\nb\n \nj\nb\ne\ny\nq\n")
    monkeypatch.setattr('sys.stdin', string_input)
    run.interpret(code)
    out, err = capsys.readouterr()

    assert out == "hello world", "Input not correctly registered!"
