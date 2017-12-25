#include "base_header.h"
#include "utility.h"
#include "shooting.h" 
#define BUF_SIZE 100 
#define MAX_CLNT 256

//MYSQL mysql_connection(void); 

//void mysql_connection
void *handle_clnt(void* arg); 
void send_msg(char *msg, int len); 

int client_count =0; 
int client_socks[MAX_CLNT]; 
pthread_mutex_t mutex; 

int main(int argc, char*argv[]){
	int serv_sock, clnt_sock; 
	struct sockaddr_in serv_adr, clnt_adr; 
	int clnt_adr_sz; 
	pthread_t t_id; 
	pthread_mutex_init(&mutex, NULL); 
	serv_sock =socket(PF_INET, SOCK_STREAM, 0); 

	memset(&serv_adr, 0, sizeof(serv_adr)); 
	serv_adr.sin_family = AF_INET; 
	serv_adr.sin_addr.s_addr = htonl(INADDR_ANY); 
	serv_adr.sin_port=htons(atoi("9090"));

	if(bind(serv_sock, (struct sockaddr*)&serv_adr, sizeof(serv_adr)) == -1) 
		error_handling("bind() error"); 
	if(listen(serv_sock, 10)==-1) 
		error_handling("listen() error"); 
	while(1){
		clnt_adr_sz = sizeof(clnt_adr); 
		clnt_sock = accept(serv_sock, (struct sockaddr*)&clnt_adr, &clnt_adr_sz);
		
		pthread_mutex_lock(&mutex); 
		client_socks[client_count++]= clnt_sock; 
		pthread_mutex_unlock(&mutex); 
		
		pthread_create(&t_id, NULL, handle_clnt, (void*)&clnt_sock); 
		pthread_detach(t_id); 
		printf("Connected clinet IP : %s\n", inet_ntoa(clnt_adr.sin_addr)); 
	}
	close(serv_sock); 
	return 0;  
}

void *handle_clnt(void* arg){
	int clnt_sock = *((int*)arg); 
	int str_len = 0, i; 
	char message[BUF_SIZE]; 
	char clnt_id[17]; 
	unsigned char session_serv; 
	UF userinfo_recv; 
	memset(&userinfo_recv, 0, sizeof(UF)); 
	int getting = 0; 
	while((str_len = read(clnt_sock,&userinfo_recv, sizeof(UF)))!=0){
		printf("getting : %d\n", getting); 
		printf(" id : %s\n", userinfo_recv.id); 
		printf(" pw : %s\n", userinfo_recv.pw);
		int db_result; 
		int login_session;  
		unsigned char try_login = 1; 
		unsigned char try_sign = 0; 
		int add_score = 100; 
		int get_rank = 200; 
			
	
		if(!(memcmp(&try_login, userinfo_recv.sake, 1))){
			printf("clnt wanna login\n");
			srand(time(NULL)); 
			DRCLNT login_result; 
			db_result =  check_try_login(&userinfo_recv); 
			if(db_result == 1){//login success
				memset (&(login_result.sake), 3, 1); 
				memset(&(login_result.session), rand()%255, 1);     
				session_serv = login_result.session;
				memset(clnt_id, 0, 17); 
				memcpy(clnt_id, userinfo_recv.id, (unsigned int)*(userinfo_recv.id_length));
			}
			else{//login fail 
				memset(&(login_result.sake),2,1); 
				memset(&(login_result.session),0,1);  
			}
			write(clnt_sock, &login_result, sizeof(DRCLNT)); 
		}
		if(!memcmp(&try_sign, userinfo_recv.sake, 1)){
			printf("clnt wanna signup\n"); 
			db_result = wanna_signup(&userinfo_recv);
			DRCLNT register_result;  
			if(db_result == 1){ //register successed 
				memset(&(register_result.sake),1,1); 
			}
                        else if(db_result == 10){//id duplicate
                                memset(&(register_result.sake),10,1);
                        }
                        else if(db_result == 20){//pw duplicate
                                memset(&(register_result.sake),20,1);
                        }
			else{//register failed 
				memset(&register_result.sake, 0, 1); 
			}
			write(clnt_sock, &register_result, sizeof(DRCLNT));
		}

		if(!memcmp(&add_score, userinfo_recv.sake, 1)){
			puts("clint want to get point"); 
			if(!memcmp(&session_serv, userinfo_recv.id, 1)){
				puts("client win!\n"); 
				db_result = adding_score(&userinfo_recv, clnt_id); 
			}
		}
		if(!memcmp(&get_rank, userinfo_recv.sake, 1)){
			puts("clint want to see ranking"); 
			RANK* ranking_db = get_ranking_db(clnt_id); 
			write(clnt_sock, ranking_db, sizeof(RANK)); 
		}
		getting ++; 
	}
	
	pthread_mutex_lock(&mutex); 
	for(i=0; i<client_count; i++){
		if(clnt_sock == client_socks[i]){
			while(i++<client_count -1)
				client_socks[i] = client_socks[i+1]; 
				break; 
		}
	}
	client_count--; 
	pthread_mutex_unlock(&mutex); 
	close(clnt_sock); 
	return NULL; 
}
