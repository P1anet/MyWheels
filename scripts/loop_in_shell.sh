#!/bin/bash

##### for #####
for i in 1 2 3
do
    echo $i
done

values="1 2 3"
for i in $values
do
    echo ${i}
done

for i in `ls`
do
    echo $i
done

##### while #####

count=0
while [ $count -lt 5 ]
do
    count=`expr $count + 1`
    echo $count
done

count=0
total=0
while read student score
do
    total=`expr $total + $score`
    count=`expr $count + 1`
    echo $count
done
avg=`expr $total / $count`
echo 'average '$avg

##### until #####

xxx="" # Variables in "" will be expanded, which in '' will not.
until [ "$xxx" = exit ]
do
    read xxx
    if [ "$xxx" != exit ]
    then
        echo $xxx
    else
        echo 'exit'
    fi
done
