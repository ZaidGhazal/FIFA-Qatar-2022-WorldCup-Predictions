#!/bin/bash
echo "------------------ 1. Creating Conda venv ------------------"
conda env create -f environment.yml
echo "------------------ 2. Activating the Created Environment ------------------"
eval "$(conda shell.bash hook)"
conda activate worldcup-winner-predictor-env
echo "------------------ 3. Installing Pre-commit hooks ------------------"
pre-commit install