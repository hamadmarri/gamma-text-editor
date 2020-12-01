

class LogEntry():
	def __init__(self, message, level):
		self.message = message
		self.level = level
		
	def __str__(self):
		return self.message
