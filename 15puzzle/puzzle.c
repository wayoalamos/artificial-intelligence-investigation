#include <stdio.h>
#include <stdlib.h>
#include <inttypes.h>
#include "include.h"

uint64_t state_to_int64(int *s) {
  uint64_t n=0x0;
  int i;
  for (i=0; i<SIZE; i++) {
    n|=(uint64_t) s[i]<<(i*4);
  }
  return n;
}

void int64_to_state(int64_t intstate,int *s) {
  int i;
  for (i=0; i<SIZE;i++) {
    uint64_t mask=0xf<<i;
    s[i]=(intstate&mask)>>i;
  }
}

int get_tile(uint64_t state,int position) {
  uint64_t mask=(uint64_t) 0xf<<(position*4);
  uint64_t element=(state&mask)>>(position*4);
  return element;
}
void new_int_state(uint64_t *state,int oldblank,int newblank) {
  uint64_t mask=(uint64_t) 0xf<<(newblank*4);
  uint64_t element=(*state&mask)>>(newblank*4);
  *state=(*state&~mask)|(element<< (oldblank*4));
}


/* INITOPS initializes the operator table. */

void initops () {
  int blank;                                   /* possible positions of blank */
  for (blank = 0; blank < SIZE; blank++)  /* for each possible blank position */
    {
      oprs[blank].num = 0;                               /* no moves initially */
      if (blank > X - 1)                                       /* not top edge */
	oprs[blank].pos[oprs[blank].num++] = blank - X;       /* add a move up */
      if (blank % X > 0)                                      /* not left edge */
	oprs[blank].pos[oprs[blank].num++] = blank - 1;     /* add a move left */
      if (blank % X < X - 1)                                 /* not right edge */
	oprs[blank].pos[oprs[blank].num++] = blank + 1;    /* add a move right */
      if (blank < SIZE - X)                                 /* not bottom edge */
	oprs[blank].pos[oprs[blank].num++] = blank + X;   /* add a move down */
    }
}


/* INPUT accepts an initial state from the terminal, assuming it is
   preceded by a problem number. It stores it in the state vector and
   returns the position of the blank tile. */

int input (int s[SIZE])
                                                 /* state vector */
{
  int index;                                       /* index to tile positions */
  int blank;                                        /* position of blank tile */

  blank=-1; /* avoid warning */

  scanf ("%*d");                                  /* skip over problem number */
  for (index = 0; index < SIZE; index++)                 /* for each position */
    {scanf ("%d", &s[index]);                  /* input tile in that position */
      if (s[index] == 0) blank = index;}     /* note blank position in passing */
  return (blank);
}

int get_blank(int s[SIZE]) {
  int index;
  for (index = 0; index < SIZE; index++)                 /* for each position */
    if (s[index] == 0) return index;
  return -1;
}
  

/* MANHATTAN returns the sum of the Manhattan distances of each tile,
   except the blank, from its goal position. */

int manhattan(const int s[SIZE])
{
  int value;                                                   /* accumulator */
  int pos;                                                   /* tile position */
  
  value = 0;
  for (pos = 0; pos < SIZE; pos++)
    if (s[pos] != 0)            /* blank isn't counted in Manhattan distance */
      value = value + abs((pos % X) - (s[pos] % X))            /* X distance */
	+ abs((pos / X) - (s[pos] / X));           /* Y distance */
  return(value);
}


/* INIT pre-computes the incremental evaluation function table. For a
   given tile moving from a given source position to a given destination
   position, it returns the net change in the value of the Manhattan
   distance, which is either +1 or -1.  */

void init_manhattan(int increment[SIZE][SIZE][SIZE]) /* incr eval function: tile, source, dest */
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
	  increment[tile][source][dest]  = abs((tile % X) - (dest % X))   
	    - abs((tile % X) - (source % X)) 
	    + abs((tile / X) - (dest / X))
	    - abs((tile / X) - (source / X));
	}
}


/* DIFF returns the number of tiles that are not in its final position */

int diff(const int state[SIZE]) {

  int value;                                                   /* accumulator */
  int pos;                                                   /* tile position */
  
  value = 0;
  for (pos = 0; pos < SIZE; pos++)
    if (s[pos] != 0)
      if (pos!=s[pos]) ++value;
  return(value);


}

/* Analogue of init_manhattan, but now for the diff heurisitc */

void init_diff(int increment[SIZE][SIZE][SIZE]) /* incr eval function: tile, source, dest */
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
	  if (tile==source)
	    increment[tile][source][dest]=1; // tile left its correct position
	  else if (tile==dest)               
 	    increment[tile][source][dest]=-1; // tile reached its correct position
	  else
	    increment[tile][source][dest]=0; // no difference 
	}
}

int zero(const int s[SIZE]) {
  return 0;
}

int zero2(int increment[SIZE][SIZE][SIZE]) {
  return 0;
}

int (*heuristic)(const int s[SIZE]) = manhattan;
void (*init)(int increment[SIZE][SIZE][SIZE]) = init_manhattan;

//int (*heuristic)(const int s[SIZE]) = diff;
//void (*init)(int increment[SIZE][SIZE][SIZE]) = init_diff;

//int (*heuristic)(const int s[SIZE]) = zero;
//void (*init)(int increment[SIZE][SIZE][SIZE]) = zero2;
