array ar = 5;
int cnst = 48;
int dgt = 0;
int number = 0;
int a = 0;
while (a < 5){
    a = a;
}
int j = 1;
int i = 0;
int n = 5;
while (j < n){
    while (i < n - j){
        int k = i + 1;
        int t1 = ar[i];
        int t2 = ar[k];
        if (t2 < t1){
            ar[i] = t2;
            ar[k] = t1;
        }
        i = i + 1;
    }
    j = j + 1;
    i = 0;
}
while (i < 5){
    t2 = ar[i];
    int t3 = 0;
    int nwln = 10;
    int cntr = 0;
    k = 1;
    while (k < t2 + 1) {
        k = k * 10;
        cntr = cntr + 1;
    }
    while (0 < cntr){
        k = k /10;
        t3 = t2/k + cnst;
        print(t3);
        t3 = t3 - cnst;
        t3 = t3*k;
        t2 = t2 - t3;
        cntr = cntr - 1;
    }
    print(nwln);
    i = i + 1;
}


interruption;
if (input != 32){
    dgt = input - cnst;
    number = dgt + number*10;
}
if (input == 32){
    ar[a] = number;
    a = a + 1;
    number = 0;
}
