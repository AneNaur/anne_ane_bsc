from Bio.Phylo.PAML import codeml
from Bio.Phylo.PAML.chi2 import cdf_chi2
import argparse
import sys
import os
from pprint import pprint
from scipy.stats import chi2


def test_LRT(lnL0, lnLAlt):
    pval=1-chi2.cdf(2*(lnLAlt-lnL0),2)
    return pval


parser =argparse.ArgumentParser(description= ''' chi2 
''')

parser.add_argument('codeml_results', type=str, help='Codeml results file as input to chi 2 test')
parser.add_argument('output_file', type=str, help='chi 2 output file')


args =parser.parse_args()
results=codeml.read(args.codeml_results)


lnL1=results["NSsites"][1]["lnL"]
lnL2=results["NSsites"][2]["lnL"]
lnL7=results["NSsites"][7]["lnL"]
lnL8=results["NSsites"][8]["lnL"]

p_values={}


if lnL1 < lnL2:
    p_values[2] =test_LRT(lnL1,lnL2)
else:
    p_values[2]=1

if lnL7 < lnL8:
    p_values[8] =test_LRT(lnL7,lnL8)
else:
    p_values[8]=1

gene_name = os.path.splitext(os.path.basename(args.codeml_results))[0]

with open(args.output_file, 'w') as f:
    for key, value in p_values.items():
        omega = 'dN/ds_close_to_1'
        if value <= 0.05 / 2:
            site = max(results["NSsites"][key]["parameters"]["site classes"].keys())
            omega = results["NSsites"][key]["parameters"]["site classes"][site]["omega"]
            with open("significant_chi2_AM_ny.txt", "a") as s:
                print(gene_name, ":", "model =", key, ", p-value =", value, ", omega =", omega, file=s, sep=" ")
        print(gene_name, ":", "model =", key, ", p-value =", value, ", omega =", omega, file=f, sep=" ")

#for key, value in p_values.items():
#    omega = 'dN/dS_close_to1'
#    with open(args.output_file, 'w') as f:
#        if value <= 1: #0.05 / 2:
#            maxsite = max(results["NSsites"][key]["parameters"]["site classes"].keys())
#            omega = results["NSsites"][key]["parameters"]["site classes"][maxsite]["omega"]
#            with open("significant_chi2.txt", "a") as s:
#                print(gene_name, key, value, omega, sep=",")
#        print(gene_name, key, value, omega, file=f, sep=',')


