import csv
import matplotlib as mpl
# mpl.use('Agg')
mpl.rcParams['grid.linestyle'] = ":"
mpl.rcParams.update({'font.size': 20})
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import numpy as np
import os
import statistics as st

# paper_ver = False

class DSInfo:
    def __init__(self, color, marker, linestyle, name, binary, ds_type):
        self.color = color
        self.marker = marker
        self.linestyle = linestyle
        self.name = name
        self.ds_type = ds_type
        self.binary = binary

mk = ['o', 'v', '^', '1', 's', '+', 'x', 'D', '|', '>', '<',]

dsinfo = {'neighbors_bench-1' :  DSInfo("C0", mk[0], "-", "CLEANN-Tree, k=1", "blah", "blah"),
          'neighbors_bench-10' : DSInfo("C1", mk[1], "-", "CLEANN-Tree, k=10", "blah", "blah"),
          'neighbors_bench_path_copy-1' :  DSInfo("C3", mk[3], "-", "CLEANN-Tree-PC, k=1", "blah", "blah"),
          'neighbors_bench_path_copy-10' : DSInfo("C4", mk[4], "-", "CLEANN-Tree-PC, k=10", "blah", "blah"),
          'range_bench-.014' : DSInfo("C0", mk[0], "-", "CLEANN-Tree, r=5", "blah", "blah"),
          'range_bench-.0176' : DSInfo("C1", mk[1], "-", "CLEANN-Tree, r=10", "blah", "blah"),
          'range_bench_path_copy-.014' : DSInfo("C3", mk[3], "-", "CLEANN-Tree-PC, r=5", "blah", "blah"),
          'range_bench_path_copy-.0176' : DSInfo("C4", mk[4], "-", "CLEANN-Tree-PC, r=10", "blah", "blah"),
} 

# # datastructures = ["leaftree", "arttree"]
# ds_list = { 'tree-ours-trylock-lb'        : ['leaftree-trylock-lb', 'arttree-trylock-lb', 'arttree_opt-trylock-lb', 'blockleaftree-trylock-lb', 'blockleaftree-b-trylock-lb'],
#             'tree-ours-trylock-lf'        : ['leaftree-trylock-lf', 'arttree-trylock-lf', 'arttree_opt-trylock-lf', 'blockleaftree-trylock-lf', 'blockleaftree-b-trylock-lf'],
#             'tree-theirs'                 : ['bronson', 'drachsler', 'natarajan'], #, 'chromatic', 'ellen', 'guerraoui', ],

#             'list-ours-trylock-lb'        : ['list-trylock-lb', 'dlist-trylock-lb'], 
#             'list-ours-trylock-lf'        : ['list-trylock-lf', 'dlist-trylock-lf'], 
#             'list-theirs'                 : ['harris_list'], #, 'mwcas_dlist', harris_list_opt'],

#             'trees'           : ['chromatic', 'leaftree-trylock-lb', 'leaftree-trylock-lf', 'bronson', 'drachsler', 'natarajan', 'ellen', 'scx_bst'],
#             'rtrees'          : ['leaftree-trylock-lb', 'leaftree-trylock-lf', 'arttree-trylock-lb', 'blockleaftree-b-lb', 'blockleaftree-b-trylock-lb', 'arttree-trylock-lf', 'blockleaftree-b-lf', 'blockleaftree-b-trylock-lf', 'hash_optimistic-trylock-lf', 'hash_optimistic-trylock-lb', ], # 'arttree_opt-trylock-lb', 'arttree_opt-trylock-lf', 
#             'lists'           : ['list-trylock-lb', 'dlist-trylock-lb', 'list-trylock-lf', 'dlist-trylock-lf', 'harris_list', 'harris_list_opt'],
#             'our-lists'           : ['list-trylock-lb', 'list-trylock-lf'],

#             # 'leftovers-list'       : ['list-trylock-lb', 'dlist-trylock-lb', 'list-trylock-lf', 'dlist-trylock-lf', 'harris_list', 'harris_list_opt'],
#             'leftovers-list'       : ['harris_list', 'harris_list_opt'],
#             'leftovers-tree'       : ['leaftree-trylock-lb', 'leaftree-trylock-lf', 'leaftree-lb', 'leaftree-lf'],
#             # 'leftovers-rtree'      : ['hash_optimistic-trylock-lf', 'hash_optimistic-trylock-lb'],
#             'leftovers-rtree'      : ['blockleaftree-b-lb', 'blockleaftree-b-lf'],

