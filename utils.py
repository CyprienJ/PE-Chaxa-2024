import collections

import tqdm
from scipy import signal
import numpy as np


def integer_histogram(data):
    """
    Build a "perfect" histogram from an array that have integer values.
    """
    cnt = collections.Counter(data)
    cnt_list = list(cnt.items())
    cnt_list.sort(key=lambda x: x[0])
    return [x for x, _ in cnt_list], [y for _, y in cnt_list]


AES_SBOX = np.array([
        0x63, 0x7c, 0x77, 0x7b, 0xf2, 0x6b, 0x6f, 0xc5,
        0x30, 0x01, 0x67, 0x2b, 0xfe, 0xd7, 0xab, 0x76,
        0xca, 0x82, 0xc9, 0x7d, 0xfa, 0x59, 0x47, 0xf0,
        0xad, 0xd4, 0xa2, 0xaf, 0x9c, 0xa4, 0x72, 0xc0,
        0xb7, 0xfd, 0x93, 0x26, 0x36, 0x3f, 0xf7, 0xcc,
        0x34, 0xa5, 0xe5, 0xf1, 0x71, 0xd8, 0x31, 0x15,
        0x04, 0xc7, 0x23, 0xc3, 0x18, 0x96, 0x05, 0x9a,
        0x07, 0x12, 0x80, 0xe2, 0xeb, 0x27, 0xb2, 0x75,
        0x09, 0x83, 0x2c, 0x1a, 0x1b, 0x6e, 0x5a, 0xa0,
        0x52, 0x3b, 0xd6, 0xb3, 0x29, 0xe3, 0x2f, 0x84,
        0x53, 0xd1, 0x00, 0xed, 0x20, 0xfc, 0xb1, 0x5b,
        0x6a, 0xcb, 0xbe, 0x39, 0x4a, 0x4c, 0x58, 0xcf,
        0xd0, 0xef, 0xaa, 0xfb, 0x43, 0x4d, 0x33, 0x85,
        0x45, 0xf9, 0x02, 0x7f, 0x50, 0x3c, 0x9f, 0xa8,
        0x51, 0xa3, 0x40, 0x8f, 0x92, 0x9d, 0x38, 0xf5,
        0xbc, 0xb6, 0xda, 0x21, 0x10, 0xff, 0xf3, 0xd2,
        0xcd, 0x0c, 0x13, 0xec, 0x5f, 0x97, 0x44, 0x17,
        0xc4, 0xa7, 0x7e, 0x3d, 0x64, 0x5d, 0x19, 0x73,
        0x60, 0x81, 0x4f, 0xdc, 0x22, 0x2a, 0x90, 0x88,
        0x46, 0xee, 0xb8, 0x14, 0xde, 0x5e, 0x0b, 0xdb,
        0xe0, 0x32, 0x3a, 0x0a, 0x49, 0x06, 0x24, 0x5c,
        0xc2, 0xd3, 0xac, 0x62, 0x91, 0x95, 0xe4, 0x79,
        0xe7, 0xc8, 0x37, 0x6d, 0x8d, 0xd5, 0x4e, 0xa9,
        0x6c, 0x56, 0xf4, 0xea, 0x65, 0x7a, 0xae, 0x08,
        0xba, 0x78, 0x25, 0x2e, 0x1c, 0xa6, 0xb4, 0xc6,
        0xe8, 0xdd, 0x74, 0x1f, 0x4b, 0xbd, 0x8b, 0x8a,
        0x70, 0x3e, 0xb5, 0x66, 0x48, 0x03, 0xf6, 0x0e,
        0x61, 0x35, 0x57, 0xb9, 0x86, 0xc1, 0x1d, 0x9e,
        0xe1, 0xf8, 0x98, 0x11, 0x69, 0xd9, 0x8e, 0x94,
        0x9b, 0x1e, 0x87, 0xe9, 0xce, 0x55, 0x28, 0xdf,
        0x8c, 0xa1, 0x89, 0x0d, 0xbf, 0xe6, 0x42, 0x68,
        0x41, 0x99, 0x2d, 0x0f, 0xb0, 0x54, 0xbb, 0x16], dtype=np.uint8)

