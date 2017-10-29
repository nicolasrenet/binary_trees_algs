#!/usr/bin/python3

import interval_tree as it
import red_black_tree as rb
import unittest



class RectYNode( it.IntervalNode ):
	
	def __init__( self, rect ):

		x1, y1, x2, y2 = rect
		super().__init__( it.Interval( y1, y2))
		self.max_x = x2

		self.rect = rect

class RectXNode( rb.rbNode ):
	
	def __init__( self, rect, high_x = False ):
		"""
		Create a node for an x-coordinate.

		:param rect: the rectangle coordinates (x1, y1, x2, y2)
		:type rect: tuple
		:param high_x: if True, use R-x coordinate as a key; use L-x coordinate otherwise
		:type high_x: bool
		"""
		x1, y1, x2, y2 = rect

		key = rect[2] if high_x else rect[0]

		super().__init__( key )
		self.interval = it.Interval(y1, y2)
		self.rect = rect
		


def rec_overlap( rect1, rect2 ):
	""" Test whether 2 rectangles overlap """
	rect_1_x_interval = it.Interval( rect1[0], rect1[2])
	rect_1_y_interval = it.Interval( rect1[1], rect1[3])
	rect_2_x_interval = it.Interval( rect2[0], rect2[2])
	rect_2_y_interval = it.Interval( rect2[1], rect2[3])

	if rect_1_x_interval.overlap( rect_2_x_interval ) and  rect_1_y_interval.overlap( rect_2_y_interval ):
		return True
	return False


def has_overlap_naive( rect_set ):
	""" This procedure has O(n^2) cost in the worst case, when all x-intervals share the same R-boundary."""

	y_tree = it.IntervalTree()

	# swipe the rectangle set by order of L-x coordinate
	for rect in rect_set: 
		# check the y-interval tree for all intervals whose R-x coordinate is lower than rect's
		# (assuming that this coordinate is stored on the node)
		for node in y_tree.match_intervals( lambda z: z.max_x < rect[0] ):
			print("Remove rectangle {}".format( node.rect ))
			# and remove them from the y-interval tree
			y_tree.delete_node( node )

		# if rect overlaps with an existing interval in the y-interval tree, return True
		rect_node = RectYNode( rect )
		found = y_tree.search_overlap( rect_node.interval )
		if found is not y_tree.nil:
			return True
		# otherwise insert the rectangle in the y-interval tree
		else:
			y_tree.insert_node( rect_node )
			print("Insert rectangle {}".format( rect ))
	return False

def has_overlap( rect_set ):
	""" A more sophisticated procedure:
		* ensure that the rectangles are sorted by order of increasing L-x coordinate at the start
		* use a second BST to keep track of the rectangles that can be deleted before an insertion 
	"""


	# Store the Y-intervals
	y_tree = it.IntervalTree()

	# Store the Y-intervals, but uses the R-x coordinate as a key
	x_tree = rb.RedBlackTree()


	# Sort the rectangles, using the L-x coordinate as a key, using a BST
	sorted_rects = rb.RedBlackTree()
	for rect in rect_set:
		sorted_rects.rb_insert_node( RectXNode( rect ))
		
	# swipe the rectangle set by order of L-x coordinate
	for intrvl_node in sorted_rects.inorder_walk():
		rect = intrvl_node.rect
		# check the x-interval tree for all intervals whose R-x coordinate is lower than rect's
		# and remove them from the x-interval tree
		minimum = x_tree.tree_minimum( x_tree.root )
		while minimum is not x_tree.nil and minimum.key  < rect[0]:
			#print("Minimum: {}".format(minimum.key))
			#print("Delete {} from x-tree".format( minimum.rect ))
			x_tree.rb_delete( minimum )
			y_tree.delete_interval( minimum.interval )
			minimum = x_tree.tree_minimum(x_tree.root)

		# if rect overlaps with an existing interval in the y-interval tree, return True
		rect_y_node = RectYNode( rect )
		found = y_tree.search_overlap( rect_y_node.interval )
		if found is not y_tree.nil:
			return True
		# otherwise insert the rectangle in both trees
		else:
			y_tree.insert_node( rect_y_node )
			#print("Insert rectangle {} in Y-tree".format( rect ))
			x_tree.rb_insert_node( RectXNode( rect, high_x=True ) )
			#print("Insert rectangle {} in X-tree".format( rect ))
		x_tree.to_bst().display()
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
		print("Test 0")
		
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


	
