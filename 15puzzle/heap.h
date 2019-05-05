#ifndef HEAP_H
#define HEAP_H

#define HEAPSIZE 10000000
#define MAXHEAPS 1
#define MAXKEYLENGTH 1

typedef struct heap heap;
struct heap
{
    HEAP_DATATYPE *array[HEAPSIZE];
    long int size;
    long int id;

    int key_index;
    int key_length;
};

heap* new_heap(int key_index, int key_length);

void empty_heap(heap *h);
HEAP_DATATYPE* top_heap(heap *h);
HEAP_DATATYPE* pop_heap(heap *h);
void insert_heap(heap *h, HEAP_DATATYPE *c);
void free_heap(heap *h);

#endif
