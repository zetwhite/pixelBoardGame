main : utility.o shooting.o main.o 
	gcc -w -o main utility.o shooting.o main.o -D_REENTRANT -lpthread -lmysqlclient 
main.o : main.c
	gcc -c -w main.c
shooting.o : shooting.c
	gcc -c -w shooting.c
utility.o : utility.c
	gcc -c -w utility.c 
clean : 
	rm *.o
	