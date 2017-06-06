class Member:
	def __init__(self, name, delay_number=0.0, pendencies_number=0.0):
		self.name = name
		self.delay_number = delay_number
		self.pendencies_number = pendencies_number

	def setDelayNumber(self, delay_number=0.0):
		self.delay_number = delay_number

	def setPendingNumber(self, pendencies_number=0.0):
		self.pendencies_number = pendencies_number