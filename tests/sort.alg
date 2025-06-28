array ar = 5;
int cnst = 48;
int dgt = 0;
int number = 0;
int a = 0;
while (a < 5){
    a = a;
}
string inpt = 7'inputed';
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
    k = 1;
    while (k < t2) {
        k = k * 10;
    }
    while (0 < t2){
        k = k /10;
        t3 = t2/k + 48;
        print(t3);
        t3 = t3 - 48;
        t3 = t3*k;
        t2 = t2 - t3;
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
