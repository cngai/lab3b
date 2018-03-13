#!/bin/python

# NAME: Virgil Jose, Christopher Ngai
# EMAIL: virgil@ucla.edu, cngai1223@gmail.com,
# ID: 904765891, 404795904

from __future__ import print_function
import sys
import csv

# Definitions for classes to store information about inodes and directories
class SuperblockInfo():
    def __init__(self, num_blocks=0, num_inodes=0, size_blocks=0, size_inodes=0, blocks_group=0, inodes_group=0, first_nr_inode=0):
        self.num_blocks = num_blocks
        self.num_inodes = num_inodes
        self.size_blocks = size_blocks
        self.size_inodes = size_inodes
        self.blocks_group = blocks_group
        self.inodes_group = inodes_group
        self.first_nr_inode = first_nr_inode

class BlockInfo():
    def __init__(self, block_num=0, inode_num=0, offset=0, level=0):
        self.block_num = block_num
        self.inode_num = inode_num
        self.offset = offset
        self.level = level

class InodeInfo():
    def __init__(self, inode_num=0, inode_mode=0, link_count=0):
        self.inode_num = inode_num
        self.inode_mode = inode_mode
        self.link_count = link_count
        self.links_found = 0
        self.addresses = []

class DirInfo():
    def __init__(self, parent_inode_num=0, ref_inode_num=0, name_entry=0):
        self.parent_inode_num = parent_inode_num
        self.ref_inode_num = ref_inode_num
        self.name_entry = name_entry


# Array/List/Dict of the above classes ^
superblock = SuperblockInfo()
freeBlocks = []
freeInodes = []
blockDict = dict()
inodeDict = dict()      # store each inode, with key being the inode # and the value being the inode class instance
pinDict = dict()
listDirs = []

def checkBlocks():
    # iterate through all the blocks
    for i in blockDict.keys():
        block = list(blockDict[i])
        realBlock = block[0]
        block_num = realBlock.block_num
        block_level = realBlock.level
        block_type = "BLOCK"
        if block_level == 1:
            block_type = "INDIRECT BLOCK"
        if block_level == 2:
            block_type = "DOUBLE INDIRECT BLOCK"
        if block_level == 3:
            block_type = "TRIPLE INDIRECT BLOCK"
        # check if the block is valid
        if i < 0 or i >= superblock.num_blocks:
            print("INVALID %s %d IN INODE %d AT OFFSET %d\n" % (block_type, block_num, realBlock.inode_num, realBlock.offset))
        # check if block is free
        if block_num in freeBlocks:
            print("ALLOCATED BLOCK %d ON FREELIST\n" % block_num)
        # check if block is reserved
        if block_num > 0 and block_num < 9:
            print("RESERVED %s %d IN INODE %d AT OFFSET %d\n" % (block_type, block_num, realBlock.inode_num, realBlock.offset))
        # check if block is duplicated
        elif len(block) > 1:
            for duplicates in block:
                block_level = duplicates.level
                block_type = "BLOCK"
                if block_level == 1:
                    block_type = "INDIRECT BLOCK"
                if block_level == 2:
                    block_type = "DOUBLE INDIRECT BLOCK"
                if block_level == 3:
                    block_type = "TRIPLE INDIRECT BLOCK"
            print("DUPLICATE %s %d IN INODE %d AT OFFSET %d\n" % (block_type, block_num, realBlock.inode_num, realBlock.offset))

    return

# wrapper functions for directory consistency audit
"""
def checkValidDirReferences():
    for i in listDirs:
        direct = i
        if direct.ref_inode_num in freeInodes:
            print("DIRECTORY INODE %d NAME '%s' UNALLOCATED INODE %d\n" % (direct.parent_inode_num, direct.name_entry, direct.ref_inode_num))
    return
    """

"""
def checkCurrAndParentDir():
    for i in listDirs:
        direct = i
        if direct.name_entry == '\'.\'':
            if direct.parent_inode_num != direct.ref_inode_num:
                print("DIRECTORY INODE %d NAME %s LINK TO INODE %d SHOULD BE %d\n" % (direct.parent_inode_num, '\'.\'', direct.ref_inode_num, direct.parent_inode_num))
    return
    """

def checkLinks():
    for key in inodeDict:
        if inodeDict[key].inode_mode > 0 and inodeDict[key].link_count != inodeDict[key].links_found:
            print("INODE %d HAS %d LINKS BUT LINKCOUNT IS %d\n" % (inodeDict[key].inode_num, inodeDict[key].link_count, inodeDict[key].links_found))
    return

