Release notes
=============

Spyking CIRCUS 0.5
------------------

This is the 0.5 release of the SpyKING CIRCUS, a new approach to the problem of spike sorting. The code is based on a smart clustering with
sub sampling, and a greedy template matching approach, such that it can resolve the problem of overlapping spikes. The publication about the software 
is available at http://biorxiv.org/content/early/2016/08/04/067843


.. figure::  launcher.png
   :align:   center

   The software can be used with command line, or a dedicated GUI


.. warning::

    The code may still evolve. Even if results are or should be correct, we can expect some more optimizations in a near future, based on feedbacks obtained on multiple datasets. If you spot some problems with the results, please be in touch with pierre.yger@inserm.fr

Contributions
~~~~~~~~~~~~~
Code and documentation contributions (ordered by the number of commits):

* Pierre Yger
* Marcel Stimberg
* Baptiste Lebfevre
* Christophe Gardella
* Olivier Marre
* Cyrille Rossant

=============
Release 0.6.0
=============

* improvements in the neuralynx wrapper
* add the possibility to exclude some portions of the recordings from the analysis (see documentation)

=============
Release 0.5.9
=============

* The validating step can now accept custom spikes as inputs
* Change the default frequency for filtering to 300Hz instead of 500Hz

=============
Release 0.5.8
=============

* fix a bug for int indices in some file wrappers (python 3.xx) (thanks to Ben Acland)
* fix a bug in the preview gui to write threshold
* fix a bug for some paths in Windows (thanks to Albert Miklos)
* add a wrapper for NeuraLynx (.ncs) file format
* fix a bug in the installation of the MATLAB GUI
* fix a bug to see results in MATLAB GUI with only 1 channel
* fix a bug to convert data to phy with only positive peaks
* add builds for python 3.6
* optimizations in file wrappers
* fix a bug for MCS headers in multifiles, if not all with same sizes
* add the possibility (with a flag) to turn off parallel HDF5 if needed
* fix a bug with latest version of HDF5, related to flush issues during clustering

=============
Release 0.5.7
=============

* Change the strsplit name in the MATLAB GUI
* Fix a bug in the numpy wrapper
* Fix a bug in the artefact removal (numpy 1.12), thanks to Chris Wilson
* Fixes in the matlab GUI to ease a refitting procedure, thanks to Chris Wilson
* Overlaps are recomputed if size of templates has changed (for refitting)
* Addition of a "second" argument for a better control of the preview mode
* Fix when using the phy GUI and the multi-file mode.
* Add a file wrapper for INTAN (RHD) file format

=============
Release 0.5.6
=============

* Fix in the smart_search when only few spikes are found
* Fix a bug in density estimation when only few spikes are found

=============
Release 0.5.5
=============

* Improvement in the smart_select option given various datasets
* Fix a regression for the clustering introduced in 0.5.2

=============
Release 0.5.2
=============

* fix for the MATLAB GUI
* smart_select can now be used [experimental]
* fix for non 0: DISPLAY
* cosmetic changes in the clustering plots
* ordering of the channels in the openephys wrapper
* fix for rates in the MATLAB GUI
* artefacts can now be given in ms or in timesteps with the trig_unit parameter

=============
Release 0.5rc
=============

* fix a bug when exporting for phy in dense mode
* compatibility with numpy 1.12
* fix a regression with artefact removal
* fix a display bug in the thresholds while previewing with a non unitary gain
* fix a bug when filtering in multi-files mode (overwrite False, various t_starts)
* fix a bug when filtering in multi-files mode (overwrite True)
* fix a bug if matlab gui (overwrite False)
* fix the gathering method, not working anymore
* smarter selection of the centroids, leading to more clusters with the smart_select option
* addition of a How to cite section, with listed publications

=============
Release 0.5b9
=============

* switch from progressbar2 to tqdm, for speed and practical issues
* optimization of the ressources by preventing numpy to use multithreading with BLAS
* fix MPI issues appearing sometimes during the fitting procedure
* fix a bug in the preview mode for OpenEphys files
* slightly more robust handling of openephys files, thanks to Ben Acland
* remove the dependency to mpi4py channel on osx, as it was crashing
* fix a bug in circus-multi when using extensions

=============
Release 0.5b8
=============

