#!/usr/bin/python3

import unittest
import math
from collections import deque

class Node():

	def __init__(self, key=None, left=None, right=None, parent=None,depth=0):
		""" Initializes a new node """
		self.key = key
		self.left = left
		self.right = right
		self.parent = parent
		self.depth=depth

	
	def add_left(self, left ):
		""" Helper function: create a L child  """
		self.left = left
		left.parent = self
		left.depth = self.depth + 1

	def add_right(self, right ):
		""" Helper function: create a R child  """
		self.right = right
		right.parent = self
		right.depth = self.depth + 1

	def __str__(self):
		return str(self.key)


class BinaryTree():
	
	def __init__(self, root=None, array=None):
		""" Initializes an empty tree 
		
		:param root: the root node reference
		:type root: Node
		:param array: (optional) if provided, a tree, in the form of nested lists
		:type array:  tuple
		"""
		self.root = root
		self.height=-1

		if array is not None:
			self.update_from_array( array )


	def list(self):
		""" Return a list of nodes, sorted by increasing order """
	
		return self.inorder_walk()


	def non_recursive_inorder_walk(self):
		""" A inorder, non-recursive treewalk: nodes are listed in this order
			* Left
			* Parent
			* Right
		:return: the list of visited nodes, inorder
		:rtype: list
		"""
		x = self.root
		stack = [self.root]
		walk = []
	
		while( len(stack)>0):
			if x.left is not None:
				stack.append(x.left)
				x = x.left
			# don't update x until we find a node
			# in the stack that has a right child
			elif x.right is None:
				listed = stack.pop()	
				walk.append( listed.key )
				if listed.right is not None:
					x = listed.right
					stack.append(x)
			# cover the case where a node has only a right child
			else:
				x = x.right	
			
		return walk
	
		
	def non_recursive_preorder_walk(self):
		""" A straightforward, non-recursive algorithm for a pre-order treewalk
		of the tree: nodes are listed in this order
			* Parent
			* Left
			* Right
		:return: the list of visited nodes, preorder
		:rtype: list
		"""
		x = self.root
		stack = [ self.root ]
		walk = []
		while (len(stack)>0):
			current = stack.pop()
			walk.append( current.key )

			if current.right is not None:
				stack.append( current.right )
			if current.left is not None:
				stack.append(current.left )
		return walk

		
	def preorder_walk( self ):
		"""
		.. _preorder_walk:

		Perform a preorder tree walk.

		:return: list of all visited nodes, preorder
		:rtype: list
		"""
