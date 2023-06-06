from gwf import Workflow
from gwf import AnonymousTarget
import os.path
import glob

gwf = Workflow(defaults={'cores':4,'memory':'16gb','account':'anne_ane_bsc','walltime':'01:00:00'})


def chi2(codeml_file, output_dir):
    gene_name = os.path.splitext(os.path.basename(codeml_file))[0]
    inputs = [codeml_file]
    outputs = [output_dir+"/{}_chi2.results".format(gene_name)]
    options = {}
    spec = """python chi123AnneMai.py {input1} {output1}""".format(input1=inputs[0], output1=outputs[0])
    return AnonymousTarget(inputs=inputs, outputs=outputs, options=options, spec=spec)



codeml_output_dir2 = "data/AMi/codeml_results"


chi2_output_dir2 = "data/AMi/chi2_results"
if not os.path.exists(chi2_output_dir2):
    os.makedirs(chi2_output_dir2)

codeml_outputs2 = gwf.glob(codeml_output_dir2+"/*.results")
for index, path in enumerate(codeml_outputs2):
    gwf.target_from_template(name="Chi2_2_{}".format(index), template=chi2(codeml_file=path, output_dir=chi2_output_dir2))