#             'test_list'       : ['list-trylock-lf'],
#             'test_tree'       : ['bronson'],
#             'test_chromatic'       : ['chromatic'],
#             'test_scx_bst'       : ['scx_bst'],
#             # 'test_abtree'       : ['abtree','sri_abtree','sri_abtree_mcs','sri_abtree_pub','chromatic'],
#             'test_abtree'       : ['chromatic', 'sri_abtree_mcs','sri_abtree_pub'],
#             # 'test_abtree'       : ['abtree'],

#             'test_mwcas_dlist'       : ['mwcas_dlist'],
#             'test_arttree'       : ['arttree-trylock-lb', "arttree-trylock-lf"],

#             'try_lock_exp'   : ['leaftree-lb', 'leaftree-lf', 'leaftree-trylock-lf', 'leaftree-trylock-lb', ],
# }

# datastructures = {}
# datastructures['lists'] = ds_list['list-ours-trylock-lb'] + ds_list['list-ours-trylock-lf'] + ds_list['list-theirs']
# datastructures['tree'] = 

def toString(algname, th, ratio):
    return algname + '-' + str(th) + 'u-' + str(ratio)

# def export_legend(legend, filename="legend.pdf", expand=[-5,-5,5,5]):
#     fig  = legend.figure
#     fig.canvas.draw()
#     bbox  = legend.get_window_extent()
#     bbox = bbox.from_extents(*(bbox.extents + np.array(expand)))
#     bbox = bbox.transformed(fig.dpi_scale_trans.inverted())
#     fig.savefig(filename, dpi="figure", bbox_inches=bbox)

def export_legend(legend, filename="legend.pdf"):
    fig  = legend.figure
    fig.canvas.draw()
    bbox  = legend.get_window_extent().transformed(fig.dpi_scale_trans.inverted())
    fig.savefig(filename, dpi="figure", bbox_inches=bbox)

def avg(numlist):
  # if len(numlist) == 1:
  #   return numlist[0]
  total = 0.0
  length = 0
  for num in numlist:
    length=length+1
    total += float(num)
  if length > 0:
    return 1.0*total/length
  else:
    return -1;

def readResultsFile(filename, throughput, stddev, threads, ratios, algs):
  throughputRaw = {}
  alg = ""
  th = ""
  ratio = ""
  maxkey = ""
  alpha = ""
  warm_up_runs = 0

  file = open(filename, 'r')
  query_sizes=[]
  for line in file.readlines():
    if line.find('query size:') != -1:
      k = int(line.split(': ')[1])
      query_sizes.append(k)

  # read csv into throughputRaw
  file = open(filename, 'r')
  for line in file.readlines():
    line = line.strip()
    if line.find('warm_up_runs') != -1:
      warm_up_runs = int(line.split(' ')[1])
    elif line.find('datastructure:') != -1:
      alg = line.split(' ')[1]
    elif line.find('threads:') != -1:
      th = int(line.split(' ')[1])
    elif line.find('update_percent:') != -1:
      ratio = int(line.split(' ')[1])
    elif line.find('throughput (Mop/s):') != -1:
      tp = float(line.split(': ')[1])
      if alg not in algs:
        algs.append(alg)
      if th not in threads:
        threads.append(th)
      if ratio not in ratios:
        ratios.append(ratio)
      key = toString(alg, th, ratio)
      if key not in throughputRaw:
        throughputRaw[key] = []
      throughputRaw[key].append(tp)

  print(throughputRaw)
  # Average througputRaw into throughput

  for key in throughputRaw:
    results = throughputRaw[key][warm_up_runs:]
    print(results)
    throughput[key] = avg(results)
    stddev[key] = st.pstdev(results)

#   print(throughput)

