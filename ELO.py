def elo(winning ,losing):
    rating_n=1/(1+10**((winning-losing)/400))
    rating_m=1/(1+10**((losing-winning)/400))
    nr=losing+(30*(0-rating_n))
    mr=winning+(30*(1-rating_m))
    return [int(nr),int(mr)]



