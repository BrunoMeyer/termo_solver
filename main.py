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

def get_word_list():
    # with open('br-latin1.txt', 'r') as f:
    with open('br-utf8.txt', 'r') as f:
        d = f.readlines()
    
    d = [unidecode(x.replace("\n", "")).lower() for x in d]
    d = [x for x in d if len(x) == 5]
    return d


def termo_solver(n_words=1,
  unknown_c = [],
  not_c = [],
  known_c = [],
  known_not_c = []
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

    cd = filter_candidates(
        wl,
        unknown_c=unknown_c,
        not_c=not_c,
        known_c=known_c,
        known_not_c=known_not_c
    )

    print(cd)

def generate_rules(
  game_history
):
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
          
  return (
    unknown_c,
    not_c,
    known_c,
    known_not_c
  )

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

  parser.set_defaults(list=[])    
  parser.set_defaults(silent=False)
  
  args = parser.parse_args()
  
  ghist = [
    # ('poeta', 'bbbby'),

    # ('poeta', ''),
    # ('mudar', ''),
    # ('tocar', ''),
    # ('tosar', ''),
    # ('armas', ''),
    # ('irmas', ''),
  ]


  while len(ghist) == 0 or ghist[-1][1] != 'ggggg':
    guess_w = input("Word guess: ")
    mask = input("Answer mask: ")

    ghist.append((guess_w, mask))
    unknown_c, not_c, known_c, known_not_c = generate_rules(ghist)
    termo_solver(1, unknown_c=unknown_c, not_c=not_c, known_c=known_c, known_not_c=known_not_c)
    # print(unknown_c, not_c, known_c, known_not_c)

if __name__ == "__main__":
    main()