HW_TABLE = np.array([
        0, 1, 1, 2, 1, 2, 2, 3, 1, 2, 2, 3, 2, 3, 3, 4, 1, 2, 2, 3, 2, 3,
        3, 4, 2, 3, 3, 4, 3, 4, 4, 5, 1, 2, 2, 3, 2, 3, 3, 4, 2, 3, 3, 4,
        3, 4, 4, 5, 2, 3, 3, 4, 3, 4, 4, 5, 3, 4, 4, 5, 4, 5, 5, 6, 1, 2,
        2, 3, 2, 3, 3, 4, 2, 3, 3, 4, 3, 4, 4, 5, 2, 3, 3, 4, 3, 4, 4, 5,
        3, 4, 4, 5, 4, 5, 5, 6, 2, 3, 3, 4, 3, 4, 4, 5, 3, 4, 4, 5, 4, 5,
        5, 6, 3, 4, 4, 5, 4, 5, 5, 6, 4, 5, 5, 6, 5, 6, 6, 7, 1, 2, 2, 3,
        2, 3, 3, 4, 2, 3, 3, 4, 3, 4, 4, 5, 2, 3, 3, 4, 3, 4, 4, 5, 3, 4,
        4, 5, 4, 5, 5, 6, 2, 3, 3, 4, 3, 4, 4, 5, 3, 4, 4, 5, 4, 5, 5, 6,
        3, 4, 4, 5, 4, 5, 5, 6, 4, 5, 5, 6, 5, 6, 6, 7, 2, 3, 3, 4, 3, 4,
        4, 5, 3, 4, 4, 5, 4, 5, 5, 6, 3, 4, 4, 5, 4, 5, 5, 6, 4, 5, 5, 6,
        5, 6, 6, 7, 3, 4, 4, 5, 4, 5, 5, 6, 4, 5, 5, 6, 5, 6, 6, 7, 4, 5,
        5, 6, 5, 6, 6, 7, 5, 6, 6, 7, 6, 7, 7, 8], dtype=np.uint8)

def hamming_weight(x: np.ndarray) -> np.ndarray:
    """
    Vectorized Hamming Weight for 8-bit variables (np.uint8).
    """
    return HW_TABLE[x]

def target_variable(key_hypothesis, plaintexts):
    """
    Computes intermediate variables for lab03.

    :param key_hypothesis: is an integer in the interval [0, 255]
    :param plaintext: is a 1D numpy array of plaintexts
    """
    return AES_SBOX[key_hypothesis ^ plaintexts]


def aes_sbox(x):
    return AES_SBOX[x]


NIST_KEY = np.array([43, 126,  21,  22,  40, 174, 210,
                     166, 171, 247,  21, 136,   9, 207,
                     79,  60], dtype=np.uint8)

def lab03_is_key_correct(key, target_byte) -> bool:
    return NIST_KEY[target_byte] == key

def lab03_key():
    return NIST_KEY


#Load plaintexts and traces
def load_traces(index: int):
    if(index==0):
        filePath = "Traces/Analysis/Unprotected/Unprotected"
    elif(index==1):
        filePath = "Traces/Analysis/Passive/Passive"
    else:
        filePath = "Traces/Analysis/ChaXa/ChaXa"
    
    file = open(filePath +"_plain_cipher_texts.txt", "r")
    plaintexts_ciphers = file.readlines()
    file.close()
    nb_traces = int(plaintexts_ciphers[0])
    plaintexts = plaintexts_ciphers[1:nb_traces+1]
    file = open(filePath + "0.txt", "r")
    data = file.readlines()
    file.close()
    nb_samples = int(data[0])
    lines = np.zeros((nb_traces, nb_samples))
    lines[0] = data[1:]
    for i in range(1, nb_traces):
        file = open(filePath + f"{i}.txt", "r")
        lines[i] = file.readlines()[1:]
        file.close()
    
    traces = np.zeros((nb_traces, nb_samples))
    for i in range(lines.shape[0]):
        for j in range(lines.shape[1]):
            traces[i,j] = (float(lines[i,j]))
    
    return traces, plaintexts

#take traces and the list of plaintexts and do the side-channel analysis
def analysis(traces : np.array, plaintexts: list):
    nb_traces = traces.shape[0]
    nb_samples = traces.shape[1]
    
    # Sample frequency
    FS = 250e6
    n_coeffs = 109 # TODO
    freqs = [0, 30e6, 36e6, 125e6]  #frequencies bandwidths
    gains = [10, 10, 0, 0]  #gains of the filter
    fir_coeffs = signal.firls(n_coeffs, freqs, gains, fs=FS)
    traces_filtered = signal.filtfilt(fir_coeffs, 1, traces, axis=1)
    hypothesis_matrice = np.zeros((256, nb_traces))
    key = []
    process_range = np.array([[0, 1000], [0, 2000], [0, 1000], [500, 1500], [1000, 2000], [1000, 2000], [1500, 2500], [2000, 3000], [2500, 3500], [2500, 3500], [2800, 3800], [3000, 4000], [3500, 4500], [3500, 4500], [4000, nb_samples], [4000, nb_samples]])

    #For each byte of the key
    for target in range(2,33, 2):

        #Hypothesis matrix
        for k in range(256):
            for j in range(nb_traces):
                target_byte = int(plaintexts[j][target-2:target], 16)
                intermediate_variable = target_variable(k, target_byte)
                hamming = hamming_weight(intermediate_variable)
                hypothesis_matrice[k,j]= hamming
        #Correlation matrix
        corr_matrice = np.zeros((256, process_range[(target-1)//2, 1]-process_range[(target-1)//2, 0]))
        for i in range(256):
            for j in range(process_range[(target-1)//2, 0], process_range[(target-1)//2, 1]):
                corr_matrice[i, j-process_range[(target-1)//2, 0]] = np.corrcoef(traces_filtered.T[j], hypothesis_matrice[i])[0, 1]

        key.append(hex(np.argmax(np.max(np.abs(corr_matrice.T), axis=0)))) #On affiche la clé en hexadécimal
        
    return key
    