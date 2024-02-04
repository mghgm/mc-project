#include <iostream>
#include <algorithm>
#include <limits>
#include <cfloat>
#include "parlay/primitives.h"
#include "parlay/internal/get_time.h"
// #include "pam/pam.h"
#include "sweep.h"
#include "range.h"

__global__ void cuda_hello(){
    printf("Hello World from GPU!\n");

}
long range(Points const &points, Queries const &queries, bool verbose) {
  cuda_hello<<<1,1>>>(); 
  parlay::internal::timer t("range", verbose);
  t.next("build");
  for(auto p: points){
    // std::cout << p.x << "," << p.y << std::endl;
  }
  sleep(4);
  t.next("query");

  t.next("clear");
  return 50;
}
