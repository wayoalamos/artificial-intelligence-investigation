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
#include "stateheap.h"

#define MIN(X,Y) ((X) < (Y) ? (X) : (Y))
#define MAX(X,Y) ((X) > (Y) ? (X) : (Y))


long long int astar_expansions;
long long int astar_generated;
long long int astar_calls;
double W;
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
  printf("hola");
  print_solution(n);
  int size;
  for (size=0;n;n=n->trace,size++);
  return size-1;
}



int astar(int start_state[SIZE], int blank)
{
  int index;

  astar_calls=astar_expansions=astar_generated=0;

  uint64_t intstate=state_to_int64(start_state);

  Node * start_node=SearchInsert(intstate,blank,hash_value(start_state),heuristic(start_state));
  heap *open = new_heap(0,2);


  ++astar_generated;
  start_node->g=0;
  start_node->key[0]=W*start_node->h;
  start_node->key[1]=0;

  insert_heap(open,start_node);

  while (top_heap(open)->h0!=0) {
    Node *node=pop_heap(open);
    int blank=node->blank;

    ++astar_expansions;

    //  printf(".");fflush(stdout);

    for (index = 0; index < oprs[blank].num; index++) {     /* for each appl opr */
      int newblank;
      int tile;
      Node *child;
      uint64_t child_state;
      newblank=oprs[blank].pos[index];

      // if (astar_expansions%100==0) printf("%ld ",open->size);

      tile = get_tile(node->state,newblank);

      child_state=node->state;
      new_int_state(&child_state,blank,newblank);

      child = SearchInsert(child_state,newblank,node->hash_value+hash_increment[tile][newblank][blank],node->h0+increment[tile][newblank][blank]);

      if (child->g==LARGE) ++astar_generated;

      int newg=node->g+1;


      if (child->g > newg) {
	child->g=newg;
	child->key[0]=child->g+W*child->h;
	child->key[1]=-child->g;
	child->back=node;
	insert_heap(open,child);
      }
    }
  }

  Node *n=top_heap(open);
  for (n=top_heap(open); n->back; n=n->back)
    n->back->trace=n;

  return solution_size(start_node);
}



int main(int argc, char **argv)
{
  int blank;                                    /* initial position of blank */
  int problem;                                           /* problem instance */


  struct timeval stv,etv;
  struct timezone stz,etz;
  float thistime;

  if (argc<2) {
    printf("Usage: %s <w>\n", argv[0]);
    return 0;
  }
  W=atof(argv[1]);


  initops();                                   /* initialize operator table */
  init(increment);                        /* initialize evaluation function */
  mm_init();                              /* initialize memory manager */
  InitHashTable();                         /* initialize Hash Table */
  init_ipow();
  init_hash_increments();                 /* initialize increments in hash table */

#ifndef SUCCINCT
  printf ("%3s %2s %6s %8s %6s %6s %6s %3s\n","#p","len","#calls","#exp","#gen","hashcnt","hashmax","time");
#endif
  for (problem = 0; problem <= 0; problem++){ /* for each initial state */
    int steps;
    blank = input(s);                                 /* input initial state */
    gettimeofday (&stv,&stz);
    ClearHashTable();                    /* clear the hash table */

    steps=astar(s,blank);

    gettimeofday (&etv,&etz);
    if (etv.tv_usec>stv.tv_usec){
      thistime=(etv.tv_sec-stv.tv_sec)+(etv.tv_usec-stv.tv_usec)/1000000.0;}
    else{
      thistime=(etv.tv_sec-stv.tv_sec)+(1000000.0+etv.tv_usec-stv.tv_usec)/1000000.0;}

    add_record(steps,astar_expansions,1,astar_generated,hashcount,hashmaxlength,thistime);

#ifndef SUCCINCT
    printf ("%3d %3d %6d %8lld %6lld %6lld %6lld %3.2f\n",problem,steps,1,astar_expansions,astar_generated,hashcount,hashmaxlength,thistime);
#endif
  }
#ifdef SUCCINCT
  printf("%d\t%f\t",bound,denominator);
#endif
  print_stats();

  return 0;
}
