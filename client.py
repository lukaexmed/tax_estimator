"""
File Average.py.
An exemplar Python code.
"""
import random
def Average (lyst):
    #lyst: an array of unit scores, ended with -1, which is not a valid score
    #double average: average of all scores
    #Initialization phase
    total = 0 #total - sum of scores
    gradeCounter = 0 #gradeCounter: to track the number of scores in the array lyst[])
    #Processing phase
    n=len(lyst)
    i=0
    if (n ==0):
        return 0
    while lyst[i] != -1:
        gradeValue = lyst[i]
        total = total + gradeValue
        gradeCounter += 1
        i +=1
    if (gradeCounter != 0 ):
        average = total / gradeCounter
        return average
    else:
        return 0
    
def main(average = Average):
    lyst = [ 10, 20, 30, 40, 50, 60 ,70, 80, 90, 100, -1]
    size = 10
    #for count in range(size):
    # lyst.append(random.randint(1, 100 ))
    print(lyst)
    a = average (lyst)
    print("The average value is:", a)
    lyst1=[ ]
    while True:
        v = input("Please enter an integer as a unit mark (enter -1 to stop):")
        x=int (v)
        if x !=-1:
            lyst1.append(x)
        else:
            lyst1.append(-1)
        break
    print(lyst1)
    a = average (lyst1)
    print("The average value is: a = ", a)


if __name__ == "__main__":
    main()