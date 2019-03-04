#!/usr/bin/python

import sys

def swap(arr, idx1, idx2):
    temp = arr[idx1]
    arr[idx1] = arr[idx2]
    arr[idx2] = temp

def quick_sort(arr, left, right, key):
    if left >= right:
        return

    pivot = arr[right-1]
    i = left
    j = right-2

    while i <= j:
        while(key(arr[i], pivot)):
            i+=1
        while(not arr[j] == pivot and not key(arr[j], pivot)):
            j-=1

        if(i<=j):
            swap(arr, i, j)
            i+=1; j-=1

    swap(arr, i, right-1)
    quick_sort(arr, left, i, key)
    quick_sort(arr, i+1, right, key)


if __name__ == "__main__":
    argv = sys.argv

    if(len(argv) < 5) or not ("-o" in argv and "-i" in argv):
        print("Wrong argvs : {}".format(argv))
        sys.exit()        

    arr = list(map(int, argv[4:]))

    if argv[(argv.index("-o"))+1] == "A":
        quick_sort(arr, 0, len(arr), lambda x, y : x < y)
    elif argv[(argv.index("-o"))+1] == "D":
        quick_sort(arr, 0, len(arr), lambda x, y : x > y)

    print(arr)