#		def preorder_rec( node, lst ):
#			lst.append( node.key )
#			if node.left is not None:
#				preorder_rec( node.left, lst)
#			if node.right is not None:
#				preorder_rec( node.right, lst)
#			return lst	
#
#		return preorder_rec( self.root, [])
		def preorder_rec( node ):
			lst.append( node.key )
			if node.left is not None:
				preorder_rec( node.left)
			if node.right is not None:
				preorder_rec( node.right)

		lst = []	
		if self.root is not None:
			preorder_rec( self.root)
		return lst
	
	def preorder_rl_walk( self ):
		"""
		.. _preorder_rl_walk:

		Perform a preorder tree walk, from R to L

		:return: list of all visited nodes, preorder RL
		:rtype: list
		"""
		def preorder_rec( node ):
			lst.append( node.key )
			if node.right is not None:
				preorder_rec( node.right)
			if node.left is not None:
				preorder_rec( node.left)

		lst = []	
		if self.root is not None:
			preorder_rec( self.root)
		return lst
	
	def postorder_walk( self ):
		"""
		.. _postorder_walk:
		
		Perform a postorder tree walk.

		:return: list of all visited nodes, postorder
		:rtype: list
		"""
		def postorder_rec( node, lst ):
			if node.left is not None:
				postorder_rec( node.left, lst)
			if node.right is not None:
				postorder_rec( node.right, lst)
			lst.append( node.key )
			return lst	

		if self.root is None:
			return []
		return postorder_rec( self.root, [])
	

	def postorder_rl_walk( self ):
		"""
		.. _postorder_rl_walk:

		Perform a postorder tree walk, from R to L

		:return: list of all visited nodes, postorder RL
		:rtype: list
		"""
		def postorder_rec( node ):
			if node.right is not None:
				postorder_rec( node.right)
			if node.left is not None:
				postorder_rec( node.left)
			lst.append( node.key )

		lst = []
		if self.root is not None:
			postorder_rec( self.root)
		return lst

	def inorder_walk( self ):
		"""
		.. _inorder_walk:
		
		Perform a inorder tree walk.

		:return: list of all visited nodes, inorder
		:rtype: list
		"""
		def inorder_rec( node, lst ):
			if node.left is not None:
				inorder_rec( node.left, lst)
			lst.append( node.key )
			if node.right is not None:
				inorder_rec( node.right, lst)
			return lst	

		if self.root is None:
			return []
		return inorder_rec( self.root, [])
	
	def inorder_rl_walk( self ):
		"""
		.. _inorder_rl_walk:
		
		Perform a inorder tree walk, from R to L

		:return: list of all visited nodes, inorder RL
		:rtype: list
		"""
		def inorder_rl_rec( node, lst ):
			if node.right is not None:
				inorder_rl_rec( node.right, lst)
			lst.append( node.key )
			if node.left is not None:
				inorder_rl_rec( node.left, lst)
			return lst	

		if self.root is None:
			return None
		return inorder_rl_rec( self.root, [])
	

	def is_bst( self ):
		"""
		.. _is_bst:

		Check for BST property, recursively.

		:return: True if this tree is a Binary Search Tree; False otherwise.
		:rtype: bool
		"""
		def is_bst_recursive( node, minimum, maximum):
			if node is None:
				return True
			if node.key < minimum or node.key > maximum:
				print("Not a bst: {}!".format( node.key ))
				return False
			return is_bst_recursive(node.left, minimum, node.key) and is_bst_recursive(node.right, node.key, maximum)

		infty = 2**14
		return is_bst_recursive( self.root, -infty, infty )	

	def bfs_walk( self ):
		queue = deque()
		walk=[]

		if self.root is None:
			return walk

		queue.enqueue(self.root)
		while len(queue)>0:
			x = queue.popleft()

			walk.append(x.key)

			if x.left:
				queue.popleft(x.left)
			if x.right:
				queue.popleft(x.right)
		return walk

	
	def bfs_rl_walk( self ):
		queue = deque()
		walk=[]

		if self.root is None:
			return walk

		queue.append(self.root)
		while len(queue)>0 :
			x = queue.popleft()

			walk.append(x.key)

			if x.right:
				queue.append(x.right)
			if x.left:
				queue.append(x.left)
		return walk

	

	## NON-ESSENTIAL FUNCTIONS: FOR TEACHING PURPOSE

	def update_from_array(self, array  ):
		""" Build a binary tree from nested tuples 
		
		Ex. BinaryTree().update_from_array( ( 1,(2,3,4),(5,None,6) ) yields the following tree:

				1
		     __________/\________
		    2                   5
		  _/\                    \
		 3   4                    6

		:param array: a list of the form ( key, ( left subtree ), (right subtree ))
		:type array: tuple
		"""
	
		def read_rec( triplet ):
			""" Inner function: build a (node,depth) pair from a triplet (parenet,left,right) """
			# base case: a leaf
			if triplet is None:
				return None
			if type(triplet) is not list and type(triplet) is not tuple:
				return (Node(triplet), 0)
			# parent node
			n = Node( triplet[0] )
			# children
			data_left = read_rec( triplet[1] )
			data_right = read_rec( triplet[2] )
			if data_left is not None: n.add_left ( data_left[0])
			if data_right is not None: n.add_right ( data_right[0])
			# returning a pair:
			# - current node pointer
			# - height, as computed from children's heights
			if data_left is None:
				if data_right is None:
					return (n,0)
				return (n,data_right[1]+1)
			elif data_right is None:
				return (n,data_left[1]+1)
			return (n, max(data_left[1],data_right[1])+1)

		data = read_rec( array )
		self.root, self.height = data
		self.update_depth( self.root, 0)

		return self
		
	def update_depth(self, node, depth):
		""" Update the depth attribute on the given node, and all its
		descendants

		:param node: root of the subtree to be updated
		:param depth: value of the new depth attribute
		:type node: Node
		:type depth: int
		"""
		if node is not None:
			node.depth=depth
			self.update_depth(node.left, depth+1)
			self.update_depth(node.right, depth+1)

	def display(self):
		"""
		Breadth-first tree-walking, displaying the nodes on the console
		"""
		if self.root is None:
			return
		q = deque()
		
		# overall width is function of the height of the tree
		root_pos = ((1<<(self.height+1))-1)
		
		prev_depth=0
		prev_pos=0
		edge_def=[]
		label_offset=0
		consumed=0
		q.append((self.root,root_pos))
		while len( q ) >0:
			(n, n_pos) = q.popleft()

			# starting a row: using absolute position for offset
			if n.depth != prev_depth or n is self.root:
				print('')
				prev_depth=n.depth
				offset = n_pos-1
				label_offset=0

				# converting edge boundaries into a string
				print( self.edge_string(edge_def) )
				edge_def=[]

			# in a row: computing an offset from last position
			# -2 takes care of label already entered
			else:
				offset = n_pos - prev_pos - label_offset

			prev_pos = n_pos
			label_offset=len(str(n.key))

			# display the node
			print('{}{}'.format(offset*' ',n.key),end="")

			
			# enqueue children, computing edge boundaries at the same time
			edge_length = int(math.ceil(root_pos/(2**(n.depth+1))))
			if n.left is not None:
				q.append( (n.left, int(n_pos - edge_length)) )
				edge_def.append( ('L', int(n_pos - edge_length),n_pos) )
			if n.right is not None:
				q.append( (n.right, int(n_pos + edge_length)) )
				edge_def.append(  ('R', n_pos+1,int(n_pos + edge_length)) )
		print('')			
		
	def edge_string( self, definition ):
		""" Build a string according to edge specs """
		last = 0
		string_arr = []
		for pair in definition:

			string_arr.append(' '*(pair[1]-last-1))
			if pair[0]=='L':
				string_arr.append(' ')
			else:
				string_arr.append( '\\' )
			string_arr.append( '_'*(pair[2]-pair[1]-1))
			if pair[0]=='L':
				string_arr.append( '/' )
			else:
				string_arr.append( ' ' )
			last = pair[2]
		return ''.join( string_arr )
			
					
	def tree_to_latex( self ):
		""" Produce a LaTeX representation of the binary tree """

		def add_child(node, tab=''):
			nonlocal latex_output
			val = str( node.key )
			if node is self.root:
				latex_output.append( tab + '\\node[circle,draw]{' + val + '}') 
			else:
				latex_output.append( tab + 'child{ node[circle,draw]{' + val + '}')
			if node.left is not None:
				add_child(node.left, tab+'  ')
			if node.right is not None:
				add_child(node.right, tab+'  ')
			if node is not self.root:
				latex_output.append('}')


		latex_output = [ '' ]
		latex_output.append('{\\footnotesize \\begin{tikzpicture}[level/.style={sibling distance = 4cm/#1, level distance = 1cm}]')
		add_child( self.root)
		latex_output.append('; \n \\end{tikzpicture}}')
		for line in latex_output:
			print(line)
	
	def get_leaves( self ):

		leaves = []
		
		def walk( node ):
			if node.left is None and node.right is None:
				leaves.append( node )
				return
			if node.left:
				walk(node.left)
			elif node.right:
				walk(node.right)
		walk( self.root )
		return leaves

	def to_array( self ):
		def to_array_rec( node ):
			if node is None:
				return None
			if node.left is None and node.right is None:
				return node.key
			return (node.key, to_array_rec( node.left ), to_array_rec(node.right))
		return to_array_rec( self.root )

			
