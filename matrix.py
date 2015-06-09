#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Python 3 compatibility
from __future__ import print_function
import sys
if sys.version_info[0]==3:
	raw_input = input

verbose = False

# Version 1:
# General idea is we loop through all cells, checking the ones to the left and above the current cell:
#    1    1    1
#      ┌  ^  ┐
#       \ | /
#    1 <- 1
# If any of these are 1's, they have been checked already, so put the current cell in the same region as them
# If the current cell is in two regions now, merge them.
#
#
# Version 2:
# For every 1 we encounter, build a tree of all connected 1's, and mark them all as seen in the cache.
# Only check spaces that aren't in the cache. This means that no '1' space will be visited more than
# once, and no expensive lookups

def solve(m=None,n=None,mat=None):
	matrix = []
	cells_to_regions = {}
	regions_to_cells = {}
	if m is None:
		try:
			m = int(raw_input("Enter m: " if verbose else ""))
		except ValueError:
			print ("M must be a number.")
			return
	if n is None:
		try:
			n = int(raw_input("Enter n: " if verbose else ""))
		except ValueError:
			print ("N must be a number.")
			return
	if verbose:
		print ("Enter "+str(m)+" rows:")
	if mat is None:
		for i in range(m):
			try:
				matrix.append([int(bool(int(j))) for j in raw_input().split()])
			except ValueError:
				print ("Rows should be numbers separated by spaces.")
				return
	else:
		matrix = mat

	if verbose:
		print ("Processing row:")
	return process_v2(matrix, m, n)

def process_v1(matrix, m, n, cells_to_regions, regions_to_cells):
	for rowindex, row in enumerate(matrix):
		if verbose:
			print (rowindex)

		for cellindex, cell in enumerate(row):
			if not cell:
				continue
			
			foundregion = False

			if cellindex!=0 and row[cellindex-1]:
				foundregion = True
				region = cells_to_regions[(rowindex,cellindex-1)]
				cells_to_regions[(rowindex,cellindex)] = region
				if not (rowindex, cellindex) in regions_to_cells[region]:
					regions_to_cells[region].append((rowindex,cellindex))


			if cellindex!=0 and rowindex!=0 and matrix[rowindex-1][cellindex-1]:
				foundregion = True
				region = cells_to_regions[(rowindex-1,cellindex-1)]
				if (rowindex,cellindex) in cells_to_regions and cells_to_regions[(rowindex,cellindex)] != region:
					oldregion = cells_to_regions[(rowindex,cellindex)]
					for cell in regions_to_cells[oldregion]:
						cells_to_regions[cell] = region
						regions_to_cells[region].append(cell)
					del regions_to_cells[oldregion]
				cells_to_regions[(rowindex,cellindex)] = region
				if not (rowindex, cellindex) in regions_to_cells[region]:
					regions_to_cells[region].append((rowindex,cellindex))


			if rowindex!=0 and matrix[rowindex-1][cellindex]:
				foundregion = True
				region = cells_to_regions[(rowindex-1,cellindex)]
				if (rowindex,cellindex) in cells_to_regions and cells_to_regions[(rowindex,cellindex)] != region:
					oldregion = cells_to_regions[(rowindex,cellindex)]
					for cell in regions_to_cells[oldregion]:
						cells_to_regions[cell] = region
						regions_to_cells[region].append(cell)
					del regions_to_cells[oldregion]
				cells_to_regions[(rowindex,cellindex)] = region
				if not (rowindex, cellindex) in regions_to_cells[region]:
					regions_to_cells[region].append((rowindex,cellindex))


			if cellindex<m-1 and rowindex!=0 and matrix[rowindex-1][cellindex+1]:
				foundregion = True
				region = cells_to_regions[(rowindex-1,cellindex+1)]
				if (rowindex,cellindex) in cells_to_regions and cells_to_regions[(rowindex,cellindex)] != region:
					oldregion = cells_to_regions[(rowindex,cellindex)]
					for cell in regions_to_cells[oldregion]:
						cells_to_regions[cell] = region
						regions_to_cells[region].append(cell)
					del regions_to_cells[oldregion]
				cells_to_regions[(rowindex,cellindex)] = region
				if not (rowindex, cellindex) in regions_to_cells[region]:
					regions_to_cells[region].append((rowindex,cellindex))
			


			if foundregion == False:
				region = max(list(regions_to_cells.keys())+[0])+1
				cells_to_regions[(rowindex,cellindex)] = region
				regions_to_cells[region] = []
				regions_to_cells[region].append((rowindex,cellindex))

	if verbose:
		print ("Final result:")

	return max([len(regions_to_cells[i]) for i in regions_to_cells])

def trace_tree(matrix, m, n, rowindex, cellindex, cache):
	num = 1
	stack = [(rowindex,cellindex)]
	while stack:
		cell = stack.pop()
		for i in range(cell[0]-1,cell[0]+2):
			for j in range(cell[1]-1,cell[1]+2):
				if i>=0 and j>=0 and i<m and j<n and matrix[i][j] and not cache[i][j]:
					num+=1
					# We can modify cache because lists are passed by reference
					cache[i][j] = True
					stack.append((i,j))
	return num

def process_v2(matrix, m, n):
	lens = []
	cache = []
	for i in range(m):
		cache.append([False]*n)
	for rowindex, row in enumerate(matrix):
		if verbose:
			print (rowindex)

		for cellindex, cell in enumerate(row):
			if not cell or cache[rowindex][cellindex]:
				continue


			cache[rowindex][cellindex] = True
			lens.append(trace_tree(matrix, m, n, rowindex, cellindex, cache))

	return max(lens)



if __name__=="__main__":
	if "-v" in sys.argv:
		verbose = True
		sys.argv = sys.argv[:sys.argv.index("-v")]+sys.argv[sys.argv.index("-v")+1:]
	if len(sys.argv)>1:
		f = open(sys.argv[1]).read()
		l = f.splitlines()
		print (solve(int(l[0]), int(l[1]), [[int(bool(int(j))) for j in i.split()] for i in l[2:]]))
	else:
		print (solve())