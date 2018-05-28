# phiDelta
Python implementation of phi-delta diagrams

The package phiDelta embodies source code that implements phidelta measures and diagrams. These measures can be used to perform classifier and / or feature assessment.

In the former case, given a run on a test set, the pair <phi,delta> measures bias and accuracy of the classifier at hand.

In the latter case, given a run on a test set, the pair <phi,delta> measures to what extent the feature at hand is characteristic / rare, and to what extent it is covariant / contravariant with the positive class.

Beyond the visualization of classifier performance, also statistics for identifying "class signatures" are provided. These statistics measure the importance of each feature in terms of phi and delta.

The current version of phidelta measures and diagrams allows to deal with binary and floating point features (although in alpha version, the code for dealing with nominal features is also included).

Some datasets are also provided for testing the software (see the datasets folder). They are all taken from the UCI ML repository. The interested reader should connect to the UCI web site for additional information on each dataset.

Please note that, in the datasets folder, you will find a file called "datasets.info". That file is useful to simplify experiments, as all useful information is supplied therein.

To start making experiments with statistics (i.e., on class signatures), the file "experiments_get.py" can be run.

The simplest way of showing a phidelta diagram consist of creating an instance of the class "View". Relevant parameters for the constructor are: phi, delta, names, and ratio. Default values apply to names (i.e., None) and ratio (i.e.,1).

Phi and delta are supposed to the outcome of an experiment (these data can refer to classifier assessment or feature importance). Please note that 

Before running the slider, please make sure that two lists or two vectors (called phi and delta) are available. These data can be manually generated or downloaded from a test file. See the main of Slider2D.py for more information.

Any test file should be in csv format (you may choose the separator, however). At present, each line of the file must contain a couple of phidelta values or a couple of specificity and sensitivity values. The function load, provided in the main of Slider2D, can load both kinds of data (see also the function ss2phidelta, which takes care of data conversion). A test file containing 100 randomly generated samples is also available (see test.csv).

This software is in alpha-release and runs under Python 2.7.

For any further information please feel free to contact me.

Giuliano Armano (email: armano@diee.unica.it).

PS Information about phidelta diagrams can be found here: https://www.sciencedirect.com/science/article/pii/S0020025515005241/pdfft?md5=15bb3eee1dd193293804576fb058b196&pid=1-s2.0-S0020025515005241-main.pdf
