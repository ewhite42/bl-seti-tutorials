from shutil import rmtree
from os import mkdir
import logging
from turbo_seti.find_doppler.find_doppler import FindDoppler
from turbo_seti.find_event.find_event_pipeline import find_event_pipeline
from turbo_seti.__init__ import __version__ as VERSION
#from turbo_seti.find_event.plot_event_pipeline import plot_event_pipeline
#from plot_event_pipeline_ellie import plot_event_pipeline
from plot_event_pipeline_sofia import plot_event_pipeline
import pylab as plt
from blimpy import Waterfall
import glob

THRESHOLD = 3
H5DIR = 'VoyagerData/' #'ParkesData/'#
OUTDIR = H5DIR + 'outdir/'
PATH_DAT_LIST_FILE = OUTDIR + 'new_dat_files.lst'
PATH_CSVF = OUTDIR + 'found_event_table.csv'
H5_LIST_FILE = OUTDIR + 'h5_files.lst'

h5_files_list = glob.glob(H5DIR+'*.h5')
h5_files_list.sort()



'''['single_coarse_guppi_59046_80036_DIAG_VOYAGER-1_0011.rawspec.0000.h5',
                'single_coarse_guppi_59046_80354_DIAG_VOYAGER-1_0012.rawspec.0000.h5',
                'single_coarse_guppi_59046_80672_DIAG_VOYAGER-1_0013.rawspec.0000.h5',
                'single_coarse_guppi_59046_80989_DIAG_VOYAGER-1_0014.rawspec.0000.h5',
                'single_coarse_guppi_59046_81310_DIAG_VOYAGER-1_0015.rawspec.0000.h5',
                'single_coarse_guppi_59046_81628_DIAG_VOYAGER-1_0016.rawspec.0000.h5']'''



def make_dat_files():
    ii = 0
    
    file_handle = open(PATH_DAT_LIST_FILE, 'w')
    h5_file_handle = open(H5_LIST_FILE, 'w')

    for filename in h5_files_list:
        path_h5 = filename
        doppler = FindDoppler(path_h5,
                              max_drift = 4,
                              snr = 10,
                              log_level_int=logging.WARNING,
                              out_dir = H5DIR
                              )
        doppler.search()
        ii += 1
        
        h5_file_handle.write('{}\n'.format(path_h5))

        path_dat = filename.replace('.h5', '.dat')
        file_handle.write('{}\n'.format(path_dat))
        print("make_dat_files: {} - finished making DAT file for {}".format(ii, path_h5))


def beginning():
    # Initialize output directory
    rmtree(OUTDIR, ignore_errors=True)
    mkdir(OUTDIR)
    # Make the DAT files
    make_dat_files()


#=================================================================

print('============== turbo_seti version ===============>', VERSION)
#beginning()

# Generate CSV file from find_event_pipeline()
num_in_cadence = len(h5_files_list)
find_event_pipeline(PATH_DAT_LIST_FILE,
                    filter_threshold = THRESHOLD,
                    number_in_cadence = num_in_cadence,
                    user_validation=False,
                    csv_name=PATH_CSVF,
                    saving=True)
print("Produced {}".format(PATH_CSVF))

plot_event_pipeline(PATH_CSVF, H5_LIST_FILE, user_validation=False)

'''file_path = '/home/ellie/research/seti/VoyagerTutorial2/VoyagerData/single_coarse_guppi_59046_80672_DIAG_VOYAGER-1_0013.rawspec.0000.h5'

f_start = 8419.51
f_stop = 8419.58
obs = Waterfall(file_path, f_start, f_stop)
obs.plot_spectrum(f_start=f_start, f_stop=f_stop)'''
