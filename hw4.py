"""
Planner for Yahtzee
Simplifications:  only allow discard and roll, only score against upper level
"""

# Used to increase the timeout, if necessary
import codeskulptor
codeskulptor.set_timeout(20)

def gen_all_sequences(outcomes, length):
    """
    Iterative function that enumerates the set of all sequences of
    outcomes of given length.
    """
    
    answer_set = set([()])
    for dummy_idx in range(length):
        temp_set = set()
        for partial_sequence in answer_set:
            for item in outcomes:
                new_sequence = list(partial_sequence)
                new_sequence.append(item)
                temp_set.add(tuple(new_sequence))
        answer_set = temp_set
    return answer_set

def score(hand):
    """
    Compute the maximal score for a Yahtzee hand according to the
    upper section of the Yahtzee score card.

    hand: full yahtzee hand

    Returns an integer score 
    """
    hand_list = list(hand)
    hand_list.sort()
    
    count_list = [0, 0, 0, 0, 0, 0]
    
    for number in hand_list:
        if number == 1:
            count_list[0] += 1
        elif number == 2:
            count_list[1] += 1
        elif number == 3:
            count_list[2] += 1
        elif number == 4:
            count_list[3] += 1
        elif number == 5:
            count_list[4] += 1
        else:
            count_list[5] += 1
    
    score_list = [count_list[0], 2*count_list[1], 3*count_list[2], 4*count_list[3], 5*count_list[4], 6*count_list[5]]
    
    return max(score_list)

print list(gen_all_sequences([1,2,3,4,5,6],1))

def expected_value(held_dice, num_die_sides, num_free_dice):
    """
    Compute the expected value based on held_dice given that there
    are num_free_dice to be rolled, each with num_die_sides.

    held_dice: dice that you will hold
    num_die_sides: number of sides on each die
    num_free_dice: number of dice to be rolled

    Returns a floating point expected value
    """    
    outcome_list = []
    for value in range(num_die_sides):
        outcome_list.append(value+1)
    
    possible_outcomes = list(gen_all_sequences(outcome_list, num_free_dice))
    
    all_scores = []
    for outcome in possible_outcomes:
        outcome_as_list = list(outcome)
        outcome_as_list.extend(list(held_dice))
        all_scores.append(score(tuple(outcome_as_list)))

    sum_scores = sum(all_scores)
    size = len(all_scores)
    
    return float(sum_scores) / size

print "expected:",expected_value((1,2), 3, 3)


def gen_all_holds(hand):
    """
    Generate all possible choices of dice from hand to hold.

    hand: full yahtzee hand

    Returns a set of tuples, where each tuple is dice to hold
    """
    result = set([()])
    
    if len(hand) == 0:
        return result
    elif len(hand) == 1:
        result.add(hand)
    else:
        
        hand_as_list = list(hand)
        
        for die_number in hand[0:len(hand)-1]:
            new_hand = hand_as_list[1:]
            hand_as_list.remove(die_number)
            new_tuples_set = gen_all_holds(tuple(new_hand))
            
            for each_tuple in new_tuples_set:
                die_number_as_list = [die_number]
                die_number_as_list.extend(list(each_tuple))
                result.add(tuple(die_number_as_list))
                
        result.add((hand[-1],))
        
    return result
        

def strategy(hand, num_die_sides):
    """
    Compute the hold that maximizes the expected value when the
    discarded dice are rolled.

    hand: full yahtzee hand
    num_die_sides: number of sides on each die

    Returns a tuple where the first element is the expected score and
    the second element is a tuple of the dice to hold
    """
    all_holds = gen_all_holds(hand)
    
    score_keeper = 0
    highest_hold = ()
    for hold in all_holds:
        num_free_lice = len(hand) - len(hold)
        hand_value = expected_value(hold, num_die_sides, num_free_lice)
        if hand_value > score_keeper:
            highest_hold = hold
            score_keeper = hand_value
        
    return (score_keeper, highest_hold)


def run_example():
    """
    Compute the dice to hold and expected score for an example hand
    """
    num_die_sides = 6
    hand = (1, 1, 1, 5, 6)
    hand_score, hold = strategy(hand, num_die_sides)
    print "Best strategy for hand", hand, "is to hold", hold, "with expected score", hand_score
    
    
#run_example()


#import poc_holds_testsuite
#poc_holds_testsuite.run_suite(gen_all_holds)
                                       
    
    
    



