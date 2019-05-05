void add_record(long int length,long int expansions,long int calls,long int updates,long int hashcount,long int hashmax,float time);
void add_record_rt(long int length,long int expansions,long int steps,long int updates,long int hashcount,long int hashmax,float time, long int searches);
void add_record_tb(long int length,long int expansions,long int steps,long int back_steps,long int updates,long int hashcount,long int hashmax,float time, long int searches);
void add_record_tbwida(long int length,long int expansions,long int calls,long int updates,long int hashcount,long int hashmax,float time,  long backSteps, long forwSteps);
void print_stats();
void print_stats_rt();
void print_stats_tb();
void print_stats_tbwida();
