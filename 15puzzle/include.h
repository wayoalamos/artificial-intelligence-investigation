#ifndef INCLUDE_H
#define INCLUDE_H

#define NUMBER 100               /* number of problem instances to be solved */ 
#define X 4                                    /* squares in the x dimension */ 
#define SIZE 16                                   /* total number of squares */ 

//#define SUCCINCT    /* whether or not the output is succinct */

int s[SIZE];                       /* state of puzzle: tile in each position */

#define LARGE 1000000000
#define MAXPATH 100000

struct operators                  
{int num;                                 /* number of applicable oprs: 2..4 */
  int pos[4];} oprs[SIZE];    /* position of adjacent tiles for each position */

#endif
