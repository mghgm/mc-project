// This code is part of the Problem Based Benchmark Suite (PBBS)
// Copyright (c) 2011 Guy Blelloch and the PBBS team
//
// Permission is hereby granted, free of charge, to any person obtaining a
// copy of this software and associated documentation files (the
// "Software"), to deal in the Software without restriction, including
// without limitation the rights (to use, copy, modify, merge, publish,
// distribute, sublicense, and/or sell copies of the Software, and to
// permit persons to whom the Software is furnished to do so, subject to
// the following conditions:
//
// The above copyright notice and this permission notice shall be included
// in all copies or substantial portions of the Software.
//
// THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
// OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
// MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
// NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
// LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
// OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
// WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

#include <iostream>
#include "parlay/primitives.h"
#include "common/graph.h"
#include "MIS.h"

// **************************************************************
//    MAXIMAL INDEPENDENT SET
// **************************************************************

parlay::sequence<char> maximalIndependentSet(Graph const &G)
{
  size_t n = G.n;
  parlay::sequence<char> Flags(n, (char) 0);
  for (size_t i = 0; i < n; i++) {
    Flags[i] = 1;
    for (size_t j = 0; j< G[i].degree; j++) {
      vertexId ngh = G[i].Neighbors[j];
      if (Flags[ngh] == 1) {
	Flags[i] = 2;
	break;
      }
    }
  }
  return Flags;
}
