from copy import deepcopy
from math import prod
from itertools import zip_longest
from random import choices

def __remove_zeros(nu):
    if nu[-1] == 0:
        k = nu.index(0)
        nu = [nu[i] for i in range(k)]
    return nu

def __is_partition(nu):
    l = len(nu)
    check = nu[0] >= 0
    i = 1
    while i < l and check:
        check = nu[i] >= 0 and nu[i] <= nu[i-1]
        i = i + 1
    return check

def __check_partition(nu):
    if __is_partition(nu):
        return __remove_zeros(nu)
    raise Exception("Not a partition.")
    
def __unlist(L):
    return [x for i in range(len(L)) for x in L[i]]

def __conjugate(nu):
    l = len(nu)
    mu = [l]
    if l >= 1:
        for i in range(1, nu[0]):
            mu.append(0)
            j = 0
            while j < len(nu) and nu[j] > i:
                mu[i] = mu[i] + 1
                j = j + 1
    return mu

def __filterNotNone(v):
    return [x for x in v if x is not None]

def __dual_syt(T):
    Tt = list(map(list, zip_longest(*T, fillvalue=None)))
    return list(map(__filterNotNone, Tt))

def __diff(v):
    out = []
    for i in range(1, len(v)):
        out.append(v[i] - v[i-1])
    return out

def __check_syt_row(v):
    diffs = __diff(v)
    positive = map(lambda x : x > 0, diffs)
    return all(positive)

def __check_syt_rows(T):
    return all(map(__check_syt_row, T))
    
def __check_contents(v):
    l = len(v)
    return all(map(lambda i : i in v, range(1, l+1)))

def __shape(T):
    return list(map(len, T))

def __is_syt(T):
    c1 = __is_partition(__shape(T))
    c2 = __check_contents(__unlist(T))
    c3 = __check_syt_rows(T)
    c4 = __check_syt_rows(__dual_syt(T))
    return all([c1, c2, c3, c4])

def __which_row(T, x):
    i = 0
    ok = x in T[i]
    while not ok:
        i = i + 1
        ok = x in T[i]
    return i

def __connected_partitions(nu0):
    nu = deepcopy(nu0)
    nu[0] = nu[0] + 1
    out = [nu]
    for i in range(1, len(nu0)):
        if nu0[i] < nu0[i-1]:
            nu = deepcopy(nu0)
            nu[i] = nu[i] + 1
            out.append(nu)
    nu = deepcopy(nu0)
    nu.append(1)
    out.append(nu)
    return out

def __ballot2syt(ballot):
    syt = []
    m = max(ballot)
    for j in range(1, m+1):
        syt.append([i+1 for i, e in enumerate(ballot) if e == j])
    return syt

def __ytbl(N, nu, a, more):
    it = N
    if more:
        nu = [0 for i in range(N)]
        nu[0] = 1
        isave = 0
        for i in range(1, N):
            nu[a[i]-1] = nu[a[i]-1] + 1
            if a[i] < a[i-1]:
                isave = i
                break        
        if isave == 0:
            return a, False
        it = nu[a[isave]]
        for i in reversed(range(N)):
            if nu[i] == it:
                a[isave] = i + 1
                nu[i] = nu[i] - 1
                it = isave
                break
    for i in range(N-len(nu)):
        nu.append(0)
    k = 0
    ir = 0
    while True:
        if N <= ir:
            break
        if nu[ir] != 0:
            a[k] = ir + 1
            nu[ir] = nu[ir] - 1
            k = k + 1
            ir = ir + 1
            continue
        if it <= k:
            break
        ir = 0
    if N == 1:
        return a, False
    for j in range(N-1):
        if a[j+1] < a[j]:
            return a, True
    return a, False

def all_sytx(nu):
    """
    All standard Young tableaux of given shape.

    Parameters
    ----------
    nu : list of decreasing positive integers
        Integer partition, the shape.

    Returns
    -------
    list
        The list of all standard Young tableaux of shape `nu`.

    Examples
    --------
    >>> from pysyt.syt import all_sytx
    >>> all_sytx([3, 2])

    """
    nu = __check_partition(nu)
    N = sum(nu)
    a, flag = __ytbl(N, deepcopy(nu), [0 for i in range(N)], False)
    As = [a]
    while flag:
        a, flag = __ytbl(N, deepcopy(nu), deepcopy(a), True)
        As.append(a)
    return list(map(__ballot2syt, As))

def hooks(nu):
    """
    Hooks of an integer partition.

    Parameters
    ----------
    nu : list of decreasing positive integers
        An integer partition.

    Returns
    -------
    list
        The hooks of `nu`.

    Examples
    --------
    >>> from pysyt.syt import hooks
    >>> hooks([3, 2])

    """
    nu = __check_partition(nu)
    dnu = __conjugate(nu)
    out = []
    for i in range(len(nu)):
        out.append([])
        for j in range(nu[i]):
            out[i].append([None, nu[i] - j])
    for j in range(len(dnu)):
        for i in range(dnu[j]):
            out[i][j][0] = dnu[j] - i
    return out

