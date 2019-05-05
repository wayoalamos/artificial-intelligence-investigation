#include <stdlib.h>
#include "heap.h"

long int current_heap_id = 0;

heap* new_heap(int key_index, int key_length)
{
    heap* h;
    h = calloc(1, sizeof(heap));
    h->key_index = key_index;
    h->key_length = key_length;
    h->size = 0;

    h->id = current_heap_id;

    current_heap_id = (current_heap_id + 1) % MAXHEAPS;

    return h;
}

void empty_heap(heap *h)
{
    int i;
    for (i = 1; i <= h->size; ++i)
    {
        h->array[i]->heap_index[h->id] = 0;
    }
    h->size = 0;
}

void clear_heap_quick(heap *h) {
  h->size=0;
}

short key_compare(heap *h, HEAP_DATATYPE *c1, HEAP_DATATYPE *c2)
{
    int i;

    for (i = h->key_index; i < h->key_index + h->key_length; ++i)
    {
      if (KEY(c1,i)< KEY(c2,i))
            return 1;
      else if (KEY(c1,i) > KEY(c2,i))
            return 0;
    }
    return 0;
}

void percolatedown(heap *h, long int hole, HEAP_DATATYPE *c)
{
    long int child;

    if (h->size != 0)
    {
        for (; 2*hole <= h->size; hole = child)
        {
            child = 2*hole;
            if (child != h->size && key_compare(h, h->array[child+1], h->array[child]))
                ++child;
            if (key_compare(h, h->array[child], c))
            {
                h->array[hole] = h->array[child];
                h->array[hole]->heap_index[h->id] = hole;
            }
            else
                break;
        }
        h->array[hole] = c;
        h->array[hole]->heap_index[h->id] = hole;
    }
}

void percolateup(heap *h, long int hole, HEAP_DATATYPE *c)
{
    if (h->size != 0)
    {
        for (; hole > 1 && key_compare(h, c, h->array[hole/2]); hole /= 2)
        {
            h->array[hole] = h->array[hole/2];
            h->array[hole]->heap_index[h->id] = hole;
        }
        h->array[hole] = c;
        h->array[hole]->heap_index[h->id] = hole;
    }
}

void percolateupordown(heap *h, long int hole, HEAP_DATATYPE *c)
{
    if (h->size != 0)
    {
        if (hole > 1 && key_compare(h, c, h->array[hole/2]))
            percolateup(h, hole, c);
        else
            percolatedown(h, hole, c);
    }
}

HEAP_DATATYPE* top_heap(heap *h)
{
    if (h->size == 0) return NULL;
    return h->array[1];
}

HEAP_DATATYPE* pop_heap(heap *h)
{
    HEAP_DATATYPE* c;
    if (h->size == 0) return NULL;
    c = h->array[1];
    c->heap_index[h->id] = 0;
    percolatedown(h, 1, h->array[h->size--]);

    return c;
}

void insert_heap(heap *h, HEAP_DATATYPE *c)
{
    if (c->heap_index[h->id] == 0)
        percolateup(h, ++h->size, c);
    else
        percolateupordown(h, c->heap_index[h->id], c);
}

void free_heap(heap *h)
{
    empty_heap(h);
//    free(h->array);
    free(h);
}