def plot_alpha_graph(throughput, stddev, thread, ratio, maxkey, alphas, algs, graph_name, paper_ver=False):
  # print(graphtitle)
  graphtitle = graph_name + '-' + str(thread) + 'th-' + str(maxkey) + 'size-' + str(ratio) + 'up'
  if paper_ver:
    outputFile = 'graphs/' + graphtitle.replace('.', '') + '.pdf'
    mpl.rcParams.update({'font.size': 25})
  else:
    outputFile = 'graphs/' + graphtitle + '.png'

  ymax = 0
  series = {}
  error = {}
  for alg in algs:
    # if (alg == 'BatchBST64' or alg == 'ChromaticBatchBST64') and (bench.find('-0rq') == -1 or bench.find('2000000000') != -1):
    #   continue
    # if toString3(alg, 1, bench) not in results:
    #   continue
    series[alg] = []
    error[alg] = []
    for alpha in alphas:
      key = toString(alg, thread, ratio, maxkey, alpha)
      if key not in throughput:
        del series[alg]
        del error[alg]
        break
      series[alg].append(throughput[key])
      error[alg].append(stddev[key])
  
  if len(series) < 3:
    return

  fig, axs = plt.subplots()
  # fig = plt.figure()
  opacity = 0.8
  rects = {}
  
  xpos = np.arange(start=0, stop=len(alphas))

  for alg in algs:
    alginfo = dsinfo[alg]
    if alg not in series:
      continue
    ymax = max(ymax, max(series[alg]))
    # rects[alg] = axs.errorbar(xpos, series[alg], yerr=error[alg],
    # if graph_name == 'try_vs_strict_lock' and alginfo.name.find('leaftree-strict') == -1:
    if 'leaftree-lf' in algs and alginfo.name.find('leaftree-strict') == -1:
      rects[alg] = axs.plot(xpos, series[alg],
      alpha=opacity,
      color=alginfo.color,
      linewidth=3.0,
      #hatch=hatch[ds],
      linestyle=alginfo.linestyle,
      marker=alginfo.marker,
      markersize=14,
      label=alginfo.name.replace('leaftree-', 'leaftree-trylock-'))
    else:
      rects[alg] = axs.plot(xpos, series[alg],
        alpha=opacity,
        color=alginfo.color,
        linewidth=3.0,
        #hatch=hatch[ds],
        linestyle=alginfo.linestyle,
        marker=alginfo.marker,
        markersize=14,
        label=alginfo.name)

  plt.xticks(xpos, alphas)
  axs.set_ylim(bottom=-0.02*ymax)
  # plt.xticks(threads, threads)
  # axs.set_xlabel('Number of threads')
  # axs.set_ylabel('Throughput (Mop/s)')
  axs.set(xlabel='Zipfian parameter', ylabel='Throughput (Mop/s)')
  legend_x = 1
  legend_y = 0.5 
  # if this_file_name == 'Update_heavy_with_RQ_-_100K_Keys':
  #   plt.legend(loc='center left', bbox_to_anchor=(legend_x, legend_y))

  # plt.legend(framealpha=0.0)

  plt.grid()
  if 'leaftree-lf' in algs:
    plt.legend(loc='center left', bbox_to_anchor=(legend_x, legend_y))
  elif not paper_ver:
    plt.title(graphtitle)
    plt.legend(loc='center left', bbox_to_anchor=(legend_x, legend_y))
  plt.savefig(outputFile, bbox_inches='tight')
  plt.close('all')

def plot_alpha_graphs(throughput, stddev, threads, ratios, maxkeys, alphas, algs, graph_name, paper_ver=False):
  for thread in threads:
    for size in maxkeys:
      for ratio in ratios:
        sufficient_datapoints = False
        for alg in algs:
          num_datapoints = 0
          for alpha in alphas:
            if toString(alg, thread, ratio, size, alpha) in throughput:
              num_datapoints += 1
          if num_datapoints > 2:
            sufficient_datapoints = True
        if sufficient_datapoints:
          plot_alpha_graph(throughput, stddev, thread, ratio, size, alphas, algs, graph_name, paper_ver)

