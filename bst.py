#!/usr/bin/python3

import unittest
import math
import binary_tree as bt
from queue import *


class BST(bt.BinaryTree):
	"""
	A Binary Search Tree implementation. Add BST-specific functionalities to a Binary Tree class
		* constructing and maintaining BSTs: insert_, transplant_, delete_
		* querying BSTs: search_, predecessor_, successor_, minimum_, maximum_
	"""

################ TREE CONSTRUCTION #################	

	def __init__(self, keys=[], array=None):
		""" Construct a new BST, from a list of keys.

		:param keys: keys
		:type keys: list
		"""
		super().__init__()

		if array:
			self.update_from_array( array )
		else:
			for k in keys:
				self.insert_key( k )

			
	def insert_node(self, node, comparable_func=None):
		"""
		.. _insert_node:

		Insert a new node in the tree

		:param key: a key
		:type key: int
		:param comparable_func: a Boolean function that checks a condition on the node to be inserted before performing the key comparison; if it returns False, the insertion attempt aborts.
		:type comparable_func: func
		:return: True if the insertion successed; False otherwise
		:rtype: bool
		"""
		y = None
		x = self.root
		depth =	0
		# walking down the tree for a place
		while x is not None:
			y = x
			depth += 1
			if comparable_func and not comparable_func( node.key, x.key): return  False
			if node.key < x.key:
				x = x.left
			else:
				x = x.right
		node.parent = y
		
		# non-essential code meant for tree display (see display() function)
		if depth > self.height:
			self.height = depth
		node.depth=depth

		# the following inserts the node
		# tree was empty
		if (y is None):
			self.root = node
		 
		elif comparable_func and not comparable_func( node.key, y.key ): return False
		elif node.key < y.key:
			y.left = node 
		else:
			y.right = node

		return True

	def insert_key( self, key, comparable_func=None):
	
		return self.insert_node( bt.Node(key), comparable_func )


	def transplant(self, u, v):
		"""
		.. _transplant:

		Replace subtree rooted at node u 
		with subtree rooted at node v

		:param u: subtree to be replaced
		:param v: subtree to be used as a replacement
		:type u: bt.Node
		:type v: bt.Node
		"""
		# updating parent's pointer
		if u.parent is None:
			self.root = v
		elif u is u.parent.left:
			u.parent.left = v
		else: u.parent.right = v

		# updating transplanted subtree's pointer
		if v is not None:
			v.parent = u.parent
			if v.parent is None:
				self.update_depth( v, 0)
			else:
				self.update_depth( v, v.parent.depth+1) 


	def delete_node(self, z):
		"""
		.. _delete:

		Delete a node from the tree.

		:param z: a node
		:type z: bt.Node
		"""
		if z.left is None:
			self.transplant(z, z.right)
		elif z.right is None:
			self.transplant(z, z.left)
		else:
			y = self.minimum( z.right )
			if y.parent is not z:
				self.transplant(y, y.right)
				y.right = z.right
				y.right.parent = y
			self.transplant(z,y)

			y.left = z.left
			y.left.parent = y


	def delete_key(self, key):
		""" 
		Remove the key from the tree, and return it.
		"""
		node_to_delete = self.search(key)

		if node_to_delete is None:
			return None
		value = node_to_delete.key
		self.delete_node( node_to_delete )
		return value
		

############## TREE QUERIES ######################


	def search( self, key):
		return self.search_rec(self.root, key)

	def search_rec(self, x, key):
		if x is None or x.key == key:
			return x
		if key < x.key:
			return self.search_rec(x.left, key)
		else:	return self.search_rec(x.right, key)
	
	def minimum(self, tree=None):
		x = tree
		if x is None:
			x = self.root
		while( x.left is not None):
			x = x.left
		return x

	def maximum(self, tree=None):
		x = tree
		if x is None:
			x = self.root
		while (x.right is not None):
			x = x.right
		return x

	def minimum_recursive( self ):
		def recproc( root ):
			if root.left is None:
				return root
			return recproc( root.left)	
		return recproc( self.root )

	def successor(self, x):
		if x.right is not None:	
			return self.minimum(x.right)
		y = x.parent
		# go up only if parent is smaller (i.e. node is a R child)
		while y is not None and x is y.right:
			x = y
			y = y.parent
		return y

		
	def predecessor(self, x):
		if x.left is not None:
			return self.maximum(x.left)
		y = x.parent
		# go up only if parent is larger (i.e. node is a L child)
		while y is not None and x is y.left:
			x = y
			y = y.parent
		return y

			
################## TESTING #############

