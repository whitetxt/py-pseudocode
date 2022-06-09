from dataclasses import dataclass
from typing import Any

@dataclass()
class Variable:
	name: str
	value: Any
	type: str
	constant: bool

	@property
	def real_value(self):
		if self.type == "String":
			return self.value
		elif self.type == "Real":
			return float(self.value)
		elif self.type == "Integer":
			return int(self.value)
		elif self.type == "Array":
			return self.value
		else:
			return self.value