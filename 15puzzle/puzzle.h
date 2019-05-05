#include <inttypes.h>
void initops();
int input(int s[SIZE]);
int get_blank(int s[SIZE]);
int get_tile(uint64_t state,int position);
void new_int_state(uint64_t *state,int oldblank,int newblank);
uint64_t state_to_int64(int *s);

extern int (*heuristic)(const int s[SIZE]);
extern void (*init)(int increment[SIZE][SIZE][SIZE]);
