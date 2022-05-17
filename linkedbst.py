"""
File: linkedbst.py
Author: Ken Lambert
"""
import math
import random
import time
import sys

from abstractcollection import AbstractCollection
from bstnode import BSTNode
from linkedstack import LinkedStack
sys.setrecursionlimit(300000)

class LinkedBST(AbstractCollection):
    """An link-based binary search tree implementation."""

    def __init__(self, sourceCollection=None):
        """Sets the initial state of self, which includes the
        contents of sourceCollection, if it's present."""
        self._root = None
        AbstractCollection.__init__(self, sourceCollection)

    # Accessor methods
    def __str__(self):
        """Returns a string representation with the tree rotated
        90 degrees counterclockwise."""

        def recurse(node, level):
            string = ""
            if node != None:
                string += recurse(node.right, level + 1)
                string += "| " * level
                string += str(node.data) + "\n"
                string += recurse(node.left, level + 1)
            return string

        return recurse(self._root, 0)

    def __iter__(self):
        """Supports a preorder traversal on a view of self."""
        if not self.isEmpty():
            stack = LinkedStack()
            stack.push(self._root)
            while not stack.isEmpty():
                node = stack.pop()
                yield node.data
                if node.right != None:
                    stack.push(node.right)
                if node.left != None:
                    stack.push(node.left)

    def preorder(self):
        """Supports a preorder traversal on a view of self."""
        lyst = list()

        def recurse(node):
            if node is not None:
                lyst.append(node.data)
                recurse(node.left)
                recurse(node.right)

        recurse(self._root)
        return iter(lyst)

    def inorder(self):
        """Supports an inorder traversal on a view of self."""
        lyst = list()

        def recurse(node):
            if node != None:
                recurse(node.left)
                lyst.append(node.data)
                recurse(node.right)

        recurse(self._root)
        return iter(lyst)

    def postorder(self):
        """Supports a postorder traversal on a view of self."""
        lyst = list()

        def recurse(node):
            if node != None:
                recurse(node.left)
                recurse(node.right)
                lyst.append(node.data)

        recurse(self._root)
        return iter(lyst)

    def levelorder(self):
        """Supports a levelorder traversal on a view of self."""
        return None

    def __contains__(self, item):
        """Returns True if target is found or False otherwise."""
        return self.find(item) != None

    def find(self, item):
        """If item matches an item in self, returns the
        matched item, or None otherwise."""

        def recurse(node):
            if node is None:
                return None
            elif item == node.data:
                return node.data
            elif item < node.data:
                return recurse(node.left)
            else:
                return recurse(node.right)

        return recurse(self._root)

    # Mutator methods
    def clear(self):
        """Makes self become empty."""
        self._root = None
        self._size = 0

    def add(self, item):
        """Adds item to the tree."""

        # Helper function to search for item's position
        def recurse(node):
            # New item is less, go left until spot is found
            if item < node.data:
                if node.left == None:
                    node.left = BSTNode(item)
                else:
                    recurse(node.left)
            # New item is greater or equal,
            # go right until spot is found
            elif node.right == None:
                node.right = BSTNode(item)
            else:
                recurse(node.right)
                # End of recurse

        # Tree is empty, so new item goes at the root
        if self.isEmpty():
            self._root = BSTNode(item)
        # Otherwise, search for the item's spot
        else:
            recurse(self._root)
        self._size += 1

    def remove(self, item):
        """Precondition: item is in self.
        Raises: KeyError if item is not in self.
        postcondition: item is removed from self."""
        if not item in self:
            raise KeyError("Item not in tree.""")

        # Helper function to adjust placement of an item
        def max_in_left(top):
            # Replace top's datum with the maximum datum in the left subtree
            # Pre:  top has a left child
            # Post: the maximum node in top's left subtree
            #       has been removed
            # Post: top.data = maximum value in top's left subtree
            parent = top
            current_node = top.left
            while not current_node.right == None:
                parent = current_node
                current_node = current_node.right
            top.data = current_node.data
            if parent == top:
                top.left = current_node.left
            else:
                parent.right = current_node.left

        # Begin main part of the method
        if self.isEmpty():
            return None

        # Attempt to locate the node containing the item
        removed_item = None
        pre_root = BSTNode(None)
        pre_root.left = self._root
        parent = pre_root
        direction = 'L'
        current_node = self._root
        while not current_node == None:
            if current_node.data == item:
                removed_item = current_node.data
                break
            parent = current_node
            if current_node.data > item:
                direction = 'L'
                current_node = current_node.left
            else:
                direction = 'R'
                current_node = current_node.right

        # Return None if the item is absent
        if removed_item == None: return None

        # The item is present, so remove its node

        # Case 1: The node has a left and a right child
        #         Replace the node's value with the maximum value in the
        #         left subtree
        #         Delete the maximium node in the left subtree
        if not current_node.left == None \
                and not current_node.right == None:
            max_in_left(current_node)
        else:

            # Case 2: The node has no left child
            if current_node.left == None:
                new_child = current_node.right

                # Case 3: The node has no right child
            else:
                new_child = current_node.left

                # Case 2 & 3: Tie the parent to the new child
            if direction == 'L':
                parent.left = new_child
            else:
                parent.right = new_child

        # All cases: Reset the root (if it hasn't changed no harm done)
        #            Decrement the collection's size counter
        #            Return the item
        self._size -= 1
        if self.isEmpty():
            self._root = None
        else:
            self._root = pre_root.left
        return removed_item

    def replace(self, item, new_item):
        """
        If item is in self, replaces it with newItem and
        returns the old item, or returns None otherwise."""
        probe = self._root
        while probe != None:
            if probe.data == item:
                old_data = probe.data
                probe.data = new_item
                return old_data
            elif probe.data > item:
                probe = probe.left
            else:
                probe = probe.right
        return None

    def height(self):
        '''
        Return the height of tree
        :return: int
        '''

        def height1(top):
            '''
            Helper function
            :param top:
            :return:
            '''
            if top is None:
                return -1
            left_or_right = max(height1(top.left), height1(top.right))
            return left_or_right + 1
        return height1(self._root)

    def is_balanced(self):
        '''
        Return True if tree is balanced
        :return:
        '''
        amount = len(list(self.inorder()))
        height = self.height()
        return height < 2 * math.log2(amount + 1) - 1

    def range_find(self, low, high):
        """
        Returns a list of the items in the tree, where low <= item <= high.
        :param low:
        :param high:
        :return:
        """
        result = []
        for i in self.inorder():
            if low <= i and i <= high:
                result.append(i)
        return result

    def rebalance(self):
        """Rebalances the tree.
        :return:"""

        elements = list(self.inorder())

        def recurse(lyst):
            if len(lyst) == 0:
                return
            elif len(lyst) == 1:
                middle = BSTNode(lyst[0])
                return middle
            elif len(lyst) == 2:
                middle = BSTNode(lyst[1])
                middle.left = BSTNode(lyst[0])
            else:
                middle = BSTNode(lyst[len(lyst)//2])
                middle.left = recurse(lyst[:len(lyst)//2])
                middle.right = recurse(lyst[(len(lyst)//2 + 1):])
            return middle

        self._root = recurse(elements)

    def successor(self, item):
        """
        Returns the smallest item that is larger than
        item, or None if there is no such item.
        :param item:
        :type item:
        :return:
        :rtype:
        """
        for i in self.inorder():
            if i > item:
                return i
        return None

    def predecessor(self, item):
        """
        Returns the largest item that is smaller than
        item, or None if there is no such item.
        :param item:
        :type item:
        :return:
        :rtype:
        """
        elements = list(self.inorder())[::-1]
        i = 0
        while i <= len(elements) - 1:
            if elements[i] < item:
                return elements[i]
            i += 1
        return None

    def demo_bst(self, path):
        """
        Demonstration of efficiency binary search tree for the search tasks.
        :param path:
        :type path:
        :return:
        :rtype:
        """
        AMOUNT = 10000

        with open(path) as file:
            elements = list(file)

        word_amount = len(elements)
        search_word = [elements[random.randint(0, word_amount)] for i in range(AMOUNT)]

        # list part
        list_time = 0.0
        for i in range(AMOUNT):
            cur_element = search_word[i]
            start = time.time()
            if cur_element in elements:
                pass
            list_time += time.time() - start
        print('Time in list is:', list_time)

        # binary tree part
        binary_tree = LinkedBST()
        for i in elements:
            binary_tree.add(i)

        binary_tree_time = 0.0
        for pos in search_word:
            start = time.time()
            print(binary_tree.find(pos))
            binary_tree_time += time.time() - start
        print('Time in binary search tree is:', binary_tree_time)

        # random binary tree
        random_binary_tree = LinkedBST()
        for i in range(word_amount):
            current_element = elements.pop(random.randint(0, len(elements)-1))
            random_binary_tree.add(current_element)

        random_binary_tree_time = 0.0
        for pos in search_word:
            start = time.time()
            random_binary_tree.find(pos)
            random_binary_tree_time += time.time() - start
        print('Time in random binary search tree is:', random_binary_tree_time)

        # rebalance tree
        binary_tree.rebalance()
        rebalance_binary_tree_time = 0.0
        for pos in search_word:
            start = time.time()
            binary_tree.find(pos)
            rebalance_binary_tree_time += time.time() - start
        print('Time in rebalance  tree is:', rebalance_binary_tree_time)
