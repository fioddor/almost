# SPDX-License-Identifier: GPL-3.0-or-later
#
# Author: Fioddor Superconcentrado <fioddor@gmail.com>

from almost import Almost


def test_almost_same_number():
  almost = Almost()
  f = almost.same
  # vs non-zero:
  assert not f(1.2345683, 1.234567)
  assert     f(1.2345682, 1.234567)
  assert     f(1.2345658, 1.234567)
  assert not f(1.2345655, 1.234567)
  # vs 0:
  assert     f(0.0000009, 0)
  assert not f(0.000001 , 0)
  # explicit tolerance:
  almost.configure(tolerance=0.01)
  assert not f(1.25241, 1.24)
  assert     f(1.2524 , 1.24)

def test_almost_same_set():
  # configure the difference:
  lst_rd = [1.234567 , 1.234567 , 1.234567 ]
  lst_d  = [1.2345682, 1.2345658, 1.2345683]
  # configure irrelevant differences. Only the 3rd element differs significantly:
  lst_rs = lst_rd[:2]
  lst_s  = lst_d[:2]
  # generate other types:
  set_rd, tpl_rd = set(lst_rd), tuple(lst_rd)
  set_rs, tpl_rs = set(lst_rs), tuple(lst_rs)
  set_s, tpl_s = set(lst_s), tuple(lst_s)
  set_d, tpl_d = set(lst_d), tuple(lst_d)
  # run test:
  nearly = Almost()
  nearly.configure(verbose=False)
  f = nearly.same
  assert     f(lst_rs, lst_s)
  assert     f(lst_rs, set_s)
  assert     f(lst_rs, tpl_s)
  assert not f(lst_rd, lst_d)
  assert not f(lst_rd, set_d)
  assert not f(lst_rd, tpl_d)

def test_almost_same_dict():
  ref = {
    'number': 1.234567,
    'lists' : [1.234567, 1.234567, 1234567],
  }
  test_diff = {
    'number': 1.2345683,
    'lists' : [1.234567, 1.234567, 1234567],
  }
  test_same = {
    'number': 1.2345682,
    'lists' : [1.2345658, 1.234567, 1234567],
  }
  # run test:
  almost = Almost(verbose=False)
  f = almost.same_dict
  assert     f(test_same, ref)
  assert not f(test_diff, ref)

def test_almost_same_nones():
  almost = Almost()
  f = almost.same
  assert     f(None, None)
  assert not f(None, 0)
  assert not f(None, [])
  assert not f(None, {})


test_almost_same_number()
test_almost_same_set()
test_almost_same_dict()
test_almost_same_nones()
