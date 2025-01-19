# Make a calculator

def float_input(prompt):
	while True:
		try:
			return float(input(prompt))
		except ValueError:
			print("Please enter a valid number")

def operator_input():
	while True:
		operator = input("operator (+, -, *, /): ")
		if operator in "+-*/x":
			return operator
		else:
			print("Please enter a valid operator")
			
def continue_calc():
		return input("Do you want to continue? ("" to keep gonig, type to break): ") == ""
		

def calci(starting:bool=True, result:float=0):

	while True:
		num1 = float_input("number: ") if starting else result
		if num1 == 1234567890:
			print("You found the exit code!")
			break
		operator = operator_input()
		num2 = float_input("number: ")
		if num2 == 1234567890:
			print("You found the exit code!")
			break

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

		starting = False
		continue

	# 	if continue_calc():
	# 		calci(False, result)
	# print("Goodbye!")


if __name__ == "__main__":
	calci()