def plot_size_graph(throughput, stddev, thread, ratio, maxkeys, alpha, algs, graph_name, paper_ver=False):
  # print(graphtitle)
  graphtitle = graph_name + '-' + str(thread) + 'th-' + str(ratio) + 'up-' + str(alpha) + 'alpha'
  if paper_ver:
    outputFile = 'graphs/' + graphtitle.replace('.', '') + '.pdf'
    mpl.rcParams.update({'font.size': 25})
  else:
    outputFile = 'graphs/' + graphtitle + '.png'

  ymax = 0
  series = {}
  error = {}
  for alg in algs:
    # if (alg == 'BatchBST64' or alg == 'ChromaticBatchBST64') and (bench.find('-0rq') == -1 or bench.find('2000000000') != -1):
    #   continue
    # if toString3(alg, 1, bench) not in results:
    #   continue
    series[alg] = []
    error[alg] = []
    for maxkey in maxkeys:
      key = toString(alg, thread, ratio, maxkey, alpha)
      if key not in throughput:
        del series[alg]
        del error[alg]
        break
      series[alg].append(throughput[key])
      error[alg].append(stddev[key])
  if len(series) < 3:
    return

  fig, axs = plt.subplots()
  # fig = plt.figure()
  opacity = 0.8
  rects = {}
  
  for alg in algs:
    alginfo = dsinfo[alg]
    if alg not in series:
      continue
    ymax = max(ymax, max(series[alg]))
    # rects[alg] = axs.errorbar(maxkeys, series[alg], yerr=error[alg],
    rects[alg] = axs.plot(maxkeys, series[alg],
      alpha=opacity,
      color=alginfo.color,
      #hatch=hatch[ds],
      linewidth=3.0,
      linestyle=alginfo.linestyle,
      marker=alginfo.marker,
      markersize=14,
      label=alginfo.name)

  # if maxkeys[-1] > 1000000:
  #   plt.axvline(1000000, linestyle='--', color='grey') 
  axs.set_xscale('log')
  axs.set_ylim(bottom=-0.02*ymax)
  # plt.xticks(threads, threads)
  # axs.set_xlabel('Number of threads')
  # axs.set_ylabel('Throughput (Mop/s)')
  axs.set(xlabel='Datastructure size', ylabel='Throughput (Mop/s)')
  legend_x = 1
  legend_y = 0.5 
  # if this_file_name == 'Update_heavy_with_RQ_-_100K_Keys':
  #   plt.legend(loc='center left', bbox_to_anchor=(legend_x, legend_y))

  # plt.legend(framealpha=0.0)
  plt.grid()
  if not paper_ver:
    plt.title(graphtitle)
    plt.legend(loc='center left', bbox_to_anchor=(legend_x, legend_y))
  plt.savefig(outputFile, bbox_inches='tight')
  plt.close('all')

def plot_size_graphs(throughput, stddev, threads, ratios, maxkeys, alphas, algs, graph_name, paper_ver=False):
  for thread in threads:
    for ratio in ratios:
      for alpha in alphas:
        sufficient_datapoints = False
        xaxis = []
        for alg in algs:
          num_datapoints = 0
          for size in maxkeys:
            if toString(alg, thread, ratio, size, alpha) in throughput:
              num_datapoints += 1
              if size not in xaxis:
                xaxis.append(size)
          if num_datapoints > 2:
            sufficient_datapoints = True
        if sufficient_datapoints:
          plot_size_graph(throughput, stddev, thread, ratio, xaxis, alpha, algs, graph_name, paper_ver)


