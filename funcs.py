from reporting import *

def get_type(value):
	right_side_type = None
	if isinstance(value, int):
		return "Integer"
	elif isinstance(value, float):
		return "Real"
	elif isinstance(value, bool):
		return "Boolean"
	elif isinstance(value, str):
		if value[0] in ["'", '"']:
			right_side_type = "String"
		elif value.count(".") == 1:
			right_side_type = "Real"
		elif value.isdigit():
			right_side_type = "Integer"
		elif value.startswith("["):
			right_side_type = "Array"
		else:
			return "Variable"
		return right_side_type
	elif isinstance(value, list):
		return "Array"

def get_real_value(value):
	type = get_type(value)
	if type == "String":
		return value
	elif type == "Real":
		return float(value)
	elif type == "Integer":
		return int(value)
	elif type == "Array":
		return value
	elif type == "Boolean":
		return bool(value)
	else:
		return value
		