# FAQ's
frequently asked questions

### change character of division between dots

**Question:** How do I import a txt file with the points divided by commas or another character?

**Answer:** Change the content of the variable CARACTER_SEPARACION.

### Error: could not convert string to float

**Question:** Why is this error happening?

	File "Triangular-Meshes/tools/Triangular.py", line 15, in <listcomp>
    pto = tuple([float(i) for i in punto.split(',')])
	ValueError: could not convert string to float: '0.00624200000000000\t0.0394719988000000\t0.0335070007000000\n'

**Answer:** Because the file you are importing is separated by tabs, not commas.

