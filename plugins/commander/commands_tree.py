
from .splay_tree import SplayTree


# from random import randrange




######################## CommandsTree INTERFACE ##########################
# 1: for c in commands:    get all 
# 2: get first n items: breadth first search, when just opened commander
# 3: get next n items: when scrolling down
# 4: strict search: search for n items begain with search_term: return first n items, if prev serach is prefix of next search
#					   continue from the sub root node
# 5: get next n search items: 
# 6: if strict search failed: do soft search inorder: when #4 or #5 return less than n items
# 7: get next soft search for n items:


class CommandsTree(SplayTree):
	def __init__(self):
		super().__init__()
		self.seek_iter = 0
		self.search_iter = None
		self.search_iter_counter = 0
		self.queue = [] # <-- for breadth first search
		
	
	def insert(self, command):
		value = command["name"]
		node = super().insert(value.strip().lower())
		node.command = command
		command["node"] = node
		return node
		
		

	def find(self, value, match_callback=None, node=None):
		#print(f"find from {node}")
		if not match_callback:
			match_callback = self.exact_match
			
		return super().find(value.strip().lower(), match_callback, node)
		
				

	def exact_match(self, node, value):
		return (node.value == value)
			
	def strict_search_match(self, node, value):
		return (node.value.find(value) == 0)
				
	def soft_search_match(self, node, value):
		return (node.value.find(value) != -1)

	
			
	def strict_search(self, search_term, max_result=1):
		# set search_iter to first match 
		self.search_iter = self.find(search_term, self.strict_search_match, self.root)
		self.search_iter_counter = max_result
		return self.recursive_strict_search(search_term, self.search_iter)
	
	
	# good while user typying, when user is appening letters in
	# search term like first type "s" <- "strict_search" method is called
	# then user continue typing "se" <- here "continue_strict_search" is called 
	# to start from the last subtree instead of starting again from tree root 
	def continue_strict_search(self, search_term, max_result=1):
		# set search_iter to first match of subtree  
		self.search_iter = self.find(search_term, self.strict_search_match, self.search_iter)
		self.search_iter_counter = max_result
		return self.recursive_strict_search(search_term, self.search_iter)
	
	
	# in preorder
	def recursive_strict_search(self, search_term, node):
		#print(f"searching {node}")
		
		if not node:
			return
		
		if self.search_iter_counter == 0:
			return
			
		node = self.find(search_term, self.strict_search_match, node)
		if not node:
			return
				
		yield node.command
		self.search_iter_counter -= 1

		yield from self.recursive_strict_search(search_term, node.left)
		yield from self.recursive_strict_search(search_term, node.right)

			


	def soft_search(self, search_term, max_result=1):
		del self.queue[:]
		self.search_iter_counter = max_result
		return self.breadth_first_search(search_term, self.root)
		
	
	# only used for scrolling, if search term is changed, then call "soft_search" again
	def continue_soft_search(self, search_term, max_result=1):
		self.search_iter_counter = max_result
		return self.breadth_first_search(search_term, self.search_iter)
		
		
	
	# get first items starting from the top of the tree (breadth first)
	def first(self, max_result=1):
		del self.queue[:]
		self.search_iter_counter = max_result
		return self.breadth_first_search(None, self.root, show_anyway=True)
		
	# continue "first" mothed for more items
	def next(self, max_result=1):
		self.search_iter_counter = max_result
		return self.breadth_first_search(None, self.search_iter, show_anyway=True)
		
		
		
	def breadth_first_search(self, search_term, node, show_anyway=False):	
		if not node:
			return
				
		# add root
		if node == self.root:
			self.queue.append(node)
				
		# while queue not empty and search_iter_counter > 0
		while self.queue and self.search_iter_counter > 0:
			# pop
			node = self.queue.pop(0)
	
			# is solution?
			# search_term is None, then show without checking
			if show_anyway or self.soft_search_match(node, search_term):
				#search_iter_counter--
				self.search_iter_counter -= 1			
				yield node.command
				# set search_iter to node
				self.search_iter = node
							
			# enqueue children
			self.enqueue_children(node)
	
		
	def enqueue_children(self, node):
		if node.left:
			self.queue.append(node.left)
		if node.right:
			self.queue.append(node.right)
		
		
if __name__ == "__main__":
	t = CommandsTree()
	t.insert({"plugin-name": "commander", "name": "Open/Close This Window!", "ref": print,"shortcut": "<Ctrl>",	})
	t.insert({"plugin-name": "commander", "name": "Toggle maximize window", "ref": print,"shortcut": "<Ctrl>",	})
	t.insert({"plugin-name": "commander", "name": "Exit", "ref": print,"shortcut": "<Ctrl>",	})
	t.insert({"plugin-name": "commander", "name": "Close File", "ref": print,"shortcut": "<Ctrl>",	})
	t.insert({"plugin-name": "commander", "name": "Close All", "ref": print,"shortcut": "<Ctrl>",	})
	t.insert({"plugin-name": "commander", "name": "Open File", "ref": print,"shortcut": "<Ctrl>",	})
	t.insert({"plugin-name": "commander", "name": "Save File", "ref": print,"shortcut": "<Ctrl>",	})
	t.insert({"plugin-name": "commander", "name": "Search in File", "ref": print,"shortcut": "<Ctrl>",})
	t.insert({"plugin-name": "commander", "name": "Open Directory", "ref": print,"shortcut": "<Ctrl>",})
	t.insert({"plugin-name": "commander", "name": "Switch to File < commander_window.py", "ref": print,"shortcut": "<Ctrl>",})
	t.traverse(0)
	
	
#	n = t.find("Exit")
#	t.delete(n)	
#	t.traverse(0)


	SS = t.first(max_result=4)
	for n in SS:
		print(n["name"])
		
	

#	n = t.find("Sedb", n)
#	print("n", n)
		
	
	n = t.find("Search in File")
	t.splay(n)
	t.traverse(0)
	
	SS = t.first(max_result=4)
	for n in SS:
		print(n["name"])
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
#	t = SplayTree()
#	
#	for i in range(1000):
#		t.insert(randrange(1000))
#			
#	arr = []
#	for i in range(1000):
#		arr.append(0)
#		
#		
#	for i in range(2000):
#		if randrange(2000) > 500:
#			n = randrange(10)
#		else:
#			n = randrange(1000)
#		
#		N = t.find(n)
#		if N:
#			arr[n] += 1	
#			t.splay(N)
#	
#		
#		
#	t.traverse(0)
#	
#	for i in range(1000):
#		print(f"{i}: {arr[i]}: {100 * arr[i] / 2000}")