def plot_ratio_graph(throughput, stddev, thread, ratios, maxkey, alpha, algs, graph_name, paper_ver=False):
  # print(graphtitle)
  graphtitle = graph_name + '-' + str(thread) + 'th-' + str(maxkey) + 'size-' + str(alpha) + 'alpha'
  if paper_ver:
    outputFile = 'graphs/' + graphtitle.replace('.', '') + '.pdf'
    mpl.rcParams.update({'font.size': 25})
  else:
    outputFile = 'graphs/' + graphtitle + '.png'

  ymax = 0
  series = {}
  error = {}
  for alg in algs:
    # if (alg == 'BatchBST64' or alg == 'ChromaticBatchBST64') and (bench.find('-0rq') == -1 or bench.find('2000000000') != -1):
    #   continue
    # if toString3(alg, 1, bench) not in results:
    #   continue
    series[alg] = []
    error[alg] = []
    for ratio in ratios:
      key = toString(alg, thread, ratio, maxkey, alpha)
      if key not in throughput:
        del series[alg]
        del error[alg]
        break
      series[alg].append(throughput[key])
      error[alg].append(stddev[key])
  if len(series) < 3:
    return

  fig, axs = plt.subplots()
  # fig = plt.figure()
  opacity = 0.8
  rects = {}
  
  xpos = np.arange(start=0, stop=len(ratios))

  for alg in algs:
    alginfo = dsinfo[alg]
    if alg not in series:
      continue
    ymax = max(ymax, max(series[alg]))
    # rects[alg] = axs.errorbar(xpos, series[alg], yerr=error[alg],
    rects[alg] = axs.plot(xpos, series[alg],
      alpha=opacity,
      color=alginfo.color,
      linewidth=3.0,
      #hatch=hatch[ds],
      linestyle=alginfo.linestyle,
      marker=alginfo.marker,
      markersize=14,
      label=alginfo.name)

  plt.xticks(xpos, ratios)
  axs.set_ylim(bottom=-0.02*ymax)
  # plt.xticks(threads, threads)
  # axs.set_xlabel('Number of threads')
  # axs.set_ylabel('Throughput (Mop/s)')
  axs.set(xlabel='Update percentage', ylabel='Throughput (Mop/s)')
  legend_x = 1
  legend_y = 0.5 
  # if this_file_name == 'Update_heavy_with_RQ_-_100K_Keys':
  #   plt.legend(loc='center left', bbox_to_anchor=(legend_x, legend_y))

  # plt.legend(framealpha=0.0)
  plt.grid()
  if not paper_ver:
    plt.title(graphtitle)
    plt.legend(loc='center left', bbox_to_anchor=(legend_x, legend_y))
  plt.savefig(outputFile, bbox_inches='tight')
  plt.close('all')

def plot_ratio_graphs(throughput, stddev, threads, ratios, maxkeys, alphas, algs, graph_name, paper_ver=False):
  for thread in threads:
    for size in maxkeys:
      for alpha in alphas:
        sufficient_datapoints = False
        for alg in algs:
          num_datapoints = 0
          for ratio in ratios:
            if toString(alg, thread, ratio, size, alpha) in throughput:
              num_datapoints += 1
          if num_datapoints > 2:
            sufficient_datapoints = True
        if sufficient_datapoints:
          plot_ratio_graph(throughput, stddev, thread, ratios, size, alpha, algs, graph_name, paper_ver)


def plot_scalability_graph(throughput, stddev, threads, ratio, algs, graph_name, paper_ver=False):
  graphtitle = graph_name + '-' + str(ratio) 
  if paper_ver:
    outputFile = 'graphs/' + graphtitle.replace('.', '') + '.pdf'
    mpl.rcParams.update({'font.size': 25})
  else:
    outputFile = 'graphs/' + graphtitle + '.png'
  print("plotting " + outputFile)

  ymax = 0
  series = {}
  error = {}
  for alg in algs:
    series[alg] = []
    error[alg] = []
    for th in threads:
      key = toString(alg, th, ratio)
      if key not in throughput:
        del series[alg]
        del error[alg]
        break
      series[alg].append(throughput[key])
      error[alg].append(stddev[key])
  fig, axs = plt.subplots()
  # fig = plt.figure()
  opacity = 0.8
  rects = {}
  
  for alg in algs:
    alginfo = dsinfo[alg]
    if alg not in series:
      continue
    ymax = max(ymax, max(series[alg]))
    # rects[alg] = axs.errorbar(threads, series[alg], yerr=error[alg],
    rects[alg] = axs.plot(threads, series[alg],
      alpha=opacity,
      color=alginfo.color,
      linewidth=3.0,
      #hatch=hatch[ds],
      linestyle=alginfo.linestyle,
      marker=alginfo.marker,
      markersize=14,
      label=alginfo.name)

  axs.set_ylim(bottom=-0.02*ymax)
  # plt.xticks(threads, threads)
  # axs.set_xlabel('Number of threads')
  # axs.set_ylabel('Throughput (Mop/s)')
  plt.axvline(144, linestyle='--', color='grey') 
  axs.set(xlabel='Number of threads', ylabel='Throughput (Mop/s)')
  legend_x = 1
  legend_y = 0.5 
  # if this_file_name == 'Update_heavy_with_RQ_-_100K_Keys':
  #   plt.legend(loc='center left', bbox_to_anchor=(legend_x, legend_y))



  # plt.legend(framealpha=0.0)
  plt.grid()

  if not paper_ver:
    plt.title(graphtitle)
    plt.legend(loc='center left', bbox_to_anchor=(legend_x, legend_y))
  
  plt.savefig(outputFile, bbox_inches='tight')

  if paper_ver:
    if graph_name == 'lists':
      legend = plt.legend(loc='center left', bbox_to_anchor=(legend_x, legend_y), ncol=2, framealpha=0.0)
    elif graph_name == 'sets':
      legend = plt.legend(loc='center left', bbox_to_anchor=(legend_x, legend_y), ncol=3, framealpha=0.0)
    else:
      legend = plt.legend(loc='center left', bbox_to_anchor=(legend_x, legend_y), ncol=8, framealpha=0.0)
    # outputFile = 'graphs/' + graph_name + '_legend.pdf'
    # legend = plt.legend(loc='center left', bbox_to_anchor=(legend_x, legend_y), ncol=7, framealpha=0.0)
    export_legend(legend, 'graphs/' + graph_name + '_legend.pdf')
    # plt.close('all')
    # return
  
  plt.close('all')

