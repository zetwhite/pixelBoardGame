login : login.o utility.o 
	gcc -w -o login login.o utility.o `pkg-config --cflags --libs gtk+-2.0`
login.o : login.c 
	gcc -c -w login.c `pkg-config --cflags --libs gtk+-2.0`
utility.o : utility.c 
	gcc -c -w utility.c `pkg-config --cflags --libs gtk+-2.0` 
clean: 
	rm *.o 
