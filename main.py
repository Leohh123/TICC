from TICC_solver import TICC
import numpy as np
import sys
import os
import argparse
import errno
from datetime import datetime


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--window-size', '-w', dest='window_size', metavar='W',
                        type=int, default=5, help='window size')
    parser.add_argument('--clusters', '-k', dest='clusters', metavar='K',
                        type=int, default=5, help='number of clusters')
    parser.add_argument('--lambda', '-l', dest='lambda_', metavar='L',
                        type=float, default=11e-2, help='sparsity parameter')
    parser.add_argument('--beta', '-b', dest='beta', metavar='B',
                        type=float, default=600, help='temporal consistency parameter')
    parser.add_argument('--max-iters', '-i', dest='max_iters', metavar='I',
                        type=int, default=100, help='maximum number of iterations')
    parser.add_argument('--threshold', '-t', dest='threshold', metavar='T',
                        type=float, default=2e-5, help='convergence threshold')
    parser.add_argument('--processes', '-p', dest='processes', metavar='P',
                        type=int, default=1, help='number of worker processes')
    parser.add_argument('--data', '-d', dest='data', metavar='D',
                        type=str, required=True, help='input data file path')
    parser.add_argument('--out', '-o', dest='out', metavar='O',
                        type=str, default='out', help='output directory')
    return parser.parse_args()


def prepare_out_directory(args):
    run_id = datetime.now().strftime('%m%d%H%M') + \
        f'_w={args.window_size}&k={args.clusters}&b={args.beta}&i={args.max_iters}&t={args.threshold}'
    logdir = os.path.join(args.out, run_id)
    print(logdir)
    if not os.path.exists(logdir):
        try:
            os.makedirs(logdir)
        except OSError as exc:  # Guard against race condition of path already existing
            if exc.errno != errno.EEXIST:
                raise
    return logdir


args = get_args()
logdir = prepare_out_directory(args)


ticc = TICC(
    window_size=args.window_size,
    number_of_clusters=args.clusters,
    lambda_parameter=args.lambda_,
    beta=args.beta,
    maxIters=args.max_iters,
    threshold=args.threshold,
    write_out_file=True,
    prefix_string=logdir,
    num_proc=args.processes
)
cluster_assignment, cluster_MRFs = ticc.fit(input_file=args.data)

# print(cluster_assignment)
np.savetxt(os.path.join(logdir, 'assignment.out'),
           cluster_assignment, fmt='%d', delimiter=',')

# print(cluster_MRFs)
for k, v in cluster_MRFs.items():
    np.savetxt(os.path.join(logdir, f'mrf_{k}.out'),
               v, fmt='%.4f', delimiter='\t')
