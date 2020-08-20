from string import ascii_letters
from collections import deque


def check_parenthesis(expression_list):
    if expression_list.count("(") != expression_list.count(")"):
        print("Invalid expression")
        main()

def infix_to_postfix(expression_list):
    ops = {"+": 1, "-": 1, "*": 2, "/": 2}
    operators = deque()
    result = []
    for number in expression_list:
        try:
            result.append(int(number))
        except ValueError:
            if number == "(":
                operators.append(number)
            elif number == ")" and len(operators) > 0:
                while len(operators) > 0:
                    sign = operators.pop()
                    if sign == "(":
                        break
                    result.append(sign)
            elif number in ops:
                if len(operators) == 0:
                    operators.append(number)
                else:
                    if number in ops:
                        while len(operators) > 0 and operators[-1] != "(" and ops[operators[-1]] >= ops[number]:
                            result.append(operators.pop())
                        operators.append(number)
    while len(operators) > 0:
        result.append(operators.pop())
    return result

def calculate_postfix(postfix_list):
    my_stack = deque()
    for item in postfix_list:
        if isinstance(item, int):
            my_stack.append(item)
        else:
            y = my_stack.pop()
            x = my_stack.pop()
            if item == "+":
                my_stack.append(x + y)
            elif item == "-":
                my_stack.append(x - y)
            elif item == "*":
                my_stack.append(x * y)
            elif item == "/":
                if float(x // y) == x / y:
                    my_stack.append(x // y)
                else:
                    my_stack.append(x / y)
    return my_stack[0]


def main():   # TODO add POWER operations "^"
    saved_values = {}
    symbols = ["+", "-", "*", "/", "(", ")"]
    while True:
        x = input()
        if len(x) < 1:
            continue
        if x == "/exit":
            print("Bye!")
            exit()
        elif x == "/help":  # TODO KEEP UPDATING THIS!
            print("""This program currently supports addition, subtractions, multiplication and division.
Multiple operators next to each other allowed. Expression may or may not be separated by spaces.

+ for addition
- for subtraction
* for multiplication
/ for division

Supports:
    - STORING values in variables:
        + USE only a single word (combination of ONLY letters; lower and uppercase allowed)
    - EXPRESSIONS can consist of stored early variables and/or numbers
    - Order of precedence, all expressions are evaluated before calculation
    - Parenthesis calculations""")
        elif x.startswith("/"):
            print("Unknown command")
        elif x in saved_values:
            print(saved_values[x])
        elif "=" in x:
            variable_assig = [va.strip() for va in x.split("=")]
            for char in variable_assig[0]:
                if char not in ascii_letters:
                    print("Invalid identifier")
                    continue
            if len(variable_assig) != 2:
                print("Invalid assignment")
                continue
            try:
                saved_values[variable_assig[0]] = int(variable_assig[1])
            except ValueError:
                try:
                    saved_values[variable_assig[0]] = saved_values[variable_assig[1]]
                except KeyError:
                    print("Invalid assignment")
            finally:
                continue
        else:
            numbers = []
            inp = x.split()
            for item in inp:
                loops = 0
                for symbol in symbols:
                    if symbol in item:
                        loops += 1
                        while symbol in item:
                            split_point = item.index(symbol)
                            try:
                                numbers.append(item[:split_point])
                            except IndexError:
                                pass
                            item = item[split_point + 1:]
                            numbers.append(symbol)
                        else:
                            numbers.append(item)
                if loops == 0:
                    numbers.append(item)
            while "" in numbers:
                numbers.remove("")
            if numbers[0] == "-":
                numbers[1] = "-" + numbers[1]
                numbers.pop(0)
            input_numbers = []
            buffer = ""
            for count, number in enumerate(numbers):
                if count < len(numbers) - 1 and numbers[count + 1] == number and number in symbols:
                    buffer += number
                else:
                    if len(buffer) > 0:
                        if number in buffer:
                            input_numbers.append(buffer + number)
                            continue
                    input_numbers.append(number)
            for count, item in enumerate(input_numbers):
                negative_value = False
                if "+" in item and "-" not in item:
                    input_numbers[count] = "+"
                elif count != 0 and "-" in item:
                    minuses = list(item)
                    for minus in minuses:
                        if minus == "-":
                            negative_value = not negative_value
                    if negative_value:
                        input_numbers[count] = "-"
                    else:
                        input_numbers[count] = "+"
                else:
                    try:
                        input_numbers[count] = int(item)
                    except ValueError:
                        if item in saved_values:
                            input_numbers[count] = saved_values[item]
                            continue
                        elif item in symbols:
                            continue
                        if len(input_numbers) == 1:
                            print("Unknown variable")
                            main()
                        else:
                            print("Invalid Expression")
                            main()

            check_parenthesis(input_numbers)
            result = infix_to_postfix(input_numbers)
            print(calculate_postfix(result))


if __name__ == "__main__":
    main()
