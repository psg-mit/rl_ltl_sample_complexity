rm -rf code_supplement

mkdir code_supplement
mkdir -p code_supplement/models

# Copy custom mungojerrie and remove git info
rm -rf code_supplement/mungojerrie
git clone mungojerrie code_supplement/mungojerrie
# cp -R mungojerrie code_supplement
# rm -rf code_supplement/mungojerrie/build
rm -rf code_supplement/mungojerrie/.git

# Copy models
cp models/rl_ltl_pac_paper.prism code_supplement/models
cp models/rl_ltl_pac_paper.ltl code_supplement/models
cp models/gridworld_sadigh14.prism code_supplement/models
cp models/gridworld_sadigh14.ltl code_supplement/models

# Copy main notebook
cp rl_ltl_pac.ipynb code_supplement

# Copy Dockerfile
cp Dockerfile code_supplement

# Copy documentation
pandoc supplement_documentation.md \
	--number-sections \
	--highlight-style=zenburn \
	--indented-code-classes=haskell \
	--pdf-engine=xelatex \
	-V colorlinks=true \
	-o documentation.pdf

cp documentation.pdf code_supplement
