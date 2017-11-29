#!/usr/bin/python3

import binary_tree as bt
import unittest
from enum import Enum


class Color(Enum):
	BLACK=0
	RED=1
		
		
class rbNode( bt.Node ):

	def __init__( self, key=None, color=Color.BLACK, left=None, right=None ):
		
		super().__init__( key, left, right )
		self.color = color

	def __str__(self):
		return '{}'.format(self.key)
	
class RedBlackTree( bt.BinaryTree ):


	def __init__(self):
		super().__init__()

		self.nil = rbNode("n")
		self.root = self.nil


	def left_rotate( self, node ):
		"""
		.. _left_rotate:
		
		Left-rotate the subtree rooted at the given node.

		:param node: the root the subtree to be rotated.
		:type node: rbNode
		"""
		y = node.right
		node.right = y.left
		if y.left is not self.nil:
			y.left.parent = node
		y.parent = node.parent
		if node.parent is self.nil:
			self.root = y
		elif node is node.parent.left:
			node.parent.left = y
		else:
			node.parent.right = y
		y.left = node
		node.parent = y

	
	def right_rotate( self, node ):
		"""
		.. _right_rotate:
		
		Right-rotate the subtree rooted at the given node.

		:param node: the root the subtree to be rotated.
		:type node: rbNode
		"""
		x = node.left
		node.left = x.right
		if x.right is not self.nil:
			x.right.parent = node
		x.parent = node.parent
		if node.parent is self.nil:
			self.root = x
		elif node is node.parent.right:
			node.parent.right = x
		else:
			node.parent.left = x
		x.right = node
		node.parent = x



	def rb_insert( self, k, comparable_func=None ):
		""" Insert a key in the tree.
		
		Create a new node from the given key, and insert it into the tree.

		:param k: a key.
		:type k: object
		:param comparable_func: a Boolean function that checks a relationship between the key to be inserted and the key at the current node, before performing the key comparison; if it returns False, the insertion attempt aborts.
		:type comparable_func: function
		:return: True after a successful insertion; False otherwise.
		:rtype: bool
		"""

		z = rbNode( k, left=self.nil, right=self.nil )

		return self.rb_insert_node( z, comparable_func=comparable_func )

	def rb_insert_node( self, z, fix_attribute_func=None, comparable_func=None  ):
		""" 
		Insert a node into the tree.

		This procedure contains one variation with respect to CLRS3, 13.3: a reference can be passed to a function to be called on the node just inserted.

		:param z: the node to be inserted.
		:type z: rbNode
		:param fix_attribute_func: a function that is to be called on the inserted node, typically used in augmented trees to update an attribute on the ancestors
		:type fix_attribute_func: function
		:param comparable_func: a Boolean function that checks a relationship between the key to be inserted and the key at the current node, before performing the key comparison; if it returns False, the insertion attempt aborts.
		:type comparable_func: function
		:return: True after a successful insertion; False otherwise.
		:rtype: bool
		"""

		y = self.nil
		x = self.root

		while x is not self.nil:
			#print("Iteration")
			#print("x.key={} z.key={}".format(x.key, z.key))
			y = x
			if comparable_func and not comparable_func( z.key, x.key): return  False
			if z.key < x.key:
				#print("x={}".format( x.left ))
				x = x.left
			else: x = x.right
		z.parent = y

		if y is self.nil:
			self.root = z
		elif comparable_func and not comparable_func( z.key, y.key):
			return False
		elif z.key < y.key:
			y.left = z
		else: 
			y.right = z
		z.left = self.nil
		z.right = self.nil
		z.color = Color.RED

		if fix_attribute_func:
			fix_attribute_func( z )
		self.rb_insert_fixup( z )

		return True


	def rb_insert_fixup( self, z):
		""" After inserting a node, restore the Red-Black properties on its ancestors.

		:param z: the node just inserted
		:type z: rbNode
		"""
		while z.parent.color == Color.RED:
			if z.parent is z.parent.parent.left:
				y = z.parent.parent.right
				if y.color == Color.RED:
					z.parent.color = Color.BLACK
					y.color = Color.BLACK
					z.parent.parent.color = Color.RED
					z = z.parent.parent
				else:
					if z is z.parent.right:
						z = z.parent
						self.left_rotate( z )
					z.parent.color = Color.BLACK
					z.parent.parent.color = Color.RED
					self.right_rotate( z.parent.parent )
			else:
				y = z.parent.parent.left
				if y.color == Color.RED:
					z.parent.color = Color.BLACK
					y.color = Color.BLACK
					z.parent.parent.color = Color.RED
					z = z.parent.parent
				else:
					if z is z.parent.left:
						z = z.parent
						self.right_rotate( z )
					z.parent.color = Color.BLACK
					z.parent.parent.color = Color.RED
					self.left_rotate( z.parent.parent )
		self.root.color=Color.BLACK



	def rb_transplant(self, u, v):
		if u.parent is self.nil:
			self.root = v
		elif u is u.parent.left:
			u.parent.left = v
		else:
			u.parent.right = v
		v.parent = u.parent



	def rb_delete(self, z, fix_attribute_func=None ):
		""" 
		Delete a node from the tree.

		This procedure contains one variation with respect to CLRS3, 13.4: a reference can be passed to a function to be called on the lowest node affected by the change (:math:`x`).

		:param z: the node to be deleted.
		:type z: rbNode
		:param fix_attribute_func: a function that is to be called on the lowest node affected by the change, typically used in augmented trees to update an attribute on the ancestors
		:type fix_attribute_func: function
		"""
		y = z
		y_original_color = y.color
		if z.left is self.nil:
			x = z.right
			self.rb_transplant( z, z.right )
		elif z.right is self.nil:
			x = z.left
			self.rb_transplant( z, z.left )
		else:
			y = self.tree_minimum( z.right )
			y_original_color = y.color
			x = y.right
			if y.parent is z:
				x.parent = y
			else:
				self.rb_transplant( y, y.right )
				y.right = z.right
				y.right.parent = y
			self.rb_transplant( z, y)
			y.left = z.left
			y.left.parent = y
			y.color = z.color
		#print('{}'.format(x))
		if fix_attribute_func:
			fix_attribute_func( x )
		if y_original_color == Color.BLACK:
			self.rb_delete_fixup( x )



	def rb_delete_fixup(self, x ):
		""" After deleting a node, restore the Red-Black properties on the subtree affected by the change.

		:param x: the node whose ancestors should be fixed.
		:type x: rbNode
		"""
		while x is not self.root and x.color == Color.BLACK:
			if x is x.parent.left:
				w = x.parent.right
				if w.color == Color.RED:
					w.color = Color.BLACK
					x.parent.color = Color.RED
					self.left_rotate( x.parent )
					w = x.parent.right
				if w.left.color == Color.BLACK and w.right.color == Color.BLACK:
					w.color = Color.RED
					x = x.parent
				else:
					if w.right.color == Color.BLACK:
						w.left.color = Color.BLACK
						w.color = Color.RED
						self.right_rotate( w )
						w = x.parent.right
					w.color = x.parent.color
					x.parent.color = Color.BLACK
					w.right.color = Color.BLACK
					self.left_rotate(x.parent)
					x = self.root
			else:
				w = x.parent.left
				if w.color == Color.RED:
					w.color = Color.BLACK
					x.parent.color = Color.RED
					self.right_rotate( x.parent )
					w = x.parent.left
				if w.right.color == Color.BLACK and w.left.color == Color.BLACK:
					w.color = Color.RED
					x = x.parent
				else:
					if w.left.color == Color.BLACK:
						w.right.color = Color.BLACK
						w.color = Color.RED
						self.left_rotate( w )
						w = x.parent.left
					w.color = x.parent.color
					x.parent.color = Color.BLACK
					w.left.color = Color.BLACK
					self.right_rotate(x.parent)
					x = self.root
				
		x.color = Color.BLACK

	def delete_key( self, key, fix_attribute_func=None ):
		""" Remove the key from the tree, and return it.
	
		.. warning::
			 The key might not be unique; in this case, the first node that carries the key is deleted.
	
		:param key: a key value
		:type key: object
		:param fix_attribute_func: a function that is to be called on the lowest node affected by the change, typically used in augmented trees to update an attribute on the ancestors
		:type fix_attribute_func: function
		:return: the key at the deleted node, if it exists; None otherwise
		:rtype: object
		"""
		node_to_delete = self.search( key )
		if node_to_delete is None:
			return None
		value = node_to_delete.key
		self.rb_delete( node_to_delete, fix_attribute_func )
		
		return value

