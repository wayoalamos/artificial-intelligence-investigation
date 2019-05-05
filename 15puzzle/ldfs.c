#include <stdio.h>                                   /* standard I/O library */ 
#include <stdlib.h>
#include <string.h>                                                /* memcpy */ 
#include <sys/time.h>                                       /* time handling */ 
#include <unistd.h>                                         /* time handling */ 
#include <inttypes.h>
#include "include.h"
#include "puzzle.h"
#include "hash.h"
#include "mm.h"
#include "stats.h"

#define LARGE 1000000000

#define MIN(X,Y) ((X) < (Y) ? (X) : (Y))
#define MAX(X,Y) ((X) > (Y) ? (X) : (Y))


long long int ldfs_calls;
long long int ldfs_expansions;
long long int ldfs_updates;

int increment[SIZE][SIZE][SIZE]; /* table for heuristic increments */

void print_state(uint64_t s) {
  int i;
  for (i=0; i<SIZE;++i) {
    printf("%3d",get_tile(s,i));
    if((i+1)%X==0) printf("\n");
  }
}

void print_node(Node *n) {
  printf("\n[%.1f]\n",n->h);print_state(n->state);
}

void print_solution(Node *n) {
  printf("Solution found:\n");
  for (;n;n=n->trace) {
    print_node(n);
  }
}

int solution_size(Node *n) {
  int size;
  for (size=0;n;n=n->trace,size++);
  return size-1;
}

int ldfs(Node *node)
{
  int min;
  int blank=node->blank;
  int index;
  int flag;
  if (node->h == 0) return 1;     /* goal state has been found */
  
  min = LARGE;
  ++ldfs_expansions;

  /*if (node->visited==1) printf("!");*/

  node->visited=1;
  //print_state(node->state);printf("[%d] - b=%d\n",node->h,bound);
  //  printf("h=%d b=%d\n",node->h,bound);

  blank=node->blank;
  for (index = 0; index < oprs[blank].num; index++) {     /* for each appl opr */
    int newblank;
    int tile;
    Node *child;
    uint64_t child_state;
    newblank=oprs[blank].pos[index];
    
    tile = get_tile(node->state,newblank);
    
    child_state=node->state;
    new_int_state(&child_state,blank,newblank);
    
    //printf("parent:\n");
    //print_state(node->state);printf("\nchild:\n");print_state(child_state);

    child = SearchInsert(child_state,newblank,node->hash_value+hash_increment[tile][newblank][blank],node->h0+increment[tile][newblank][blank]);   
    
    if (!child->visited && child->h+1 <= node->h) {
      node->trace=child;
      flag = ldfs(child);   /* recursive call over the child */
      if (flag) {
	node->visited=0;      
	return flag;
      }
    }

    if (min>child->h+1) {
      min=child->h+1;
    }
  
  }
  
  if (node->h < min) {
    node->h = min; 
    ++ldfs_updates;
  }
  
  node->visited=0;

  return 0;
}


int ldfs_driver(int start_state[SIZE], int blank)
{
  ldfs_calls=ldfs_expansions=ldfs_updates=0;
  
  int flag = 0;
  uint64_t intstate=state_to_int64(start_state);
  //  printf("start_state=%"PRIu64"\n",intstate);print_state(intstate);
  Node * start_node=SearchInsert(intstate,blank,hash_value(start_state),heuristic(start_state));
  while(!flag) {
    flag = ldfs(start_node);
    ++ldfs_calls;
  }
  //  print_solution(start_node);
  return solution_size(start_node);
}



int main(int argc, char **argv)
{
  int blank;                                    /* initial position of blank */
  int problem;                                           /* problem instance */

  
  struct timeval stv,etv;
  struct timezone stz,etz;
  float thistime;

  
  initops();                                   /* initialize operator table */
  init(increment);                        /* initialize evaluation function */
  mm_init();                              /* initialize memory manager */
  InitHashTable();                         /* initialize Hash Table */
  init_ipow();
  init_hash_increments();                 /* initialize increments in hash table */
  
#ifndef SUCCINCT
  printf ("%3s %2s %6s %8s %6s %6s %6s %3s\n","#p","len","#calls","#exp","#upd","hashcnt","hashmax","time");
#endif
  for (problem = 1; problem <= NUMBER; problem++){ /* for each initial state */
    int steps;
    blank = input(s);                                 /* input initial state */
    gettimeofday (&stv,&stz);    
    ClearHashTable();                    /* clear the hash table */
    
    steps=ldfs_driver(s,blank);
    
    gettimeofday (&etv,&etz);
    if (etv.tv_usec>stv.tv_usec){
      thistime=(etv.tv_sec-stv.tv_sec)+(etv.tv_usec-stv.tv_usec)/1000000.0;}
    else{
      thistime=(etv.tv_sec-stv.tv_sec)+(1000000.0+etv.tv_usec-stv.tv_usec)/1000000.0;}
    
    add_record(steps,ldfs_expansions,ldfs_calls,ldfs_updates,hashcount,hashmaxlength,thistime);

#ifndef SUCCINCT
    printf ("%3d %3d %6lld %8lld %6lld %6lld %6lld %3.2f\n",problem,steps,ldfs_calls,ldfs_expansions,ldfs_updates,hashcount,hashmaxlength,thistime);
#endif
  }
#ifdef SUCCINCT
  printf("%d\t%f\t",bound,denominator);
#endif
  print_stats();

  return 0;
}
