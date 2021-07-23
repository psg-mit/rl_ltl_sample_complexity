from typing import Dict, Any, Callable

import re
import subprocess
import tempfile
import pathlib
import concurrent.futures
import os
import functools

import tqdm

mungojerrie_path = "mungojerrie/build/mungojerrie"

pattern = re.compile(rf"Probability for tol (\d+(\.\d*)?) is: (?P<satprob>\d+(\.\d*)?)")

def run_learning(model: str, 
				 reward_type: str = "multi-discount", 
				 discount: float = 0.99999,
				 gammaB: float=0.99, 
				 learn="Q", 
				 ep_number: int = 1000, 
				 tolerance=0.,
				 model_params: Dict[str, Any] = None):
	if model_params is None:
		model_params = {}

	with tempfile.NamedTemporaryFile(mode='w+') as tmp:
		model_str = pathlib.Path(f"{model}.prism").read_text()
		model_str = model_str.format(**model_params)
		tmp.write(model_str)
		tmp.flush()
		output = subprocess.check_output([
			mungojerrie_path, tmp.name, 
			"--ltl-file", f"{model}.ltl",
			"--reward-type", reward_type, 
			"--discount", str(discount),
			"--gammaB", str(gammaB),
			"--learn", learn, 
			"--tolerance", str(tolerance), 
			"--ep-number", str(ep_number)])
	output = output.decode("utf-8")
	match = pattern.search(output)
	sat_prob = float(match.group("satprob"))
	return sat_prob


def estimate_pac_probability(learn_f: Callable[[], float], 
							 epsilon: float,
							 target_value: float = 1.,
							 num_samples: int = 100):
	with concurrent.futures.ThreadPoolExecutor(os.cpu_count()) as executor:
		values = list(tqdm.tqdm(
			executor.map(lambda _: learn_f(), range(num_samples)), 
			total=num_samples))
	pac_prob = sum(1 for val in values if abs(val - target_value) < epsilon) / num_samples
	return pac_prob

prob = estimate_pac_probability(
	functools.partial(run_learning, 
		"gltl_paper_fig2", 
		model_params=dict(P2=0.9999),
		ep_number=1000
	),
	0.1
)
print(prob)
