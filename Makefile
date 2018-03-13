# NAME: Virgil Jose, Christopher Ngai
# EMAIL: virgil@ucla.edu, cngai1223@gmail.com
# ID: 904765891, 404795904

default:
	cp lab3b.py lab3b
	chmod +x lab3b

dist:
	tar -czf lab3b-404795904.tar.gz lab3b.py Makefile README

clean:
	rm -f lab3b lab3b-404795904.tar.gz