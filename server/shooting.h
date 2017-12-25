#ifndef _B_HEADER_H_ 
#define _B_HEADER_H_
#include "base_header.h" 
#endif

#ifndef _UTIL_H_
#define _UTIL_H_ 
#include "utility.h" 
#endif

#ifndef _SHOT_H_ 
#define _SHOT_H 
int check_try_login(UF* userinfo_recv); 
int wanna_signup(UF* userinfo_recv); 
int adding_score(UF* userinfo_recv, char* clnt_id); 
RANK* get_ranking_db(char* clnt_id);  
#endif 
	