class BST_UnitTest(unittest.TestCase):

	def test_init(self):
		bst = BST([15,7,3,21,19,24,7,67,8,9])

		self.assertEqual( bst.list(), [3,7,7,8,9,15,19,21,24,67])


	def test_walk(self):
		bst=BST()
		for k in [15,7,3,21,19,24,7,67,8,9]:
			bst.insert_key(k)

		self.assertEqual( bst.list(), [3,7,7,8,9,15,19,21,24,67])



	def test_non_recursive_inorder_walk(self):
		bst=BST()
		for k in [15,7,3,21,19,24,10,67,12,14,2,4,8]:
			bst.insert_key(k)

		bst.display()

		self.assertEqual( bst.non_recursive_inorder_walk(), [2,3,4,7,8,10,12,14,15,19,21,24,67])


	def test_search(self):
		bst=BST()
		for k in [15,7,3,98,21,19,124,24,10,67,12,14,2,4,8,35]:
			bst.insert_key(k)
		bst.display()
		bst=BST()
		for k in [78,32,212,23,11,55,36,10,43,57,35]:
			bst.insert_key(k)
		bst.display()

		bst=BST()
		for k in [100,45,12,89,34,36,1,24,12,9,35]:
			bst.insert_key(k)
		bst.display()


	def test_minimum_non_rec(self):
		bst = BST()
		for k in [15,7,3,21,19,24,10,67,12,14,2,4,8]:
			bst.insert_key(k)
		bst.display()
		self.assertEqual( bst.minimum(), bst.search(2) )

	
	def test_minimum_rec(self):
		bst = BST()
		for k in [15,7,3,21,19,24,10,67,12,14,2,4,8]:
			bst.insert_key(k)
		bst.display()
		self.assertEqual( bst.minimum_recursive(), bst.search(2) )

	def test_successor_1(self):
		""" Successor is in R subtree """
		bst = BST()
		for k in [15,7,3,21,19,24,10,67,12,14,2,4,8]:
			bst.insert_key(k)
		bst.display()
		self.assertEqual( bst.successor( bst.search(7)), bst.search(8)) 

	def test_successor_2(self):
		""" Successor is an ancestor """
		bst = BST()
		for k in [15,7,3,21,19,24,10,67,12,14,2,4,8]:
			bst.insert_key(k)
		bst.display()
		self.assertEqual( bst.successor( bst.search(14)), bst.search(15)) 

	
	def test_predecessor_1(self):
		""" Predecessor is in L subtree """
		bst = BST()
		for k in [15,7,3,21,19,24,10,67,12,14,2,4,8]:
			bst.insert_key(k)
		bst.display()
		self.assertEqual( bst.predecessor( bst.search(7)), bst.search(4)) 

	def test_predecessor_2(self):
		""" Predecessor is an ancestor """
		bst = BST()
		for k in [15,7,3,21,19,24,10,67,12,14,2,4,8]:
			bst.insert_key(k)
		bst.display()
		self.assertEqual( bst.predecessor( bst.search(8)), bst.search(7)) 

	

	def test_search(self):
		bst=BST()
		for k in [15,7,3,21,19,24,7,67,8,9]:
			bst.insert_key(k)

		x = bst.search( 24 )

		self.assertEqual( x.key, 24)

	def test_transplant(self):
		bst1=BST()
		for k in [15,7,3,21,19,24,7,67,8,9]:
			bst1.insert_key(k)

		print('\ntest_transplant: ')
		print('	BEFORE: target tree:')

		bst1.display()
		
		bst2 = BST()	
		bst2.insert_key( 22 )
		bst2.insert_key( 26 )
		bst2.insert_key( 25 )

		print(' grafted subtree: ')	
		bst2.display()

		u = bst1.search(24)

		bst1.transplant(u, bst2.root)
#		print ''
#
		print('\n	AFTER: ')
		bst1.display()
		

		
		
	def test_delete_1(self):
		
		bst=BST()
		for k in [15,7,3,21,19,24,7,67,8,9,1]:
			bst.insert_key(k)

		print('\ntest_delete (a) z (24) has no left child:')
		print('	BEFORE: ')
		bst.display()

		bst.delete_node( bst.search(24) )

		print('	AFTER: ')
		bst.display()

		self.assertEqual( bst.list(), [1, 3, 7, 7, 8, 9, 15, 19, 21, 67])
		
	def test_delete_2(self):
		
		bst=BST()
		for k in [15,7,3,21,19,24,7,67,8,9,1]:
			bst.insert_key(k)

		print('\ntest_delete (b) z (3) has no right child:')
		print('	BEFORE: ')
		bst.display()

		bst.delete_node( bst.search(3) )

		print('	AFTER: ')
		bst.display()

		self.assertEqual( bst.list(), [1, 7, 7, 8, 9, 15, 19, 21, 24, 67])
		
	def test_delete_3(self):
		
		bst=BST()
		for k in [15,7,3,21,19,24,7,67,8,9]:
			bst.insert_key(k)

		print('\ntest_delete (c) z (21) has 2 children, y is z\'s right child:')
		print('	BEFORE: ')
		bst.display()

		bst.delete_node( bst.search(21) )

		print('	AFTER: ')
		bst.display()

		self.assertEqual( bst.list(), [3, 7, 7, 8, 9, 15, 19, 24, 67])
		
	def test_delete_4(self):
		
		bst=BST()
		for k in [15,7,3,21,19,24,7,67,8,9]:
			bst.insert_key(k)

		print('\ntest_delete (d) z (15) has 2 children, y is not z\'s right child:')
		print('	BEFORE: ')
		bst.display()

		bst.delete_node( bst.search(15) )

		print('	AFTER: ')
		bst.display()

		self.assertEqual( bst.list(), [3, 7, 7, 8, 9, 19, 21, 24, 67])

		
def main():
        unittest.main()

if __name__ == '__main__':
        main()


	
