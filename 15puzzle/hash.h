#ifndef HASH_H
#define HASH_H

#include <inttypes.h>

/*#define MAXHASH 7057 */
//#define MAXHASH 104729
//#define MAXHASH 1046527
#define MAXHASH 29005511
#define MAX_HEAP 2
#define MAX_KEYS 2


typedef struct Node {
  uint64_t state;
  int blank;
  short int visited;
  long long hash_value;
  int bound;             /* lrta bound */
  double h;
  int search;            /* used by RTAA */
  int g;                 /* used by A* search */
  int h0;                /* original h-value */
  struct Node *trace;    /* child of the node in an A* path */
  struct Node *follow;    /* set by RTAA to the node the algorithm went after this one */
  struct Node *previous;    /* set by TBA to allow a back move */
  struct Node *back;      /* previous node (used by A* search) */
  struct Node *next;     /* next in the hash table */
  int heap_index[MAX_HEAP];
  double key[MAX_HEAP*MAX_KEYS];
} Node, *Nodeptr;


Node * SearchInsert(const uint64_t s, int blank, long long hash_value, int heuristic);
long long hash_value(const int *s);
void InitHashTable();
void ClearHashTable();
void init_ipow();
void init_hash_increments();

extern long long hashcount;
extern long long hashmaxlength;
extern long long hash_increment[SIZE][SIZE][SIZE];

#endif
