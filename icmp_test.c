#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <netinet/in_systm.h>
#include <netinet/in.h>
#include <netinet/ip.h>
#include <netinet/ip_icmp.h>
#include <signal.h>

unsigned short check_sum(unsigned short *addr, int len);

int main(int argc, char *argv[]){
  int sd;
  int len;
  unsigned short seq = 0x01;

  char *rx_packet = malloc(BUFSIZ);
  char *tx_packet = malloc(BUFSIZ);

  struct iphdr *rx_iph;
  struct icmphdr *rx_icmph;
  struct iphdr *tx_iph;
  struct icmphdr *tx_icmph;

  struct sockaddr_in local, remote;

  pid_t id = htons(getpid());

  if(argc != 2){
    printf("USAGE : ping [IP ADDRESS]\n");
    exit(-1);
  }

  if((sd = socket(PF_INET, SOCK_RAW, IPPROTO_ICMP)) < 0){
    printf("socket open error\n");
    exit(-1);
  }

  while(1){
    bzero(tx_packet, BUFSIZ);

    tx_icmph = (struct icmphdr *)(tx_packet);
    tx_icmph->type = ICMP_ECHO;
    tx_icmph->code = 0;
    tx_icmph->un.echo.id = id;
    tx_icmph->un.echo.sequence = htons(seq++);
    tx_icmph->checksum = 0;

    tx_icmph->checksum = check_sum((unsigned short *)tx_icmph, sizeof(*tx_icmph));

    bzero(&remote, sizeof(remote));
    remote.sin_addr.s_addr = inet_addr(argv[1]);
    remote.sin_family = AF_INET;

    if((len = sendto(sd, tx_icmph, sizeof(*tx_icmph), 0, (struct sockaddr *)&remote, sizeof(remote))) < 0){
      printf("sendto error\n");
      exit(-2);
    }
    
    
    if((len = recvfrom(sd, rx_packet, BUFSIZ, 0, NULL, NULL)) < 0){
      printf("recvfrom error\n");
      exit(-2);
    }

    rx_iph = (struct iphdr *)(rx_packet);

    if(rx_iph->protocol != 0x01){
      continue;
    }

    rx_icmph = (struct icmphdr *)(rx_packet + rx_iph->ihl * 4);

    if(rx_icmph->type != ICMP_ECHOREPLY){
      printf("type 0x%04x\n", rx_icmph->type);
      printf("%d Bytes from %s %dTTL \n", ntohs(rx_iph->tot_len), inet_ntoa(rx_iph->saddr), rx_iph->ttl);
      return -1;
      //continue;
    }

    if(rx_icmph->un.echo.id != id){
      printf("id 0x%04x\n", ntohs(rx_icmph->un.echo.id));
      return -1;
      //continue;
    }

    if(ntohs(rx_icmph->un.echo.sequence) != (seq-1)){
      printf("seq 0x%04x 0x%04x\n", ntohs(rx_icmph->un.echo.sequence), seq-1);
      return -1;
      //continue;
    }

    printf("%d Bytes from %s %dTTL \n", ntohs(rx_iph->tot_len), inet_ntoa(rx_iph->saddr), rx_iph->ttl);

  }
  close(sd);

  return 0;
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