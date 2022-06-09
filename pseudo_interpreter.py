import sys

from classes import *
from funcs import *
from reporting import *

if len(sys.argv) == 1:
	print("Usage: python3 pseudo_interpreter.py <file>")
	exit(1)

def eval_expr(expr):
	if "+" in expr:
		left_side = expr.split("+")[0].strip()
		right_side = expr.split("+")[1].strip()
		if not left_side.isdigit():
			if left_side not in variables:
				return ("VariableError", "Undefined variable")
			left_side = variables[left_side].value
		if not right_side.isdigit():
			if right_side not in variables:
				return ("VariableError", "Undefined variable")
			right_side = variables[right_side].value
		result = get_real_value(left_side) + get_real_value(right_side)
		type = get_type(result)
		return {"result": result, "type": type}


print(f"Reading '{sys.argv[1]}'")
file = open(sys.argv[1], "r")
contents = file.read()
lines = contents.split("\n")
lines = [line.strip() for line in lines if not line.startswith("#") or line != ""]

file.close()

variables = {}
return_point = []
types = ["String", "Real", "Integer", "Array"]

for i, line in enumerate(lines):
	if line == "" or line.startswith("#"):
		# Ignore comments or empty lines
		continue
	if "<-" in line and not line.startswith("FOR"):
		# Assignment
		left_side = line.split("<-")[0].strip()
		right_side = "<-".join(line.split("<-")[1:]).strip()
		right_side_type = None
		if right_side[0] in ["'", '"']:
			right_side_type = "String"
		elif right_side.count(".") == 1:
			right_side_type = "Real"
		elif right_side.isdigit():
			right_side_type = "Integer"
		elif right_side.startswith("["):
			right_side_type = "Array"
		else:
			# Right side is an expression
			result = eval_expr(right_side)
			if isinstance(result, tuple):
				error(result[0], result[1], line, i, line.find(right_side))
			right_side = result["result"]
			right_side_type = result["type"]
		print(f"Assigning '{right_side} : {right_side_type}' to variable {left_side}")
		if left_side in variables:
			if variables[left_side].type != right_side_type:
				error("TypeError", "Incompatible types for re-assignment", line, i, line.find(right_side))
			elif variables[left_side].constant:
				error("ConstantError", "Cannot re-assign a constant.", line, i, line.find(right_side))
			else:
				variables[left_side].value = right_side
		else:
			variables[left_side] = Variable(name = left_side, value = right_side, type = right_side_type, constant = line.startswith("CONSTANT"))
	