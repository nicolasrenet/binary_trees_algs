#!/usr/bin/python3

import interval_tree as it
import red_black_tree as rb
import unittest

INFTY = 2**14

class YNode( it.IntervalNode ):
	""" 
	Store a rectangle's Y-interval, with the L y-coordinate as a key.

	:ivar rect: the rectangle, i.e. 4 coordinates
	"""
	
	def __init__( self, rect ):

		y1, y2 = rect[1], rect[3]
		super().__init__( it.Interval( y1, y2))

		self.rect = rect

class XNode( rb.rbNode ):
	"""
	Store a rectangle's X coordinate.

	:ivar start: set to True if this is a L x-coordinate; False otherwise
	:ivar rect: the rectangle, i.e. a 4-tuple of coordinates
	:ivar interval: the corresponding Y-interval
	"""
	
	def __init__( self, rect, high_x = False ):
		"""
		Create a node for an x-coordinate.

		:param rect: the rectangle coordinates (x1, y1, x2, y2)
		:type rect: tuple
		:param high_x: if True, use R x-coordinate as a key; use L-x coordinate otherwise
		:type high_x: bool
		"""
		x1, y1, x2, y2 = rect
			
		key = x2 if high_x else x1
		super().__init__( key )

		self.start = False if high_x else True

		self.interval = it.Interval(y1, y2)
		self.rect = rect

	def __str__( self ):
		return '{}:{}'.format(self.key, '[' if self.start else ']')
		
	@staticmethod
	def sentinel():
		""" 
		Create a sentinel node.

		:return: a sentinel node, from a rectangle of infinite size
		:rtype: XNode
		"""
		return XNode( (INFTY, INFTY, INFTY, INFTY ))


def build_endpoints_schedule( rectangles ):
	"""
	Build a sorted list of L and R x-coordinates for all rectangles. 

	:param rectangles: a list of 4-tuples of coordinates
	:type rectangles: list
	:return: a list of XNode objects
	:rtype: list
	"""
	low_x_tree = rb.RedBlackTree()
	for rect in rectangles:
		low_x_tree.rb_insert_node( XNode( rect ))
	left_endpoints = low_x_tree.inorder_walk() + [ XNode.sentinel() ] 

	#print([ '{}'.format(pt) for pt in left_endpoints], "Size: ", len(left_endpoints))


	high_x_tree = rb.RedBlackTree()
	for rect in rectangles:
		high_x_tree.rb_insert_node( XNode( rect, high_x=True ))
	right_endpoints = high_x_tree.inorder_walk() + [ XNode.sentinel() ]

	#print([ '{}'.format(pt) for pt in right_endpoints], len(right_endpoints))
	
	# Merge the two sets of points
	pos_l, pos_r = 0, 0

	schedule = [None] * (len(rectangles)*2)
	for i in range(0, len(schedule)):
		# L endpoints comes first
		if left_endpoints[ pos_l ].key <= right_endpoints[ pos_r ].key:
			schedule[i] = left_endpoints[ pos_l ]
			pos_l += 1
		else:
			schedule[i] = right_endpoints[ pos_r ]
			pos_r += 1
		#print('{}'.format([ ('{}'.format(pt) if not None else '') for pt in schedule ]))

	return schedule
			
		
def has_overlap( rectangles ):
	""" 
	Test whether a set of rectangles contain at least 2 overlapping elements.

	:param rectangles: a list of 4-tuples of coordinates
	:type rectangles: list
	:return: True if the set contains at least 2 overlapping elements; False otherwise
	:rtype: bool
	"""
	schedule = build_endpoints_schedule( rectangles )

	# Store the Y-intervals
	y_tree = it.IntervalTree()

	for pt in schedule:
		if pt.start:
			found = y_tree.search_overlap( pt.interval )
			if found is not y_tree.nil:
				return True
			y_tree.insert_node( YNode( pt.rect ))
		else:
			y_tree.delete_interval( pt.interval )
	
	return False

		

class VLSI_UniTest( unittest.TestCase ):

	def setUp( self ):

		# non-overlapping rectangles
		self.rectangles = [ 
			(1,15,1.5,16), # 0
			(1,2,10,7),     
			(2,8,4,14),     
			(5,8,13,9),    
			(5,10,7,13),
			(5,13.5,13,15), # 5
			(10,10,21,12),
			(11,2,12,3),
			(12,4,14,7),
			(14,8,19,9),
			(14,13,18.5,18), # 10
			(16.5,6,18.5,7.5),
			(20,3.5,21,9),
			(20,18,27,19),
			(22,1,25,17),
			(26,2,27,3),
			]

	def test_non_overlapping( self ):
		print("Non overlapping rectangles")
		
		self.assertFalse( has_overlap( self.rectangles ) )

	
	def test_overlapping_1( self ):
		print("Test 1")

		overlapping_rectangles_1 = self.rectangles[:]
		overlapping_rectangles_1[11] = (17.5, 7, 19.5, 8.5 )

		self.assertTrue( has_overlap( overlapping_rectangles_1 ))
			
	
	def test_overlapping_2( self ):
		print("Test 2")
		overlapping_rectangles_2 = self.rectangles[:]
		overlapping_rectangles_2[5] = (7,13.5,15,15)

		self.assertTrue( has_overlap( overlapping_rectangles_2 ))

	def test_overlapping_3( self ):
		print("Test 3")
		overlapping_rectangles_3 = self.rectangles[:]
		overlapping_rectangles_3[10] = (14,11,18.5,16)

		self.assertTrue( has_overlap( overlapping_rectangles_3 ))


	def test_overlapping_4( self ):
		print("Test 4")
		overlapping_rectangles_4 = self.rectangles[:]
		overlapping_rectangles_4[5] = (5,15.5,13,17)
		overlapping_rectangles_4[13] = (4.5,13.5,21,19)

		self.assertTrue( has_overlap( overlapping_rectangles_4 ))

	
	def test_overlapping_5( self ):
		""" Rectangles touch, but do not overlap """
		print("Touching rectangles")
		overlapping_rectangles_5 = self.rectangles[:]
		overlapping_rectangles_5[11] = (18, 6.5, 20, 8 )

		self.assertTrue( has_overlap( overlapping_rectangles_5 ))
			


def main():
        unittest.main()

if __name__ == '__main__':
        main()


	
