from gwf import Workflow
from gwf import AnonymousTarget
import os.path
import glob

gwf = Workflow(defaults={'cores':4,'memory':'16gb','account':'anne_ane_bsc','walltime':'01:00:00'})

### Codeml

work_path="data/output_donejohn"

def codeml(chrom, gene, output_dir,number):
    inputs = [work_path+"/{}/{}/{}.phylip".format(chrom, gene, gene), work_path+"/{}/{}/{}.nw".format(chrom, gene, gene)]
    outputs = [output_dir+"/{}_{}.results".format(chrom, gene), "codeml_ctl_{}/{}_{}.ctl".format(number, chrom, gene)]
    options = {}
    spec = """python codeml2.py {input1} {input2} {output1} {output2}_{output3}.ctl codeml_ctl_{dir}""".format(input1=inputs[0], input2=inputs[1], output1=outputs[0], output2=chrom, output3=gene, dir=number)
    return AnonymousTarget(inputs=inputs, outputs=outputs, options=options, spec=spec)

gene_dict={'chr1': ['CD2', 'CR2', 'DR1', 'GBA', 'CR1', 'ACKR1'], 'chr10': ['HK1'], 'chr11': ['CXCR5', 'TH'], 'chr12': ['MIP'], 'chr16': ['CD19'], 'chr17': ['PITPNM3', 'CCR7', 'PYY', 'CCR10'], 'chr18': ['TYMS'], 'chr1_GL383519v1_alt': ['GBA'], 'chr2': ['CXCR4', 'ACKR3', 'CXCR1', 'CXCR2'], 'chr3': ['CP', 'CCRL2', 'CCR2', 'ACKR4', 'ACKR2', 'GPR15', 'CCR5', 'CCR1', 'CX3CR1', 'CXCR6', 'XCR1', 'CCR9', 'CCR8', 'CCR3', 'CCR4'], 'chr4': ['KDR'], 'chr6': ['CCR6'], 'chr7': ['NPY'], 'chr8': ['ARC'], 'chrX': ['CXCR3']}
AM_dir = "data/AMi"
if not os.path.exists(AM_dir):
    os.makedirs(AM_dir)


codeml_output = AM_dir+"/codeml_results"
if not os.path.exists(codeml_output):
    os.makedirs(codeml_output)

for key in gene_dict:
    for value in gene_dict[key]:
        chromosome=key
        genename=value
        targetname="RunCodeml_{}_{}".format(chromosome, genename.replace("-", "_"))
        gwf.target_from_template(name=targetname, template=codeml(chrom=chromosome, gene=genename, output_dir=codeml_output, number="AM"))

