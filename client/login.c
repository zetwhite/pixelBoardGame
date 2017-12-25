#include "base_header.h" 
#include "utility.h"
#include <errno.h> 
#include <signal.h> 
#include <sys/wait.h> 

void *send_msg(void *arg, void* msg); 
void *recv_msg(void *arg);
char msg[BUF_SIZE];
int sock;
unsigned char session; 
struct sockaddr_in serv_addr;

struct logininfo pointerentry; 
void send_login_try(GtkWidget *widget, struct logininfo* pointerentry);
void send_register_try(GtkWidget *widget, int* register_clicked);
void quit(void); 
void pixel_game_making(void); 
void exit_window_making(void); 
void getting_making_ranking(void);  

GtkWidget *login_window; 
GtkWidget *login_button; 
GtkWidget *register_button; 
int register_clicked = 0; 
GtkWidget *login_table; 
GtkEntry *id_text; 
GtkEntry *pw_text; 
GtkEntry *email_text; 
GtkLabel *id_label;
GtkLabel *pw_label; 
GtkLabel *email_label; 
GtkLabel *notice; 
GtkLabel *noticetwo; 


//for eixt window 
GtkWidget *exit_window;
GtkWidget *exit_button;
GtkWidget *continue_button;
GtkWidget *ranking_button;
GtkWidget *button_table;

int main(int argc, char*argv[]){
//========================SOCK READY============================================
        sock = socket(PF_INET, SOCK_STREAM, 0);
        memset(&serv_addr, 0, sizeof(serv_addr));
        serv_addr.sin_family = AF_INET;
        serv_addr.sin_addr.s_addr = inet_addr("114.206.206.193"); //server ip address
        serv_addr.sin_port=htons(atoi("8080"));

        if(connect(sock, (struct sockaddr*)&serv_addr, sizeof(serv_addr)) == -1){
                printf("%s\n", strerror(errno)); 
		error_handling("connect() error!");
		printf("%s", strerror(errno)); 
	}

//=========================GUI PROG==============================================
	gtk_init(&argc, &argv); 

	login_window = gtk_window_new(GTK_WINDOW_TOPLEVEL); 
	gtk_window_set_title(GTK_WINDOW(login_window), "ROONMAP::enter"); 
	gtk_window_set_default_size(GTK_WINDOW(login_window), 300, 150); 
	gtk_window_set_position(GTK_WINDOW(login_window), GTK_WIN_POS_CENTER); 
	gtk_signal_connect(GTK_OBJECT(login_window), "destroy", GTK_SIGNAL_FUNC(quit), NULL); 
	
        login_table = gtk_table_new(4, 6, FALSE);

	id_label = gtk_label_new("id");  
	pw_label = gtk_label_new("pw");  
	email_label = gtk_label_new("email"); 
	gtk_table_attach(GTK_TABLE(login_table), id_label, 0,1,0,1, GTK_EXPAND, GTK_SHRINK, 0, 4);
	gtk_table_attach(GTK_TABLE(login_table), pw_label, 0,1,1,2, GTK_EXPAND, GTK_SHRINK, 0,4);
	gtk_table_attach(GTK_TABLE(login_table), email_label, 0,1,2,3, GTK_EXPAND, GTK_SHRINK, 0,4); 
	

	id_text = gtk_entry_new_with_max_length(16);
        pw_text = gtk_entry_new_with_max_length(16);
        gtk_entry_set_visibility(pw_text, FALSE);
        email_text = gtk_entry_new_with_max_length(30);
        gtk_table_attach(GTK_TABLE(login_table), id_text, 1, 4, 0, 1,GTK_EXPAND, GTK_SHRINK,0,4);
        gtk_table_attach(GTK_TABLE(login_table), pw_text, 1, 4, 1, 2, GTK_EXPAND, GTK_SHRINK,0,4);
	gtk_table_attach(GTK_TABLE(login_table), email_text,1, 4, 2,3, GTK_EXPAND, GTK_SHRINK,0,4);  

	pointerentry.id_text_st = id_text;
        pointerentry.pw_text_st = pw_text;

	login_button = gtk_button_new_with_label("LOGIN");
        register_button = gtk_button_new_with_label("Didn't you Register yet?");

        gtk_signal_connect(GTK_OBJECT(login_button), "clicked", GTK_SIGNAL_FUNC(send_login_try), &pointerentry);  
        gtk_table_attach(GTK_TABLE(login_table), login_button, 4, 6, 0, 2, GTK_EXPAND, GTK_EXPAND, 8, 8);
	
	gtk_signal_connect(GTK_OBJECT(register_button), "clicked", GTK_SIGNAL_FUNC(send_register_try), &register_clicked); 
	gtk_table_attach(GTK_TABLE(login_table), register_button, 1,6, 3,4, GTK_EXPAND, GTK_SHRINK, 8, 6);	

	notice = gtk_label_new(""); 
	gtk_table_attach(GTK_TABLE(login_table), notice, 4,6,0,2, GTK_SHRINK, GTK_SHRINK, 0, 0); 
	
	noticetwo = gtk_label_new("id or pw is wrong"); 
	gtk_table_attach(GTK_TABLE(login_table), noticetwo, 1,4,2,3,GTK_EXPAND, GTK_SHRINK, 0, 4); 

	gtk_container_add(GTK_CONTAINER(login_window), login_table); 
	gtk_widget_show(id_label); 
	gtk_widget_show(pw_label); 
	gtk_widget_show(id_text); 
	gtk_widget_show(pw_text); 
	gtk_widget_show(login_button); 
	gtk_widget_show(register_button); 
	gtk_widget_show(login_table); 
	gtk_widget_show(login_window); 

//=========================SOCK PROG==============================================
	gtk_main(); 
	return 0; 
}

