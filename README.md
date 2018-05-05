# BSP Header Generator
This project aims to provide a simple script, that generates a board support package header file for C or C++ Code from a comma separated value file.

## Getting started

### Installing
To use the script you need a Python installation. I tested it with 3.5.2, but it should work with any 3.X Python version.
It may even work with Python 2.7.
Just clone the repository to use the script. 
At the moment no non-standard libraries are necessary to run it.

### Running the Generator
#### Prerequisites
To use the script you need to have bsp.csv file present in the directory you are running the script from. 
The first row must contain a header with column descriptions.
The following Keywords must be present and will be the only ones that are used by the script:
* Module
* Submodule
* Function
* Address/Value
* Comment

The order of these keywords does not matter.
Any other columns you want to use should have no influence on the script.

#### Running the script
If such a csv file is present just call the script from the shell using
```
python bsp_generator.py [options]
```
and wait for it to finish.
A bsp.h file should appear in the directory.

#### Command Line Options
* -i \<filename> | --input="\<filename>" Change the input file to \<filename>
* -o \<filename> | --output="\<filename>" Change the output file to \<filename>
* --docstring="\<filename>" Instead of the standard docstring, read out the 
docstring from \<filename>
* --include="\<include1> \<include2>" Adds header includes specified by \<includeN>
includes should be without a suffix (.h) and seperated by spaces.

#### Output
The Output is a C header file with the following structure:
```
#ifndef __BSP_INCLUDED__
#define __BSP_INCLUDED__

<Multiline Docstring>

<includes>

// Defines for MODULE1
#define MODULE1_FUNCTION1 ADDRESS/VALUE1 [// COMMENT1]
#define MODULE1_FUNCTION2 ADDRESS/VALUE2 [// COMMENT2]
...

// Defindes for MODULE2 -> SUBMODULE21
#define MODULE2_SUBMODULE21_FUNCTION1 ADDRESS/VALUE1 [// COMMENT1]
#define MODULE2_SUBMODULE21_FUNCTION2 ADDRESS/VALUE2 [// COMMENT1]
...

#endif // __BSP_INCLUDED__
```

## Contributing
### Create an issue
If you want to add functionality or fix a bug, create an issue first.
If it is a bug include the following information:
* What were doing? -> What steps are necessary to reproduce the error?
* What were you expecting to happen? -> Why is what is happening a bug?
* What did happen? -> How did the bug manifest itself?
* System/Environment information
* (Optional) A proposed solution

and use the bug label for that issue.

If it is a feature request use the enhancement label and include the following information:
* What feature do you want to be added?
* Why do you want to change it?
* (Optional) How would you achieve this feature?

### Writing code
If you are writing code, please adhere to the coding style guide in PEP8 and PEP257.
To ensure compliance run the [pep8](https://pypi.org/project/pep8/) checker on your code. 
It should return with no errors.

Currently no automatic test are available.
If you are fixing a bug, check the output file if the bug fix has no side effects.
If you are adding a feature, test it with different inputs and don't forget how it reacts to special characters in the csv-file.

### Pull requests
To have your changes integrated create a pull request containing the following information:
* The issue that will be resolved by this pull request
* What features are added or which bug is fixed
