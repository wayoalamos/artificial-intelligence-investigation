#include <stdio.h>
#include "include.h"

int num_records;

struct record {
  long int length;  /* solution length --- for RTAA, solution length without cycles */
  long int expansions;
  long int calls;
  long int updates;
  long int hashcount;
  long int hashmax;
  float time;
  long int searches; /* number of real-time searches */
  long int steps;  /* number of agent movements until reaching the goal */
  long int back_steps;  /* number of agent back-movements until reaching the goal relevant only to algorithms that physically backtrack */
};

struct record records[NUMBER];

void init_stats() {
  num_records=0;
}


void add_record(long int length,long int expansions,long int calls,long int updates,long int hashcount,long int hashmax,float time) {
  records[num_records].length=length;
  records[num_records].expansions=expansions;
  records[num_records].calls=calls;
  records[num_records].updates=updates;
  records[num_records].hashcount=hashcount;
  records[num_records].hashmax=hashmax;
  records[num_records].time=time;
  ++num_records;
}

void add_record_tbwida(long int length,long int expansions,long int calls,long int updates,long int hashcount,long int hashmax,float time, long int backSteps, long int forwSteps) {
  records[num_records].length=length;
  records[num_records].expansions=expansions;
  records[num_records].calls=calls;
  records[num_records].updates=updates;
  records[num_records].hashcount=hashcount;
  records[num_records].hashmax=hashmax;
  records[num_records].time=time;
  records[num_records].back_steps=backSteps;
  records[num_records].steps=forwSteps;
  ++num_records;
}

void add_record_rt(long int length,long int expansions,long int steps,long int updates,long int hashcount,long int hashmax,float time, long int searches) {
  records[num_records].length=length;
  records[num_records].expansions=expansions;
  records[num_records].steps=steps;
  records[num_records].updates=updates;
  records[num_records].hashcount=hashcount;
  records[num_records].hashmax=hashmax;
  records[num_records].searches=searches;
  records[num_records].time=time;
  ++num_records;
}

void add_record_tb(long int length,long int expansions,long int steps, long int back_steps,long int updates,long int hashcount,long int hashmax,float time, long int searches) {
  records[num_records].length=length;
  records[num_records].expansions=expansions;
  records[num_records].steps=steps;
  records[num_records].back_steps=back_steps;
  records[num_records].updates=updates;
  records[num_records].hashcount=hashcount;
  records[num_records].hashmax=hashmax;
  records[num_records].searches=searches;
  records[num_records].time=time;
  ++num_records;
}

void print_stats() {
  long total_length=0;
  long total_expansions=0;
  long total_calls=0;
  long total_updates=0;
  long total_hashcount=0;
  long total_hashmax=0;
  float total_time=0.0;
  int i;

  for (i=0;i<num_records;i++) {
    total_length+=records[i].length;
    total_expansions+=records[i].expansions;
    total_calls+=records[i].calls;
    total_updates+=records[i].updates;
    total_hashcount+=records[i].hashcount;
    total_hashmax+=records[i].hashmax;
    total_time+=records[i].time;
  }

#ifdef SUCCINCT
  printf("%ld\t%ld\t%ld\t%ld\t%ld\t%ld\t%f\n",total_length,total_expansions,total_calls,total_updates,total_hashcount,total_hashmax,total_time);
#else
  printf("Total Length=%ld\nTotal Expansions=%ld\nTotal Calls=%ld\nTotal Updates=%ld\nTotal Hashcount=%ld\nTotal Hashmax=%ld\nTotal Time=%.2f\n",total_length,total_expansions,total_calls,total_updates,total_hashcount,total_hashmax,total_time);
#endif 
}

