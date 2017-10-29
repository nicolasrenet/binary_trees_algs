#!/usr/bin/python3

import red_black_tree as rbt
import unittest


class IntervalNode(rbt.rbNode):
	"""
	A tree node, that stores an interval.

	:ivar: interval
	:max: the maximum right boundary for all intervals in the subtree
	"""
	
	def __init__( self, interval=None):
		"""
		Create a new interval node.

		:param interval: an interval
		:type interval: Interval
		"""

		self.interval = interval

		# For NIL nodes
		if interval is None:
			super().__init__( 'n' )
			self.max = -(2**16)
		else:
			# the key is interval.low
			super().__init__( interval.low )
			self.max = interval.high


class Interval():
	""" An interval representation 
	
	:ivar low: lower boundary
	:ivar high: upper boundary
	"""

	
	def __init__(self, low, high ):
		
		self.low=low
		self.high=high
	
	def overlap(self,  interval ):
		"""
		Check if this interval overlaps with the given interval.

		:param interval: the interval we compare this interval to
		:type interval: Interval
		:return: True if the two intervals overlap; False otherwise
		:rtype: bool
		"""
		return ((interval.low <= self.high) and (self.low <= interval.high))


	def equal(self, interval):
		"""
		Check if this interval and the given interval have the same boundaries.

		:param interval: the interval we compare this interval to
		:type interval: Interval
		:return: True if the two intervals have the same boundaries; False otherwise
		:rtype: bool
		"""
		return ((self.low == interval.low) and (self.high == interval.high))
	
	def __str__(self):
		return '[{}:{}]'.format(self.low, self.high)


class IntervalTree( rbt.RedBlackTree ):

	def __init__(self):
		super().__init__()
		self.nil = IntervalNode()
		self.root = self.nil
	
	def fix_max_up( self, node ):
		"""
		Given a node that has just been inserted into the tree, update the max value on the ancestors.

		:param node: an interval node
		:type node: IntervalNode 
		"""
		#print("fix_max_up({})".format( node ))		
		while node.parent is not self.nil: 
			node.parent.max = max( node.parent.interval.high, node.parent.left.max, node.parent.right.max)
			node = node.parent

	def left_rotate(self, node ):
		"""
		.. _left_rotate:
		
		Left-rotate the subtree rooted at the given node. Update the max attribute when appropriate.

		:param node: the root the subtree to be rotated.
		:type node: IntervalNode
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
		if node.max > y.max:
			y.max = node.max
		elif node.max > node.left.max:
			node.max = max( node.interval.high, node.left.max, node.right.max)

	def right_rotate(self, node):
		"""
		.. _right_rotate:
		
		Right-rotate the subtree rooted at the given node. Update the max attribute when appropriate.

		:param node: the root the subtree to be rotated.
		:type node: IntervalNode
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
		if node.max > x.max:
			x.max = node.max
		elif node.max > node.right.max:
			node.max = max( node.interval.high, node.left.max, node.right.max)


	def insert_interval( self, intrvl):
		"""
		Insert a new interval into the tree.

		:param intrvl: the interval to be inserted
		:type intrvl: Interval
		"""
		node = IntervalNode( intrvl )
		self.insert_node( node )

	def insert_node( self, node):
		"""
		Insert a new node into the tree.

		:param node: the interval node to be inserted
		:type node: IntervalNode
		"""
		self.rb_insert_node( node, self.fix_max_up )

	def delete_interval(self, interval ):
		"""
		Delete an interval from the tree.

		Search the first interval node with matching boundaries, and remove it from the tree.

		:param intrvl: the interval to be deleted
		:type intrvl: Interval
		"""
		to_delete = self.search_interval( interval )
		if to_delete:
			self.delete_node( to_delete )
	
	
	def delete_node(self, z ):
		"""
		Delete an interval node from the tree.

		Search the given interval node, and remove it from the tree.

		:param z: the node to be deleted
		:type z: IntervalNode
		"""
		self.rb_delete( z, self.fix_max_up )
	
	
	def search_interval(self, interval):
		""" 
		Search for the given interval.

		:param interval: an interval
		:type interval: Interval
		:return: the first interval node with the same boundaries, if it exists in the tree; the NIL node otherwise.
		:rtype: IntervalNode
		"""
		x = self.root
		while x is not self.nil and not interval.equal( x.interval ):
			#print("search({} against {})".format( interval, x.interval ))
			if interval.low < x.key:
				x = x.left
			else:
				x = x.right
		return x

	def search_overlap(self, interval ):
		""" 
		Search for an interval that overlaps with the given interval.

		:param interval: an interval
		:type interval: Interval
		:return: the first interval node whose boundaries overlap with the given interval, if it exists in the tree; the NIL node otherwise.
		:rtype: IntervalNode
		"""
		x = self.root
		#print("search({})".format( interval ))
		while x is not self.nil and not interval.overlap( x.interval ):
			if x.left is not self.nil and x.left.max >= interval.low:
				x = x.left
			else:
				x = x.right
		return x


	def list(self):
		return self.inorder_walk( lambda x: '{}:{}:{}'.format(x.key, x.interval.high, x.max))
	
	def match_intervals(self, match_func=None) :
		""" Search all nodes that match a given criteria.

		:match_func: a boolean function, to be run on each visited node: it it returns True, the node is added to the result set
		:type match_func: function
		:return: a set of nodes; None if the tree does not contain any matching node
		:rtype: list
		"""
		def match( node, lst):
			if node is self.nil:
				return lst
			if node.left is not self.nil:
				match( node.left, lst )
			if match_func( node ):
				lst.append( node )
			if node.right is not self.nil:
				match(node.right, lst)
			return lst

		return match( self.root, [])




