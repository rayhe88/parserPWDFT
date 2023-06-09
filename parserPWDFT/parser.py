import re
from munch import Munch
import numpy as np
import json
import sys

def isJobDone(text):
    done = False
    for line in text:
        x = re.search(r"writing rtdbjson", line)
        if x is not None:
            done = True
            break

    return done


def get_NumCycles(text):
    total, step = getListData(text,"total time", 2)
    array = np.array(total)
    return array.size


def getSum(data):
    array = np.array(data)
    return np.sum(array)


def getListData(text, key, num):
    datatotal = []
    datastep  = []
    for line in text:
        x = re.search(key, line)
        if x is not None:
            y = x.string.split()
            datatotal.append(float(y[num]))
            datastep.append(float(y[num + 1]))

    return datatotal, datastep


def get_time(text):
    total, step = getListData(text,"total time", 2)
    return getSum(total), getSum(step)


def get_fft(text):
    total, step = getListData(text,"total FFT time", 3)
    return getSum(total), getSum(step)


def get_lag(text):
    total, step = getListData(text,"lagrange multipliers", 2)
    return getSum(total), getSum(step)


def get_vxc(text):
    total, step = getListData(text,"exchange correlation", 2)
    return getSum(total), getSum(step)


def get_pot(text):
    total, step = getListData(text,"local potentials", 2)
    return getSum(total), getSum(step)


def get_non(text):
    total, step = getListData(text,"non-local potentials", 2)
    return getSum(total), getSum(step)


def get_ffm(text):
    total, step = getListData(text,"ffm_dgemm", 1)
    return getSum(total), getSum(step)


def get_fmf(text):
    total, step = getListData(text,"fmf_dgemm", 1)
    return getSum(total), getSum(step)


def get_dia(text):
    total, step = getListData(text,"m_diagonalize", 1)
    return getSum(total), getSum(step)


def get_mmm(text):
    total, step = getListData(text,"mmm_multiply", 1)
    return getSum(total), getSum(step)



def get_Ecut(text):
    for line in text:
        x = re.search("Next rtdbstr=", line)
        if x is not None:
            json_str = line.split('Next rtdbstr=')[-1]

            data = json.loads(json_str)

            nwpw = data["nwpw"]

            ecut = nwpw["cutoff"]

            if ecut[0] is None:
                val = 0
            else:
                val = ecut[0]

            return val

    return


def loadQE(fname):
    qe = Munch()
    qe.status = None
    qe.ncycles = None
    qe.ecut = None

    qe.total = Munch()
    qe.step  = Munch()

    try:
        with open(fname,"r") as file:
            text = file.readlines()

            try:
                qe.status = isJobDone(text)
                if qe.status is False:
                    print('The file {0} did not finish correctly!'.format(fname))
            except IOError as error:
                print('The file {0} did not finish correctly!'.format(fname))
                qe = None
            else:
                qe.ecut = get_Ecut(text)
                qe.ncycles = get_NumCycles(text)
                qe.total.time, qe.step.time = get_time(text)
                qe.total.fft , qe.step.fft  = get_fft(text)
                qe.total.lag , qe.step.lag  = get_lag(text)
                qe.total.vxc , qe.step.vxc  = get_vxc(text)
                qe.total.pot , qe.step.pot  = get_pot(text)
                qe.total.non , qe.step.non  = get_non(text)
                qe.total.ffm , qe.step.ffm  = get_ffm(text)
                qe.total.fmf , qe.step.fmf  = get_fmf(text)
                qe.total.dia , qe.step.dia  = get_dia(text)
                qe.total.mmm , qe.step.mmm  = get_mmm(text)
    except IOError as error:
        print('Error to open file: {0}'.format(fname))
    else:
       return qe



def print_info(qe):
    if qe.status is True:
        print(" STATUS")
        print(" The job is done      : ", qe.status)
        print(" Number of cycles     : ", qe.ncycles)
        print(" Ecut is              : ", qe.ecut)

        print("")

        print(" TIME - TOTAL ")
        print(" Total time           : ", qe.total.time)
        print(" Total FFT time       : ", qe.total.fft)
        print(" Lagrange multipliers : ", qe.total.lag)
        print(" Exchange correlation : ", qe.total.vxc)
        print(" local potentials     : ", qe.total.pot)
        print(" non-local potentials : ", qe.total.non)
        print(" ffm dgemm            : ", qe.total.ffm)
        print(" fmf dgemm            : ", qe.total.fmf)
        print(" m_diagonalize        : ", qe.total.dia)
        print(" mmm_multiply         : ", qe.total.mmm)
        print("")

        print(" TIME - STEP ")
        print(" Total time           : ", qe.step.time)
        print(" Total FFT time       : ", qe.step.fft)
        print(" Lagrange multipliers : ", qe.step.lag)
        print(" Exchange correlation : ", qe.step.vxc)
        print(" local potentials     : ", qe.step.pot)
        print(" non-local potentials : ", qe.step.non)
        print(" ffm dgemm            : ", qe.step.ffm)
        print(" fmf dgemm            : ", qe.step.fmf)
        print(" m_diagonalize        : ", qe.step.dia)
        print(" mmm_multiply         : ", qe.step.mmm)
        print("")

