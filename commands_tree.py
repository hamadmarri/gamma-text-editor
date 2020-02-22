
#from .splay_tree import SplayTree
import splay_tree

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


class CommandsTree(splay_tree.SplayTree):
	def __init__(self):
		super().__init__()
		self.seek_iter = 0
		self.search_iter = None
		self.search_iter_counter = 0
		self.queue = [] # <-- for breadth first search
		
	
	def insert(self, value):
		super().insert(value.lower())
		
		

	def find(self, value, match_callback, node=None):
		#print(f"find from {node}")
		return super().find(value.strip().lower(), match_callback, node)
		
				

		
	def strict_search_match(self, node, value):
		if node.value.find(value) == 0:
			return True
		
		return False
		
	
	def soft_search_match(self, node, value):
		if node.value.find(value) != -1:
			return True
		
		return False
				
			
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
				
		yield node
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
		
		# if not root we don't need to retrieve
		# that last item in previuse results
		#else:
			# enqueue children
		#	self.enqueue_children(node)
		
		# while queue not empty and search_iter_counter > 0
		while self.queue and self.search_iter_counter > 0:
			# pop
			node = self.queue.pop(0)
			#print("visit", node)
	
			# is solution?
			# search_term is None, then show without checking
			if show_anyway or self.soft_search_match(node, search_term):
				#search_iter_counter--
				self.search_iter_counter -= 1			
				yield node
				# set search_iter to node
				self.search_iter = node
							
				 
			# enqueue children
			self.enqueue_children(node)
		
#		if not queue:
#			self.search_iter = None
	
		
	def enqueue_children(self, node):
		if node.left:
			self.queue.append(node.left)
		if node.right:
			self.queue.append(node.right)
		
		
if __name__ == "__main__":
	t = CommandsTree()
	t.insert("Minimize window")
	t.insert("Toggle maximize window")
	t.insert("Exit")
	t.insert("Close File")
	t.insert("Close All")
	t.insert("Open File")
	t.insert("Save File")
	t.insert("Search in File")
	t.insert("Open Directory")
	t.insert("Switch to File < commander_window.py")
	t.insert("oz")
	t.insert("Saa")
	t.insert("Seaa")
	t.insert("Sed")
	t.insert("Sed")
	t.insert("Seda")
	t.insert("Sede")
	t.insert("Sedb")
	t.insert("Sedd")
	t.insert("Sw")
	t.insert("Sl")
	t.insert("R")
	
	t.traverse(0)
	
	

		
	SS = t.first(max_result=4)
	for n in SS:
		print("-----------------------> ", n)

	print()
	SS = t.next(max_result=4)
	for n in SS:
		print("-----------------------> ", n)

	
	print()
	SS = t.first(max_result=10)
	for n in SS:
		print("-----------------------> ", n)
	
	
#	n = t.find("Sedb", n)
#	print("n", n)
		
	
	#t.splay(t.find("Switch to File < commander_window.py"))
#	t.splay(t.find("R"))
#	t.splay(t.find("Search in File"))
	#t.traverse(0)
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
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