//=======================fucn definition============================================
void* recv_msg(void * arg){
	int sock = *((int*)arg); 
	char message_address[BUF_SIZE]; 
	int str_len; 
	while(1){
		str_len=read(sock, message_address, BUF_SIZE -1); 
		if(str_len = -1) 
			return (void*)-1; 
		message_address[str_len] = 0; 
		fputs(message_address, stdout); 
	}
	return NULL; 
}

void send_login_try(GtkWidget *widget, struct logininfo* pointerentry){
        g_print("login button is clicked\n");
        const gchar* id_text_c = gtk_entry_get_text(GTK_ENTRY(pointerentry->id_text_st));
        const gchar* pw_text_c = gtk_entry_get_text(GTK_ENTRY(pointerentry->pw_text_st));
        printf(" id : %s\n",id_text_c);
        printf(" pw : %s\n",pw_text_c);

        UF login_packet;
	login_packet.start_mark = 1; 
        memset(&(login_packet.sake), 1, 1);
        memset(&(login_packet.id_length),strlen(id_text_c),1);
        memset(&(login_packet.pw_length),strlen(pw_text_c),1);
        memset(&(login_packet.email_length),0,1);
        memcpy((void*)&login_packet.id, (void*)id_text_c, strlen(id_text_c)); 
	memcpy((void*)&login_packet.pw, (void*)pw_text_c, strlen(pw_text_c));  
        memset(&(login_packet.email),0,30);
	write(sock, &login_packet, sizeof(UF));
        printf("send message to server\n");

	DRCLNT result_recv; 
	unsigned char login_success = 3; 
	unsigned char login_fail = 2; 
	
	read(sock, &result_recv, sizeof(DRCLNT)); 
	if(!memcmp(&login_fail, &(result_recv.sake),1)){
		gtk_widget_show(noticetwo); 
		//login fail 
	} 
	else if(!memcmp(&login_success, &(result_recv.sake), 1)){
		session = result_recv.session; 
		gtk_widget_hide(noticetwo);
		gtk_widget_hide(login_window);
		pixel_game_making(); 
	}
	return NULL; 
}

void send_register_try(GtkWidget *widget, int* register_clicked){
	if(*register_clicked == 0){
		gtk_widget_hide(noticetwo); 
		gtk_widget_show(email_label); 
		gtk_widget_show(email_text); 
		gtk_button_set_label(register_button,"submit"); 
		*register_clicked = 1; 
		gtk_widget_hide(login_button); 
		return NULL;  
	}
	if(*register_clicked == 1){
		const gchar* id_text_c = gtk_entry_get_text(GTK_ENTRY(id_text)); 
		const gchar* pw_text_c = gtk_entry_get_text(GTK_ENTRY(pw_text)); 
		const gchar* email_text_c = gtk_entry_get_text(GTK_ENTRY(email_text)); 
		printf("email : %s\n", email_text_c); 
		UF register_packet; 
		memset(&(register_packet.sake), 0, 1); 
		memset(&(register_packet.id_length),strlen(id_text_c),1); 
		memset(&(register_packet.pw_length),strlen(pw_text_c),1); 
		memset(&(register_packet.email_length),strlen(email_text_c), 1); 
		memcpy((void*)&register_packet.id, (void*)id_text_c, strlen(id_text_c)); 
		memcpy((void*)&register_packet.pw, (void*)pw_text_c, strlen(pw_text_c));
		memcpy((void*)&register_packet.email, (void*)email_text_c, strlen(email_text_c));
		write(sock, &register_packet, sizeof(UF)); 
		printf("send to message to server\n"); 
		
		DRCLNT result_recv; 
		unsigned char register_success = 1; 
		unsigned char register_failed = 0; 
		unsigned char id_duplicate = 10; 
		unsigned char pw_duplicate = 20; 
		 
		read(sock, &result_recv, sizeof(DRCLNT));
		if(!memcmp(&register_failed,&(result_recv.sake),1)){
			printf("register failed\n");
			gtk_label_set_text(notice, "sorry, some connection error;\n plz contact roonm813@naver.com"); 
			gtk_widget_show(notice); 
			return NULL; 			
		}
		if(!memcmp(&id_duplicate , &(result_recv.sake), 1)){
			printf("id duplicate\n"); 
			gtk_label_set_text(notice, "Oops, ID duplicate!"); 
			gtk_widget_show(notice); 
			return NULL; 
		}
                if(!memcmp(&pw_duplicate, &(result_recv.sake), 1)){
                        printf("pw duplicate\n");
                        gtk_label_set_text(notice, "Oops, Password duplicate!");
                        gtk_widget_show(notice);
                        return NULL;
                }
		gtk_widget_hide(email_label); 
		gtk_widget_hide(email_text);
		gtk_button_set_label(register_button, "try login now :)");  
		gtk_widget_hide(notice);  
		gtk_widget_show(login_button); 
		*register_clicked = 0; 
		return NULL; 
	}
}

