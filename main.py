import argparse
import numpy as np

import os
import sys

from unidecode import unidecode

def edit_distance(string1, string2):
    """Ref: https://bit.ly/2Pf4a6Z"""

    if len(string1) > len(string2):
        difference = len(string1) - len(string2)
        string1[:difference]

    elif len(string2) > len(string1):
        difference = len(string2) - len(string1)
        string2[:difference]

    else:
        difference = 0

    for i in range(len(string1)):
        if string1[i] != string2[i]:
            difference += 1

    return difference

def filter_candidates(wl, unknown_c=[], known_c=[], known_not_c=[], not_c=[]):
    candidates = []
    for w in wl:
        add_w = True

        for c in not_c:
            if c in w:
                add_w = False
                break
        
        if add_w:
            for i, c in known_not_c:
                if w[i] == c:
                    add_w = False
                    break
            
            
            if add_w:
                for i, c in known_c:
                    if w[i] != c:
                        add_w = False
                        break
                if add_w:
                    for c in unknown_c:
                        if not c in w:
                            add_w = False
                            break
        
        if add_w:
            candidates.append(w)
    
    return candidates


def order_candidates(wl, candidates):
  a = list(''.join(candidates))
  unique, counts = np.unique(a, return_counts=True)
  converted_partial_score = {
    x:y
    for x,y in zip(unique,counts)
  }
  # print(converted_partial_score)
  def get_element_score(x):
    s = 0
    for c in set(x):
      if c in converted_partial_score:
        s += converted_partial_score[c]

    return s
      
  count_sum_order = sorted(candidates, key=get_element_score)

  # print([get_element_score(x) for x in count_sum_order])
  return count_sum_order

def get_word_list():
    # with open('br-latin1.txt', 'r') as f:
    with open('br-utf8.txt', 'r') as f:
        d = f.readlines()
    
    d = [unidecode(x.replace("\n", "")).lower() for x in d]
    d = [x for x in d if len(x) == 5]
    return d


def termo_solver(
  # n_words=1,
  # unknown_c = [],
  # not_c = [],
  # known_c = [],
  # known_not_c = []
  restraint_list
):
    wl = get_word_list()

    # cd = filter_candidates(
    #     wl,
    #     unknown_c=['d'],
    #     known_c=[(1, 'e'), (2, 'n'), (4, 'a')],
    #     known_not_c=[(3, 'd')],
    #     not_c = ['m', 'v', 'c', 'l', 'h', 'l', 'f', 'g', 't', 'p']
    # )


    # cd = filter_candidates(
    #     wl,
    #     unknown_c=[], #yellow
    #     not_c = [] # black (all)
    #     known_c=[], #green
    #     known_not_c=[], #black but with at least 1 yellow
    # )

    # cd = filter_candidates(
    #     wl,
    #     unknown_c=[], #yellow
    #     not_c = ['p', 'o', 'e', 't'], # black (all)
    #     known_c=[(4, 'a')], # green at
    #     known_not_c=[], # yellow at (without green)
    # )


    # cd = filter_candidates(
    #     wl,
    #     unknown_c=[], #yellow
    #     not_c = ['p', 'e', 't', 'c', 'g', 'm', 'i'], # black (all)
    #     known_c=[(1, 'a'), (3, 'o'), (4, 'r')], # green at
    #     known_not_c=[], # yellow at (without green)
    # )


    # cd = filter_candidates(
    #     wl,
    #     unknown_c=['e'], #yellow
    #     not_c = ['p', 'o', 'a', 'c', 'r', 'g', 'o'], # black (all)
    #     known_c=[(2, 'i'), (3, 't')], # green at
    #     known_not_c=[], # yellow at (without green)
    # )


    # cd = filter_candidates(
    #     wl,
    #     unknown_c=['s', 'd', 'i'], #yellow
    #     not_c = ['p', 'o', 'e', 't', 'f', 'c', 'r', 'h', 'n', 't', 'v'], # black (all)
    #     known_c=[(4, 'a')], # green at
    #     known_not_c=[(1, 'i'), (0, 'd'), (3, 'a')], # yellow at (without green)
    # )

    
    cd_list = []
    for unknown_c, not_c, known_c, known_not_c in restraint_list:
      cd = filter_candidates(
          wl,
          unknown_c=unknown_c,
          not_c=not_c,
          known_c=known_c,
          known_not_c=known_not_c
      )

      cd = order_candidates(wl, cd)
      cd_list.append(cd)
    
    merge_cd = []
    for cd in cd_list:
      merge_cd += cd
    
    merge_cd = order_candidates(wl, merge_cd)
    cd_list.append(merge_cd)
    
    return cd_list

def generate_rules(
  game_list
):

  ret_list = []

  for game_history in game_list:
    unknown_c = []
    not_c = []
    known_c = []
    known_not_c = []
    for w, mask in game_history:
      for i in range(len(w)):
        c = w[i]
        mi = mask[i]

        if mi == 'y':
          unknown_c.append(c)
          known_not_c.append((i, c))
        if mi == 'b' and not (c in unknown_c) and (not c in [x[1] for x in known_c]):
          not_c.append(c)
        if mi == 'g':
          known_c.append((i, c))
          
    ret_list.append((
      unknown_c,
      not_c,
      known_c,
      known_not_c
    ))
  
  return ret_list

def main():
  parser = argparse.ArgumentParser(description='Process some integers.')
#   parser.add_argument('-f', '--input_file', dest='input_file', type=str,
#                       required=True)
#   parser.add_argument('-o', '--output_file', dest='output_file', type=str,
#                       required=False, default='result_toniot.json')
  
#   parser.add_argument('-l','--list', nargs='+', dest='list', help='List of ',
#                       type=int)
  
#   parser.add_argument('-s', dest='silent', action='store_true')
  
#   parser.add_argument('-t', '--type', dest='type', type=str,
#                       required=False, choices=['type1', 'type2', 'type3', 'type4'], default='type1')

  parser.add_argument('-n', '--n_words', dest='n_words', type=int,
                      required=False, default=1)
  parser.set_defaults(list=[])    
  parser.set_defaults(silent=False)
  
  args = parser.parse_args()
  
  # ghist = [
  #   # ('poeta', 'bbbby'),

  #   # ('poeta', ''),
  #   # ('mudar', ''),
  #   # ('tocar', ''),
  #   # ('tosar', ''),
  #   # ('armas', ''),
  #   # ('irmas', ''),
  # ]

  ghist = [[] for i in range(args.n_words)]


  def check_win(games):
    if len(games[0]) == 0:
      return True
    
    for hist in games:
      if(hist[-1][1] != 'ggggg'):
        return True
    
    return False
  
  # while len(ghist) == 0 or ghist[-1][1] != 'ggggg':
  while check_win(ghist):
        
    # guess_list = []
    # mask_list = []
    guess_w = input("Word guess for word: ")
    for i in range(args.n_words):
      mask = input("Answer mask for word {}: ".format(i+1))
      # guess_list.append(guess_w)
      # mask_list.append(mask)
      ghist[i].append((guess_w, mask))
    
    restraint_list = generate_rules(ghist)

    # candidates = termo_solver(1, unknown_c=unknown_c, not_c=not_c, known_c=known_c, known_not_c=known_not_c)
    candidates_list = termo_solver(restraint_list)
    # candidates = order_candidates(wl, candidates)
    # print(unknown_c, not_c, known_c, known_not_c)
    for candidate in candidates_list:
      print("\n\n---\n\n")
      print(candidate)
      # print("\n\n---\n\n")

if __name__ == "__main__":
    main()