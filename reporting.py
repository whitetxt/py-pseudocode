def error(error_type: str, msg: str, line: str, line_num: int, pos: int):
	print()
	print(f"An error has occurred during execution in line {line_num + 1}:")
	print(f"{line_num + 1:<5} {line}")
	print(f"{' ' * (5 + pos)} ^--")
	print(f"{error_type}: {msg}")
	print()
	exit(1)

def base_error(error_type: str, msg: str, value: str):
	print()
	print(f"An error has occurred during execution.")
	print(value)
	print(f"{error_type}: {msg}")
	print()
	exit(1)