# FAQ´s
preguntas frecuentes

### cambiar caracter de division entre los puntos

**Pregunta**¿como importo un archivo txt con los puntos divididos por comas o otro caracter?

**Respueta:**cambie el contenido de la variable CARACTER_SEPARACION.

### Error: could not convert string to float

**Pregunta:**¿por que sucede este error?

	File "Triangular-Meshes/tools/Triangular.py", line 15, in <listcomp>
    pto = tuple([float(i) for i in punto.split(',')])
	ValueError: could not convert string to float: '0.00624200000000000\t0.0394719988000000\t0.0335070007000000\n'

**Respuesta:**por que el archivo que usted esta importando esta separado por tabs, no por comas .