void print_stats_rt() {
  long total_length=0;
  long total_expansions=0;
  long total_steps=0;
  long total_updates=0;
  long total_hashcount=0;
  long total_hashmax=0;
  long total_searches=0;
  float total_time=0.0;
  int i;

  for (i=0;i<num_records;i++) {
    total_length+=records[i].length;
    total_expansions+=records[i].expansions;
    total_steps+=records[i].steps;
    total_searches+=records[i].searches;
    total_updates+=records[i].updates;
    total_hashcount+=records[i].hashcount;
    total_hashmax+=records[i].hashmax;
    total_time+=records[i].time;
  }

#ifdef SUCCINCT
  printf("%ld\t%ld\t%ld\t%ld\t%ld\t%ld\t%f\n",total_length,total_expansions,total_steps,total_searches,total_updates,total_hashcount,total_hashmax,total_time);
#else
  printf("Total Length=%ld\nTotal Expansions=%ld\nTotal Steps=%ld\nTotal Searches=%ld\nTotal Updates=%ld\nTotal Hashcount=%ld\nTotal Hashmax=%ld\nTotal Time=%.2f\n",total_length,total_expansions,total_steps,total_searches,total_updates,total_hashcount,total_hashmax,total_time);
#endif 
}


void print_stats_tb() {
  long total_length=0;
  long total_expansions=0;
  long total_steps=0;
  long total_back_steps=0;
  long total_updates=0;
  long total_hashcount=0;
  long total_hashmax=0;
  long total_searches=0;
  float total_time=0.0;
  int i;

  for (i=0;i<num_records;i++) {
    total_length+=records[i].length;
    total_expansions+=records[i].expansions;
    total_steps+=records[i].steps;
    total_back_steps+=records[i].back_steps;
    total_searches+=records[i].searches;
    total_updates+=records[i].updates;
    total_hashcount+=records[i].hashcount;
    total_hashmax+=records[i].hashmax;
    total_time+=records[i].time;
  }

#ifdef SUCCINCT
  printf("%ld\t%ld\t%ld\t%ld\t%ld\t%ld\t%ld\t%f\n",total_length,total_expansions,total_steps,total_back_steps,total_searches,total_updates,total_hashcount,total_hashmax,total_time);
#else
  printf("Total Length=%ld\nTotal Expansions=%ld\nTotal Steps=%ld\nTotal Back-Steps=%ld\nTotal Searches=%ld\nTotal Updates=%ld\nTotal Hashcount=%ld\nTotal Hashmax=%ld\nTotal Time=%.2f\n",total_length,total_expansions,total_steps,total_back_steps,total_searches,total_updates,total_hashcount,total_hashmax,total_time);
#endif 
}

void print_stats_tbwida() {
  long total_length=0;
  long total_expansions=0;
  long total_calls=0;
  long total_updates=0;
  long total_hashcount=0;
  long total_hashmax=0;
  long total_steps=0;
  long total_back_steps=0;
  float total_time=0.0;
  int i;

  for (i=0;i<num_records;i++) {
    total_length+=records[i].length;
    total_expansions+=records[i].expansions;
    total_calls+=records[i].calls;
    total_updates+=records[i].updates;
    total_hashcount+=records[i].hashcount;
    total_hashmax+=records[i].hashmax;
    total_time+=records[i].time;
    total_steps+=records[i].steps;
    total_back_steps+=records[i].back_steps;
  }

#ifdef SUCCINCT
  printf("%ld\t%ld\t%ld\t%ld\t%ld\t%ld\t%f\t%ld\t%ld\n",total_length,total_expansions,total_calls,total_updates,total_hashcount,total_hashmax,total_time,total_back_steps, total_steps);
#else
  printf("Total Length=%ld\nTotal Expansions=%ld\nTotal Calls=%ld\nTotal Updates=%ld\nTotal Hashcount=%ld\nTotal Hashmax=%ld\nTotal Time=%.2f\nTotal back_steps=%ld\nTotal steps=%ld\n",total_length,total_expansions,total_calls,total_updates,total_hashcount,total_hashmax,total_time,total_back_steps,total_steps);
#endif 
}
