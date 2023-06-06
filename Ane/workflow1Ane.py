from gwf import Workflow
from gwf import AnonymousTarget
import os.path
import glob

gwf = Workflow(defaults={'cores':4,'memory':'16gb','account':'anne_ane_bsc','walltime':'01:00:00'})

### Codeml

work_path="data/output_donejohn"

def codeml(chrom, gene, output_dir, number):
    inputs = [work_path+"/{}/{}/{}.phylip".format(chrom, gene, gene), work_path+"/{}/{}/{}.nw".format(chrom, gene, gene)]
    outputs = [output_dir+"/{}_{}.results".format(chrom, gene), "codeml_ctl_{}/{}_{}.ctl".format(number, chrom, gene)]
    options = {}
    spec = """python codeml2.py {input1} {input2} {output1} {output2}_{output3}.ctl codeml_ctl_{dir}""".format(input1=inputs[0], input2=inputs[1], output1=outputs[0], output2=chrom, output3=gene, dir=number)
    return AnonymousTarget(inputs=inputs, outputs=outputs, options=options, spec=spec)

# Channel gene dictionary printet by cvs_to_dict.py
channel_dict={'chr1': ['MCOLN3', 'CACNA1S', 'KCNK2', 'KCNC4', 'KCNQ4', 'KCNK1', 'KCNA10', 'KCNH1', 'KCNN3', 'HCN3', 'MCOLN2', 'KCND3', 'KCNA3', 'KCNA2', 'CATSPERE', 'CATSPER4', 'CACNA1E'], 'chr10': ['PKD2L1', 'KCNMA1', 'CACNB2', 'KCNK18'], 'chr11': ['KCNQ1', 'TRPM5', 'KCNC1', 'CNGA4', 'TRPC6', 'SCN2B', 'TPCN2', 'SCN3B', 'KCNK7', 'CATSPER1', 'SCN4B', 'KCNA4', 'KCNK4', 'CATSPERZ'], 'chr12': ['TRPV4', 'KCNA1', 'HVCN1', 'KCNH3', 'CACNA2D4', 'CACNA1C', 'KCNA6', 'KCNC2', 'CACNB3', 'TPCN1', 'SCN8A'], 'chr13': ['TRPC4'], 'chr14': ['CATSPERB', 'KCNH5', 'KCNK13'], 'chr15': ['TRPM7', 'HCN4', 'CATSPER2'], 'chr16': ['CACNG3', 'CNGB1', 'KCNG4', 'CACNA1H'], 'chr17': ['CACNA1G', 'SCN4A', 'CACNB1', 'CACNG5', 'CACNG4', 'KCNH4', 'CACNG1', 'TRPV3', 'KCNH6', 'TRPV2', 'TRPV1'], 'chr18': ['KCNG2'], 'chr19': ['MCOLN1', 'KCNK6', 'CATSPERG', 'KCNN4', 'KCNA7', 'CACNG7', 'KCNN1', 'SCN1B', 'CACNG6', 'TRPM4', 'KCNC3', 'CACNA1A', 'CATSPERD'], 'chr2': ['SCN2A', 'SCN1A', 'TRPM8', 'SCN3A', 'KCNF1', 'SCN9A', 'KCNS3', 'KCNG3', 'KCNK3', 'CACNB4', 'KCNK12', 'KCNH7'], 'chr20': ['KCNG1', 'KCNQ2', 'KCNS1', 'KCNK15', 'KCNB1'], 'chr21': ['TRPM2'], 'chr22': ['CACNG2'], 'chr3': ['CACNA2D2', 'TRPC1', 'CACNA1D', 'CACNA2D3', 'SCN11A', 'SCN5A', 'KCNH8', 'SCN10A'], 'chr4': ['PKD2', 'TRPC3', 'CNGA1'], 'chr5': ['TRPC7', 'PKD2L2', 'KCNN2', 'CATSPER3'], 'chr6': ['KCNK16', 'KCNK17', 'KCNK5'], 'chr7': ['KCNH2', 'TRPV5', 'CACNA2D1', 'KCND2'], 'chr8': ['TRPA1', 'KCNS2', 'KCNV1', 'KCNK9', 'KCNB2', 'KCNQ3', 'KCNU1'], 'chr9': ['TRPM3', 'TRPM6', 'CACNA1B', 'KCNV2'], 'chrX': ['TRPC5', 'KCND1', 'CNGA2']}

Ane_dir = "data/Ane1"
if not os.path.exists(Ane_dir):
    os.makedirs(Ane_dir)

# Run Codeml on Channel Genes
codeml_channel_output_dir = Ane_dir+"/codeml_results_channels"
if not os.path.exists(codeml_channel_output_dir):
    os.makedirs(codeml_channel_output_dir)

for key in channel_dict:
    for value in channel_dict[key]:
        chromosome=key
        genename=value
        targetname="RunCodeml_channels_{}_{}".format(chromosome, genename.replace("-", "_"))
        gwf.target_from_template(name=targetname, template=codeml(chrom=chromosome, gene=genename, output_dir=codeml_channel_output_dir, number="_channel"))
