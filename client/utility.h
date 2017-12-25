#ifndef _B_HEADER_H_ 
#define _B_HEADER_H_ 
#include "base_header.h" 
#endif 

#ifndef _UTIL_H_ 
#define _UTIL_H_
struct userinfo{
        short int start_mark;
        char sake[1];
        char id_length[1];
        char pw_length[1];
        char email_length[1];
        char id[16];
        char pw[16];
        char email[30];
        short int end_mark;
};

typedef struct userinfo UF;

typedef struct dearclient{
        short int start_mark;
        char sake;
        unsigned int session;
        short int end_mark;
} DRCLNT;

struct logininfo{
        GtkEntry *id_text_st; 
        GtkEntry *pw_text_st; 
};

typedef struct ranking{
	char id[170]; 
	int num; 
} RNK; 

void error_handling(char* msg);  
#endif
