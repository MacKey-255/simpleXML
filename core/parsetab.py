
# parsetab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'END EQUAL GT GTS ID START TAG VALUE WORDSxml : opentag words children closetag\n           | alonetag wordsopentag : START attributes GTclosetag : ENDalonetag : START attributes GTSattributes : ID EQUAL VALUE attributes\n               | emptychildren : xml children\n            | emptywords : ID words\n             | emptyempty :'
    
_lr_action_items = {'START':([0,2,3,5,6,7,8,13,15,16,17,19,20,],[4,-12,-12,4,-12,-11,-2,4,-10,-3,-5,-1,-4,]),'$end':([1,3,6,7,8,15,17,19,20,],[0,-12,-12,-11,-2,-10,-5,-1,-4,]),'ID':([2,3,4,6,16,17,22,],[6,6,10,6,-3,-5,10,]),'END':([2,3,5,6,7,8,12,13,14,15,16,17,19,20,21,],[-12,-12,-12,-12,-11,-2,20,-12,-9,-10,-3,-5,-1,-4,-8,]),'GT':([4,9,11,22,23,],[-12,16,-7,-12,-6,]),'GTS':([4,9,11,22,23,],[-12,17,-7,-12,-6,]),'EQUAL':([10,],[18,]),'VALUE':([18,],[22,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'xml':([0,5,13,],[1,13,13,]),'opentag':([0,5,13,],[2,2,2,]),'alonetag':([0,5,13,],[3,3,3,]),'words':([2,3,6,],[5,8,15,]),'empty':([2,3,4,5,6,13,22,],[7,7,11,14,7,14,11,]),'attributes':([4,22,],[9,23,]),'children':([5,13,],[12,21,]),'closetag':([12,],[19,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> xml","S'",1,None,None,None),
  ('xml -> opentag words children closetag','xml',4,'p_xml','sintatic.py',28),
  ('xml -> alonetag words','xml',2,'p_xml','sintatic.py',29),
  ('opentag -> START attributes GT','opentag',3,'p_opentag','sintatic.py',44),
  ('closetag -> END','closetag',1,'p_closetag','sintatic.py',51),
  ('alonetag -> START attributes GTS','alonetag',3,'p_alonetag','sintatic.py',75),
  ('attributes -> ID EQUAL VALUE attributes','attributes',4,'p_attributes','sintatic.py',81),
  ('attributes -> empty','attributes',1,'p_attributes','sintatic.py',82),
  ('children -> xml children','children',2,'p_children','sintatic.py',90),
  ('children -> empty','children',1,'p_children','sintatic.py',91),
  ('words -> ID words','words',2,'p_words','sintatic.py',96),
  ('words -> empty','words',1,'p_words','sintatic.py',97),
  ('empty -> <empty>','empty',0,'p_empty','sintatic.py',102),
]
