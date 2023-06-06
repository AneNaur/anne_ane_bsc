from gwf import Workflow
from gwf import AnonymousTarget
import os.path
import glob

gwf = Workflow(defaults={'cores':4,'memory':'16gb','account':'anne_ane_bsc','walltime':'01:00:00'})


def chi2(codeml_file, output_dir, significant_file):
    gene_name = os.path.splitext(os.path.basename(codeml_file))[0]
    inputs = [codeml_file]
    outputs = [output_dir+"/{}_chi2.results".format(gene_name)]
    options = {}
    spec = """python chi123Ane.py {input1} {output1} {output2}""".format(input1=inputs[0], output1=outputs[0], output2=significant_file)
    return AnonymousTarget(inputs=inputs, outputs=outputs, options=options, spec=spec)


# Channel genes
codeml_output_dir_channel = "data/Ane1/codeml_results_channels"

chi2_output_dir_channel = "data/Ane1/chi2_results_channels"
if not os.path.exists(chi2_output_dir_channel):
    os.makedirs(chi2_output_dir_channel)

significant_channel = "significant_chi2_channels.txt"

codeml_outputs_channel = gwf.glob(codeml_output_dir_channel+"/*.results")
for index, path in enumerate(codeml_outputs_channel):
    gwf.target_from_template(name="Chi2_channel_{}".format(index), template=chi2(codeml_file=path, output_dir=chi2_output_dir_channel, significant_file=significant_channel))