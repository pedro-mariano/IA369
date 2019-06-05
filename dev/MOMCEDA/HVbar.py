"""
========
Barchart
========
A bar plot with errorbars and height labels on individual bars
"""
import cPickle as pickle
import numpy as np
import matplotlib.pyplot as plt
import json

SMALL_SIZE = 8
MEDIUM_SIZE = 12
BIGGER_SIZE = 20

##plt.rc('font', size=SMALL_SIZE)          # controls default text sizes
plt.rc('axes', titlesize=BIGGER_SIZE)     # fontsize of the axes title
plt.rc('axes', labelsize=BIGGER_SIZE)    # fontsize of the x and y labels
plt.rc('xtick', labelsize=MEDIUM_SIZE)    # fontsize of the tick labels
plt.rc('ytick', labelsize=MEDIUM_SIZE)    # fontsize of the tick labels
plt.rc('legend', fontsize=SMALL_SIZE)    # legend fontsize
plt.rc('figure', titlesize=BIGGER_SIZE)  # fontsize of the figure title

def showHVBar(function,Nsamples,NEval):

    algo = 'MOMCEDA'
    with open(''.join(['../dev/files/HV_',function,'_',algo,'.pk1']),'r') as filename:
        hv_MOMCEDA = pickle.load(filename)

    Nsamples = 10
    NEval = 20000

    ##NGer = len(hv_MOMCEDA[0])
    ##gen_ind = (np.linspace(0,NGer-1,Nsamples+1)[1:]).astype(int)
    ##eval_ind = (gen_ind + 2)*100

    eval_ind = (np.linspace(0,NEval,Nsamples+1)[1:]).astype(int)
    gen_ind = eval_ind/100 - 2

    meanHV_MOMCEDA = hv_MOMCEDA[:,gen_ind].mean(axis=0)
    stdHV_MOMCEDA = hv_MOMCEDA[:,gen_ind].std(axis=0)

    ind = np.arange(Nsamples)  # the x locations for the groups
    width = 0.2       # the width of the bars

    fig, ax = plt.subplots(figsize=(12,12))
    rects1 = ax.bar(ind + 3*width, meanHV_MOMCEDA, width, color='r', yerr=stdHV_MOMCEDA)

    algo = 'NSGA2'
    with open(''.join(['../dev/files/HV_',function,'_',algo,'.json']),'r') as filename:
        hv_NSGA2 = np.asarray(json.load(filename))

    meanHV_NSGA2 = hv_NSGA2[:,gen_ind].mean(axis=0)
    stdHV_NSGA2 = hv_NSGA2[:,gen_ind].std(axis=0)

    rects2 = ax.bar(ind + 0*width, meanHV_NSGA2, width, color='y', yerr=stdHV_NSGA2)

    # add some text for labels, title and axes ticks
    ax.set_ylabel('Average Hypervolume')
    ax.set_xlabel('Evaluations')
    ax.set_title(''.join(['Average hypervolume evolution for ',function]))
    ax.set_xticks(ind + 2*width)
    ax.set_xticklabels(eval_ind)
    ax.set_ylim([0,max(meanHV_MOMCEDA)*1.2])

    ax.legend((rects2[0],rects1[0]), ('NSGA-II','MOMCEDA'),
               loc='center left', bbox_to_anchor=(1, 0.5),fancybox=True, shadow=True, ncol=1, fontsize='large')

    ##def autolabel(rects):
    ##    """
    ##    Attach a text label above each bar displaying its height
    ##    """
    ##    for rect in rects:
    ##        height = rect.get_height()
    ##        ax.text(rect.get_x() + rect.get_width()/2., 1.05*height,
    ##                '%.2f' % height,
    ##                ha='center', va='bottom')
    ##
    ##autolabel(rects1)
    ##autolabel(rects2)
    ##autolabel(rects3)

    plt.show()

    ##plt.savefig(''.join(['HVbar_',function,'.png']), bbox_inches='tight')
