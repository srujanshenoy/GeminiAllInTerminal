# Make a calculator

def float_input(prompt):
	while True:
		try:
			return float(input(prompt))
		except ValueError:
			print("Please enter a valid number")

def operator_input():
	while True:
		operator = input("Enter an operator (+, -, *, /): ")
		if operator in "+-*/":
			return operator
		else:
			print("Please enter a valid operator")
			
def continue_calc():
		return input("Do you want to continue? ("" to keep gonig, type to break): ") == ""
		

def calci(starting:bool=True, result:float=0):

	while True:
		num1 = float_input("Enter the first number: ") if starting else result
		operator = operator_input()
		num2 = float_input("Enter the second number: ") if starting else float_input("Enter the next number")

		match operator:
			case "+":
				result = num1 + num2
			
			case "-":
				result = num1 - num2
			
			case "*" "x":
				result = num1 * num2
			
			case "/":
				if num2 == 0:
					print("Cannot divide by zero")
					continue
				result = num1 / num2
			
			case _:
				print("Invalid operator")
				continue

		print(f"{num1} {operator} {f"({num2})" if num2 < 0 else str(num2)} = {result}")

		if continue_calc():
			calci(False, result)
	print("Goodbye!")


if __name__ == "__main__":
	calci()