class BinaryTree_UnitTest(unittest.TestCase):

	def test_build_from_array_1(self):
		bst = BinaryTree().update_from_array( ('-',('+',5,('*', ('+',1,2), 4)), 3) ) 
		self.assertEqual( bst.root.key, '-')
		self.assertEqual(bst.root.left.key , '+' )
		self.assertEqual(bst.root.right.key, 3 )
		self.assertEqual(bst.root.left.left.key, 5 )
		self.assertEqual(bst.root.left.right.key, '*')
		self.assertEqual(bst.root.left.right.left.key, '+')
		self.assertEqual(bst.root.left.right.right.key, 4)
		self.assertEqual(bst.root.left.right.left.left.key, 1)
		self.assertEqual(bst.root.left.right.left.right.key, 2)
		bst.display()
		

	def test_build_from_array_2(self):
		""" Correct handling of null pointers """
		bst = BinaryTree().update_from_array( (1,None,3) )
		bst.display()
		self.assertEqual( bst.root.key, 1)
		self.assertEqual( bst.root.left, None)
		self.assertEqual( bst.root.right.key, 3)


	def test_non_recursive_inorder_walk(self):
		bst=BinaryTree( array = (15, (7, (3,2,4), (10,8,(12,14,None))), (21, 19 ,(24,None,67))))
		bst.display()

		self.assertEqual( bst.non_recursive_inorder_walk(), [ 2,3,4,7,8,10,14,12,15,19,21,24,67])

