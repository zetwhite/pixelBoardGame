#include "base_header.h" 

void error_handling(char*msg){
        fputs(msg, stderr);
        fputc('\n', stderr);
        exit(1);
}
