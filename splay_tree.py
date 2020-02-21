from random import randrange



class TreeNode():
	def __init__(self, value, parent=None):
		self.value = value
		self.parent = parent
		self.left = None
		self.right = None
	
	def __str__(self):
		return str(self.value)
		
		

class SplayTree():
	
	def __init__(self):
		self.root = None
	
	
	def insert(self, value):
		# if tree root is null, then just set it
		if not self.root:
			self.root = TreeNode(value, None)
			return self.root
	
		return self.insert_helper(self.root, value)
	
	
	def insert_helper(self, root, value, parent=None):
		if not root:
			new_node = TreeNode(value, parent)
			if new_node.value < parent.value:
				parent.left = new_node
			else:
				parent.right = new_node
			return new_node
			
			
		elif value == root.value:
			# duplicate
			return root
		elif value < root.value:
			self.insert_helper(root.left, value, parent=root)
		else: 	
			self.insert_helper(root.right, value, parent=root)
		
		
			
	def find(self, value):
		node = self.root
		
		while node:
			if value == node.value:
				return node
			elif value < node.value:
				node = node.left
			else:
				node = node.right
		
		return node
		



	def delete(self, node):		
		if not node:
			return
		
		# case 1: no children
		if not node.left and not node.right:
			# remove the node
			self.replace_node(node, None)
			
		# case 2: two children
		elif node.left and node.right:
			# need to get the right most node on the left child, or vise versa
			successor = self.get_successor(node)
			
			# copy successor to node
			node.value = successor.value
			
			self.delete(successor)
			
				
		# case 3: one child
		elif node.left:
			self.replace_node(node, node.left)
		elif node.right:
			self.replace_node(node, node.right)
		else:
			print("error")
		
		
		
		
		
	def get_successor(self, node):
		successor = node.left
		while successor.right:
			successor = successor.right
		
		return successor


	
	def replace_node(self, node, new_node=None):
		parent = node.parent
		
		if parent:
			if node == parent.left:
				 parent.left = new_node
			else:
				parent.right = new_node
		 
		if new_node:
			new_node.parent = parent
		
		if node == self.root:
			self.root = new_node
		 


	
	def traverse(self, order):
		if order == 0:
			self.inorder(self.root)
		elif order == 1:
			self.preorder(self.root)
		elif order == 2:
			self.postorder(self.root)
		
		print()
		print("---------------------------------")
	

	
	def inorder(self, root, tabs=""):
		if not root:
			return
			
		self.inorder(root.right, tabs + "      ")
		print(tabs + str(root.value))
		self.inorder(root.left, tabs + "      ")



	def preorder(self, root):
		if not root:
			return
		print(root.value, end=" ")
		self.preorder(root.left)
		self.preorder(root.right)
		
		
		
	def postorder(self, root):
		if not root:
			return			
		self.postorder(root.left)
		self.postorder(root.right)
		print(root.value, end=" ")




	def splay(self, node):
		
		# if root just return
		if node == self.root or not node:
			return
			
		#print(f"splay {node.value}") 
			
		# if it's child of root
		if node.parent == self.root:
			if node == self.root.left:
				# zig: right rotation
				self.R_Rot(node)
				
			elif node == self.root.right:
				 # zag: left rotation
				self.L_Rot(node)
				
		else:
			parent = node.parent
			grand_parent = node.parent.parent
			# is it left left grandchild
			if node == parent.left and parent == grand_parent.left:
				# zig zig: right right rotation
				self.R_Rot(node.parent)
				self.R_Rot(node)
			
			# if right right child
			elif node == parent.right and parent == grand_parent.right:
				# zig zig: left left rotation
				self.L_Rot(node.parent)
				self.L_Rot(node)
				
			# if right left child 
			elif node == parent.right and parent == grand_parent.left:
				# zig zag: left right rotation
				self.L_Rot(node)
				self.R_Rot(node)
				
			# if left right child 
			elif node == parent.left and parent == grand_parent.right:
				# zig zag: right left rotation
				self.R_Rot(node)
				self.L_Rot(node)
		
		
		self.splay(node)
		
		
		
	def R_Rot(self, node):
		#print(f"R:{node}")
		
		parent = node.parent
		grand_parent = node.parent.parent
		
		# right rotation
		parent.left = node.right
		
		if node.right:
			node.right.parent = parent
		
		node.right = parent
		parent.parent = node
		node.parent = grand_parent
		
		# if parent is root
		if not grand_parent:
			self.root = node
		elif parent == grand_parent.left:
			grand_parent.left = node
		else:
			grand_parent.right = node
			
		#self.traverse(0)
			
	
	
	def L_Rot(self, node):
		#print(f"L:{node}")
		parent = node.parent
		grand_parent = node.parent.parent
		
		# left rotation
		parent.right = node.left
		
		if node.left:
			node.left.parent = parent
		
		node.left = parent
		parent.parent = node
		node.parent = grand_parent
		
		
		# if parent is root
		if not grand_parent:
			self.root = node
		elif parent == grand_parent.left:
			grand_parent.left = node
		else:
			grand_parent.right = node
			
		#self.traverse(0)
			
		
	
		
		
if __name__ == "__main__":
	t = SplayTree()
	
	for i in range(99):
		t.insert(randrange(100))
		
	
	#t.traverse(0)
	#t.traverse(1)
	#t.traverse(2)
	
	
	# print(t.find(7))
	#t.delete(t.find(10))
	
	arr = []
	for i in range(100):
		arr.append(0)
		
		
	for i in range(2000):
		if randrange(2000) > 100:
			n = randrange(10)
		else:
			n = randrange(100)
		arr[n] += 1	
		t.splay(t.find(n))
	
		
#		
	t.traverse(0)
	
	for i in range(100):
		print(f"{i}: {arr[i]}: {100 * arr[i] / 2000}")
	