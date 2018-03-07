#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <signal.h>
#include <sys/socket.h>
#include <netinet/in_systm.h>
#include <netinet/in.h>
#include <netinet/ip.h>
#include <netinet/ip_icmp.h>
#include <sys/time.h>

#define RECV_SUCC 0
#define RECV_FAIL 1

void send_request(unsigned char *);
int recv_response(unsigned char *, struct iphdr **, struct icmp **);
unsigned short check_sum(unsigned short *, int);
void tv_sub(struct timeval *, struct timeval *);

int sd;
struct sockaddr_in remote;
pid_t id;
unsigned short seq = 0x01;
int tx_icmp_data_size = 56;

int main(int argc, char *argv[]){
  unsigned char *rx_packet = malloc(BUFSIZ);
  unsigned char *tx_packet = malloc(BUFSIZ);
  struct iphdr *rx_iph;
  struct icmp *rx_icmph;
  struct timeval tv_recv;
  struct timeval *tv_snd;
  double rtt;

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

  printf("PING %s %d(%d) bytes of data\n", argv[1], tx_icmp_data_size, (20 + ICMP_MINLEN + tx_icmp_data_size));

  while(1){
    send_request(tx_packet);
    
    while(recv_response(rx_packet, &rx_iph, &rx_icmph) == RECV_FAIL);

    ioctl(sd, SIOCGSTAMP, &tv_recv);
    tv_snd = (struct timeval *)rx_icmph->icmp_data;
    tv_sub(&tv_recv, tv_snd);
    rtt = tv_recv.tv_sec * 1000.0 + tv_recv.tv_usec / 1000.0;

    printf("%d bytes from %s icmp_seq=%d ttl=%d times=%.1f ms\n", (ntohs(rx_iph->tot_len) - rx_iph->ihl*4), inet_ntoa(rx_iph->saddr), ntohs(rx_icmph->icmp_seq), rx_iph->ttl, rtt);
    sleep(1);
  }
  
  close(sd);
  free(tx_packet);
  free(rx_packet);
  return 0;
}

void send_request(unsigned char *tx_packet){
    bzero(tx_packet, sizeof(*tx_packet));
    struct icmp *tx_icmph = (struct icmp *)(tx_packet);

    tx_icmph->icmp_type = ICMP_ECHO;
    tx_icmph->icmp_code = 0;
    tx_icmph->icmp_id = id;
    tx_icmph->icmp_seq = htons(seq++);
    gettimeofday((struct timeval *)tx_icmph->icmp_data, NULL);
    memset((tx_icmph->icmp_data + sizeof(struct timeval)), 0x01, tx_icmp_data_size-sizeof(struct timeval));
    tx_icmph->icmp_cksum = 0;
    tx_icmph->icmp_cksum = check_sum((unsigned short *)tx_icmph, ICMP_MINLEN + tx_icmp_data_size);

    if((sendto(sd, tx_icmph, (ICMP_MINLEN + tx_icmp_data_size), 0, (struct sockaddr *)(&remote), sizeof(remote))) < 0){
      printf("sendto error\n");
      exit(-1);
    }
}

int recv_response(unsigned char *rx_packet, struct iphdr **rx_iph, struct icmp **rx_icmph){
  bzero(rx_packet, sizeof(*rx_packet));
  
  if((recvfrom(sd, rx_packet, BUFSIZ, 0, NULL, NULL)) < 0){
    printf("recvfrom error\n");
    exit(-1);
  }

  *rx_iph = (struct iphdr *)(rx_packet);

  if((*rx_iph)->protocol != IPPROTO_ICMP){
    return RECV_FAIL;
  }

  if((*rx_iph)->saddr != remote.sin_addr.s_addr){
    return RECV_FAIL;
  }
  
  *rx_icmph = (struct icmp *)(rx_packet + (*rx_iph)->ihl * 4);

  if((*rx_icmph)->icmp_type != ICMP_ECHOREPLY){
    return RECV_FAIL;
  }

  if((*rx_icmph)->icmp_id != id){
    return RECV_FAIL;
  }

  if(ntohs((*rx_icmph)->icmp_seq) != (seq-1)){
    return RECV_FAIL;
  }

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

void tv_sub(struct timeval *out, struct timeval *in){
  if((out->tv_usec -= in->tv_usec) < 0){
    --(out->tv_sec);
    out->tv_usec += 1000000;
  }

  out->tv_sec -= in->tv_sec;
}