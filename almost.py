# SPDX-License-Identifier: GPL-3.0-or-later
#
# Author: Fioddor Superconcentrado <fioddor@gmail.com>

class Almost():
  '''Comparer class with tolerance for numbers'''
  NUMBER_TYPES = (int, float)
  SET_TYPES = (list, set, tuple)

  def __init__(cls, tolerance=1E-6, verbose=True):
    cls.configure(tolerance, verbose)

  def configure(cls, tolerance=None, verbose=None):
    if not tolerance is None:
      cls.tolerance = tolerance
    if not verbose is None:
      cls.verbose = verbose

  def say(cls, msg:str):
    if cls.verbose:
       print(msg)

  def same_number(cls, a, b) -> bool:
    '''Assess if a = b within the given  tolerance level

    Tolerance is relative to the reference (b) except when the reference is 0.
    When expecting a = 0, the tolerance is taken as an absolute value.

    :param a: Value to be compared.
    :param b: Reference value for the comparison.
    :param tolerance: Tolerance level.
    '''
    if 0 == b:
      return abs(a) < cls.tolerance
    return abs( (a - b) / b ) < cls.tolerance

  def same_set(cls, a, b) -> bool:
    '''Compare to sets (or lists or tuples)'''
    is_same = True
    if len(a) != len(b):
      return False
    norm_a, norm_b = sorted(list( a )), sorted(list( b ))
    # cls.say( '{} vs {}'.format(norm_a, norm_b) )
    for i in range(0, len(norm_b)):
      if not cls.same( norm_a[i], norm_b[i] ):
        cls.say(
          'difference: {}({}) vs {}({})'.format(
            norm_a[i], type(norm_a[i]), norm_b[i], type(norm_b[i])
          )
        )
        is_same = False
    return is_same

  def same_dict(cls, a:dict, b:dict) -> bool:
    '''Compare 2 dicts with tolerance for numbers'''

    if set(a.keys()) != set(b.keys()):
      cls.say( 'Dict keys mismatch: {} vs. {}'.format(a.keys(), b.keys()) )
      return False

    is_same = True
    for k, v in a.items():
      vb = b[k]
      if not cls.same(v, vb):
        cls.say( 'Different {}: {}({}) vs {}({})'.format(k, v, type(v), vb, type(vb) ) )
        is_same = False
    return is_same

  def _compatible_types(cls, a, b):
    '''Assess type compatibility for almost functions'''
    ta, tb = type(a), type(b)
    if ta==tb:
       return True
    if ta in cls.NUMBER_TYPES and tb in cls.NUMBER_TYPES:
       return True
    if ta in cls.SET_TYPES and tb in cls.SET_TYPES:
       return True
    return False

  def same(cls, a, b) -> bool:
    '''Compare 2 vars with tolerance for numbers'''
    if a is None and b is None:
      return True
    if not cls._compatible_types(a,b):
      return False
    ta, tb = type(a), type(b)
    if ta in cls.NUMBER_TYPES and tb in cls.NUMBER_TYPES:
      return cls.same_number(a, b)
    if ta in cls.SET_TYPES and tb in cls.SET_TYPES:
      return cls.same_set(a,b)
    if ta == dict and tb == ta:
      return cls.same_dict(a,b)
    raise Exception('Unimplemented type combo: {} vs. {}'.format(ta, tb))
