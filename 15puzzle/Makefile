#CFLAGS=-Wall -g -pg
CFLAGS=-Wall -O6
CC=gcc
IDA_INCLUDES=include.h puzzle.h stats.h
LDFS_INCLUDES=hash.h include.h mm.h puzzle.h stats.h
LRTA_INCLUDES=hash.h include.h mm.h puzzle.h stats.h
RTA_INCLUDES=hash.h include.h mm.h puzzle.h stats.h
ASTAR_INCLUDES=hash.h include.h mm.h puzzle.h stats.h stateheap.h heap.h
RTAA_INCLUDES=hash.h include.h mm.h puzzle.h stats.h stateheap.h heap.h
TBA_INCLUDES=hash.h include.h mm.h puzzle.h stats.h stateheap.h heap.h
TBWIDA_INCLUDES=hash.h include.h mm.h puzzle.h stats.h
RTBWIDA_INCLUDES=hash.h include.h mm.h puzzle.h stats.h
BINARIES=ida wida ldfs lrta rta rlrta astar rtaa tba rtbaa rtbwa tbwida rtbwida

all: $(BINARIES)

#
ida: $(IDA_INCLUDES) puzzle.o ida.o stats.o
	gcc $(CFLAGS) -o ida ida.o puzzle.o stats.o

#
wida: $(IDA_INCLUDES) puzzle.o wida.o stats.o
	gcc $(CFLAGS) -o wida wida.o puzzle.o stats.o

tbwida: $(TBWIDA_INCLUDES) puzzle.o tbwida.o stats.o
	gcc $(CFLAGS) -o tbwida tbwida.o puzzle.o stats.o

rtbwida: $(RTBWIDA_INCLUDES) puzzle.o rtbwida.o stats.o
	gcc $(CFLAGS) -o rtbwida rtbwida.o puzzle.o stats.o

# ?? not found
lrta: $(LRTA_INCLUDES) puzzle.o lrta.o hash.o mm.o stats.o
	gcc $(CFLAGS) -o lrta lrta.o puzzle.o hash.o mm.o stats.o

#
rta: $(RTA_INCLUDES) puzzle.o rta.o hash.o mm.o stats.o
	gcc $(CFLAGS) -o rta rta.o puzzle.o hash.o mm.o stats.o

#
rlrta: $(LRTA_INCLUDES) puzzle.o rlrta.o hash.o mm.o stats.o
	gcc $(CFLAGS) -o rlrta rlrta.o puzzle.o hash.o mm.o stats.o

#
astar: $(ASTAR_INCLUDES) puzzle.o astar.o hash.o mm.o stats.o stateheap.o
	gcc $(CFLAGS) -o astar astar.o puzzle.o hash.o mm.o stats.o stateheap.o

#
rtaa: $(RTAA_INCLUDES) puzzle.o rtaa.o hash.o mm.o stats.o stateheap.o
	gcc $(CFLAGS) -o rtaa rtaa.o puzzle.o hash.o mm.o stats.o stateheap.o

tba: $(TBA_INCLUDES) puzzle.o tba.o hash.o mm.o stats.o stateheap.o
	gcc $(CFLAGS) -o tba tba.o puzzle.o hash.o mm.o stats.o stateheap.o

rtbaa: $(TBA_INCLUDES) puzzle.o rtbaa.o hash.o mm.o stats.o stateheap.o
	gcc $(CFLAGS) -o rtbaa rtbaa.o puzzle.o hash.o mm.o stats.o stateheap.o

rtbwa: $(TBA_INCLUDES) puzzle.o rtbwa.o hash.o mm.o stats.o stateheap.o
	gcc $(CFLAGS) -o rtbwa rtbwa.o puzzle.o hash.o mm.o stats.o stateheap.o

ldfs: $(LDFS_INCLUDES) puzzle.o ldfs.o hash.o mm.o stats.o
	gcc $(CFLAGS) -o ldfs ldfs.o puzzle.o hash.o mm.o stats.o

clean:
	rm -f *.o $(BINARIES)
