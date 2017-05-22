class Member:
	def __init__(self, name, delay_number=0.0):
		self.name = name
		self.delay_number = delay_number

	def setDelayNumber(self, delay_number=0.0):
		self.delay_number = delay_number