// NAME: Virgil Jose, Christopher Ngai
// EMAIL: virgil@ucla.edu, cngai1223@gmail.com
// ID: 904765891, 404795904

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

/* STRUCTS */
struct superblock {
    int total_num_blocks;
    int total_num_inodes;
    int block_size;
    int inode_size;
    int blocks_per_group;
    int inodes_per_group;
    int first_nr_inode;
}

struct inode {
    int inode_num;
    char file_type;
    int inode_mode;
    int inode_owner;
    int inode_group;
    int link_count;
    string ctime;
    string mtime;
    string atime;
    int file_size;
    int num_blocks;
}

struct dirent {
    int p_inode_num;
    int log_byte_offset;
    int ref_inode_num;
    int entry_length;
    int name_length;
    string name;
}

struct indirect {
    int inode_num;
    int ind_level;
    int log_block_offset;
    int ind_block_num;
    int ref_block_num;
}

void check_dirs(int fd) {
    return;
}

void check_inodes(int fd) {
    return;
}

void check_blocks(int fd) {
    return;
}

int main(int argc, char * argv[]){
	/* check to make sure correct number of arguments */
    if (argc != 2){
    	fprintf(stderr, "Error: incorrect number of arguments.\n");
    	exit(1);
    }
    /* open the file system image */
    int fd = open(argv[1], O_RDONLY);
    if (fd < 0){
    	fprintf(stderr, "Error opening file system.\n");
    	exit(1);
    }

    check_blocks(fd);
    check_inodes(fd);
    check_dirs(fd);
    
    exit(0);
}