def hook_lengths(nu):
    """
    Hook lengths of an integer partition.

    Parameters
    ----------
    nu : list of decreasing positive integers
        An integer partition.

    Returns
    -------
    list
        The hook lengths of `nu`.

    Examples
    --------
    >>> from pysyt.syt import hook_lengths
    >>> hook_lengths([3, 2])

    """
    h = hooks(nu)
    f = lambda y : sum(y) - 1
    g = lambda x : list(map(f, x))
    return list(map(g, h))

def count_sytx(nu):
    """
    Count all standard Young tableaux of given shape.

    Parameters
    ----------
    nu : list of decreasing positive integers
        Integer partition, the shape.

    Returns
    -------
    integer
        The number of all standard Young tableaux of shape `nu`.

    Examples
    --------
    >>> from pysyt.syt import count_sytx
    >>> count_sytx([3, 2])

    """
    h = hook_lengths(nu)
    numterms = []
    denterms = __unlist(h)
    denterms = [x for x in denterms if x != 1]
    for i in range(2, sum(nu)+1):
        if i in denterms:
            idx = denterms.index(i)
            denterms.pop(idx)
        else:
            numterms.append(i)
    return prod(numterms) // prod(denterms)

def dual_syt(T):
    """
    Dual standard Young tableau.

    Parameters
    ----------
    T : list
        A standard Young tableau.

    Returns
    -------
    list
        The dual standard Young tableau of `T`.

    Examples
    --------
    >>> from pysyt.syt import dual_syt
    >>> dual_syt([[1, 3, 5], [2, 4]])

    """
    if not __is_syt(T):
        raise Exception("Not a standard Young tableau.")
    return __dual_syt(T)

def young_path_to_syt(path):
    """
    Standard Young tableau corresponding to a path on the Young graph.

    Parameters
    ----------
    path : list of integer partitions
        A path on the Young graph, starting from `[1]`.

    Returns
    -------
    list
        A standard Young tableau.

    Examples
    --------
    >>> from pysyt.syt import young_path_to_syt
    >>> young_path_to_syt([[1], [2], [2,1], [3,1], [3,1,1]])

    """
    path1 = list(map(__check_partition, path))
    check0 = sum(path1[0]) == 1
    N = len(path1)
    i = 1
    while i < N and check0:
        check0 = sum(path1[i]) == i + 1
        i = i + 1
    if not check0:
        raise Exception("Invalid path. The n-th element of the path must be a partition of n.")
    if N == 1:
        return [[1]]
    weights = list(map(len, path1))
    b = weights[1] - weights[0]
    check1 = b == 0 or b == 1
    i = 2
    while i < N and check1:
        b = weights[i] - weights[i-1]
        check1 = b == 0 or b == 1
        i = i + 1
    if not check1:
        raise Exception("Invalid path.")
    l = len(path1[-1])
    path2 = []
    for i in range(N):
        p = deepcopy(path1[i])
        li = len(p)
        for i in range(l-li):
            p.append(0)
        path2.append(p)
    tpath2 = list(map(list, zip(*path2)))
    diffs = list(map(__diff, tpath2))
    tdiffs = list(map(list, zip(*diffs)))
    check2 = True
    i = 0
    while check2 and i < N-1:
        d = tdiffs[i]
        check2 = sum(d) == 1
        j = 0
        while check2 and j < l:
            check2 = d[j] == 0 or d[j] == 1
            j = j + 1
        i = i + 1
    if not check2:
        raise Exception("Invalid path.")
    syt = [[] for i in range(l)]
    syt[0] = [1]
    for i in range(N-1):
        idx = tdiffs[i].index(1)
        syt[idx].append(i+2)

def syt_to_young_path(syt):
    """
    Young path corresponding to a standard Young tableau.

    Parameters
    ----------
    syt : list
        A standard Young tableau.

    Returns
    -------
    list
        A path of the Young graph, starting from `[1]`.

    Examples
    --------
    >>> from pysyt.syt import syt_to_young_path
    >>> syt_to_young_path([[1,2,4], [3], [5]])

    """
    if not __is_syt(syt):
        raise Exception("Not a standard Young tableau.")
    N = sum(list(map(len, syt)))
    path = []
    part = [0 for i in range(len(syt))]
    part[0] = 1
    path.append(part)
    for k in range(1, N):
        part = deepcopy(path[k-1])
        i = __which_row(syt, k+1)
        part[i] = part[i] + 1
        path.append(part)
    return list(map(__remove_zeros, path))

def random_young_path(n):
    """
    Young path at random according to the Plancherel growth process.

    Parameters
    ----------
    n : integer
        Size of the path.

    Returns
    -------
    list
        A path of the Young graph, starting from `[1]`.

    Examples
    --------
    >>> from pysyt.syt import random_young_path
    >>> random_young_path(6)

    """
    path = [[1]]
    for i in range(n-1):
        partitions = __connected_partitions(path[i])
        weights = list(map(count_sytx, partitions))
        path.append(choices(partitions, weights, k=1)[0])
    return path