# DIECTORY CONSISTENCY AUDIT
def checkDirs():
    #keys = inodeDict.keys()

    for i in listDirs:
        # check if invalid inode
        if i.ref_inode_num < 1 or i.ref_inode_num > superblock.num_inodes:
            print("DIRECTORY INODE %d NAME %s INVALID INODE %d" % (i.parent_inode_num, i.name_entry, i.ref_inode_num))
            continue

        #update link count
        if i.ref_inode_num in inodeDict.keys():
            inodeDict[i.ref_inode_num].links_found += 1

        #check current directory
        if i.name_entry == '\'.\'':
            if i.parent_inode_num != i.ref_inode_num:
                print("DIRECTORY INODE %d NAME %s LINK TO INODE %d SHOULD BE %d\n" % (i.parent_inode_num, i.name_entry, i.ref_inode_num, i.parent_inode_num))
        #check parent directory
        elif i.name_entry == '\'..\'':
            if i.parent_inode_num == 2 or i.ref_inode_num == 2:
                grandparent_inode_num = 2
            else:
                grandparent_inode_num = pinDict[i.parent_inode_num]

            #check grandparent directory
            if grandparent_inode_num != i.ref_inode_num:
                print("DIRECTORY INODE %d NAME %s LINK TO INODE %d SHOULD BE %d" % (i.parent_inode_num, i.name_entry, i.ref_inode_num, grandparent_inode_num))

        #check if unallocated
        elif i.ref_inode_num in freeInodes:
            if i.ref_inode_num >= superblock.first_nr_inode and i.ref_inode_num <= num_blocks:
                print("DIRECTORY INODE %d NAME '%s' UNALLOCATED INODE %d\n" % (i.parent_inode_num, i.name_entry, i.ref_inode_num))
        elif i.ref_inode_num in inodeDict.keys() and inodeDict[i.ref_inode_num].inode_mode <= 0:
            print("DIRECTORY INODE %d NAME '%s' UNALLOCATED INODE %d\n" % (i.superblock, i.name_entry, i.ref_inode_num))
        elif i.ref_inode_num not in inodeDict.keys() and i.ref_inode_num > superblock.first_nr_inode:
            print("DIRECTORY INODE %d NAME '%s' UNALLOCATED INODE %d\n" % (i.parent_inode_num, i.name_entry, i.ref_inode_num))


    #check if reference count matches link count
    checkLinks()

    #checkValidDirReferences()
    #checkCurrAndParentDir()
    return


# I-NODE ALLOCATION AUDIT
def checkInodes():
    for i in (superblock.first_nr_inode, superblock.num_inodes+1):
        if i in inodeDict.keys():
            inode = inodeDict[i]
            if inode.inode_mode > 0 and inode.link_count > 0:
                if inode.inode_num in freeInodes:
                    print("ALLOCATED INODE %d ON FREELIST\n" % inode.inode_num)
                elif inode.inode_mode < 0 and inode.inode_num not in freeInodes:
                    print("UNALLOCATED INODE %d NOT ON FREELIST\n" % inode.inode_num)
    else:
        if i not in freeInodes:
            print("UNALLOCATED INODE %d NOT ON FREELIST\n" % i)
    return

def parse_csv_file():
    # check if we have the correct number of arguments
    if len(sys.argv) != 2:
        print("Invalid number of arguments. Usage: ./lab3b.py csvfile.csv\n", file=sys.stderr)
        sys.exit(1)
    
    # open the CSV file
    try:
        csvFile = open(sys.argv[1], "rb")
    except:
        print("Error opening CSV file\n", file=sys.stderr)
        sys.exit(1)

    # parse the CSV file
    parser = csv.reader(csvFile, delimiter=',')

    # go through every line in ther CSV file
    for row in parser:
        if row[0] == 'SUPERBLOCK':
            superblock.num_blocks = int(row[1])
            superblock.num_inodes = int(row[2])
            superblock.size_blocks = int(row[3])
            superblock.size_inodes = int(row[4])
            superblock.blocks_group = int(row[5])
            superblock.inodes_group = int(row[6])
            superblock.first_nr_inode = int(row[7])
            
        elif row[0] == 'BFREE':
            freeBlocks.append(int(row[1]))

        elif row[0] == 'IFREE':
            freeInodes.append(int(row[1]))

        elif row[0] == 'INODE':
            inode = InodeInfo(int(row[1]),int(row[3]),int(row[6]))
            
            # iterate through each block addresses
            for x in range(15):
                block_addrs = int(row[12+x])
                inode.addresses.append(block_addrs)
                level = 0
                offset = x
                
                # if single, double, triple indirect block
                if x >= 12:
                    level = x - 11      #level will be either 1, 2, 3
                    # set original offset
                    if level == 1:
                        offset = 12
                    elif level == 2:
                        offset = 268
                    elif level == 3:
                        offset = 65804
                        
                # create BlockInfo object and add to blockDict
                if block_addrs > 0:
                    block = BlockInfo(block_addrs, int(row[1]), offset, level)

                    #check if block already in blockDict
                    if block_addrs not in blockDict:
                        blockDict[block_addrs] = set()
                    blockDict[block_addrs].add(block)

            # append inode to inodeDict
            inodeDict[int(row[1])] = inode
        
        elif row[0] == 'DIRENT':
            name_entry = row[6]
            direct = DirInfo(int(row[1]), int(row[3]), name_entry)
            listDirs.append(direct)
            if name_entry != '\'.\'' and name_entry != '\'..\'':
                pinDict[int(row[3])] = int(row[1])

        elif row[0] == 'INDIRECT':
            block_addrs = int(row[5])
            block = BlockInfo(block_addrs, int(row[1]), int(row[3]), int(row[2]) - 1)

            #check if block already in blockDict
            if block_addrs not in blockDict:
                blockDict[block_addrs] = set()
            blockDict[block_addrs].add(block)

if __name__ == "__main__":
    parse_csv_file()
    #countLinks()
    checkDirs()
    checkBlocks()
    checkInodes()

