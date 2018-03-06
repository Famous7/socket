#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <netinet/in_systm.h>
#include <netinet/in.h>
#include <netinet/ip.h>
#include <netinet/ip_icmp.h>
#include <signal.h>

#define RECV_SUCC 0
#define RECV_FAIL 1

void send_request(unsigned char *);
int recv_response(unsigned char *);
unsigned short check_sum(unsigned short *addr, int len);

int sd;
struct sockaddr_in remote;
pid_t id;
unsigned short seq = 0x01;

int main(int argc, char *argv[]){
  unsigned char *rx_packet = malloc(BUFSIZ);
  unsigned char *tx_packet = malloc(BUFSIZ);

  if(argc != 2){
    printf("USAGE : ping [IP ADDRESS]\n");
    exit(-1);
  }

  bzero(&remote, sizeof(remote));
  remote.sin_addr.s_addr = inet_addr(argv[1]);
  remote.sin_family = AF_INET;
  pid_t id = htons(getpid()) & 0xffff;

  if((sd = socket(PF_INET, SOCK_RAW, IPPROTO_ICMP)) < 0){
    printf("socket open error\n");
    exit(-1);
  }

  while(1){
    send_request(tx_packet);

    while(recv_response(rx_packet) == RECV_FAIL);

    sleep(1);
  }
  
  close(sd);
  free(tx_packet);
  free(rx_packet);
  return 0;
}

void send_request(unsigned char *tx_packet){
    bzero(tx_packet, sizeof(*tx_packet));
    struct icmphdr *tx_icmph = (struct icmphdr *)(tx_packet);

    tx_icmph->type = ICMP_ECHO;
    tx_icmph->code = 0;
    tx_icmph->un.echo.id = id;
    tx_icmph->un.echo.sequence = htons(seq++);
    tx_icmph->checksum = 0;
    tx_icmph->checksum = check_sum((unsigned short *)tx_icmph, sizeof(*tx_icmph));

    if((sendto(sd, tx_icmph, sizeof(*tx_icmph), 0, (struct sockaddr *)(&remote), sizeof(remote))) < 0){
      printf("sendto error\n");
      exit(-1);
    }
}

int recv_response(unsigned char *rx_packet){
  static struct iphdr *rx_iph;
  static struct icmphdr *rx_icmph;
  static struct sockaddr_in recv;
  static int len = sizeof(recv);

  bzero(rx_packet, sizeof(*rx_packet));
  bzero(&recv, sizeof(recv));
  
  if((recvfrom(sd, rx_packet, BUFSIZ, 0, (struct sockaddr *)&recv, &len)) < 0){
    printf("recvfrom error\n");
    return RECV_FAIL;
  }

  rx_iph = (struct iphdr *)(rx_packet);

  if(rx_iph->protocol != 0x01){
    return RECV_FAIL;
  }

  if(rx_iph->saddr != remote.sin_addr.s_addr){
    return RECV_FAIL;
  }
  
  rx_icmph = (struct icmphdr *)(rx_packet + rx_iph->ihl * 4);

  if(rx_icmph->type != ICMP_ECHOREPLY){
    return RECV_FAIL;
  }

  if(rx_icmph->un.echo.id != id){
    return RECV_FAIL;
  }

  if(ntohs(rx_icmph->un.echo.sequence) != (seq-1)){
    return RECV_FAIL;
  }

  printf("%d Bytes from %s %dTTL \n", ntohs(rx_iph->tot_len), inet_ntoa(rx_iph->saddr), rx_iph->ttl);
  return RECV_SUCC;
}

unsigned short check_sum(unsigned short *ip, int len){
  unsigned long sum = 0;
  unsigned short odd = 0;

  while(len > 1){
    sum += *ip++;
    len -= 2;
  }

  if(len == 1){
    *(unsigned char *)(&odd) = (*(unsigned char *)ip);
    sum += odd;
  }

  while(sum >> 16)
    sum = (sum >> 16) + (sum & 0xffff);

  return ~sum;
}
