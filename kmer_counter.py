import numpy as np
"""
This file contains an efficient implementation of a kmer counting algorithm for amino acids.
"""
'''
class for nodes inside of the tree
'''
class InternalNode:
   def __init__(self):
        self.A = None
        self.C = None
        self.D = None
        self.E = None
        self.F = None
        self.G = None
        self.H = None
        self.I = None
        self.K = None
        self.L = None
        self.M = None
        self.N = None
        self.P = None
        self.Q = None
        self.R = None
        self.S = None
        self.T = None
        self.V = None
        self.W = None
        self.Y = None      
'''
class for leaf nodes that carry a counter
'''
class LeafNode:
   def __init__(self, data: int):
      self.data = data
   def Increment(self):
      self.data = self.data + 1
'''
tiny class to hold an array so that it can be modified recursively.
p much a C struct lol
'''
class ArrayHolder:
    def __init__(self, array: np.ndarray):
        self.array = array
'''
method to generate the counter tree
'''
def generateTree(node: InternalNode, depth: int): 
   if (depth > 1):
        node.A = InternalNode()
        node.C = InternalNode()
        node.D = InternalNode()
        node.E = InternalNode()
        node.F = InternalNode()
        node.G = InternalNode()
        node.H = InternalNode()
        node.I = InternalNode()
        node.K = InternalNode()
        node.L = InternalNode()
        node.M = InternalNode()
        node.N = InternalNode()
        node.P = InternalNode()
        node.Q = InternalNode()
        node.R = InternalNode()
        node.S = InternalNode()
        node.T = InternalNode()
        node.V = InternalNode()
        node.W = InternalNode()
        node.Y = InternalNode() 
        generateTree(node.A, depth - 1)
        generateTree(node.C, depth - 1)
        generateTree(node.D, depth - 1)
        generateTree(node.E, depth - 1)
        generateTree(node.F, depth - 1)
        generateTree(node.G, depth - 1)
        generateTree(node.H, depth - 1)
        generateTree(node.I, depth - 1)
        generateTree(node.K, depth - 1)
        generateTree(node.L, depth - 1)
        generateTree(node.M, depth - 1)
        generateTree(node.N, depth - 1)
        generateTree(node.P, depth - 1)
        generateTree(node.Q, depth - 1)
        generateTree(node.R, depth - 1)
        generateTree(node.S, depth - 1)
        generateTree(node.T, depth - 1)
        generateTree(node.V, depth - 1)
        generateTree(node.W, depth - 1)
        generateTree(node.Y, depth - 1)
   else:
        node.A = LeafNode(0)
        node.C = LeafNode(0)
        node.D = LeafNode(0)
        node.E = LeafNode(0)
        node.F = LeafNode(0)
        node.G = LeafNode(0)
        node.H = LeafNode(0)
        node.I = LeafNode(0)
        node.K = LeafNode(0)
        node.L = LeafNode(0)
        node.M = LeafNode(0)
        node.N = LeafNode(0)
        node.P = LeafNode(0)
        node.Q = LeafNode(0)
        node.R = LeafNode(0)
        node.S = LeafNode(0)
        node.T = LeafNode(0)
        node.V = LeafNode(0)
        node.W = LeafNode(0)
        node.Y = LeafNode(0) 
'''
count each k-mer
'''
def increment_leaves(sequence: str, root: InternalNode, k: int):
   seqLen = len(sequence)
   for i in range(0, seqLen - k):
      kmer = sequence[i:i + k]
      if (sequence.find('U') == -1): 
        incrementLeaf(root, k, kmer)
'''
navigate down the tree and then increment the leaf.
'''
def incrementLeaf(root: InternalNode, k: int, kmer: str):
   if kmer[0] == 'A':
      node = root.A
   elif kmer[0] == 'C':
      node = root.C
   elif kmer[0] == 'D':
      node = root.D
   elif kmer[0] == 'E':
      node = root.E
   elif kmer[0] == 'F':
      node = root.F
   elif kmer[0] == 'G':
      node = root.G
   elif kmer[0] == 'H':
      node = root.H  
   elif kmer[0] == 'I':
      node = root.I
   elif kmer[0] == 'K':
      node = root.K
   elif kmer[0] == 'L':
      node = root.L
   elif kmer[0] == 'M':
      node = root.M
   elif kmer[0] == 'N':
      node = root.N
   elif kmer[0] == 'P':
      node = root.P 
   elif kmer[0] == 'Q':
      node = root.Q
   elif kmer[0] == 'R':
      node = root.R  
   elif kmer[0] == 'S':
      node = root.S
   elif kmer[0] == 'T':
      node = root.T
   elif kmer[0] == 'V':
      node = root.V
   elif kmer[0] == 'W':
      node = root.W
   elif kmer[0] == 'Y':
      node = root.Y
   for j in range(1, k):
      if kmer[j] == 'A':
            node = node.A
      elif kmer[j] == 'C':
            node = node.C
      elif kmer[j] == 'D':
            node = node.D
      elif kmer[j] == 'E':
            node = node.E
      elif kmer[j] == 'F':
            node = node.F
      elif kmer[j] == 'G':
            node = node.G
      elif kmer[j] == 'H':
            node = node.H
      elif kmer[j] == 'I':
            node = node.I
      elif kmer[j] == 'K':
            node = node.K
      elif kmer[j] == 'L':
            node = node.L
      elif kmer[j] == 'M':
            node = node.M
      elif kmer[j] == 'N':
            node = node.N
      elif kmer[j] == 'P':
            node = node.P
      elif kmer[j] == 'Q':
            node = node.Q
      elif kmer[j] == 'R':
            node = node.R
      elif kmer[j] == 'S':
            node = node.S
      elif kmer[j] == 'T':
            node = node.T
      elif kmer[j] == 'V':
            node = node.V
      elif kmer[j] == 'W':
            node = node.W
      elif kmer[j] == 'Y':
            node = node.Y
   node.Increment()
'''
creates a numpy array from the counted tree data
'''
def create_array_from_tree(root: InternalNode, array_holder: ArrayHolder) -> np.ndarray:
    if (root.__class__ == LeafNode):
        array_holder.array[np.where(array_holder.array==-1)[0][0]] = root.data
    else:
        create_array_from_tree(root.A, array_holder)
        create_array_from_tree(root.C, array_holder)
        create_array_from_tree(root.D, array_holder)
        create_array_from_tree(root.E, array_holder)
        create_array_from_tree(root.F, array_holder)
        create_array_from_tree(root.G, array_holder)
        create_array_from_tree(root.H, array_holder)
        create_array_from_tree(root.I, array_holder)
        create_array_from_tree(root.K, array_holder)
        create_array_from_tree(root.L, array_holder)
        create_array_from_tree(root.M, array_holder)
        create_array_from_tree(root.N, array_holder)
        create_array_from_tree(root.P, array_holder)
        create_array_from_tree(root.Q, array_holder)
        create_array_from_tree(root.R, array_holder)
        create_array_from_tree(root.S, array_holder)
        create_array_from_tree(root.T, array_holder)
        create_array_from_tree(root.V, array_holder)
        create_array_from_tree(root.W, array_holder)
        create_array_from_tree(root.Y, array_holder)
'''
runner method for the file
'''
def kmer_count(sequence: str, k):
    root = InternalNode()
    generateTree(root, k)
    increment_leaves(sequence, root, k)
    array_holder = ArrayHolder
    array_holder.array = np.ones(20**k)*-1
    create_array_from_tree(root, array_holder)
    return array_holder.array