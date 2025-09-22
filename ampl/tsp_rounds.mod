# ---------- Sets & Data ----------
set CITIES ordered;
param N := card(CITIES);
set ROUNDS := 1..N;
param dist {CITIES, CITIES} >= 0;

# Named aliases (same symbols as in .dat)
param SAKHIR symbolic;
param JEDDAH symbolic;
param MELBOURNE symbolic;
param SHANGHAI symbolic;
param SUZUKA symbolic;
param MONACO symbolic;
param SILVERSTONE symbolic;
param MONZA symbolic;
param SPA_FRANCORCHAMPS symbolic;
param MONTREAL symbolic;
param MIAMI symbolic;
param AUSTIN symbolic;
param MEXICO_CITY symbolic;
param SAO_PAULO symbolic;
param LAS_VEGAS symbolic;
param SINGAPORE symbolic;
param BAKU symbolic;
param BUDAPEST symbolic;
param SPIELBERG symbolic;
param LUSAIL symbolic;
param YAS_MARINA_ABU_DHABI symbolic;
param IMOLA symbolic;

# ---------- Decision Vars ----------
var y {c in CITIES, r in ROUNDS} binary;

# ---------- Objective (quadratic) ----------
minimize TotalDistance:
  sum {r in 1..N-1, i in CITIES, j in CITIES} dist[i,j] * y[i,r] * y[j,r+1]
+ sum {i in CITIES, j in CITIES} dist[i,j] * y[i,N] * y[j,1];

# ---------- Assignment ----------
subject to OneRoundPerCity {c in CITIES}:  sum {r in ROUNDS} y[c,r] = 1;
subject to OneCityPerRound {r in ROUNDS}:  sum {c in CITIES} y[c,r] = 1;

# ---------- Examples of business rules ----------

# Bahrain first; UAE last
subject to BahrainFirst: y[SAKHIR, 1] = 1;
subject to UAELast:     y[YAS_MARINA_ABU_DHABI, N] = 1;

# Montreal after round 8
subject to MontrealAfter8 {r in 1..8}: y[MONTREAL, r] = 0;

# Singapore only in R1..R7 or R18..R22 (ban mid rounds)
subject to BanSingaporeMid {r in 8..17}: y[SINGAPORE, r] = 0;

# USA group not adjacent between consecutive rounds
set USA := { MIAMI, AUSTIN, LAS_VEGAS };
subject to NoAdjacentUSA {r in 1..N-1}:
  sum {c in USA} y[c, r] + sum {c in USA} y[c, r+1] <= 1;

# Suzuka & Shanghai must be consecutive (either order)
subject to SuzukaShanghaiConsecutive:
  sum {r in 1..N-1} ( y[SUZUKA, r] * y[SHANGHAI, r+1]
                    + y[SHANGHAI, r] * y[SUZUKA, r+1] ) = 1;

# If Monaco in first half, then Sao Paulo in second half
param FIRSTHALF integer := ceil(N/2);
subject to MonacoFirstHalfImpSaoSecond:
  sum {r in 1..FIRSTHALF} y[MONACO, r]
  <= sum {r in FIRSTHALF+1..N} y[SAO_PAULO, r];
