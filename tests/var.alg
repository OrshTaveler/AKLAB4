int a = 1000;
int b = 1000;
int res = 0;
while (900 < a){
    a = a - 1;
    b = a;
    while (900 < b){
        b = b - 1;
        int k = 1;
        int p = a*b;
        int err = 0;
        while (k < p){
            k = k*10;
        }
        k = k / 10;
        while(0 < k){ 
         int forward = p/k;
         int backward = p/10*10;
         backward = p - backward;
         
         p = p - forward*k;
         p = p - backward;
         p = p/10;
         if (forward != backward){
            err = 1;
            k = 0;
         }
         k = k /100;
        }
        if (err == 0){
            res = a*b;
            a = 0;
            b = 0;
        }
    }
}
while(0 < res){
    int pr = res/10;
    pr = pr*10;
    pr = res - pr + 48;
    print(pr);
    res = res/10;
}