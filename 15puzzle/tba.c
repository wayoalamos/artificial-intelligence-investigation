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

long int astar_expansions;
long int astar_generated;
long int astar_calls;
long int tba_updates;
long int tba_searches;
long int tba_steps;
long int tba_back_steps;
long int total_expansions;
int increment[SIZE][SIZE][SIZE]; /* table for heuristic increments */
double W;

int k;

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

int solution_size(Node *start, Node *end) {
  int size;
  Node *n;
  for (n=start,size=0;n!=end;n=n->trace,size++);
  return size;
}

long int solution_size_no_cycles(Node *n) {
  long int size;
  for (size=0;n->h0!=0;n=n->follow,size++);
  return size;
}

void initialize_state(Node *node, int search) {
  if (node->search!=search) {
    node->g=LARGE;  /* reset g-value if seen previously */
  }
}


void astar(heap * open, int search,Node **closed_list)
{
  int index;
  
  astar_calls=astar_expansions=astar_generated=0;

  while (top_heap(open)->h0!=0 && astar_expansions < k) {
    Node *node=pop_heap(open);
    int blank=node->blank;

    closed_list[astar_expansions]=node;

    ++astar_expansions;
    ++total_expansions;


    for (index = 0; index < oprs[blank].num; index++) {     /* for each appl opr */
      int newblank;
      int tile;
      Node *child;
      uint64_t child_state;
      newblank=oprs[blank].pos[index];
     
      
      tile = get_tile(node->state,newblank);
      
      child_state=node->state;
      new_int_state(&child_state,blank,newblank);
      
      child = SearchInsert(child_state,
			   newblank,
			   node->hash_value+hash_increment[tile][newblank][blank],
			   node->h0+increment[tile][newblank][blank]);   

      initialize_state(child,search);
      
      int newg=node->g+1;

      if (child->g > newg) {
	child->g=newg;
	child->key[0]=child->g+W*child->h;
	child->key[1]=-child->g;
	child->back=node;
	child->search=search;
	insert_heap(open,child);
      }
    }

  }

  //  Commenting out for TBA* to avoid doing this twice
  //  Node *n=top_heap(open);
  //  for (n=top_heap(open); n->back; n=n->back)
  //  n->back->trace=n;
}

// current: node for the agent position
// node: the best node in the open list
// this function returns true if current is in the A*
// path from root to node
// sets also trace pointers to from current to best if
// current is in the path from root to best
int in_path(Node *current, Node *node) {
  int flag=0;
  Node *previous = NULL;
  while (node->g >= current->g) {
    node->trace=previous;
    if (node==current) {
      flag=1;
      break;
    } else {
      previous=node;
      node=node->back;
    }
  }
  return flag;
}


long int tba(int start_state[SIZE], int blank)
{
   uint64_t intstate=state_to_int64(start_state);
   Node *node=SearchInsert(intstate,blank,hash_value(start_state),heuristic(start_state));
   Node *start_node=node;
   heap *open = new_heap(0,2);  
   tba_searches=0;
   tba_steps=0;
   tba_back_steps=0;
   tba_updates=0;
   Node **closed_list=(Node **) malloc(sizeof(Node*)*k);

   ++tba_searches;
   // insert root node into open
   node->g=0;
   node->key[0]=node->h;  
   node->key[1]=0;
   node->search=tba_searches;
   node->back=NULL;
   empty_heap(open);
   insert_heap(open,node);

   while (node->h0!=0) {
     Node *best;
     astar(open,tba_searches,closed_list);
     best=top_heap(open);

     if (in_path(node,best)) {
       if (best->h0==0) {      // we've found the goal so, move all the way

	 while (node!=best) {
	   node->follow=node->trace;
	   node=node->follow;
	   ++tba_steps;
	 }
       } else {
	 node->follow=node->trace;
	 node->follow->previous=node;
	 node=node->follow;
	 ++tba_steps;
       }
     } else {   // the node is not in the current path, so move back
       node=node->previous;
       ++tba_steps;
       ++tba_back_steps;
     }
   }

   return solution_size_no_cycles(start_node);
}

int main(int argc, char **argv)
{
  int blank;                                    /* initial position of blank */
  int problem;                                           /* problem instance */

  
  struct timeval stv,etv;
  struct timezone stz,etz;
  float thistime;

  if (argc<3) {
     printf("Usage: %s <w> <k>\n", argv[0]);
     return 0;
  }
  W=atof(argv[1]);
  k=atof(argv[2]);
  
  initops();                                   /* initialize operator table */
  init(increment);                        /* initialize evaluation function */
  mm_init();                              /* initialize memory manager */
  InitHashTable();                         /* initialize Hash Table */
  init_ipow();
  init_hash_increments();                 /* initialize increments in hash table */
  
#ifndef SUCCINCT
  printf ("%3s %7s %7s %7s %7s %8s %6s %6s %6s %3s\n","#p","len","steps","bsteps","searches","#exp","#upd","hashcnt","hashmax","time");
#endif
  for (problem = 1; problem <= NUMBER; problem++){ /* for each initial state */
    long int size;
    blank = input(s);                                 /* input initial state */
    gettimeofday (&stv,&stz);    
    ClearHashTable();                    /* clear the hash table */
    total_expansions=0;
    size=tba(s,blank);
    gettimeofday (&etv,&etz);
    if (etv.tv_usec>stv.tv_usec){
      thistime=(etv.tv_sec-stv.tv_sec)+(etv.tv_usec-stv.tv_usec)/1000000.0;}
    else{
      thistime=(etv.tv_sec-stv.tv_sec)+(1000000.0+etv.tv_usec-stv.tv_usec)/1000000.0;}
    add_record_tb(size,total_expansions,tba_steps,tba_back_steps,tba_updates,hashcount,hashmaxlength,thistime,tba_searches);

#ifndef SUCCINCT
    printf ("%3d %7ld %7ld %7ld %7ld %8ld %6ld %6lld %6lld %3.2f\n",problem,size,tba_steps,tba_back_steps,tba_searches,total_expansions,tba_updates,hashcount,hashmaxlength,thistime);
#endif
  }
  print_stats_tb();

  return 0;
}
