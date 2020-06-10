import Queue
import time

class __Queue:
	def __init__(self):
		self.q = Queue.Queue()

	def add_to_queue(self,  action):
		self.q.put(action)
		return self.q

	def get_queue(self):
		for elem in list(self.q.queue):
			print(elem.get_command())

	def clear_queue(self):
		with self.q.mutex:
			self.q.queue.clear()

	def is_empty(self):
		if(self.q.empty()):
			return True
		else:
			return False

	def queue_listener(self):
		while True:
			time.sleep(0.1)
			print('tasks in queue: ')
			print(self.q.qsize())
			print('currently processed request: ')
			#self.get_queue()
			print('currently processed request: 2')
			item = self.q.get()
			print('currently processed request: 3')
			item.process_action()
			print('currently processed request: 4')
			self.q.task_done()
			print("action end")
