# ebv-2021
This is the collection of image analysis scripts used in: *Epstein-Barr virus inactivates the transcriptome and disrupts the chromatin architecture of its host cell in the first phase of lytic reactivation*.

The scripts are written in Python 3.7. I used anaconda to set up a dedicated image-analysis python environment. To re-create the environment, please use the included YAML file as described [here](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#creating-an-environment-from-an-environment-yml-file).

The images were acquired on a Leica SP8 confocal microscope with a Plan-Apo 40x NA 1.3 objective at 2048x2048 pixel with an effective pixel size of 189 nm. We organized the files as collections in the Leica Application Suite ([LAS X](https://www.leica-microsystems.com/products/microscope-software/p/leica-las-x-ls/)) by time and Tamoxifen concentration. All files were single optical sections.

The steps of the analysis pipeline are:
  * **saveSingleTiff-ver5.py** converts Leica LIF files to individual TIFF files. The script generates a unique file name based on *date*, *time*, *concentration*, *image number*, and *channel*.
  * **stardist-save-labels.ipynb** finds nuclei in the DAPI channel with [StarDist](https://github.com/mpicbg-csbd/stardist) and saves label images.
  * **membrane-segmentation.ipynb** takes the centroids of the StarDist objects as seeds for [RACE](https://bitbucket.org/jstegmaier/race/src/master/) with **myRACECSV-param-tune-4.xml** as configuration file and finds cell boundaries from the membrane channel. The segmentation output from RACE is saved.
  * **measure-channels-3.ipynb** combines the nuclei labels from StarDist and cell objects from RACE. I used a distance map followed by individually testing whether nuclei lie within a cell object to find correct pairs of nuclei and cells. The script then generates masks and measures intensity values in BZLF1 and gp350 channels.

As of today (5/1/2021) the notebooks still contain a lot of code I used for testing and trying out different analysis approaches. I hope to clean up and reduce the scripts to the minimal code that is needed to reproduce the analysis for the paper.