void quit(void){
        gtk_main_quit();
        close(sock);
        exit(0);
}  

void exit_window_making(void){

        exit_window = gtk_window_new(GTK_WINDOW_TOPLEVEL);
        gtk_window_set_title(GTK_WINDOW(exit_window), "thank you XD");
        gtk_window_set_default_size(GTK_WINDOW(exit_window), 150, 50);
        gtk_window_set_position(GTK_WINDOW(exit_window), GTK_WIN_POS_CENTER);

        button_table = gtk_table_new(1,3,FALSE);

        exit_button = gtk_button_new_with_label("exit");
        continue_button = gtk_button_new_with_label("new game");
        ranking_button = gtk_button_new_with_label("show ranking");

        gtk_table_attach(GTK_TABLE(button_table), exit_button, 0,1,0,1, GTK_EXPAND, GTK_EXPAND, 0, 0);
        gtk_table_attach(GTK_TABLE(button_table), continue_button, 1,2,0,1, GTK_EXPAND, GTK_EXPAND, 0, 0);
        gtk_table_attach(GTK_TABLE(button_table), ranking_button, 2,3,0,1, GTK_EXPAND, GTK_EXPAND, 0, 0);

        gtk_signal_connect(GTK_OBJECT(exit_button), "clicked", GTK_SIGNAL_FUNC(quit), NULL);
        gtk_signal_connect(GTK_OBJECT(continue_button),"clicked", GTK_SIGNAL_FUNC(pixel_game_making), NULL); 
	gtk_signal_connect(GTK_OBJECT(ranking_button), "clicked", GTK_SIGNAL_FUNC(getting_making_ranking), NULL); 

        gtk_container_add(GTK_CONTAINER(exit_window), button_table);
        gtk_widget_show(exit_button);
        gtk_widget_show(continue_button);
        gtk_widget_show(ranking_button);
        gtk_widget_show(button_table);
        gtk_widget_show(exit_window);
        gtk_main();
}

void pixel_game_making(void){
        int status;
        int end_value;
        pid_t pixelgame_process;
        pixelgame_process = fork();
        if(pixelgame_process == 0){//child porcess 
        	printf("here childprocess\n");
                execl("/usr/bin/python3", "python3", "Pixel.py", NULL);
        }
        else{//parent process 
                wait(&status);
                if(WIFEXITED(status)){
                	printf("pixel game end\n");
                        end_value = WEXITSTATUS(status);
                        printf("end_value : %d\n", end_value);
                        if(end_value== 4) //exit rignt how
                        	exit(1);
                        else if(end_value == 1){//winn sned to db
				puts("here!!"); 
                        	UF score_packet;
                                memset((score_packet.sake), 100, 1);
				int st = 100; 
				if(memcmp(&st, score_packet.sake, 1)!=0)
					puts("sth wrong"); 
				memset((score_packet.id), session, 1); 
                                write(sock, &score_packet, sizeof(UF));
                                puts("send to server the message\m");
                        }
              	}
       exit_window_making();
       }
}

void getting_making_ranking(void){
	UF get_ranking; 
	memset((get_ranking.sake), 200, 1); 
	write(sock, &get_ranking, sizeof(UF)); 
	puts("send to server the message\n"); 
	
	RNK rank_recv; 
	read(sock, &rank_recv, sizeof(RNK)); 
	char* rankf = rank_recv.id; 
	char* ranks = rank_recv.id + 17; 
	char *rankt = rank_recv.id + 34; 
	char *rank4 = rank_recv.id + 51; 
	char *rank5 = rank_recv.id + 68; 
		
	char rank_ch[100]; 
	sprintf(rank_ch,"%s%s\n%s%s\n%s%s\n%s%s\n%s%s","1 ", rankf, "2 ", ranks, "3 ", rankt, "4 ",rank4, "5 ", rank5);   

	GtkWidget *dialog; 
	dialog = gtk_about_dialog_new(); 
	gtk_about_dialog_set_name(GTK_ABOUT_DIALOG(dialog), "RANK");
	gtk_about_dialog_set_comments(GTK_ABOUT_DIALOG(dialog), rank_ch);
	gtk_dialog_run(GTK_DIALOG(dialog)); 
	gtk_widget_destroy(dialog);  
}
