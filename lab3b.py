#!/bin/python

# NAME: Virgil Jose, Christopher Ngai
# EMAIL: virgil@ucla.edu, cngai1223@gmail.com,
# ID: 904765891, 404795904

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

class DirInfo():
    def __init__(self, parent_inode_num=0, ref_inode_num=0, name_entry=0):
        self.parent_inode_num = parent_inode_num
        self.ref_inode_num = ref_inode_num
        self.name_entry = name_entry


# Array/List/Dict of the above classes ^
superblock = None
listBlocks = []
inodeDict = dict()      # store each inode, with key being the inode # and the value being the inode class instance
freeInodes = []
listDirs = []

def checkBlocks():
    return

# wrapper functions for directory consistency audit
def checkCurrAndParentDir():
    for i in listDirs:
        dir = listDirs[i]
        if dir.name_entry == '\'.\'':
            if dir.parent_inode_num != dir.ref_inode_num:
                print("DIRECTORY INODE %d NAME %s LINK TO INODE %d SHOULD BE %d\n" % (dir.parent_inode_num, '\'.\'', dir.ref_inode_num, dir.parent_inode_num))
    return

def checkValidDirReferences():
    for i in listDirs:
        dir = listDirs[i]
        if dir.ref_inode_num in freeInodes:
            print("DIRECTORY INODE %d NAME '%s' UNALLOCATED INODE %d\n" % (dir.parent_inode_num, dir.name_entry, dir.ref_inode_num))
    return

def countLinks():
    for i in listDirs:
        dir = listDirs[i]
        if dir.ref_inode_num in inodeDict.keys():
            inodeDict[dir.ref_inode_num].listBlocks += 1
    for key in inodeDict:
        if inodeDict[key].link_count != inodeDict[key].links_found:
            print("INODE %d HAS %d LINKS BUT LINKCOUNT IS %d\n" % (int(key), inodeDict[key].link_count, inodeDict[key].links_found))
    return

# DIECTORY CONSISTENCY AUDIT
def checkDirs():
    countLinks()
    checkValidDirReferences()
    checkCurrAndParentDir()
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
        print("Invalid number of arguments. Usage: ./lab3b.py csvfile.csv\n")
        sys.exit(1)
    # open the CSV file
    try:
        csvFile = open(sys.argv[1], "w+")
    except:
        print("Error opening CSV file\n")
        sys.exit(1)
    # parse the CSV file
    parser = csv.reader(csvFile, delimiter=',')
    # go through every line in ther CSV file
    for row in parser:
        if row[0] == "INODE":
            inode = InodeInfo(int(row[1]),int(row[3]),int(row[6]))
            inodeDict[int(row[1])] = inode
        elif row[0] == "IFREE":
            freeInodes.add(int(row[1]))
        elif row[0] == "DIRENT":
            dir = DirInfo(int(row[1]), int(row[3]), row[6])
            listDirs.add(dir)

    return

if __name__ == "__main__":
    parse_csv_file()
    countLinks()
    checkInodes()
    checkDirs()
