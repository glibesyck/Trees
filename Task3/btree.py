"""
Module for implementing LinkedBinaryTree.
"""


class LinkedBinaryTree:
    """
    Class representing linked binary tree.
    """

    def __init__(self, value: list):
        """
        Initialize a node for linked binary tree (we implement a node and a tree here).
        """
        self.data = value
        self.right = None
        self.left = None

    def insert_left(self, left_node: list):
        """
        Inserting left child.
        """
        self.left = LinkedBinaryTree(left_node)

    def insert_right(self, right_node: list):
        """
        Inserting right child.
        """
        self.right = LinkedBinaryTree(right_node)

    def get_left(self):
        """
        Return left child.
        """
        return self.left

    def get_right(self):
        """
        Return right child.
        """
        return self.right
