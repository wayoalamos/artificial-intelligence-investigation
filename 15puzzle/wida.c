
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
#include <stdlib.h>
#include "include.h"
#include "puzzle.h"
#include "stats.h"


int increment [SIZE] [SIZE] [SIZE];    /* incr eval func: tile, source, dest */

double wida_thresh;                                       /* search cutoff threshold for wida */
double ida_thresh;                                        /* search cutoff threshold for ida */
double generated;                /* number of states generated per iteration */
double total;                            /* total number of states generated */
double w;
double min_f;
double min_fastar;

/* SEARCH performs one depth-first iteration of the search, cutting
   off when the depth plus the heuristic evaluation exceeds THRESH. If
   it succeeds, it returns 1 and records the sequence of tiles moved in
   the solution.  Otherwise, it returns 0 */

int search (int blank, int oldblank, int g, int h)

/*int blank;			                 current position of blank */
/*int oldblank;			                previous position of blank */
/*int g;                                             current depth of search */
/*int h;	                            value of heuristic evaluation function */

{ int index;                                    /* index into operator array */
  int newblank;                               /* blank position in new state */
  int tile;                                              /* tile being moved */
  int newh;                             /* heuristic evaluation of new state */
  double f;
  double fastar;

  for (index = 0; index < oprs[blank].num; index++)     /* for each appl opr */
    if ((newblank = oprs[blank].pos[index]) != oldblank) /*not inv last move */
      {
	int condition;
	tile = s[newblank];            /* tile moved is in new blank position */
	newh = h + increment[tile][newblank][blank];   /* new heuristic est */
	generated++;                                 /* count nodes generated */

	if (newh==h) printf("N");
	f = newh*w + g +1;
	fastar =newh +g + 1;
	
	if (1) {
	  condition=(f-wida_thresh<0.001);
	} else {
	  condition=(fastar<=ida_thresh);
	}
	
	if (condition) {                   /* less than search cutoff */
	  s[blank] = tile;                               /* make actual move */
                                 /* exit with success */
	  if (newh==0) return g;
	  int len;
	  len = search(newblank, blank, g+1, newh);
	  if (len>0) return len;
	  s[newblank] = tile;
	} else {
	  /* this node will not be expanded */
	  if (min_f-f>0.0001) min_f=f;
	  if (min_fastar>fastar) min_fastar=fastar;
	}

      }       /* undo current move before doing next */
  return (0);                                 /* exit with failure */
}          
/* Main program does the initialization, inputs an initial state, solves it,
   and prints the solution. */

int main (int argc, char **argv)

{
  int length;                         /* length of the solution */
  int blank;                                    /* initial position of blank */
  int initeval;                       /* manhattan distance of initial state */
  int problem;                                           /* problem instance */
  int calls;

  struct timeval stv,etv;
  struct timezone stz,etz;
  float thistime;
  float totaltime=0.0;
  long totalexpansions=0;
  if (argc<2) {
     printf("Usage: %s <w>\n", argv[0]);
     return 0;
  }
  w=atof(argv[1]);
  

  initops ();                                   /* initialize operator table */
  init (increment);                        /* initialize evaluation function */
 
#ifndef SUCCINCT
  printf ("%3s %3s %3s %10s %2s\n", "#p", "t-2", "#calls", "#gen",
	    "time");
#endif
  for (problem = 1; problem <= NUMBER; problem++){ /* for each initial state */
    blank = input(s);                                 /* input initial state */
    gettimeofday (&stv,&stz);
    initeval = heuristic(s);              /* initial threshold is initial h */
    wida_thresh = w*initeval;
    ida_thresh=initeval;
    total = 0;                           /* initialize total nodes generated */
    calls = 0;                 /* initialize total number of calls to search */
    do{                    /* depth-first iterations until solution is found */
      generated = 0;            /* initialize number generated per iteration */
      ++calls;
      min_fastar=min_f=LARGE;
      //   printf("call %d:ida_thresh=%.2f --- wida_thresh=%.9f w=%.3f\n",calls,ida_thresh,wida_thresh,w);
      length = search (blank, -1, 0, initeval);           /* perform search */
      fflush(stdout);       /* flush output buffer to see progress of search */
      total = total + generated;    /* keep track of total nodes per problem */
      wida_thresh = min_f;                  /* threshold always increases by two */
      ida_thresh = min_fastar;
      
    }                     
    while (length==0);                             /* until solution is found */
    
    totalexpansions+=total;
    gettimeofday (&etv,&etz);
    if (etv.tv_usec>stv.tv_usec){
      thistime=(etv.tv_sec-stv.tv_sec)+(etv.tv_usec-stv.tv_usec)/1000000.0;}
    else{
      thistime=(etv.tv_sec-stv.tv_sec)+(1000000.0+etv.tv_usec-stv.tv_usec)/1000000.0;}
    
    totaltime+=thistime;
    
#ifndef SUCCINCT    
    printf ("%3d %3d %3d %10.f %2.2f \n", problem,length, calls, total, thistime);
#endif
    add_record(length,total,calls,0,0,0,thistime);
  }

  print_stats();
  
  return 0;
}



