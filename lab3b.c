// NAME: Virgil Jose, Christopher Ngai
// EMAIL: virgil@ucla.edu, cngai1223@gmail.com
// ID: 904765891, 404795904

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

    exit(0);
}