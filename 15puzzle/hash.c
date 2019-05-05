#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <assert.h>
#include <inttypes.h>
#include "include.h"
#include "puzzle.h"
#include "hash.h"
#include "mm.h"


#define LARGE_PRIME 961748941

Nodeptr hash_array[MAXHASH];
long long hashcount;
long long hashmaxlength;
long long ipow_table[SIZE];
long long hash_increment[SIZE][SIZE][SIZE];


long long ipow(int base,int exponent) {
  int i;
  long long int result=1;
  for (i=1;i<=exponent;++i) {
    result*=base;
  }
  return result;
}

void init_ipow() {
  int i;
  for (i=0; i<SIZE; i++) {
    ipow_table[i]=ipow(SIZE-1,i);
  }
}

long long hash_value(const int *s) {  /* hash value for a state */
  long long hash_value=0;
  int i;
  for (i=0;i<SIZE;i++) {
    hash_value=(hash_value+s[i]*ipow_table[i])%LARGE_PRIME;
  }
  return hash_value;
}

void init_hash_increments() /* incr eval function: tile, source, dest */
{
  int tile;                                               /* tile to be moved */
  int source, dest;                       /* source and destination positions */
  int destindex;                       /* destination index in operator table */
  
  for (tile = 1; tile < SIZE; tile++)                   /* all physical tiles */
    for (source = 0; source < SIZE; source++)   /* all legal source positions */
      for (destindex = 0; destindex < oprs[source].num; destindex++) 
	/* legal destinations of source */
	{
	  dest = oprs[source].pos[destindex];    /* dest is new blank position */
	  hash_increment[tile][source][dest]  = tile*(ipow_table[dest]-ipow_table[source])%LARGE_PRIME;
	}
}


/* Intializes the hash table */

void InitHashTable()
{
  int i;
  hashcount=0;
  hashmaxlength=0;
  for (i = 0;i < MAXHASH; i++) 
    hash_array[i] = NULL;
}


/* Returns the position in the table for a string */

void ClearHashTable() {
  int pos;
  hashcount=0;
  hashmaxlength=0;
  for (pos=0; pos<MAXHASH ;++pos) {
    hash_array[pos]=NULL;
  }
  mm_discardall();
}


Node * SearchInsert(const uint64_t s, int blank, long long hashval, int heuristic)
{
  int i;
  hashval+=LARGE_PRIME;  /* because we use increments we make sure hashval is in the correct range */
  hashval%=LARGE_PRIME;
  int pos = hashval%MAXHASH; 
  Nodeptr *idptr; 
  
  int length=0;
  for (idptr = &hash_array[pos]; *idptr ; idptr = &((*idptr)->next)) {
    ++length;
    if (hashval==(*idptr)->hash_value && blank==(*idptr)->blank && (*idptr)->state==s) 
      goto end;
  }
  *idptr = (Nodeptr) mm_malloc(sizeof(Node));
  (*idptr)->state=s;
  (*idptr)->h = (*idptr)->h0 = heuristic;
  (*idptr)->hash_value = hashval;
  (*idptr)->visited = 0;
  (*idptr)->g = LARGE;
  (*idptr)->blank = blank;
  (*idptr)->next = NULL;
  (*idptr)->trace = NULL;
  (*idptr)->follow = NULL; 
  (*idptr)->back = NULL; 
  (*idptr)->bound = 0;
  (*idptr)->search = 0;
  
  for (i=0; i<MAX_HEAP; i++)
    (*idptr)->heap_index[i]=0;

      
  ++hashcount;
 end:
  if (hashmaxlength<length) hashmaxlength=length;
  return (*idptr); 
} 

  
