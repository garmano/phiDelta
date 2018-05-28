# phiDelta
*** Python implementation of phi-delta diagrams ***

The package phiDelta embodies source code that implements phidelta measures and diagrams. These measures and diagrams come in two forms: standard and generalized. The former is intended to measure instrinsic (i.e., unbiased) properties of classifiers / features, whereas the latter actual (i.e., biased) properties.

In ether form, phidelta measures and diagrams can be used to perform classifier and / or feature assessment, with the following inherent semantics:

Classifier performance

Given a run on a test set, the pair <phi,delta> measures bias and accuracy of the classifier at hand. In this case, the four corners of a diagram are related to the concepts of oracle (top), anti-oracle (bottom), and dummy classifiers (left and right). To start making experiments with classifier assessment, you should come up with one or more <phi,delta> pairs. For instance, you may run 30-fold cross-validation and for each run store information about specificity and sensitivity. To convert your <spec,sens> pairs into <phi,delta> pairs you can use the function model.phidelta_std (in the event inputs are in fact arrays, the conversion is made with a single call). To visualize a diagram you should use the class "View" --several examples of how to use it are given (e.g., in experiments_get.py).

Feature importance

Beyond the evaluation / visualization of classifier performance, also statistics for identifying "class signatures" are provided. These statistics measure the importance of each feature in terms of phi and delta. In particular, given a run on a test set, for each feature, the pair <phi,delta> measures to what extent it is characteristic / rare (phi), and to what extent it is covariant / contravariant with the positive class (delta). In this case, the four corners of a diagram are related to the concepts of highest-covariance (top), highest contravariance (bottom), rare feature (left) and characteristic feature (right). To start making experiments with feature importance (i.e., on class signatures), the file "experiments_get.py" can be run. It run as it is, although you may want to change the list of datasets and/or ratio values.

The current version of phidelta measures allows to deal with binary and floating point features (the code for dealing with nominal features, although in alpha version, is also included).

Note that some datasets are also provided for testing the software. They are all taken from the UCI ML repository. The interested reader should connect to the UCI web site for additional information on each dataset.

Please note also that you are supposed to set up a datasets folder (do not forget to properly set the "path" parameter --see source code-- which should be set accordingly). In the dataset folder you will also find a file called "datasets.info". That file is useful to simplify experiments, as relevant information for each dataset is supplied therein.

As for visualization, the simplest way of showing a phidelta diagram consist of creating an instance of the class "View". Relevant parameters for the constructor are: phi, delta, names, and ratio. Default values apply to names (i.e., None) and ratio (i.e., 1).

The parameters phi and delta are supposed to be the outcome of an experiment (no matter whether they refer to classifier assessment or feature importance). If needed, you may also save them in csv format for future visualizations using the functions save_csv_data and load_csv_data (see utils.py).

Please note that, before saving, you should supply phi and delta as "single parameter" using zip. Conversely, if you want to get phi and delta after loading a previously saved file, you should unzip the result (see also the function unzip2 in utils.py). An example of how to use save_csv_data and load_csv_data follows:

from utils import load_csv_data, save_csv_data, unzip2

... # Here you should generate phi and delta as outcome of some experiment(s)

save_csv_data(zip(phi,delta),'test-2018-05-30.dat',path='../datasets/')

... # More code here

phi, delta = unzip2(load_csv_data('test-2018-05-30.dat',path='../datasets/')

... # Now you can reuse phi and delta ...

Not least of all, the package comes in two versions: object-oriented and procedural.

For the object oriented version see, in particular: model.phidelta_std, model.phidelta_std2gen, view.View, and statistics.Statistics.

The procedural version has been provided for compatibility with the corresponding implementation made for the R language by prof. D. Heider and dr. U. Neumann (Phillips University, Marburg, Germany). Its most relevant functions are:

funmodel.convert(spec,sens,ratio=1.)
funmodel.stats(data,labels,info=None,verbose=False)
funmodel.plot(phi,delta,ratio=1.,names=None,title='')

This software is in beta-release and runs under Python 3.

For any further information please feel free to contact me.

Giuliano Armano (email: armano@diee.unica.it).

PS Information about phidelta diagrams can be found here: https://www.sciencedirect.com/science/article/pii/S0020025515005241/pdfft?md5=15bb3eee1dd193293804576fb058b196&pid=1-s2.0-S0020025515005241-main.pdf
