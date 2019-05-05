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


long long int lrta_calls;
long long int lrta_expansions;
long long int lrta_updates;

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

int lrta(Node *node)
{
  int index;
  float W=0.75;

  int converged=1;

  while (1) {
    int blank=node->blank;
    if (node->h0 == 0) return converged;     /* goal state has been found */
    int min = LARGE;
    float min_cost = LARGE;
    Node *min_child=NULL;
    
    ++lrta_expansions;
    
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
      
      child = SearchInsert(child_state,newblank,node->hash_value+hash_increment[tile][newblank][blank],node->h0+increment[tile][newblank][blank]);   
      
      if (min>child->h+1) {
	min=child->h+1;
      }

      if (min_cost>child->h0+1+W*(child->h-child->h0)) {
	min_cost=1+child->h0+W*(child->h-child->h0); // 1+child->h0 + w*Delta-h
	min_child=child;
      }
    }
    
    if (node->h < min) {
      converged=0;
      node->h = min; 
      ++lrta_updates;
    }
    if (node==NULL) {
      printf("next node is NULL, exiting"); exit(1);
    }
    node->trace=min_child;
    node=min_child;
  }
  return converged;
}


int lrta_driver(int start_state[SIZE], int blank)
{
  //int i;
  lrta_calls=lrta_expansions=lrta_updates=0;
  
  // int flag = 0;
  uint64_t intstate=state_to_int64(start_state);
  //  printf("start_state=%"PRIu64"\n",intstate);print_state(intstate);
  Node * start_node=SearchInsert(intstate,blank,hash_value(start_state),heuristic(start_state));
  //  i=0;
  // while(!flag) {
  //   if (i>1) break;
  /*flag =*/ lrta(start_node);
    ++lrta_calls;
    //  ++i;
    // }
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
    
    steps=lrta_driver(s,blank);
    
    gettimeofday (&etv,&etz);
    if (etv.tv_usec>stv.tv_usec){
      thistime=(etv.tv_sec-stv.tv_sec)+(etv.tv_usec-stv.tv_usec)/1000000.0;}
    else{
      thistime=(etv.tv_sec-stv.tv_sec)+(1000000.0+etv.tv_usec-stv.tv_usec)/1000000.0;}
    
    add_record(steps,lrta_expansions,lrta_calls,lrta_updates,hashcount,hashmaxlength,thistime);

#ifndef SUCCINCT
    printf ("%3d %3d %6lld %8lld %6lld %6lld %6lld %3.2f\n",problem,steps,lrta_calls,lrta_expansions,lrta_updates,hashcount,hashmaxlength,thistime);
#endif
  }
#ifdef SUCCINCT
  printf("%d\t%f\t",bound,denominator);
#endif
  print_stats();

  return 0;
}
