"""
File: linkedbst.py
Author: Ken Lambert
"""
from __future__ import annotations
from ctypes import sizeof
from time import time
from pprint import pprint
import re
from abstractcollection import AbstractCollection
from bstnode import BSTNode
from linkedstack import LinkedStack
from linkedqueue import LinkedQueue
from math import log
import itertools
import random
import sys
import os, psutil


process = psutil.Process(os.getpid())

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
            s = ""
            if node != None:
                s += recurse(node.right, level + 1)
                s += "| " * level
                s += str(node.data) + "\n"
                s += recurse(node.left, level + 1)
            return s

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
        return None

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
        return None

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


    # End of recurse
        if self.isEmpty():
            self._root = BSTNode(item)
        # Otherwise, search for the item's spot
        else:
            node_q = set()
            node_old = self._root
            while node_old:
                node = node_old
                if item < node.data:
                    if node.left == None:
                        node.left = BSTNode(item)
                        node_old = None
                    else:
                        node_old = node.left
                # New item is greater or equal,
                # go right until spot is found
                elif node.right == None:
                    node.right = BSTNode(item)
                    node_old = None

                else:
                    node_old = node.right

        self._size += 1
        

    def remove(self, item):
        """Precondition: item is in self.
        Raises: KeyError if item is not in self.
        postcondition: item is removed from self."""
        if not item in self:
            raise KeyError("Item not in tree.""")

        # Helper function to adjust placement of an item
        def liftMaxInLeftSubtreeToTop(top):
            # Replace top's datum with the maximum datum in the left subtree
            # Pre:  top has a left child
            # Post: the maximum node in top's left subtree
            #       has been removed
            # Post: top.data = maximum value in top's left subtree
            parent = top
            currentNode = top.left
            while not currentNode.right == None:
                parent = currentNode
                currentNode = currentNode.right
            top.data = currentNode.data
            if parent == top:
                top.left = currentNode.left
            else:
                parent.right = currentNode.left

        # Begin main part of the method
        if self.isEmpty(): return None

        # Attempt to locate the node containing the item
        itemRemoved = None
        preRoot = BSTNode(None)
        preRoot.left = self._root
        parent = preRoot
        direction = 'L'
        currentNode = self._root
        while not currentNode == None:
            if currentNode.data == item:
                itemRemoved = currentNode.data
                break
            parent = currentNode
            if currentNode.data > item:
                direction = 'L'
                currentNode = currentNode.left
            else:
                direction = 'R'
                currentNode = currentNode.right

        # Return None if the item is absent
        if itemRemoved == None: return None

        # The item is present, so remove its node

        # Case 1: The node has a left and a right child
        #         Replace the node's value with the maximum value in the
        #         left subtree
        #         Delete the maximium node in the left subtree
        if not currentNode.left == None \
                and not currentNode.right == None:
            liftMaxInLeftSubtreeToTop(currentNode)
        else:

            # Case 2: The node has no left child
            if currentNode.left == None:
                newChild = currentNode.right

                # Case 3: The node has no right child
            else:
                newChild = currentNode.left

                # Case 2 & 3: Tie the parent to the new child
            if direction == 'L':
                parent.left = newChild
            else:
                parent.right = newChild

        # All cases: Reset the root (if it hasn't changed no harm done)
        #            Decrement the collection's size counter
        #            Return the item
        self._size -= 1
        if self.isEmpty():
            self._root = None
        else:
            self._root = preRoot.left
        return itemRemoved

    def replace(self, item, newItem):
        """
        If item is in self, replaces it with newItem and
        returns the old item, or returns None otherwise."""
        probe = self._root
        while probe != None:
            if probe.data == item:
                oldData = probe.data
                probe.data = newItem
                return oldData
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


        # Base Case
        if self._root is None:
            return 0
        
        # Create a empty queue for level order traversal
        q = []
        
        # Enqueue Root and Initialize Height
        q.append(self._root)
        height = 0
    
        while(True):
            
            # nodeCount(queue size) indicates number of nodes
            # at current level
            nodeCount = len(q)
            if nodeCount == 0 :
                return height
        
            height += 1
    
            # Dequeue all nodes of current level and Enqueue
            # all nodes of next level
            while(nodeCount > 0):
                node = q[0]
                q.pop(0)
                if node.left is not None:
                    q.append(node.left)
                if node.right is not None:
                    q.append(node.right)
    
                nodeCount -= 1

    def is_balanced(self):
        '''
        Return True if tree is balanced
        :return:
        '''
        n = self._size
        return 2 * log(n + 1, 2) - 1 > self.height()

    def rangeFind(self, low, high):
        '''
        Returns a list of the items in the tree, where low <= item <= high."""
        :param low:
        :param high:
        :return:
        '''
        high = self._root.left
        low = self._root.right


    def into_list(self):
        return [i for i in self.inorder()]
    def rebalance(self):
        '''
        Rebalances the tree.
        :return:
        '''
        def bin_search(llist):
            lists = []
            lists.append(llist)
            for lst in lists:
                mid = len(lst)//2

                if len(lst) == 1:

                    self.add(lst[0])
                elif not lst:
                    pass
                else:
                    left = lst[:mid]
                    right = lst[mid+1:]
                    lists.append(left)
                    lists.append(right)

                    self.add(lst[mid])
            del lists
            

        llist = self.into_list()
        self.clear()
        bin_search(llist)




    def successor(self, item):
        """
        Returns the smallest item that is larger than
        item, or None if there is no such item.
        :param item:
        :type item:
        :return:
        :rtype:
        """
        vals = []
        def bin_search(llist):
            mid = (int(round(len(llist)/2, 0)))
            if len(llist) == 1:
                if llist[0] > item:
                    vals.append(llist[0])
                return llist[0]
            elif len(llist) == 0:
                return None
            else:
                left = llist[:mid]
                right = llist[mid+1:]
                if llist[mid] > item:
                    vals.append(llist[mid])
                return bin_search(left), bin_search(right)
        self._root.left, self._root.right
        llist = self.into_list()
        bin_search(llist)

        try:
            return min(vals)
        except ValueError:
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
        vals = []
        
        def bin_search(llist):
            mid = (int(round(len(llist)/2, 0)))
            if len(llist) == 1:

                if llist[0] < item:
                    vals.append(llist[0])
                return llist[0]
            elif len(llist) == 0:
                return None
            else:
                left = llist[:mid]
                right = llist[mid+1:]

                if llist[mid] < item:
                    vals.append(llist[mid])
                return bin_search(left), bin_search(right)
        self._root.left, self._root.right
        llist = self.into_list()
        bin_search(llist)

        try:
            return max(vals)
        except ValueError:
            return None

    def path_into_dict(self, path) -> dict[str, list[str]]:
        """
        reads dictionary as dict
        """
        dct = {}
        with open(path,"r") as file:
            
            data = file.readline()[:-1]
            while data:
                if re.search(r"[A-Z]$", data):
                    key = data
                    dct[key] = []
                else:
                    dct[key].append(data)
                data = file.readline()[:-1]
        return dct
    def dict_into_list(self, dct) -> list[str]:
        """
        turns dictionary into list
        """
        lst = []
        for key in dct:
            lst.extend(dct[key])
        return lst
    def demo_bst(self, path):
        """
        Demonstration of efficiency binary search tree for the search tasks.
        :param path:
        :type path:
        :return:
        :rtype:
        """
        dct = self.path_into_dict(path)
        lst = self.dict_into_list(dct)
        rand_lst = random.sample(lst, 10000)
        def lst_search(rand_lst, lst: list[str]):
            """
            ordered list
            """
            for i in rand_lst:
                indx = lst.index(i)
        def dct_search(rand_lst, dct: dict[str, list[str]]):
            """
            ordered dict
            """
            for i in rand_lst:
                indx = dct[i[0].capitalize()].index(i)
        def bst_search(rand_lst, bst: LinkedBST):
            """
            binary search tree 
            """
            for i in rand_lst:
                bst.find(i)

        def time_ex(func, *args, i=1):
            """
            measures execusion time for a func
            """
            start = time()
            for i in range(i):
                func(*args)

            print(f"{func.__name__} time:", time() - start)

        iterations = 1
        time_ex(lst_search, rand_lst, lst, i=iterations)
        time_ex(dct_search, rand_lst, dct, i=iterations)
        # adding elements from ordered sequence to a tree is irrational use of binary search tree dts
        # it doesn't take advantage of the tree's ability to split and is rather linear
        # the time complexity is O(n) instead of O(h)
        # e. g. it is difference of n = 200 000 and h = 42 for a dictionary
        #
        random.shuffle(lst)
        tree = LinkedBST(lst)
        print("tree height", tree.height())
        print("is the tree balanced:",tree.is_balanced())
        time_ex(bst_search, rand_lst, tree, i=iterations)
        tree.rebalance()
        print("is the tree balanced:",tree.is_balanced())
        print("tree height:", tree.height())
        time_ex(bst_search, rand_lst, tree, i=iterations)

