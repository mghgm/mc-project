/*
	Based on papers:
	PAM: Parallel Augmented maps
	Yihan Sun, Daniel Ferizovic and Guy Blelloch
	PPoPP 2018
	
	Parallel Range, Segment and Rectangle Queries with Augmented Maps
	Yihan Sun and Guy Blelloch
	arXiv:1803.08621
*/

#include <algorithm>
#include <limits>
#include <cfloat>
#include "parlay/primitives.h"
#include "parlay/internal/get_time.h"
// #include "pam/pam.h"
#include "range.h"
#include "cuda.h"
// #include "cuda_kernel.h"
#include "cuda_runtime.h"

__global__ void count(point* points, query* queries, int* result, int n){
  int tid = blockIdx.x * blockDim.x + threadIdx.x;
  result[tid] = 0;
  for (int i = 0; i < n; i++)
  {
    if (points[i].x <= queries[tid].x1 &&
       points[i].y <= queries[tid].x1 &&
       points[i].x >= queries[tid].x2 &&
       points[i].y >= queries[tid].y2){
        result[tid]++;
       }
  }
  
}

long range(Points const &points, Queries const &queries, bool verbose) {
  parlay::internal::timer t("range", verbose);
  point* point_list = (point*) malloc(points.size() * sizeof(point));
  query* query_list = (query*) malloc(queries.size() * sizeof(query));
  int* result_list = (int*) malloc(queries.size() * sizeof(int));

  for (int i = 0; i < points.size(); i++){
    point_list[i] = points.at(i);
  }
  for (int i = 0; i < queries.size(); i++){
    query_list[i] = queries.at(i);
  }
  point* dev_points;
  query* dev_queries;
  int* dev_result;


  cudaMalloc(&dev_points, points.size() * sizeof(point));
  cudaMalloc(&dev_queries, queries.size() * sizeof(query));
  cudaMalloc(&dev_result, queries.size() * sizeof(int));

  cudaMemcpy(dev_points, point_list, points.size() * sizeof(point), cudaMemcpyHostToDevice);
  cudaMemcpy(dev_queries, query_list, queries.size() * sizeof(query), cudaMemcpyHostToDevice);



  t.next("build");
  count <<<1,queries.size()>>>(dev_points, dev_queries, dev_result, points.size());
  cudaMemcpy(result_list, dev_result, queries.size() * sizeof(int), cudaMemcpyDeviceToHost);
  for (int i = 0; i < queries.size(); i++)
  {
    std::cout<<result_list[i] << std::endl;
  }
  std::cerr << "salam";
  
  /*auto result_s = parlay::map(queries, [&] (query q) {
  	          return (long) r.count_in_range(q);});
  long total = parlay::reduce(result_s);*/
  t.next("query");

#ifdef CHECK
  //check
  //int num_queries = queries.size();
  int num_queries = 10; //only check 10 of them 
  int n = points.size();
  size_t total_check = 0;
	for (int i = 0; i < num_queries; i++) {
		//cout << "query: " << queries[i].x1 << " " << queries[i].y1 << " " << queries[i].x2 << " " << queries[i].y2 << endl;
		size_t t = 0;
		for (int j = 0; j < n; j++) {
			 if ((points[j].x > queries[i].x1) && (points[j].x < queries[i].x2) && (points[j].y > queries[i].y1) && (points[j].y < queries[i].y2)) t++;
		}
		long res = r.count_in_range(queries[i]);
		cout << "query " << i << ", naive: " << t << ", PAM: " << res << endl;
		total_check += t;
	}
  cout << "total: " << total << endl;
  cout << "total_check: " << total_check << endl;
#endif

  cudaFree(&dev_points);
  cudaFree(&dev_queries);
  cudaFree(&dev_result);

  // r.clear();
  t.next("clear");
  return 0;
}