class IntervalTree_UnitTest( unittest.TestCase ):


	intervals = (	Interval(0,3), Interval(5,8), Interval(6,10), Interval(8,9), Interval( 15,23),
			Interval(16,21), Interval(17,19), Interval(19,20), Interval(25,30), Interval( 26,26))
	
			
	def test_interval_equal( self ):
		self.assertTrue( Interval(1,5).equal( Interval(1,5)))


	def test_interval_overlap_true( self ):
		self.assertTrue( Interval(1,5).overlap( Interval(0,2)))
		self.assertTrue( Interval(1,5).overlap( Interval(2,3)))
		self.assertTrue( Interval(1,5).overlap( Interval(2,6)))
		self.assertTrue( Interval(1,5).overlap( Interval(0,1)))
		self.assertTrue( Interval(1,5).overlap( Interval(5,6)))


	def test_interval_overlap_false( self ):
		self.assertFalse( Interval(1,5).overlap( Interval(0,0.5)))
		self.assertFalse( Interval(1,5).overlap( Interval(5.5,6)))
	
	def test_create_IntervalTree_1(self):
		""" Empty tree """
		it = IntervalTree()

		self.assertTrue( it.root is it.nil)

	def test_create_IntervalTree_2(self):
		""" Single-node tree """
		it = IntervalTree()
		it.insert_interval( Interval(5,8) )

		self.assertTrue( it.root.key == 5)

	def test_create_IntervalTree_3( self ):
		
		it = IntervalTree()

		for i in self.intervals:
			#print("{}: {} : {}".format(type(int_node), int_node.key, int_node.max) )
			it.insert_interval( i )
			#print(it.list())
			#it.to_bst().display()
		it.to_bst().display()
		print( it.list())


	def test_create_IntervalTree_4( self ):
		
		it = IntervalTree()

		for i in ( Interval(16,21), Interval(8,9), Interval(25,30), Interval(5,8),  Interval( 15,23), Interval(17,19), Interval( 26,26), Interval(0,3), Interval(6,10), Interval(19,20)):
			#print("{}: {} : {}".format(type(int_node), int_node.key, int_node.max) )
			it.insert_interval( i )
			#print(it.list())
			#it.to_bst().display()
		it.to_bst().display()
		print(it.list())


	def test_search_overlap_1( self ):
		""" Search overlapping interval: successful search """
		it = IntervalTree()

		for i in self.intervals:
			it.insert_interval( i )
		found = it.search_overlap( Interval(22,25))
		print("Found: Interval({},{})".format(found.interval.low, found.interval.high))
		self.assertTrue(  found.interval.equal( Interval(15,23)))

	def test_search_overlap_2( self ):
		""" Search overlapping interval: unsuccessful search """
		it = IntervalTree()

		for i in self.intervals:
			it.insert_interval( i )
		found = it.search_overlap( Interval(34,40))
		self.assertEqual(  found, it.nil )

	def test_search_overlap_3(self):
		""" Search an empty tree """
		it = IntervalTree()

		found = it.search_overlap( Interval(7,9))
		self.assertEqual( found, it.nil)


	def test_search_interval_1( self ):
		""" Search exact interval: successful search """
		
		it = IntervalTree()

		for i in self.intervals:
			it.insert_interval( i )
		it.to_bst().display()
		found = it.search_interval( Interval(17,19))
		print("Found: Interval({},{})".format(found.interval.low, found.interval.high))
		self.assertTrue(  found.interval.equal( Interval(17,19)))


	def test_search_interval_2( self ):
		""" Search exact interval: unsuccessful search """
		
		it = IntervalTree()

		for i in self.intervals:
			it.insert_interval( i )
		found = it.search_interval( Interval(17,20))
		print("found: {}".format( found ))
		self.assertEqual(  found, it.nil )


	def test_search_interval_3(self):
		""" Search an empty tree """
		it = IntervalTree()

		found = it.search_interval( Interval(7,9))
		self.assertEqual( found, it.nil)

	
	def test_delete_interval_1( self ):
		""" Delete interval"""
		it = IntervalTree()

		for i in self.intervals:
			it.insert_interval( i )
		it.to_bst().display()
		it.delete_interval( Interval(17,19 ))
		it.to_bst().display()
		print(it.list())
		self.assertEqual( it.list(), ['0:3:3', '5:8:10', '6:10:10', '8:9:30', '15:23:23', '16:21:30', '19:20:20', '25:30:30', '26:26:26'])

	def test_delete_interval_2( self ):
		""" Delete interval"""
		it = IntervalTree()

		for i in self.intervals:
			it.insert_interval( i )
		it.to_bst().display()
		it.delete_interval( Interval(8,9 ))
		it.to_bst().display()
		self.assertEqual( it.list(), ['0:3:3', '5:8:10', '6:10:10', '15:23:30', '16:21:21', '17:19:19', '19:20:30', '25:30:30', '26:26:26'])
		print(it.list())

	def test_match_intervals( self ):
		""" Retrieve all nodes matching a given criteria """
		
		it = IntervalTree()

		for i in self.intervals:
			it.insert_interval( i )
		it.to_bst().display()

		
		self.assertEqual( len(it.match_intervals( lambda x: x.interval.high < 15 )), 4)

	
	def test_match_intervals( self ):
		""" Retrieve all nodes matching a given criteria: empty tree """
		
		it = IntervalTree()

		self.assertEqual( len(it.match_intervals( lambda x: x.interval.high < 15 )), 0)

	

def main():
        unittest.main()

if __name__ == '__main__':
        main()
