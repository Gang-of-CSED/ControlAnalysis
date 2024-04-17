import matplotlib.pyplot as plt
import control as ct
import numpy as np
def findlines(artist):
    return (isinstance(artist, plt.Line2D)
            and artist.get_linestyle()=='-'
            and isinstance(artist.get_xdata(), np.ndarray))
def plotRootLocus(denom, num=[1]):
    if len(denom) < 2:
        return
    denom = np.array(denom)
    denom = denom.astype(float)
    num = np.array(num)
    num = num.astype(float)
    G = ct.tf(num, denom)
    # get the poles and zeros of the system
    poles = ct.poles(G)
    print(poles)
    zeros = ct.zeros(G)
    print(zeros)
    plt.figure(facecolor='#e8ebef')
    plt.rcParams['lines.linewidth'] = 3
    plt.rcParams.update({'font.size': 13})
    ct.rlocus(G)
    h = plt.gca().findobj(match=findlines)
    for i, h_ in enumerate(h): h_.set_color(f'C{i}')
    plt.xlabel('Real')
    plt.ylabel('Imaginary')
    # plt.title(r'$\frac{1}{s^2 + 3s + 5}$')
    # title is G(s)H(s) = num/denom
    num_str = '+'.join([str(num[i]) + ('s' if len(num)-i-1 == 1 else ('s^' + str(len(num)-i-1) if len(num)-i-1 > 0 else '')) for i in range(len(num)) if num[i] != 0])
    denom_str = '+'.join([str(denom[i]) + ('s' if len(denom)-i-1 == 1 else ('s^' + str(len(denom)-i-1) if len(denom)-i-1 > 0 else '')) for i in range(len(denom)) if denom[i] != 0])
    # plt.title(r'$Root Locus\nG(S)H(S) = \frac{' + num_str + '}{' + denom_str + '}$')
    plt.suptitle(r'Root Locus of $G(S)H(S) = \frac{' + num_str + '}{' + denom_str + '}$')
    plt.subplots_adjust(top=0.85)

def getPolesandZeros(denom, num=[1]):
    denom = np.array(denom)
    denom = denom.astype(float)
    num = np.array(num)
    num = num.astype(float)
    print(num)
    print(denom)
    G = ct.tf(num, denom)
    # get the poles and zeros of the system
    poles = ct.poles(G)
    print(poles)
    zeros = ct.zeros(G)
    print(zeros)
    return poles, zeros