#
	def test_non_recursive_preorder_walk_1(self):
		bst=BinaryTree( array =(15, (7, (3,2,4), (10,8,(12,14,None))), (21, 19 ,(24,None,67))))
		bst.display()

		self.assertEqual( bst.non_recursive_preorder_walk(), [15,7,3,2,4,10,8,12,14,21,19,24,67])

	def test_non_recursive_preorder_walk_2(self):
		""" 
	                                       -
		               _______________/\______________ 
		              +                               3
	              _______/\______ 
	             5              *
		                ___/\__ 
		               +       4
		             _/\ 
		            1   2
		"""

		bst = BinaryTree( array=( ('-',('+',5,('*', ('+',1,2), 4)), 3) ) )
		bst.display()
		self.assertEqual( bst.non_recursive_preorder_walk(), ['-', '+', 5, '*', '+', 1, 2, 4, 3])


	def test_preorder_walk(self):
		" Test pre-order tree walk """	
		bst=BinaryTree( array = (15, (7, (3,2,3), (10,8,(14,12,None))), (21, 19 ,(24,24,67))))
		print("test pre-order walk")
		bst.display()
		self.assertEqual( bst.preorder_walk(),  [15, 7, 3, 2, 3, 10, 8, 14, 12, 21, 19, 24, 24, 67])
	
	def test_postorder_walk(self):
		" Test post-order tree walk """	
		bst=BinaryTree( array = (15, (7, (3,2,3), (10,8,(14,12,None))), (21, 19 ,(24,24,67))))
		print("test post-order walk")
		bst.display()
		self.assertEqual( bst.postorder_walk(),  [2, 3, 3, 8, 12, 14, 10, 7, 19, 24, 67, 24, 21, 15])
	

	def test_is_bst_true_1(self):
		""" Test BST property true: note that keys might be equal """
		bst=BinaryTree( array = (15, (7, (3,2,3), (10,8,(14,12,None))), (21, 19 ,(24,24,67))))
		print("test BST true")
		bst.display()
		self.assertTrue( bst.is_bst() )

	
	def test_is_bst_true_2(self):
		""" Test BST property: leaf """
		bst=BinaryTree( array = (15,None,None))
		print("test BST true: testing leaf")
		bst.display()
		self.assertTrue( bst.is_bst() )
		

	def test_is_bst_false_1(self):
		""" Test BST property false: property is broken between R child and parent
		"""
		bst=BinaryTree( array = (15, (7, (3,2,4), (10,8,(12,None,None))), (21, 19 ,(24,None,23))))
		print("test BST false: R child/parent")
		bst.display()
		self.assertFalse( bst.is_bst() )

	def test_is_bst_false_2(self):
		""" Test BST property false: property is broken between L child and parent
		"""
		bst=BinaryTree( array = (15, (7, (3,2,4), (10,8,(12,14,None))), (21, 19 ,(24,25,None))))
		print("test BST false: L child/parent")
		bst.display()
		self.assertFalse( bst.is_bst() )

	def test_is_bst_false_3(self):
		""" Test BST property false: property is broken between R descendant and ancestor
		"""
		bst=BinaryTree( array = (15, (7, (3,2,4), (10,8,(12,9,None))), (21, 19 ,(24,None,25))))
		print("test BST false: R descendant/ancestor")
		bst.display()
		self.assertFalse( bst.is_bst() )


	def test_is_bst_false_4(self):
		""" Test BST property false: property is broken between R descendant and ancestor
		"""
		bst=BinaryTree( array = (15, (7, (3,2,4), (10,8,(16,11,None))), (21, 19 ,(24,None,25))))
		print("test BST false: L descendant/ancestor")
		bst.display()
		self.assertFalse( bst.is_bst() )


def main():
        unittest.main()

if __name__ == '__main__':
        main()


	
