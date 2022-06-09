import sys

from classes import *
from funcs import *
from reporting import *

if len(sys.argv) == 1:
	print("Usage: python3 pseudo_interpreter.py <file>")
	exit(1)

def eval_expr(expr: str):
	expr = expr.strip()
	for op in ["+", "-", "*", "/", "MOD", "DIV", ">=", "<=", ">", "<", "!=", "=", "AND", "OR"]:
		if op in expr:
			left_side = expr.split(op)[0].strip()
			right_side = expr.split(op)[1].strip()
			if not left_side.isdigit():
				if left_side not in variables:
					return ("VariableError", f"Undefined variable '{left_side}'")
				left_side = variables[left_side].value
			if not right_side.isdigit():
				if right_side not in variables:
					return ("VariableError", f"Undefined variable '{right_side}'")
				right_side = variables[right_side].value
			if op in ["+", "-", "*", "/", "MOD", "DIV"]:
				if op == "+":
					result = get_real_value(left_side) + get_real_value(right_side)
				elif op == "-":
					result = get_real_value(left_side) - get_real_value(right_side)
				elif op == "*":
					result = get_real_value(left_side) * get_real_value(right_side)
				elif op == "/":
					result = get_real_value(left_side) / get_real_value(right_side)
				elif op == "MOD":
					result = get_real_value(left_side) % get_real_value(right_side)
				elif op == "DIV":
					result = get_real_value(left_side) // get_real_value(right_side)
				type = get_type(result)
				return {"result": result, "type": type}
			if op in [">=", "<=", ">", "<", "!=", "="]:
				result = get_real_value(left_side)
				if op == ">":
					result = result > get_real_value(right_side)
				elif op == "<":
					result = result < get_real_value(right_side)
				elif op == ">=":
					result = result >= get_real_value(right_side)
				elif op == "<=":
					result = result <= get_real_value(right_side)
				elif op == "!=":
					result = result != get_real_value(right_side)
				elif op == "=":
					result = result == get_real_value(right_side)
				return {"result": result, "type": "Boolean"}
			if op in ["AND", "OR"]:
				result = get_real_value(left_side)
				if op == "AND":
					result = bool(result & get_real_value(right_side))
				elif op == "OR":
					result = bool(result | get_real_value(right_side))
				type = get_type(result)
				return {"result": result, "type": "Boolean"}
	if expr.startswith("NOT"):
		expr = expr.split("NOT")[1].strip()
		if not expr.isdigit():
			if expr not in variables:
				return ("VariableError", f"Undefined variable '{expr}'")
			expr = variables[expr].value
		result = not get_real_value(expr)
		return {"result": result, "type": "Boolean"}


print(f"Reading '{sys.argv[1]}'")
file = open(sys.argv[1], "r")
contents = file.read()
lines = contents.split("\n")
lines = [line.strip() for line in lines if not line.startswith("#") or line != ""]

file.close()

variables = {}
return_point = []
types = ["String", "Real", "Integer", "Array", "Boolean"]

i = -1
while i < len(lines):
	i += 1
	line = lines[i]
	if line == "" or line.startswith("#"):
		# Ignore comments or empty lines
		continue
	if "<-" in line and not line.startswith("FOR"):
		# Assignment
		left_side = line.split("<-")[0].replace("CONSTANT", "").strip()
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
		#print(f"Assigning '{right_side} : {right_side_type}' to variable {left_side}")
		if left_side in variables:
			if variables[left_side].type != right_side_type:
				error("TypeError", "Incompatible types for re-assignment", line, i, line.find(right_side))
			elif variables[left_side].constant:
				error("ConstantError", "Cannot re-assign a constant.", line, i, line.find(right_side))
			else:
				variables[left_side].value = right_side
		else:
			if right_side_type == "String":
				right_side = right_side[1:-1]
			variables[left_side] = Variable(name = left_side, value = right_side, type = right_side_type, constant = line.startswith("CONSTANT"))
	elif line.startswith("OUTPUT"):
		to_out = "OUTPUT".join(line.split("OUTPUT")[1:]).strip()
		type = get_type(to_out)
		if type == "Variable":
			val = variables[to_out].real_value
			print(val)
		else:
			print(to_out)
	elif line.startswith("REPEAT"):
		return_point.append(i)
	elif line.startswith("UNTIL"):
		if not return_point:
			error("SyntaxError", "UNTIL without REPEAT", line, i, line.find("UNTIL"))
		expr = line.split("UNTIL")[1].strip()
		result = eval_expr(expr)
		if isinstance(result, tuple):
			error(result[0], result[1], line, i, line.find(expr))
		if result["result"] is False:
			i = return_point[-1] - 1
		else:
			return_point.pop()
	elif line.startswith("WHILE"):
		expr = line.split("WHILE")[1].strip()
		result = eval_expr(expr)
		if isinstance(result, tuple):
			error(result[0], result[1], line, i, line.find(expr))
		if result["result"] is True:
			return_point.append(i)
		else:
			while not line.strip().startswith("ENDWHILE"):
				i += 1
				line = lines[i]
	elif line.startswith("ENDWHILE"):
		if not return_point:
			error("SyntaxError", "ENDWHILE without WHILE", line, i, line.find("ENDWHILE"))
		i = return_point[-1] - 1