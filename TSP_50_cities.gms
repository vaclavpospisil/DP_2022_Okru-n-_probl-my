set i /i1*i50/;
table xy(i,*)
          x     y
    i1  485   142
    i2  597   470
    i3  238   461
    i4  642   312
    i5  835    60
    i6  627   586
    i7  330   473
    i8  386   230
    i9  334   500
   i10  716   163
   i11  325    39
   i12  680   192
   i13  162    68
   i14  335   128
   i15  420   200
   i16  316   223
   i17 1031   426
   i18  414   411
   i19  945   127
   i20  494   515
   i21  993   155
   i22  511   461
   i23  723   467
   i24  126   193
   i25  302    77
   i26  859   605
   i27  587   472
   i28  147   270
   i29  982   161
   i30  804   612
   i31  577   154
   i32  777   453
   i33  374   113
   i34  643   503
   i35  111   427
   i36  486   204
   i37  607   534
   i38  555   513
   i39  953   214
   i40  397   567
   i41 1013   477
   i42  190   514
   i43  612   316
   i44 1005   505
   i45  252   353
   i46  815   565
   i47  111   294
   i48  745   497
   i49  195   602
   i50  793   160
;

alias (i, j);
parameter c(i, j);

set arcs(i,j);
arcs(i,j)$(not sameas(i,j)) = yes;

c(arcs(i,j)) = round(sqrt(sqr(xy(i,'x')-xy(j,'x'))+sqr(xy(i,'y')-xy(j,'y'))));

scalar n 'poèet uzlù';
n = card(i);

binary variables x(i,j);
positive variables y(i,j);
variable z;

scalar f /0.01/;

equations
   delkatrasy
   FlowY(i)
   TotalX
   ArcGain(i,j)
   FlowX(i)
;

set i2(i);
i2(i)$(ord(i)>=2) = yes;

delkatrasy..  z =e= sum(arcs, c(arcs)*x(arcs));
FlowY(i2(i)).. sum(arcs(i,j), y(i,j)) - sum(arcs(i,j), y(j,i)) =e= f;
TotalX.. sum(arcs, x(arcs)) =L= n;
ArcGain(arcs).. y(arcs) =l= (1+n*f)*x(arcs);
FlowX(i2(i))..  sum(arcs(i,j),x(i,j)) =e= sum(arcs(i,j),x(j,i));

option optcr=0;
option iterlim=10000000;

model tsp/all/;
solve tsp minimizing z using mip;

display x.l;
