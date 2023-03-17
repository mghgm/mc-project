#!/bin/bash
cd ~/pbbsbench/benchmarks/rangeSearch/vamana

make clean all
P=/ssd1/data/FB_ssnpp
R=/ssd1/results/FB_ssnpp
./range -a 1.2 -R 150 -L 400 -q $P/FB_ssnpp_public_queries.u8bin -g $R/1M_150_400 -c $P/ssnpp-1M -res $R/vamana_res.csv $P/FB_ssnpp_database.u8bin.crop_nb_1000000
./range -a 1.2 -R 150 -L 400 -q $P/FB_ssnpp_public_queries.u8bin -g $R/10M_150_400 -c $P/ssnpp-10M -res $R/vamana_res.csv $P/FB_ssnpp_database.u8bin.crop_nb_10000000
./range -a 1.2 -R 150 -L 400 -q $P/FB_ssnpp_public_queries.u8bin -g $R/100M_150_400 -c $P/ssnpp-100M -res $R/vamana_res.csv $P/FB_ssnpp_database.u8bin.crop_nb_100000000
./range -a 1.2 -R 150 -L 400 -q $P/FB_ssnpp_public_queries.u8bin -g $R/1B_150_400 -c $P/FB_ssnpp_public_queries_1B_GT.rangeres -res $R/vamana_res.csv $P/FB_ssnpp_database.u8bin

cd ~/pbbsbench/benchmarks/rangeSearch/HCNNG
make clean all
Q=/ssd1/data/FB_ssnpp
S=/ssd1/results/FB_ssnpp
./range -a 1000 -R 3 -L 50 -b 1 -q $Q/FB_ssnpp_public_queries.u8bin -g $S/1M_3_50 -c $Q/ssnpp-1M -res $S/hcnng_res.csv $Q/FB_ssnpp_database.u8bin.crop_nb_1000000
./range -a 1000 -R 3 -L 50 -b 1 -q $Q/FB_ssnpp_public_queries.u8bin -g $S/10M_3_50 -c $Q/ssnpp-10M -res $S/hcnng_res.csv $Q/FB_ssnpp_database.u8bin.crop_nb_10000000
./range -a 1000 -R 3 -L 50 -b 1 -q $Q/FB_ssnpp_public_queries.u8bin -g $S/100M_3_50 -c $Q/ssnpp-100M -res $S/hcnng_res.csv $Q/FB_ssnpp_database.u8bin.crop_nb_100000000
./range -a 1000 -R 3 -L 50 -b 1 -q $Q/FB_ssnpp_public_queries.u8bin -o $S/1B_3_50 -c $Q/FB_ssnpp_public_queries_1B_GT.rangeres -res $S/hcnng_res.csv $Q/FB_ssnpp_database.u8bin

cd ~/pbbsbench/benchmarks/rangeSearch/pyNNDescent

make clean all
T=/ssd1/data/FB_ssnpp
U=/ssd1/results/FB_ssnpp
./range -R 60 -L 1000 -a 20 -d 1.4 -q $T/FB_ssnpp_public_queries.u8bin -o $U/1M_60 -c $T/ssnpp-1M -res $U/pynn_res.csv $T/FB_ssnpp_database.u8bin.crop_nb_1000000
./range -R 60 -L 1000 -a 20 -d 1.4 -q $T/FB_ssnpp_public_queries.u8bin -o $U/10M_60 -c $T/ssnpp-10M -res $U/pynn_res2.csv $T/FB_ssnpp_database.u8bin.crop_nb_10000000
./range -R 60 -L 1000 -a 20 -d 1.4 -q $T/FB_ssnpp_public_queries.u8bin -o $U/100M_60 -c $T/ssnpp-100M -res $U/pynn_res2.csv $T/FB_ssnpp_database.u8bin.crop_nb_100000000

