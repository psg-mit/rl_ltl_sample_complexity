from typing import Dict, Any, Callable

import re
import subprocess
import tempfile
import pathlib
import concurrent.futures
import os
import functools

import typer
import tqdm

mungojerrie_path = "mungojerrie/build/mungojerrie"

pattern = re.compile(rf"PAC Probability for tol (\d+(\.\d*)?) is: (?P<satprob>\d+(\.\d*)?)±(?P<std>\d+(\.\d*)?)")

def estimate_pac_probability(epsilon: float, 
                             model: str, 
                             min_num_samples: int = 100, 
                             max_est_std: float = 1e-3,
                             reward_type: str = "multi-discount", 
                             discount: float = 0.99999,
                             gammaB: float=0.99, 
                             learn="Q", 
                             ep_number: int = 100, 
                             tolerance=0.,
                             model_params: Dict[str, Any] = None):
    if model_params is None:
        model_params = {}

    with tempfile.NamedTemporaryFile(mode='w+') as tmp:
        model_str = pathlib.Path(f"{model}.prism").read_text()
        model_str = model_str.format(**model_params)
        tmp.write(model_str)
        tmp.flush()
        output = subprocess.check_output(
            [
                mungojerrie_path, tmp.name, 
                "--ltl-file", f"{model}.ltl",
                "--est-pac",
                "--reward-type", reward_type, 
                "--discount", str(discount),
                "--gammaB", str(gammaB),
                "--learn", learn, 
                "--tolerance", str(tolerance), 
                "--ep-number", str(ep_number),
                "--est-pac-probability-min-samples", str(min_num_samples),
                "--est-pac-max-std", str(max_est_std),
                "--est-pac-epsilon", str(epsilon),
                # "--seed", str(2),
            ], 
            # stderr=subprocess.DEVNULL
        )
    output = output.decode("utf-8")
    print(output)
    match = pattern.search(output)
    pac_prob = float(match.group("satprob"))
    pac_prob_std = float(match.group("std"))
    return pac_prob, pac_prob_std

def binsearch_ep_number(f, n, interval):
    lb, ub = interval
    lb_val, lb_val_var =f(lb)

prob = estimate_pac_probability(
    epsilon=0.001,
    model="models/gltl_paper_fig2",
    model_params=dict(P1=1, P2=0.99),
    ep_number=10000,
    min_num_samples=1000,
    max_est_std=0.05,
)
print(prob)
