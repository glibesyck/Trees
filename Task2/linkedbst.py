"""
File: linkedbst.py
Author: Ken Lambert
"""

from abstractcollection import AbstractCollection
from bstnode import BSTNode
from linkedstack import LinkedStack
from linkedqueue import LinkedQueue
from math import log
import time
from random import sample, choice


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
            info = ""
            if node != None:
                info += recurse(node.right, level + 1)
                info += "| " * level
                info += str(node.data) + "\n"
                info += recurse(node.left, level + 1)
            return info

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
            if node != None:
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
        lyst = list()
        queue = LinkedQueue()

        def recurse():
            if not queue.isEmpty():
                node = queue.pop()
                lyst.append(node.data)
                if node.left is not None:
                    queue.add(node.left)
                if node.right is not None:
                    queue.add(node.right)
                recurse()

        if self._root is not None:
            queue.add(self._root)
        recurse()
        return iter(lyst)

    def __contains__(self, item):
        """Returns True if target is found or False otherwise."""
        return self.find(item) != None

    def find(self, item):
        """If item matches an item in self, returns the
        matched item, or None otherwise.
        !!! Usage of different method (without recursion)."""

        probe = self._root
        while probe is not None:
            if probe.data < item:
                probe = probe.right
            elif probe.data > item:
                probe = probe.left
            else:
                return probe.data
        return None

    # Mutator methods
    def clear(self):
        """Makes self become empty."""
        self._root = None
        self._size = 0

    def add(self, item):
        """Adds item to the tree.
        Important!!! It is not the same as in the first realization as 
        there are troubles with recursion."""
        if self.isEmpty():
            self._root = BSTNode(item)
        else:
            probe = self._root
            while probe is not None:
                add_probe = probe
                if item < probe.data:
                    probe = probe.left
                else:
                    probe = probe.right
            if add_probe.data < item:
                add_probe.right = BSTNode(item)
            else:
                add_probe.left = BSTNode(item)
        self._size += 1

    def remove(self, item):
        """Precondition: item is in self.
        Raises: KeyError if item is not in self.
        postcondition: item is removed from self."""
        if not item in self:
            raise KeyError("Item not in tree.""")

        # Helper function to adjust placement of an item
        def lift_max_in_left_subtree_to_top(top):
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
        if self.isEmpty(): return None

        # Attempt to locate the node containing the item
        item_removed = None
        pre_root = BSTNode(None)
        pre_root.left = self._root
        parent = pre_root
        direction = 'L'
        current_node = self._root
        while not current_node == None:
            if current_node.data == item:
                item_removed = current_node.data
                break
            parent = current_node
            if current_node.data > item:
                direction = 'L'
                current_node = current_node.left
            else:
                direction = 'R'
                current_node = current_node.right

        # Return None if the item is absent
        if item_removed == None: return None

        # The item is present, so remove its node

        # Case 1: The node has a left and a right child
        #         Replace the node's value with the maximum value in the
        #         left subtree
        #         Delete the maximium node in the left subtree
        if not current_node.left == None \
                and not current_node.right == None:
            lift_max_in_left_subtree_to_top(current_node)
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
        return item_removed

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
        Return the height of tree.
        :return: int
        '''

        def height1(top):
            '''
            Helper function
            :param top: BSTNode
            :return: int
            '''
            if top is None:
                return -1 #top is None means we made step from leaf into nowhere
            else:
                return 1 + max(height1(top.left), height1(top.right))

        return height1(self._root)

    def is_balanced(self):
        '''
        Return True if tree is balanced.
        :return: bool
        '''
        return self.height() < 2*log(self._size + 1, 2) - 1

    def range_find(self, low, high):
        '''
        Returns a list of the items in the tree, where low <= item <= high."""
        :param low:
        :param high:
        :return:
        '''
        list_of_values = []
        sorted_list = list(self.inorder())
        for value in sorted_list:
            if low <= value <= high:
                list_of_values.append(value)
        return list_of_values

    def rebalance(self):
        '''
        Rebalances the tree.
        :return: self
        '''
        sorted_list = list(self.inorder())
        self.clear()

        def recurse(tree, list_of_items: list):
            """
            Add elements to tree so it become balanced.
            """
            if not list_of_items:
                return None
            middle = len(list_of_items) // 2
            node = list_of_items[middle]
            tree.add(node)
            recurse(tree, list_of_items[:middle])
            recurse(tree, list_of_items[middle+1:])
            return tree

        self = recurse(self, sorted_list)
        return self

    def successor(self, item):
        """
        Returns the smallest item that is larger than
        item, or None if there is no such item.
        :param item:
        :type item:
        :return:
        :rtype:
        """
        sorted_list = list(self.inorder())
        for value in sorted_list:
            if value > item:
                return value
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
        sorted_list = list(self.inorder())
        for value in reversed(sorted_list):
            if value < item:
                return value
        return None

    def demo_bst(self, path):
        """
        Demonstration of efficiency binary search tree for the search tasks.
        :param path:
        :type path: str
        :return:
        :rtype:
        """
        list_of_words = []
        with open(path, 'r') as dictionary:
            for line in dictionary:
                line = line.strip()
                list_of_words.append(line)
        random_words = sample(list_of_words, 10000)
        print(f"The first way of searching takes {self.first_way(list_of_words, random_words)} seconds.")
        print(f"The second way of searching takes {self.second_way(list_of_words, random_words)} seconds.")
        print(f"The third way of searching takes {self.third_way(list_of_words, random_words)} seconds.")
        print(f"The fourth way of searching takes {self.fourth_way(list_of_words, random_words)} seconds.")

    @staticmethod
    def first_way(full_list: list, find_list: list):
        """
        Search for 10000 random words in list of words which are placed by alphabet.
        """
        now = time.time()
        for word in find_list:
            for _, value in enumerate(full_list): 
                #when we search we are looking for index but here we don't use it
                if word == value:
                    break
        return time.time() - now

    @staticmethod
    def second_way(full_list: list, find_list: list):
        """
        Search for 10000 random words in BSTree where elements were added by alphabet.
        """
        tree = LinkedBST()
        for word in full_list:
            tree.add(word)
        now = time.time()
        for word in find_list:
            tree.find(word)
        return time.time() - now

    @staticmethod
    def third_way(full_list: list, find_list: list):
        """
        Search for 10000 random words in BSTree where elements were added in random way.
        """
        tree = LinkedBST()
        while full_list:
            random_el = choice(full_list)
            tree.add(random_el)
            full_list.remove(random_el)
        now = time.time()
        for word in find_list:
            tree.find(word)
        return time.time() - now

    @staticmethod
    def fourth_way(full_list: list, find_list: list):
        """
        Search for 10000 random words in BSTree which is balanced.
        """
        tree = LinkedBST()
        for word in full_list:
            tree.add(word)
        tree.rebalance()
        now = time.time()
        for word in find_list:
            tree.find(word)
        return time.time() - now

