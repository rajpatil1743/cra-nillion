from nada_dsl import *


def initialize_voters(nr_voters):
   
    voters = []
    for i in range(nr_voters):
        voters.append(Party(name="Voter" + str(i)))

    return voters


def inputs_initialization(nr_voters, nr_candidates, voters):
    
    votes_per_candidate = []
    for c in range(nr_candidates):
        votes_per_candidate.append([])
        for v in range(nr_voters):
            votes_per_candidate[c].append(
                SecretUnsignedInteger(
                    Input(name="v" + str(v) + "_c" + str(c), party=voters[v])
                )
            )

    return votes_per_candidate


def count_votes(nr_voters, nr_candidates, votes_per_candidate, outparty):
    
    votes = []
    for c in range(nr_candidates):
        result = votes_per_candidate[c][0]
        for v in range(1, nr_voters):
            result += votes_per_candidate[c][v]
        votes.append(Output(result, "final_vote_count_c" + str(c), outparty))

    return votes


def fn_check_sum(nr_voters, nr_candidates, votes_per_candidate, outparty):
   
    check_sum = []
    for v in range(nr_voters):
        check = votes_per_candidate[0][v]
        for c in range(1, nr_candidates):
            vote_v_c = votes_per_candidate[c][v]
            check += vote_v_c
        check_sum.append(Output(check, "check_sum_v" + str(v), outparty))

    return check_sum


def fn_check_prod(nr_voters, nr_candidates, votes_per_candidate, outparty):
   
    check_prod = []
    for v in range(nr_voters):
        for c in range(nr_candidates):
            vote_v_c = votes_per_candidate[c][v]
            check_v_c_product = (UnsignedInteger(1) - vote_v_c) * (
                UnsignedInteger(2) - vote_v_c
            )
            check_prod.append(
                Output(
                    check_v_c_product, "check_prod_v" + str(v) + "_c" + str(c), outparty
                )
            )

    return check_prod


def nada_main():

    # 0. Compiled-time constants
    nr_voters = 3
    nr_candidates = 2

    # 1. Parties initialization
    voters = initialize_voters(nr_voters)
    outparty = Party(name="OutParty")

    # 2. Inputs initialization
    votes_per_candidate = inputs_initialization(nr_voters, nr_candidates, voters)

    # 3. Computation
    # Count the votes
    votes = count_votes(nr_voters, nr_candidates, votes_per_candidate, outparty)
    # Check input soundness
    check_sum = fn_check_sum(nr_voters, nr_candidates, votes_per_candidate, outparty)
    check_prod = fn_check_prod(nr_voters, nr_candidates, votes_per_candidate, outparty)

    # 4. Output
    # Concatenate lists
    results = votes + check_sum + check_prod
    return results