def plot_scalability_graphs(throughput, stddev, threads, ratios, algs, graph_name, paper_ver=False):
  for ratio in ratios:
    sufficient_datapoints = False
    print(algs)
    for alg in algs:
        num_datapoints = 0
        for th in threads:
            print(toString(alg, th, ratio))
            if toString(alg, th, ratio) in throughput:
                num_datapoints += 1
        # print(num_datapoints)
        if num_datapoints > 2:
            sufficient_datapoints = True
    print(sufficient_datapoints)
    if sufficient_datapoints:
        plot_scalability_graph(throughput, stddev, threads, ratio, algs, graph_name, paper_ver)


def plot_all_graphs(throughput, stddev, threads, ratios, maxkeys, alphas, algs, graph_name):
  print("plotting scalability graphs for: " + graph_name)
  plot_scalability_graphs(throughput, stddev, threads, ratios, maxkeys, alphas, algs, graph_name)
  print("plotting ratio graphs for: " + graph_name)
  plot_ratio_graphs(throughput, stddev, threads, ratios, maxkeys, alphas, algs, graph_name)
  print("plotting alpha graphs for: " + graph_name)
  plot_alpha_graphs(throughput, stddev, threads, ratios, maxkeys, alphas, algs, graph_name)
  print("plotting size graphs for: " + graph_name)
  plot_size_graphs(throughput, stddev, threads, ratios, maxkeys, alphas, algs, graph_name)

if __name__ == "__main__":
  throughput = {}
  stddev = {}
  threads = []
  ratios = []
  maxkeys = []
  alphas = []
  algs = []

  for filename in input_files:
    readResultsFile(filename, throughput, stddev, threads, ratios, maxkeys, alphas, algs)

  threads.sort()
  ratios.sort()
  maxkeys.sort()
  alphas.sort()

  print('threads: ' + str(threads))
  print('update ratios: ' + str(ratios))
  print('maxkeys: ' + str(maxkeys))
  print('alphas: ' + str(alphas))
  print('algs: ' + str(algs))

  plot_scalability_graph(throughput, stddev, threads, 50, 100000, 0.75, ds_list["try_lock_exp"], "try_vs_strict_lock", True)
  plot_scalability_graph(throughput, stddev, threads, 50, 100000, 0.75, ds_list["trees"], "trees", True)
  plot_scalability_graph(throughput, stddev, threads, 50, 100, 0.75, ds_list["lists"], "lists", True)
  plot_scalability_graph(throughput, stddev, threads, 50, 100000, 0.75, ds_list["rtrees"], "rtrees", True)

  plot_all_graphs(throughput, stddev, threads, ratios, maxkeys, alphas, ds_list["try_lock_exp"], "try_vs_strict_lock")
  plot_all_graphs(throughput, stddev, threads, ratios, maxkeys, alphas, ds_list["trees"], "trees")
  plot_all_graphs(throughput, stddev, threads, ratios, maxkeys, alphas, ds_list["lists"], "lists")
  plot_all_graphs(throughput, stddev, threads, ratios, maxkeys, alphas, ds_list["rtrees"], "rtrees")