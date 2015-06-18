"""
Merge function for 2048 game.
"""

def merge(line):
    """
    Function that merges a single row or column in 2048.
    """
    nonzero = []
    
    for iter1 in range(len(line)):
        if line[iter1] != 0:
            nonzero.append(line[iter1])
    
    results = [0] * len(line)
    for iter2 in range(len(nonzero)):
        results[iter2] = nonzero[iter2]
    
    #print "after move: " + str(results)
    
    for iter3 in (range(len(results)-1)):
        if results[iter3] == results[iter3+1]:
            results[iter3] = 2*results[iter3]
            results[iter3+1] = 0
            
    #print "after add: " + str(results)
    
    second_nonzero = []
    
    for iter4 in range(len(results)):
        if results[iter4] != 0:
            second_nonzero.append(results[iter4])
    
    final_results = [0] * len(line)
    for iter5 in range(len(second_nonzero)):
        final_results[iter5] = second_nonzero[iter5]
    
    #print "final: " + str(final_results)
    
    return final_results
