#voyager.py

""" This program is a demo program to experiment
    with blimpy and practice processing BL data.

    Ellie White 30 March 2020

"""
#import pylab as plt
import blimpy as bl

def main():
    obs = bl.Waterfall('voyager_f1032192_t300_v2.fil')

if __name__ == '__main__':
    main()
    
