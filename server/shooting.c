#include "utility.h" 

int check_try_login(UF* userinfo_recv){
	UF* try_login_ad = userinfo_recv; 
	MYSQL *conn; 
	conn = mysql_connection(conn); 
	MYSQL_RES *result; 
	unsigned int result_number; 

	char query[100];  
	char got_id[17]; 
	char got_pw[17];
	unsigned int id_length; 
	unsigned int pw_length; 
   
	memset(got_id, 0, 17); 	
	memset(got_pw, 0, 17); 
	memcpy(got_id,(try_login_ad->id),(unsigned int) *(try_login_ad->id_length));
 	memcpy(got_pw,(try_login_ad->pw),(unsigned int)  *(try_login_ad->pw_length)); 
	sprintf(query, "%s%s%s%s%s%s%s", "select * from userinfo where id = \'", got_id, "\'", " and pw = \'", got_pw, "\'", "\n"); 
	printf("%s", query);
	if(mysql_query(conn, query)){
		error_handling("mysql query error"); 
		printf("error_message : %s\n", mysql_error(conn)); 
		return -1; 
	}
	result = mysql_store_result(conn); 
	result_number = mysql_num_rows(result);
	if(result_number == 0){//login failed
		printf("login failed\n");
		return 0; 
	} 
	if(result_number > 0){//login sucessed 
		printf("login success\n"); 
		return 1; 
	}
	return 0;  
}

int duplication_check(MYSQL* conn, char* field_name, char* content){
	char query[100]; 
        MYSQL_RES *result;
        unsigned int result_number;
	sprintf(query, "%s%s%s%s%s%s", "select * from userinfo where ",field_name," = \'", content, "\'", "\n");
        printf("%s\n", query);
        if(mysql_query(conn, query)){
                error_handling("mysql query error");
                printf("error_message : %s\n", mysql_error(conn));
                return -1;
        }
        result = mysql_store_result(conn);
        result_number = mysql_num_rows(result);
        if(result_number == 0){//no duplication
                printf("no duplication\n");
                return 0;
        }
        if(result_number > 0){//duplciation exists
                printf("duplication!!\n");
                return 1;
        }

}

int wanna_signup(UF* userinfo_recv){
	UF* try_signup_ad = userinfo_recv; 
	MYSQL *conn; 
	conn = mysql_connection(conn); 
	MYSQL_RES *result; 
	unsigned int result_number; 
	
	char query[100]; 
	char got_id[17];
	char got_pw[17];
	char got_email[30];
	unsigned int id_length; 
	unsigned int pw_length; 
	unsigned int email_length; 
	memset(got_id, 0, 17); 
	memset(got_pw, 0, 17); 
	memset(got_email, 0, 30); 
	memcpy(got_id, (try_signup_ad->id), (unsigned int)*(try_signup_ad->id_length)); 
	memcpy(got_pw, (try_signup_ad->pw), (unsigned int)*(try_signup_ad->pw_length)); 
	memcpy(got_email, (try_signup_ad->email), (unsigned int)*(try_signup_ad->email_length));

	if(duplication_check(conn,"id",got_id)){
		return 10; 
	} 
	if(duplication_check(conn, "pw", got_pw)){
		return 20; 
	}
	sprintf(query, "%s%s%s%s%s%s%s%s%s", "insert into userinfo (id, pw, email, score) ", "Values (\'", got_id,"\',\'", got_pw, "\',\'", got_email,"\',"," 0)\n"); 
	printf("query : %s", query); 
	if(mysql_query(conn, query)){
		error_handling(mysql_error(conn)); 
		printf("register failed!\n");  
		return 0; 
	}
	else{
		printf("register successed!\n"); 
		return 1; 
	} 
	return -1; 
}

int adding_score(UF* userinfo_recv, char* clnt_id){
	MYSQL* conn; 
	conn = mysql_connection(conn); 
	
	char query[100]; 
	sprintf(query, "%s%s%s" , "update userinfo set score = score+1 where id = \'", clnt_id, "\'"); 
	printf("query ; %s\n", query); 
	if(mysql_query(conn, query)){
		error_handling(mysql_error(conn)); 
		printf("score ++ failed");
		return 0; 
	}
	else{
		printf("score ++ success"); 
		return 1; 
	}
		return 0; 
}

RANK* get_ranking_db(char* clnt_id){
	MYSQL * conn; 
	MYSQL_RES * result; 
	MYSQL_ROW * row; 
	RANK return_result; 

	conn = mysql_connection(conn); 
	char* query = "select * from userinfo order by score\00"; 
	if(mysql_query(conn, query)){
		error_handling(mysql_error(conn)); 
		return 0; 
	}
	
	result = mysql_store_result(conn); 
	int i = 0;
        memset(return_result.id, 0, 170); 
	for(i = 0; i< 5; i++){
		row= mysql_fetch_row(result); 
		printf("%s\n", row[1]); 
		printf("%d\n", strlen(row[1])); 
		memcpy(return_result.id + i*17, row[1], strlen(row[1]));  
		printf("%s\n", &(return_result.id[17*i])); 
	}
	return &return_result;
}





















