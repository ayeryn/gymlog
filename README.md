# gym_report
A simple function that takes a monthly journal and outputs a gym attendance report.

## Journal
The journal is recorded in the following format in a csv file. Capitalization doesn't matter in class names as the report generator use the titlecase version of the class name

`<day of month>,<class taken on that day>`   
sample.csv  
```
1,one & done
15, Swimming
```

## Main
The program prompts user to enter a month in `yyyymm` format and keeps asking until valid input is received -
- input is a numerical value
- length of input is 6

## Report
Example output
```
   December 2022
Mo Tu We Th Fr Sa Su
          1  2  3  4
          x         
 5  6  7  8  9 10 11
 x                 x
12 13 14 15 16 17 18
 x  x  x        x   
19 20 21 22 23 24 25
    x  x        x   
26 27 28 29 30 31
                 



Total classes taken: 10
Average classes per week: 2

==== Classes taken (sorted) ====
Class:        Hot Yoga, taken 2 times
Class:           Dance, taken 2 times
Class:      One & Done, taken 2 times
Class:        Swimming, taken 2 times
Class:     Muscle Camp, taken 1 times
Class:         Workout, taken 1 times
```