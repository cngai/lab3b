// NAME: Virgil Jose, Christopher Ngai
// EMAIL: virgil@ucla.edu, cngai1223@gmail.com
// ID: 904765891, 404795904

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

/* to use strtok() */
#include <string.h>

/* to use open */
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>

/* to use isdigit() */
#include <ctype.h>

/* STRUCTS */
struct superblock {
    int total_num_blocks;
    int total_num_inodes;
    int block_size;
    int inode_size;
    int blocks_per_group;
    int inodes_per_group;
    int first_nr_inode;
};

struct inode {
    int inode_num;
    char file_type;
    int inode_mode;
    int inode_owner;
    int inode_group;
    int link_count;
    char* c_time;
    char* m_time;
    char* a_time;
    int file_size;
    int num_blocks;
};

struct dirent {
    int p_inode_num;
    int log_byte_offset;
    int ref_inode_num;
    int entry_length;
    int name_length;
    char* name;
};

struct indirect {
    int inode_num;
    int ind_level;
    int log_block_offset;
    int ind_block_num;
    int ref_block_num;
};

/* WRAPPER FUNCTIONS */

/* gets certain field value of line in CSV file */
const char* getfield(char* line, int num)
{
    const char* tok;
    for (tok = strtok(line, ","); tok && *tok; tok = strtok(NULL, ",\n")){
        if (!--num)
            return tok;
    }
    return NULL;
}

/* converts string to int */
int str_to_int(const char *s){
    int num = 0;
    while (*s){
        if (!isdigit(*s)){
            break;
        }
        num *= 10;
        num += *s++ - '0';
    }

    return num;
}

void parse_file(FILE* stream) {
    char line[1024];
    while (fgets(line, 1024, stream) != NULL){
        const char* type = getfield(line, 1);
        printf("%s\n", type);
        if (strcmp(type, "SUPERBLOCK") == 0){
            printf("%s\n", "superblock");
        }
        else{
            printf("%s\n", "not superblock");
        }
    }
}

void check_dirs() {
    return;
}

void check_inodes() {
    return;
}

void check_blocks() {
    return;
}

int main(int argc, char * argv[]){
	/* check to make sure correct number of arguments */
    if (argc != 2){
    	fprintf(stderr, "Error: incorrect number of arguments.\n");
    	exit(1);
    }
    /* open the file system image */
    //int fd = open(argv[1], O_RDONLY);
    FILE* input_file = fopen(argv[1], "r");
    if (input_file == NULL){
    	fprintf(stderr, "Error opening file system.\n");
    	exit(1);
    }

    parse_file(input_file);
    check_blocks();
    check_inodes();
    check_dirs();
    
    exit(0);
}
