def frontera(punto):
    return not len(vecindades[punto][0]) == len(vecindades[punto][1]) + 1