############# QUERY METHODS #########################

	def search(self,key):
		""" 
		Search for the node that contains the given key.

		If multiple nodes contain the same key, the first node to be visited will be returned.
		:param key: the value to be searched.
		:type key: object
		:return: the node containing the key, if it exists; None otherwise
		:rtype: bool
		"""
		def search_rec(x):
			if x is self.nil:
				return None
			if x.key == key:
				return x
			if key < x.key:
				return search_rec(x.left)
			else:
				return search_rec(x.right)

		return search_rec(self.root)


	def tree_minimum( self, node ):
		""" In the subtree rooted at the given node, retrieve the node with the minimum key.

		:param node: root of the subtree to be searched
		:type node: rbNode
		:return: the node with the minimum key, i.e. the leftmost node in the subtree
		:rtype: rbNode
		"""
		if node is not self.nil:
			while node.left is not self.nil:
				node = node.left
		return node

	def tree_maximum( self, node ):
		""" In the subtree rooted at the given node, retrieve the node with the maximum key.

		:param node: root of the subtree to be searched
		:type node: rbNode
		:return: the node with the maximum key, i.e. the rightmost node in the subtree
		:rtype: rbNode
		"""
		if node is not self.nil:
			while node.right is not self.nil:
				node = node.right
		return node

	def successor(self, node):
		""" Retrieve the successor of the given node.

		:param node: a node in the tree
		:type node: rbNode
		:return: node that contains the smallest key that is larger than the node's key
		:rtype: rbNode
		"""
		if node.right is not self.nil:
			return self.tree_minimum(node.right)
		y = node.parent
		while y is not self.nil and node is y.right:
			node = y
			y = y.parent
		if y is self.nil:
			return None
		return y

	def predecessor(self, node):
		""" Retrieve the predecessor of the given node.

		:param node: a node in the tree
		:type node: rbNode
		:return: node that contains the highest key that is smaller than the node's key
		:rtype: rbNode
		"""
		if node.left is not self.nil:
			return self.tree_maximum(node.left)
		y = node.parent
		while y is not self.nil and node is y.left:
			node = y
			y = y.parent
		if y is self.nil:
			return None
		return y
		

	def to_array( self ):
		""" Return a nested list representation of the tree.

		:return: a nested list representation of the tree, that does not include the NIL node.
		:rtype: list
		"""
		def to_array_rec( node ):
			if node is self.nil:
				return None
			if node.left is self.nil and node.right is self.nil:
				return node.key
			return ( node.key, to_array_rec( node.left ), to_array_rec( node.right ))
		return to_array_rec( self.root )


	def inorder_walk( self, func=None ):
		"""
		.. _inorder_walk:
		
		Perform a inorder tree walk, listing nodes, or node attributes along the way.

		:param func: an optional reference to a procedure that extracts information for the visited nodes
		:type func: function
		:return: a list of nodes by default (or other information returned by the function passed as an optional parameter)
		:rtype: list
		"""
		def inorder_rec( node, lst ):
			if node.left is not self.nil:
				inorder_rec( node.left, lst)
			if func is None:
				lst.append( node )
			else:	
				lst.append( func(node))
			if node.right is not self.nil:
				inorder_rec( node.right, lst)
			return lst	

		return inorder_rec( self.root, [])

	def to_binary_tree(self):
		""" Return a plain binary tree, with no sentinel nodes.

		:return: a binary tree
		:rtype: bt.BinaryTree
		"""
		return bt.BinaryTree( array=self.to_array() )

			


