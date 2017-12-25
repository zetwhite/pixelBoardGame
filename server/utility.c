#include "base_header.h"

void error_handling(char* msg){
        fputs(msg, stderr);
        fputc('\n', stderr);
        exit(1);
}

MYSQL* mysql_connection(MYSQL *mysql){
	MYSQL *conn = mysql; 
        char *server = "127.0.0.1"; 
        char *user = "root"; 
        char *password = "???"; 
        char *database = "roonmap"; 
        conn = mysql_init(NULL); 

        if(!mysql_real_connect(conn, server,user,password, database, 0, NULL, 0)){
                printf("connection to mysql failed :( - %s\n", mysql_error(conn)); 
                exit(1); 
        }
        else{
                printf("connection to mysql successed :)\n"); 
        }
        return conn; 
 
}
