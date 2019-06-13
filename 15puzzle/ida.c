
/* This program performs iterative-deepening A* on the sliding tile
puzzles, using the Manhattan distance evaluation function. It was
written by Richard E.  Korf, Computer Science Department, University
of California, Los Angeles, Ca.  90024.

This program implements a slight modification over the original
version: time is accounted for every instance solved and various stats
about time are provided while the test set is being solved */

#include <stdio.h>                                   /* standard I/O library */
#include <string.h>                                                /* memcpy */
#include <sys/time.h>                                       /* time handling */
#include <unistd.h>                                         /* time handling */
#include <inttypes.h>
#include "include.h"
#include "puzzle.h"
#include "stats.h"

int increment [SIZE] [SIZE] [SIZE];    /* incr eval func: tile, source, dest */

int thresh;                                       /* search cutoff threshold */
long long int generated;                /* number of states generated per iteration */
long long int expanded;                /* number of states expanded per iteration */
long long int total;                            /* total number of states generated */
long long int total_exp;

FILE *fp;

int NUMBER_OF_PROBLEMS = 144;

void write_in_file(int blank){
  fprintf(fp, "%i\n", blank);
}

void open_file(int problem) {
  char name[50];
  snprintf(name, 50, "../moves-from-generated-data/ida_problem_%d_.txt", problem); // puts string into buffer
  fp = fopen(name, "w+");
}

void close_file() {
  fclose(fp);
}

/* SEARCH performs one depth-first iteration of the search, cutting
   off when the depth plus the heuristic evaluation exceeds THRESH. If
   it succeeds, it returns 1 and records the sequence of tiles moved in
   the solution.  Otherwise, it returns 0 */

int search (int blank, int oldblank, int g, int h, int problem)

/*int blank;			                 current position of blank */
/*int oldblank;			                previous position of blank */
/*int g;                                             current depth of search */
/*int h;	                            value of heuristic evaluation function */

{ int index;                                    /* index into operator array */
  int newblank;                               /* blank position in new state */
  int tile;                                              /* tile being moved */
  int newh;                             /* heuristic evaluation of new state */
  ++expanded;
  for (index = 0; index < oprs[blank].num; index++)     /* for each appl opr */
    if ((newblank = oprs[blank].pos[index]) != oldblank) /*not inv last move */
      {tile = s[newblank];            /* tile moved is in new blank position */
	newh = h + increment[tile][newblank][blank];   /* new heuristic est */
	generated++;                                 /* count nodes generated */
	if (newh+g+1 <= thresh)                    /* less than search cutoff */
	  {s[blank] = tile;                               /* make actual move */
	    if ((newh == 0) ||                     /* goal state is reached or */
		(search(newblank, blank, g+1, newh, problem))){       /* search succeeds */
        write_in_file(blank);
        return (1);                                 /* exit with success */
        }
	    s[newblank] = tile;}}       /* undo current move before doing next */
  return (0);                                 /* exit with failure */
}
/* Main program does the initialization, inputs an initial state, solves it,
   and prints the solution. */

int main ()

{
  int success;                         /* boolean flag for success of search */
  int blank;                                    /* initial position of blank */
  int initeval;                       /* manhattan distance of initial state */
  int problem;                                           /* problem instance */
  int calls;

  struct timeval stv,etv;
  struct timezone stz,etz;
  float thistime;
  float totaltime=0.0;
  long totalexpansions=0;

  initops ();                                   /* initialize operator table */
  init (increment);                        /* initialize evaluation function */

#ifndef SUCCINCT
  printf ("%3s %3s %5s %10s %10s %2s\n", "#p", "t-2", "#calls", "#exp", "#gen",
	    "time");
#endif

  for (problem = 0; problem <= NUMBER_OF_PROBLEMS; problem++){ /* for each initial state */
    blank = input(s);                                 /* input initial state */ // initial blank = 7
    gettimeofday (&stv,&stz);
    thresh = initeval = heuristic(s);      /* initial threshold is initial h */
    total = 0;                           /* initialize total nodes generated */
    total_exp = 0;                           /* initialize total nodes generated */
    calls = 0;                 /* initialize total number of calls to search */
    open_file(problem);
    do{                    /* depth-first iterations until solution is found */
      generated = 0;            /* initialize number generated per iteration */
      expanded=0;
      ++calls;
      success = search (blank, -1, 0, initeval, problem);           /* perform search */
      fflush(stdout);       /* flush output buffer to see progress of search */
      total = total + generated;    /* keep track of total nodes per problem */
      total_exp += expanded;
      thresh += 2;                  /* threshold always increases by two */
    }
    while (!success);                             /* until solution is found */
    close_file();
    totalexpansions+=total;
    gettimeofday (&etv,&etz);
    if (etv.tv_usec>stv.tv_usec){
      thistime=(etv.tv_sec-stv.tv_sec)+(etv.tv_usec-stv.tv_usec)/1000000.0;}
    else{
      thistime=(etv.tv_sec-stv.tv_sec)+(1000000.0+etv.tv_usec-stv.tv_usec)/1000000.0;}

    totaltime+=thistime;

#ifndef SUCCINCT
    printf ("%3d %3d %5d %10lld %10lld %2.2f \n", problem,  thresh-2, calls, total_exp,total,
	    thistime);
#endif
    add_record(thresh-2,total,calls,0,0,0,thistime);
  }

  print_stats();

  return 0;
}