* fix a bug in the MATLAB GUI in the BestElec while saving
* more consistency with "both" peak detection mode. Twice more waveforms are always collect during whitening/clustering
* sparse export for phy is now available
* addition of a dir_path parameter to be compatible with new phy
* fix a bug in the meta merging GUI when only one template left

=============
Release 0.5b7
=============

* fix a bug while converting data to phy with a non unitary gain
* fix a bug in the merging gui with some version of numpy, forcing ucast
* fix a bug if no spikes are detected while constructing the basis
* Optimization if both positive and negative peaks are detected
* fix a bug with the preview mode, while displaying non float32 data

=============
Release 0.5b6
=============

* fix a bug while launching the MATLAB GUI

=============
Release 0.5b3
=============

* code is now hosted on GitHub
* various cosmetic changes in the terminal
* addition of a garbage collector mode, to collect also all unfitted spikes, per channel
* complete restructuration of the I/O such that the code can now handle multiple file formats
* internal refactoring to ease interaction with new file formats and readibility
* because of the file format, slight restructuration of the parameter files
* N_t and radius have been moved to the [detection] section, more consistent
* addition of an explicit file_format parameter in the [data] section
* every file format may have its own parameters, see documentation for details (or --info)
* can now work natively with open ephys data files (.openephys)
* can now work natively with MCD data files (.mcd) [using neuroshare]
* can now work natively with Kwik (KWD) data files (.kwd)
* can now work natively with NeuroDataWithoutBorders files (.nwb)
* can now work natively with NiX files (.nix)
* can now work natively with any HDF5-like structure data files (.h5)
* can now work natively with Arf data files (.arf)
* can now work natively with 3Brain data files (.brw)
* can now work natively with Numpy arrays (.npy)
* can now work natively with all file format supported by NeuroShare (plexon, blackrock, mcd, ...)
* can still work natively with raw binary files with/without headers :)
* faster IO for raw binary files
* refactoring of the exports during multi-file/preview/benchmark: everything is now handled in raw binary
* fix a bug with the size of the safety time parameter during whitening and clustering
* all the interactions with the parameters are now done in the circus/shared/parser.py file
* all the interactions with the probe are now done in the circus/shared/probes.py file
* all the messages are now handled in circus/shared/messages.py
* more robust and explicit logging system
* more robust checking of the parameters
* display the electrode number in the preview/result GUI
* setting up a continuous integration workflow to test all conda packages with appveyor and travis automatically
* cuda support is now turned off by default, for smoother install procedures (GPU yet do not bring much)
* file format can be streamed. Over several files (former multi-file mode), but also within the same file
* several cosmetic changes in the default parameter file
* clustering:smart_search and merging:correct_lag are now True by default
* fix a minor bug in the smart search, biasing the estimation of densities
* fix a bug with the masks and the smart-search: improving results
* addition of an overwrite parameter. Note that any t_start/t_stop infos are lost
* if using streams, or internal t_start, output times are on the same time axis than the datafile
* more robust parameter checking


=============
Release 0.4.3
=============

* cosmetic changes in the terminal
* suggest to reduce chunk sizes for high density probes (N_e > 500) to save memory
* fix a once-in-a-while bug in the smart-search


=============
Release 0.4.2
=============

* fix a bug in the test suite
* fix a bug in python GUI for non integer thresholds
* fix a bug with output strings in python3
* fix a bug to kill processes in windows from the launcher
* fix graphical issues in the launcher and python3
* colors are now present also in python3
* finer control of the amplitudes with the dispersion parameter
* finer control of the cut off frequencies during the filtering
* the smart search mode is now back, with a simple True/False flag. Use it for long or noisy recordings
* optimizations in the smart search mode, now implementing a rejection method based on amplitudes
* show the mean amplitude over time in the MATLAB GUI
* MATLAB is automatically closed when closing the MATLAB GUI
* mean rate is now displayed in the MATLAB GUI, for new datasets only
* spike times are now saved as uint32, for new datasets only
* various fixes in the docs
* improvements when peak detection is set on "both"
* message about cc_merge for low density probes
* message about smart search for long recordings
* various cosmetic changes
* add a conda app for anaconda navigator


=============
Release 0.4.1
=============

* fix a bug for converting millions of PCs to phy, getting rid of MPI limitation to int32
* fix bugs with install on Windows 10, forcing int64 while default is int32 even on 64bits platforms
* improved errors messages if wrong MCS headers are used
* Various cosmetic changes


===========
Release 0.4
===========

First realease of the software
