/* mm.c: A simple memory manager */
#include <stdio.h>
#include <stdlib.h>
#include <inttypes.h>
#include "include.h"
#include "hash.h"


#define BLOCKSIZE sizeof(Node)*10000
#define MAXBLOCKS 100000

void * memoryblocks[MAXBLOCKS];
int next[MAXBLOCKS];
int current_block;

void mm_init() {
  int i;
  current_block=-1;
  for (i=0; i<MAXBLOCKS; ++i) {
    memoryblocks[i]=NULL;
  }
}

void * mm_malloc(int size) {
  void *blockptr;
  if (current_block==-1 || next[current_block]+size>BLOCKSIZE) {
    ++current_block;
    if (current_block==MAXBLOCKS) {
      printf("Out of memory. Increase MAXBLOCKS in mm.c");
      exit(1);
    }
    if (memoryblocks[current_block]==NULL) {
      memoryblocks[current_block]=malloc(BLOCKSIZE);
      //  printf("+cb=%d\n",current_block);
    }
    next[current_block]=0;
  }
  blockptr = memoryblocks[current_block]+next[current_block];
  next[current_block]+=size;
  // printf("just returned %p\n",blockptr);
  return blockptr;
}

void mm_discardall() {
  int i;
  if (current_block>=0) {
    for (i=0; i<=current_block; ++i) 
      next[i]=0;
    current_block=0;
    //   printf("cb=0\n");
  }
}
