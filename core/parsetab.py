
# parsetab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'END EQUAL GT GTS ID START TAG VALUE WORDSxml : opentag words children closetag\n           | opentag children words closetag\n           | alonetag wordsopentag : START attributes GTclosetag : ENDalonetag : START attributes GTSattributes : ID EQUAL VALUE attributes\n               | emptychildren : xml children\n            | emptywords : ID words\n             | emptyempty :'
    
_lr_action_items = {'GT':([4,12,13,26,27,],[-13,-8,21,-13,-7,]),'VALUE':([22,],[26,]),'$end':([1,2,5,6,7,15,20,23,24,25,],[0,-13,-3,-13,-12,-11,-6,-1,-5,-2,]),'EQUAL':([14,],[22,]),'START':([0,2,3,5,6,7,8,9,10,15,20,21,23,24,25,],[4,-13,4,-3,-13,-12,-12,4,4,-11,-6,-4,-1,-5,-2,]),'GTS':([4,12,13,26,27,],[-13,-8,20,-13,-7,]),'ID':([2,3,4,5,6,7,8,9,11,15,16,17,20,21,23,24,25,26,],[6,6,14,-3,6,-12,-10,-13,6,-11,-10,-9,-6,-4,-1,-5,-2,14,]),'END':([2,3,5,6,7,8,9,10,11,15,16,17,18,19,20,21,23,24,25,],[-13,-13,-3,-13,-12,-10,-13,-13,-13,-11,-10,-9,24,24,-6,-4,-1,-5,-2,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'words':([2,3,6,11,],[5,10,15,19,]),'attributes':([4,26,],[13,27,]),'empty':([2,3,4,6,9,10,11,26,],[7,8,12,7,16,16,7,12,]),'children':([3,9,10,],[11,17,18,]),'xml':([0,3,9,10,],[1,9,9,9,]),'closetag':([18,19,],[23,25,]),'alonetag':([0,3,9,10,],[2,2,2,2,]),'opentag':([0,3,9,10,],[3,3,3,3,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> xml","S'",1,None,None,None),
  ('xml -> opentag words children closetag','xml',4,'p_xml','sintatic.py',29),
  ('xml -> opentag children words closetag','xml',4,'p_xml','sintatic.py',30),
  ('xml -> alonetag words','xml',2,'p_xml','sintatic.py',31),
  ('opentag -> START attributes GT','opentag',3,'p_opentag','sintatic.py',46),
  ('closetag -> END','closetag',1,'p_closetag','sintatic.py',53),
  ('alonetag -> START attributes GTS','alonetag',3,'p_alonetag','sintatic.py',73),
  ('attributes -> ID EQUAL VALUE attributes','attributes',4,'p_attributes','sintatic.py',79),
  ('attributes -> empty','attributes',1,'p_attributes','sintatic.py',80),
  ('children -> xml children','children',2,'p_children','sintatic.py',88),
  ('children -> empty','children',1,'p_children','sintatic.py',89),
  ('words -> ID words','words',2,'p_words','sintatic.py',94),
  ('words -> empty','words',1,'p_words','sintatic.py',95),
  ('empty -> <empty>','empty',0,'p_empty','sintatic.py',100),
]
