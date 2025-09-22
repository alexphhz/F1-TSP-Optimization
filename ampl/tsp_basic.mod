# ---------- Sets & Data ----------
set CITIES ordered;
param N := card(CITIES);
param dist {CITIES, CITIES} >= 0;

param HOME symbolic default first(CITIES);

# ---------- Decision Vars ----------
var x {i in CITIES, j in CITIES: i <> j} binary;
var u {i in CITIES} >= 0 <= N-1;

# ---------- Objective ----------
minimize TotalDistance:
  sum {i in CITIES, j in CITIES: i <> j} dist[i,j] * x[i,j];

# ---------- Degree constraints ----------
subject to OutDegree {i in CITIES}:
  sum {j in CITIES: j <> i} x[i,j] = 1;

subject to InDegree  {j in CITIES}:
  sum {i in CITIES: i <> j} x[i,j] = 1;

# ---------- MTZ subtour elimination ----------
subject to Subtour {i in CITIES, j in CITIES: i <> j && i <> HOME && j <> HOME}:
  u[i] - u[j] + N * x[i,j] <= N - 1;

subject to FixHome:
  u[HOME] = 0;
