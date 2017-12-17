#!/bin/bash

FILE_TO_KEEP="progress.dat bestfitval.dat bestfit_containers.dat"

if [ $# -ne 1 ] 
then
    echo "Script to compress exp files and keep only files useful for result analysis."
    echo "Files kepts: $FILE_TO_KEEP"
    echo "Usage: $0 num_gen"
    exit
fi

LAST_GEN=$1

echo "Compressing files for exp that have reached gen_$LAST_GEN"
echo "Files kepts: $FILE_TO_KEEP"



function clean_exp {
    EXP=$1
    GREP=""
    PIPE=""
    for FILE in $FILE_TO_KEEP
    do
	GREP=$GREP$PIPE" grep -v $FILE"
	PIPE="|"
    done
    #echo $GREP
    FILES=$(find $EXP -type f | eval $GREP)
    rm $FILES
    
}

for a in exp*
do
    if [ -d $a ]
    then
	echo "Processing $a..."
	for b in $(find $a -maxdepth 1 -mindepth 1 -type d)
	do
	    echo -n "Is $b ready to be compressed ..."
	    if [ $(find $b -iname gen_$1 | wc -l ) -ge 1 ]
	    then
		if [ -e $b.tar.gz ]
		then
		    echo "[Already compressed...]"
		else
		    echo "[OK]"
		    tar zcvf $b.tar.gz $b >/dev/null && clean_exp $b
		fi
	    else
		echo "[KO]"
	    fi
	done
    fi

done
