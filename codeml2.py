from Bio.Phylo.PAML import codeml
import argparse
import sys
import os


parser = argparse.ArgumentParser(description='''
 codeml 
 ''')

parser.add_argument('alignment_file', type=str,
                    help='Alignment file')
parser.add_argument('tree_file', type=str,
                    help='Tree file.')
parser.add_argument('results_file', type=str,
                    help='Results file')
parser.add_argument('control_file', type=str,
                    help='Control file')
parser.add_argument('working_dir', type=str,
                    help='Working directory')

args = parser.parse_args()

cml = codeml.Codeml(alignment = args.alignment_file, tree = args.tree_file,
                out_file =  args.results_file, 
                working_dir = args.working_dir)


cml.set_options(noisy = 0, verbose=1, seqtype=1, ndata = 1, icode = 0, cleandata = 1, NSsites=[ 1, 2, 7, 8], CodonFreq = 2, fix_omega = 0, omega = 1, clock = 0, fix_alpha = 1, alpha = 0, getSE = 0)
#cml.set_options(runmode = 0, model = 0, aaDist = 0, Mgene = 0, fix_kappa = 0, kappa = 2, Malpha = 0, ncatG = 1, RateAncestor = 0, Small_Diff = .5e-06, method = 0, fix_blength = None)
cml.ctl_file = args.control_file


cml.run(verbose = True, command=os.path.abspath('codeml'))