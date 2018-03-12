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

class InodeInfo():
    def __init__(self, inode_num=0, inode_mode=0, link_count=0):
        self.inode_num = inode_num
        self.inode_mode = inode_mode
        self.link_count = link_count
        self.links_found = 0

class DirInfo():
    def __init__(self, parent_inode_num, ref_inode_num, name_entry):
        self.parent_inode_num = parent_inode_num
        self.ref_inode_num = ref_inode_num
        self.name_entry = name_entry


# Array/List/Dict of the above classes ^
freeInodes = []
listDirs = []
inodeDict = dict()

def checkBlocks():
    return

# DIECTORY CONSISTENCY AUDIT
def checkDirs():
    return

# I-NODE ALLOCATION AUDIT
def checkInodes():

    for key in inodeDict:
        inode = inodeDict[key]
        if inode.inode_mode > 0 and inode.link_count > 0:
            for i in range(len(freeInodes)):
                if inode.inode_num == freeInodes[i]:
                    print("ALLOCATED INODE %d ON FREELIST" % inode.inode_num)
        elif inode.inode_mode < 0:
            onList = 0
            for i in range(len(freeInodes)):
                if inode.inode_num == freeInodes[i]:
                    onList = 1
                    break
            if onList == 0:
                print("UNALLOCATED INODE %d NOT ON FREELIST" % inode.inode_num)

    return

# count the number of links in all the directories.
# enumarate them in the inodeDict
def countLinks():
    
    
    
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