class RedBlackTreeUniTest( unittest.TestCase ):


	def test_create_rbTree_1( self ):
		bst = RedBlackTree()

		for key in (41,38,31,12,19,8):
			bst.rb_insert( key )
		#bst.to_binary_tree().display()	

		self.assertEqual( bst.to_array(), (38,(19, (12,8,None),31),41))
	
	def test_create_rbTree_2( self ):
		bst = RedBlackTree()

		for key in (3, 7, 10, 12, 14, 15, 16, 17,19,20, 21,23,26, 28,30,35,38,39,41,47):
			bst.rb_insert( key )
		self.assertEqual( bst.to_array(), (17, (12, (7, 3, 10), (15, 14, 16)), (23, (20, 19, 21), (35, (28, 26, 30), (39, 38, (41, None, 47))))))
	
	

	def test_create_rbTree_3( self ):
		bst = RedBlackTree()

		for key in (11,2,14,15,1,7,5,8,4):
			bst.rb_insert( key )
		bst.to_binary_tree().display()	
		self.assertEqual( bst.to_array(), (7, (2, 1, (5, 4, None)), (11, 8, (14, None, 15))))
	

	def test_delete( self ):
		bst = RedBlackTree()

		for key in (11,2,14,15,1,7,5,8,4):
			bst.rb_insert( key )
		bst.to_binary_tree().display()	

		bst.rb_delete( bst.root.left )
		bst.rb_delete( bst.root.left )
		bst.rb_delete( bst.root.left )
		bst.rb_delete( bst.root.left )
		self.assertEqual( bst.to_array(), (11, (7, None, 8), (14, None, 15)))
	
		bst.to_binary_tree().display()	

	def test_tree_minimum_1(self):
		
		bst = RedBlackTree()
		for key in (11,2,14,15,1,7,5,8,4):
			bst.rb_insert( key )
		bst.to_binary_tree().display()	

		self.assertEqual( bst.tree_minimum( bst.root ).key, 1)

	def test_tree_minimum_2(self):
		
		bst = RedBlackTree()
		bst.rb_insert( 11 )
		bst.to_binary_tree().display()	

		self.assertEqual( bst.tree_minimum( bst.root ).key, 11)

def main():
        unittest.main()

if __name__ == '__main__':
        main()


	
