sets
   i /i1*i13/
;
alias (i,j);

table c(i,j) 'matice sousednosti (km)'

      i1  i2  i3  i4  i5  i6  i7  i8  i9 i10 i11 i12 i13
 i1      183 276 208 250 110  95 100  90  73 114  84 121
 i2          140  64  77  77 112 126 208 246 293 242 158
 i3               79  81 200 181 180 251 315 389 352 292
 i4                   51 122 117 122 204 258 321 279 213
 i5                      152 163 171 253 305 362 315 234
 i6                           73  92 157 179 216 164  94
 i7                               19  96 142 208 175 151
 i8                                   83 137 211 183 169
 i9                                       73 166 165 204
 i10                                          95 112 190
 i11                                              65 181
 i12                                                 117
 i13
;

set arcs(i,j);
arcs(i,j)$(not sameas(i,j)) = yes;

c(arcs(i,j)) = max(c(i,j),c(j,i));

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
