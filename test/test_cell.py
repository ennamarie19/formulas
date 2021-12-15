#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# Copyright 2016-2021 European Commission (JRC);
# Licensed under the EUPL (the 'Licence');
# You may not use this work except in compliance with the Licence.
# You may obtain a copy of the Licence at: http://ec.europa.eu/idabc/eupl
import time
import unittest
import ddt
import schedula as sh
from formulas.cell import Cell
from formulas.functions import Error
from formulas.functions.date import DEFAULT_DATE

DEFAULT_DATE[0] = 2019


def inp_ranges(*rng):
    return dict.fromkeys(rng, sh.EMPTY)


@ddt.ddt
class TestCell(unittest.TestCase):
    @ddt.idata([
        ('A1', '=NPER(1,4,5)', {}, '<Ranges>(A1)=[[-1.1699250014423124]]'),
        ('A1', '=NPER(0,4,5)', {}, '<Ranges>(A1)=[[-1.25]]'),
        ('A1', '=FV(0.06,-10,-200,-500,1)', {},
         '<Ranges>(A1)=[[-1281.1410664423581]]'),
        ('A1', '=FV(0.06,-10,200,-500,1)', {},
         '<Ranges>(A1)=[[1839.5358433574759]]'),
        ('A1', '=CUMIPMT(0.09/12,30*12,125000,13,24,4)', {},
         '<Ranges>(A1)=[[#NUM!]]'),
        ('A1', '=CUMIPMT(0.09/12,30*12,125000,13,24,0)', {},
         '<Ranges>(A1)=[[-11135.232130750845]]'),
        ('A1', '=CUMIPMT(3,5.5,125000,3,5,1)', {},
         '<Ranges>(A1)=[[-265999.0229604315]]'),
        ('A1', '=CUMIPMT(3,5.5,125000,1,5,1)', {},
         '<Ranges>(A1)=[[-359611.6267708859]]'),
        ('A1', '=CUMIPMT(3,5.5,125000,1,6,1)', {}, '<Ranges>(A1)=[[#NUM!]]'),
        ('A1', '=RATE(1500,-200,8000)', {},
         '<Ranges>(A1)=[[0.025000000047328684]]'),
        ('A1', '=RATE(43,-200,8000)', {},
         '<Ranges>(A1)=[[0.0033315518252391286]]'),
        ('A1', '=PV(100,3,22.4)', {}, '<Ranges>(A1)=[[-0.22399978258780684]]'),
        ('A1', '=PV(100,3.1,22)', {}, '<Ranges>(A1)=[[-0.21999986540577623]]'),
        ('A1', '=PV(100,3,22)', {}, '<Ranges>(A1)=[[-0.21999978647016746]]'),
        ('A1', '=DATEDIF("01/01/01","06/02/08","YD")', {},
         '<Ranges>(A1)=[[152]]'),
        ('A1', '=DATEDIF("01/09/01","06/02/08","YD")', {},
         '<Ranges>(A1)=[[144]]'),
        ('A1', '=DATEDIF("01/31/2001","01/29/2008","YD")', {},
         '<Ranges>(A1)=[[363]]'),
        ('A1', '=DATEDIF("01/01/2001","02/29/2008","YD")', {},
         '<Ranges>(A1)=[[59]]'),
        ('A1', '=DATEDIF("01/01/2001","03/01/2008","YD")', {},
         '<Ranges>(A1)=[[59]]'),
        ('A1', '=DATEDIF("01/09/00","06/02/08","YD")', {},
         '<Ranges>(A1)=[[145]]'),
        ('A1', '=DATEDIF("01/31/2001","03/29/2007","YD")', {},
         '<Ranges>(A1)=[[57]]'),
        ('A1', '=DATEDIF("01/31/01","02/29/08","YM")', {},
         '<Ranges>(A1)=[[0]]'),
        ('A1', '=DATEDIF(1, 0, "YD")', {}, '<Ranges>(A1)=[[#NUM!]]'),
        ('A1', '=DATEDIF(-1, 222222, "YD")', {}, '<Ranges>(A1)=[[#NUM!]]'),
        ('A1', '=DATEDIF(-1, 222222, "D")', {}, '<Ranges>(A1)=[[#NUM!]]'),
        ('A1', '=DATEDIF(0, 222222, "YD")', {}, '<Ranges>(A1)=[[154]]'),
        ('A1', '=DATEDIF(1, 222222, "YD")', {}, '<Ranges>(A1)=[[153]]'),
        ('A1', '=DATEDIF("01/09/01","02/29/08","YD")', {},
         '<Ranges>(A1)=[[51]]'),
        ('A1', '=DATEDIF(60,222222,"YD")', {}, '<Ranges>(A1)=[[94]]'),
        ('A1', '=DATEDIF(222,222290,"YD")', {}, '<Ranges>(A1)=[[0]]'),
        ('A1', '=DATEDIF(222,222289,"YD")', {}, '<Ranges>(A1)=[[364]]'),
        ('A1', '=DATEDIF(222,222222,"YD")', {}, '<Ranges>(A1)=[[297]]'),
        ('A1', '=DATEDIF(222,222290,"YM")', {}, '<Ranges>(A1)=[[0]]'),
        ('A1', '=DATEDIF(222,222289,"YM")', {}, '<Ranges>(A1)=[[11]]'),
        ('A1', '=DATEDIF(222,222222,"YM")', {}, '<Ranges>(A1)=[[9]]'),
        ('A1', '=DATEDIF(222,222290,"MD")', {}, '<Ranges>(A1)=[[0]]'),
        ('A1', '=DATEDIF(222,222289,"MD")', {}, '<Ranges>(A1)=[[30]]'),
        ('A1', '=DATEDIF(222,222222,"MD")', {}, '<Ranges>(A1)=[[24]]'),
        ('A1', '=DATEDIF(222,222290,"Y")', {}, '<Ranges>(A1)=[[608]]'),
        ('A1', '=DATEDIF(222,222289,"Y")', {}, '<Ranges>(A1)=[[607]]'),
        ('A1', '=DATEDIF(222,222222,"Y")', {}, '<Ranges>(A1)=[[607]]'),
        ('A1', '=DATEDIF(222,222290,"M")', {}, '<Ranges>(A1)=[[7296]]'),
        ('A1', '=DATEDIF(222,222289,"M")', {}, '<Ranges>(A1)=[[7295]]'),
        ('A1', '=DATEDIF(222,222222,"M")', {}, '<Ranges>(A1)=[[7293]]'),
        ('A1', '=DATEDIF(222,222290,"D")', {}, '<Ranges>(A1)=[[222068]]'),
        ('A1', '=DATEDIF(222,222289,"D")', {}, '<Ranges>(A1)=[[222067]]'),
        ('A1', '=DATEDIF(222,222222,"D")', {}, '<Ranges>(A1)=[[222000]]'),
        ('A1', '=WEEKNUM(0, 21)', {}, '<Ranges>(A1)=[[52]]'),
        ('A1', '=WEEKNUM(1, 21)', {}, '<Ranges>(A1)=[[52]]'),
        ('A1', '=WEEKNUM(2, 21)', {}, '<Ranges>(A1)=[[1]]'),
        ('A1', '=WEEKNUM(8, 21)', {}, '<Ranges>(A1)=[[1]]'),
        ('A1', '=WEEKNUM(15, 21)', {}, '<Ranges>(A1)=[[2]]'),
        ('A1', '=WEEKNUM(22, 21)', {}, '<Ranges>(A1)=[[3]]'),
        ('A1', '=WEEKNUM(29, 21)', {}, '<Ranges>(A1)=[[4]]'),
        ('A1', '=WEEKNUM(9, 21)', {}, '<Ranges>(A1)=[[2]]'),
        ('A1', '=WEEKNUM(16, 21)', {}, '<Ranges>(A1)=[[3]]'),
        ('A1', '=WEEKNUM(23, 21)', {}, '<Ranges>(A1)=[[4]]'),
        ('A1', '=WEEKNUM(30, 21)', {}, '<Ranges>(A1)=[[5]]'),
        ('A1', '=WEEKNUM(9, 21)', {}, '<Ranges>(A1)=[[2]]'),
        ('A1', '=WEEKNUM(64, 21)', {}, '<Ranges>(A1)=[[9]]'),
        ('A1', '=WEEKNUM(65, 21)', {}, '<Ranges>(A1)=[[10]]'),
        ('A1', '=WEEKNUM(0, 11)', {}, '<Ranges>(A1)=[[1]]'),
        ('A1', '=WEEKNUM(0, 12)', {}, '<Ranges>(A1)=[[1]]'),
        ('A1', '=WEEKNUM(0, 13)', {}, '<Ranges>(A1)=[[1]]'),
        ('A1', '=WEEKNUM(0, 14)', {}, '<Ranges>(A1)=[[1]]'),
        ('A1', '=WEEKNUM(0, 15)', {}, '<Ranges>(A1)=[[1]]'),
        ('A1', '=WEEKNUM(0, 16)', {}, '<Ranges>(A1)=[[1]]'),
        ('A1', '=WEEKNUM(0, 17)', {}, '<Ranges>(A1)=[[0]]'),
        ('A1', '=WEEKNUM(0, 1)', {}, '<Ranges>(A1)=[[0]]'),
        ('A1', '=WEEKNUM(0, 2)', {}, '<Ranges>(A1)=[[1]]'),
        ('A1', '=WEEKNUM(60, 21)', {}, '<Ranges>(A1)=[[9]]'),
        ('A1', '=WEEKNUM(60, 11)', {}, '<Ranges>(A1)=[[10]]'),
        ('A1', '=WEEKNUM(60, 12)', {}, '<Ranges>(A1)=[[10]]'),
        ('A1', '=WEEKNUM(60, 13)', {}, '<Ranges>(A1)=[[10]]'),
        ('A1', '=WEEKNUM(60, 14)', {}, '<Ranges>(A1)=[[9]]'),
        ('A1', '=WEEKNUM(60, 15)', {}, '<Ranges>(A1)=[[9]]'),
        ('A1', '=WEEKNUM(60, 16)', {}, '<Ranges>(A1)=[[9]]'),
        ('A1', '=WEEKNUM(60, 17)', {}, '<Ranges>(A1)=[[9]]'),
        ('A1', '=WEEKNUM(60, 1)', {}, '<Ranges>(A1)=[[9]]'),
        ('A1', '=WEEKNUM(60, 2)', {}, '<Ranges>(A1)=[[10]]'),
        ('A1', '=WEEKNUM(11690, 21)', {}, '<Ranges>(A1)=[[53]]'),
        ('A1', '=WEEKNUM(12055, 21)', {}, '<Ranges>(A1)=[[52]]'),
        ('A1', '=WEEKNUM(12056, 21)', {}, '<Ranges>(A1)=[[1]]'),
        ('A1', '=WEEKNUM(12057, 21)', {}, '<Ranges>(A1)=[[1]]'),
        ('A1', '=WEEKNUM(12425, 11)', {}, '<Ranges>(A1)=[[1]]'),
        ('A1', '=WEEKNUM(12425, 12)', {}, '<Ranges>(A1)=[[2]]'),
        ('A1', '=WEEKNUM(12425, 13)', {}, '<Ranges>(A1)=[[2]]'),
        ('A1', '=WEEKNUM(12425, 14)', {}, '<Ranges>(A1)=[[2]]'),
        ('A1', '=WEEKNUM(12425, 15)', {}, '<Ranges>(A1)=[[2]]'),
        ('A1', '=WEEKNUM(12425, 16)', {}, '<Ranges>(A1)=[[2]]'),
        ('A1', '=WEEKNUM(12425, 17)', {}, '<Ranges>(A1)=[[1]]'),
        ('A1', '=WEEKNUM(12425, 1)', {}, '<Ranges>(A1)=[[1]]'),
        ('A1', '=WEEKNUM(12425, 2)', {}, '<Ranges>(A1)=[[1]]'),
        ('A1', '=WEEKNUM(60, 11)', {}, '<Ranges>(A1)=[[10]]'),
        ('A1', '=WEEKNUM(60, 12)', {}, '<Ranges>(A1)=[[10]]'),
        ('A1', '=WEEKNUM(60, 13)', {}, '<Ranges>(A1)=[[10]]'),
        ('A1', '=WEEKNUM(60, 14)', {}, '<Ranges>(A1)=[[9]]'),
        ('A1', '=WEEKNUM(60, 15)', {}, '<Ranges>(A1)=[[9]]'),
        ('A1', '=WEEKNUM(60, 16)', {}, '<Ranges>(A1)=[[9]]'),
        ('A1', '=WEEKNUM(60, 17)', {}, '<Ranges>(A1)=[[9]]'),
        ('A1', '=WEEKNUM(60, 1)', {}, '<Ranges>(A1)=[[9]]'),
        ('A1', '=WEEKNUM(60, 2)', {}, '<Ranges>(A1)=[[10]]'),
        ('A1', '=WEEKNUM(11326)', {}, '<Ranges>(A1)=[[1]]'),
        ('A1', '=WEEKNUM(36534)', {}, '<Ranges>(A1)=[[3]]'),
        ('A1', '=WEEKNUM(36527)', {}, '<Ranges>(A1)=[[2]]'),
        ('A1', '=WEEKNUM(12420)', {}, '<Ranges>(A1)=[[1]]'),
        ('A1', '=WEEKNUM(12421)', {}, '<Ranges>(A1)=[[1]]'),
        ('A1', '=WEEKNUM(11323)', {}, '<Ranges>(A1)=[[53]]'),
        ('A1', '=WEEKNUM(11325)', {}, '<Ranges>(A1)=[[1]]'),
        ('A1', '=WEEKNUM(11327)', {}, '<Ranges>(A1)=[[2]]'),
        ('A1', '=WEEKNUM(36533)', {}, '<Ranges>(A1)=[[2]]'),
        ('A1', '=WEEKNUM(36526)', {}, '<Ranges>(A1)=[[1]]'),
        ('A1', '=WEEKNUM(36525)', {}, '<Ranges>(A1)=[[53]]'),
        ('A1', '=WEEKDAY(36525)', {}, '<Ranges>(A1)=[[6]]'),
        ('A1', '=WEEKDAY(0,17)', {}, '<Ranges>(A1)=[[7]]'),
        ('A1', '=WEEKDAY("a",FALSE)', {}, '<Ranges>(A1)=[[#VALUE!]]'),
        ('A1', '=WEEKDAY(0,FALSE)', {}, '<Ranges>(A1)=[[#NUM!]]'),
        ('A1', '=WEEKDAY(0,11)', {}, '<Ranges>(A1)=[[6]]'),
        ('A1', '=WEEKDAY("2.9", "3.9")', {}, '<Ranges>(A1)=[[0]]'),
        ('A1', '=WEEKDAY(TRUE, 2)', {}, '<Ranges>(A1)=[[7]]'),
        ('A1', '=WEEKDAY(DATE(1008,5,23))', {}, '<Ranges>(A1)=[[4]]'),
        ('A1', '=CUMIPMT(0.09/12,30*12,125000,13,24,TRUE)', {},
         '<Ranges>(A1)=[[#VALUE!]]'),
        ('A1', '=PRODUCT({3,4},{8,9})', {}, '<Ranges>(A1)=[[864.0]]'),
        ('A1', '=SLOPE({3,4},{8,9})', {}, '<Ranges>(A1)=[[1.0]]'),
        ('A1', '=CORREL(A2:A4,{8,2})', {'A2:A4': [[sh.EMPTY] * 3]},
         '<Ranges>(A1)=[[#N/A]]'),
        ('A1', '=CORREL({"2",4,1},{7,"",TRUE})', {},
         '<Ranges>(A1)=[[#DIV/0!]]'),
        ('A1', '=CORREL(A2:A3,{8,2})', {'A2:A3': [[sh.EMPTY] * 2]},
         '<Ranges>(A1)=[[#DIV/0!]]'),
        ('A1', '=CORREL(A2,{8,2})', {'A2': [[sh.EMPTY]]},
         '<Ranges>(A1)=[[#VALUE!]]'),
        ('A1', '=CORREL({"2",4,1},{7,3,6})', {}, '<Ranges>(A1)=[[-1.0]]'),
        ('A1', '=CORREL({2,4,1},{7,3,6})', {},
         '<Ranges>(A1)=[[-0.8386278693775346]]'),
        ('A1', '=NPER(0.12/12, -100, -1000, 10000, 1)', {},
         '<Ranges>(A1)=[[59.67386567429457]]'),
        ('A1', '=NPER(0.12/12, -100, -1000)', {},
         '<Ranges>(A1)=[[-9.578594039813161]]'),
        ('A1', '=IPMT(0.1/12, "01/01/1900", 3*12, 8000)', {},
         '<Ranges>(A1)=[[-66.66666666666667]]'),
        ('A1', '=IPMT(0.1/12, 60, 3*12, 8000)', {},
         '<Ranges>(A1)=[[#NUM!]]'),
        ('A1', '=FV(0.06/12, 10, -200, -500, 1)', {},
         '<Ranges>(A1)=[[2581.4033740601367]]'),
        ('A1', '=RATE(4*12, -200, 8000)', {},
         '<Ranges>(A1)=[[0.00770147248823337]]'),
        ('A1', '=PV(0.08/12, 12*20, 500000,,0)', {},
         '<Ranges>(A1)=[[-59777145.85118777]]'),
        ('A1', '=PPMT(0.1/12, 1, 2*12, 2000)', {},
         '<Ranges>(A1)=[[-75.62318600836664]]'),
        ('A1', '=PMT("33","3","33","10000","1")', {},
         '<Ranges>(A1)=[[-32.2771768657085]]'),
        ('A1', '=PMT(0.08/12,0,10000)', {}, '<Ranges>(A1)=[[#NUM!]]'),
        ('A1', '=PMT(0.08/12,10,10000,10000,1)', {},
         '<Ranges>(A1)=[[-1994.1034887930407]]'),
        ('A1', '=PMT(0.08/12,10,10000,,1)', {},
         '<Ranges>(A1)=[[-1030.1643271779772]]'),
        ('A1', '=PMT(0.08/12,10,10000)', {},
         '<Ranges>(A1)=[[-1037.0320893591636]]'),
        ('A1', '=FORECAST(1,A2,{8,2})', {'A2': [[sh.EMPTY]]},
         '<Ranges>(A1)=[[#VALUE!]]'),
        ('A1', '=FORECAST(1,A2:A3,A2:A3)', {'A2:A3': [[sh.EMPTY, sh.EMPTY]]},
         '<Ranges>(A1)=[[#DIV/0!]]'),
        ('A1', '=FORECAST(A2,{3,4},{8,9})', {'A2': [[sh.EMPTY]]},
         '<Ranges>(A1)=[[-5.0]]'),
        ('A1', '=FORECAST(#N/A,{"3"},{9})', {}, '<Ranges>(A1)=[[#N/A]]'),
        ('A1', '=FORECAST(5,{3},{9})', {}, '<Ranges>(A1)=[[#DIV/0!]]'),
        ('A1', '=FORECAST(5,{3},{8,9})', {}, '<Ranges>(A1)=[[#N/A]]'),
        ('A1', '=FORECAST(2,A2:A5,{7,TRUE,8,9})',
         {'A2:A5': [[sh.EMPTY, 4, 3, 4]]}, '<Ranges>(A1)=[[-3.0]]'),
        ('A1', '=FORECAST(2,{"1",4,3,4},{7,TRUE,8,9})', {},
         '<Ranges>(A1)=[[-3.0]]'),
        ('A1', '=FORECAST(2,{"1","4",3,4},{7,4,8,9})', {},
         '<Ranges>(A1)=[[-3.0]]'),
        ('A1', '=FORECAST(5,{"a",2,3}, {7,8,9})', {}, '<Ranges>(A1)=[[-1.0]]'),
        ('A1', '=FORECAST(5,{1,2,3}, {7,8,9})', {}, '<Ranges>(A1)=[[-1.0]]'),
        ('A1', '=SEARCH(5,45)', {}, '<Ranges>(A1)=[[2]]'),
        ('A1', '=SEARCH("n", "printer")', {}, '<Ranges>(A1)=[[4]]'),
        ('A1', '=SEARCH("BASE","database",5.8)', {}, '<Ranges>(A1)=[[5]]'),
        ('A1', '=SEARCH("BASE","database",6.1)', {},
         '<Ranges>(A1)=[[#VALUE!]]'),
        ('A1', '=SEARCH("BASE","database",FALSE)', {},
         '<Ranges>(A1)=[[#VALUE!]]'),
        ('A1', '=SEARCH("BASE","database",TRUE)', {}, '<Ranges>(A1)=[[5]]'),
        ('A1', '=SEARCH("x","database")', {}, '<Ranges>(A1)=[[#VALUE!]]'),
        ('A1', '=EDATE(0, 0)', {}, '<Ranges>(A1)=[[0]]'),
        ('A1', '=EDATE(0.7, "15-Jan-11")', {}, '<Ranges>(A1)=[[1234460]]'),
        ('A1', '=EDATE(2.8, ".7")', {}, '<Ranges>(A1)=[[2]]'),
        ('A1', '=EDATE(2.4, TRUE)', {}, '<Ranges>(A1)=[[#VALUE!]]'),
        ('A1', '=EDATE("15-Jan-11", 1)', {}, '<Ranges>(A1)=[[40589]]'),
        ('A1', '=EDATE(1, "2")', {}, '<Ranges>(A1)=[[61]]'),
        ('A1', '=EDATE(2.4, 1)', {}, '<Ranges>(A1)=[[33]]'),
        ('A1', '=A2 %', {'A2': [[20]]}, '<Ranges>(A1)=[[0.2]]'),
        ('A3', '=SINGLE(F1:F3)', {'F1:F3': [[1], [2], [3]]},
         '<Ranges>(A3)=[[3]]'),
        ('A3', '=COLUMN(SINGLE(F1:F3))', {'F1:F3': [[1], [2], [3]]},
         '<Ranges>(A3)=[[6]]'),
        ('A4', '=COLUMN(SINGLE(F1:F3))', {'F1:F3': [[1], [2], [3]]},
         '<Ranges>(A4)=[[#VALUE!]]'),
        ('A4', '=SINGLE(F1:F3)', {'F1:F3': [[1], [2], [3]]},
         '<Ranges>(A4)=[[#VALUE!]]'),
        ('A1', '=__xludf.DUMMYFUNCTION("(GOOGLEFINANCE($A1,""Name""))")', {},
         "<Ranges>(A1)=[[#NAME?]]"),
        ('A1', '=IFS(-1,A2,1, TRUE)', {'A2': [[sh.EMPTY]]},
         "<Ranges>(A1)=[[0]]"),
        ('A1', '=A2 =A3', {'A2': [[1]], 'A3': [[1]]}, "<Ranges>(A1)=[[True]]"),
        ('A1', '=A2 =-A3', {'A2': [[1]], 'A3': [[-1]]},
         "<Ranges>(A1)=[[True]]"),
        ('A1', '=A2 A3', {'A2': [[1]], 'A3': [[-1]]},
         "<Ranges>(A1)=[[#NULL!]]"),
        ('A1', '="\\n"&SUM(1,2)', {}, "<Ranges>(A1)=[['\\\\n3']]"),
        ('A1', '=SUM("2","4", A2:B2)',
         {'A2:B2': [[True, False]]}, '<Ranges>(A1)=[[6.0]]'),
        ('A1', '=SUM("2","4","ciao")', {}, '<Ranges>(A1)=[[#VALUE!]]'),
        ('A1', '=SUM("2","4")', {}, '<Ranges>(A1)=[[6.0]]'),
        ('A1', '=STDEVPA(B1)',
         {'B1': [[sh.EMPTY]]}, '<Ranges>(A1)=[[#DIV/0!]]'),
        ('A1', '=STDEV.P(B1)',
         {'B1': [[sh.EMPTY]]}, '<Ranges>(A1)=[[#DIV/0!]]'),
        ('A1', '=STDEV.P(1)', {}, '<Ranges>(A1)=[[0.0]]'),
        ('A1', '=STDEV.S(1)', {}, '<Ranges>(A1)=[[#DIV/0!]]'),
        ('A1', '=STDEV.S(1, "a")', {}, '<Ranges>(A1)=[[#VALUE!]]'),
        ('A1', '=STDEV.S(1, "3", 2)', {}, '<Ranges>(A1)=[[1.0]]'),
        ('A1', '=STDEV.P(2, 3)', {}, '<Ranges>(A1)=[[0.5]]'),
        ('A1', '=STDEV.S(1, 2, 3)', {}, '<Ranges>(A1)=[[1.0]]'),
        ('A1', '=CONCAT(1, TRUE, 3)', {}, '<Ranges>(A1)=[[\'1TRUE3\']]'),
        ('A1', '=SUM(B1:D1  (  B1:B2  ,  D1:D2  ))',
         {'B1': 1, 'D1': 1}, '<Ranges>(A1)=[[2.0]]'),
        ('A1', '=LARGE({-1.1,10.1;"40",-2},1.1)', {}, '<Ranges>(A1)=[[-1.1]]'),
        ('A1', '=LARGE(A2:H2,"01/01/1900")', {
            'A2:H2': [[0.1, -10, 0.9, 2.2, -0.1, sh.EMPTY, "02/01/1900", True]]
        }, '<Ranges>(A1)=[[2.2]]'),

        ('A1:B1', '=SMALL(A2:B2,A3:B3)', {
            'A2:B2': [[4, sh.EMPTY]], 'A3:B3': [[1, Error.errors['#N/A']]]
        }, '<Ranges>(A1:B1)=[[4.0 #N/A]]'),
        ('A1', '=SMALL({-1.1,10.1;4.1,"40"},4)', {}, '<Ranges>(A1)=[[#NUM!]]'),
        ('A1', '=SMALL({-1.1,10.1;"40",TRUE},2)', {}, '<Ranges>(A1)=[[10.1]]'),
        ('A1', '=LARGE({-1.1,4.1,#REF!},"c")', {}, '<Ranges>(A1)=[[#VALUE!]]'),
        ('A1', '=LARGE({-1.1,4.1,#REF!},#N/A)', {}, '<Ranges>(A1)=[[#N/A]]'),
        ('A1', '=LARGE({-1.1,10.1;4.1,"40"},4)', {}, '<Ranges>(A1)=[[#NUM!]]'),
        ('A1', '=LARGE({-1.1,10.1;"40",-2},2)', {}, '<Ranges>(A1)=[[-1.1]]'),
        ('A1', '=LOOKUP(2,{-1.1,2.1,3.1,4.1},{#REF!,2.1,3.1,4.1})', {},
         '<Ranges>(A1)=[[#REF!]]'),
        ('A1', '=XIRR({-10000,2750,3250,4250,2},'
               '      {"39448",39508,39859,"30/10/2008", TRUE}, 0)',
         {}, '<Ranges>(A1)=[[#VALUE!]]'),
        ('A1', '=XIRR({-10,1,5,0.0001,4.5},{1,20,4,4,5},"26/08/1987")',
         {}, '<Ranges>(A1)=[[38.321500577844446]]'),
        ('A1', '=XIRR({-10000,2750,3250,4250},'
               '      {"39448",39508,39859,"30/10/2008"}, 0)',
         {}, '<Ranges>(A1)=[[0.03379137764398378]]'),
        ('A1', '=XIRR({-10,1,1,2,3},{3,6,7,4,9})',
         {}, '<Ranges>(A1)=[[#NUM!]]'),
        ('A1', '=XIRR({-10,1,1,2,7},{3,6,7,4,9})', {},
         '<Ranges>(A1)=[[1937.5566679300437]]'),
        ('A1', '=XIRR({-10000,2750,3250,4250},{39448,39508,39859,39751}, 1)',
         {}, '<Ranges>(A1)=[[0.03379137764432629]]'),
        ('A1', '=IRR({-7,2,-1,4,-3;7,2,-1,4,4},1)', {},
         '<Ranges>(A1)=[[0.19086464188385843]]'),
        ('A1', '=IRR({2,0,4},A2)',
         {'A2': [[sh.EMPTY]]}, '<Ranges>(A1)=[[#NUM!]]'),
        ('A1', '=IRR({7,2,-1,4,-3;7,2,-1,4,4},A2)',
         {'A2': [[3]]}, '<Ranges>(A1)=[[#NUM!]]'),
        ('A1', '=XNPV(0.02,{-10000,2750,3250,4250},{39448,39508,39859,39751})',
         {}, '<Ranges>(A1)=[[100.10102845727761]]'),
        ('A1', '=XNPV(0.02,{-10000,2750,3250,4250},{0,39508,39859,39751})',
         {}, '<Ranges>(A1)=[[#NUM!]]'),
        ('A1', '=NPV(1, A3:C3)', {'A3:C3': [[5, 4, 3]]},
         '<Ranges>(A1)=[[3.875]]'),
        ('A1', '=NPV(D2, A2:C2)',
         {'D2': [["ciao"]], 'A2:C2': [[5, sh.EMPTY, Error.errors['#N/A']]]},
         '<Ranges>(A1)=[[#VALUE!]]'),
        ('A1', '=NPV(5, A2:D2)',
         {'A2:D2': [[5, sh.EMPTY, 'ciao', Error.errors['#N/A']]]},
         '<Ranges>(A1)=[[#N/A]]'),
        ('A1', '=NPV(-0.1, {-0.1,2,0,4,5})', {},
         '<Ranges>(A1)=[[16.922200206608068]]'),
        ('A1', '=COUNT(0,345,TRUE,#VALUE!,"26/08")', {}, '<Ranges>(A1)=[[4]]'),
        ('A1', '=MAX("")', {}, '<Ranges>(A1)=[[#VALUE!]]'),
        ('A1', '=MAXA("")', {}, '<Ranges>(A1)=[[#VALUE!]]'),
        ('A1', '=COUNTIF(A2:B2, "<>-1")', {'A2:B2': [[-1, 2]]},
         '<Ranges>(A1)=[[1]]'),
        ('A1', '=COUNTA(A2)', {'A2': [[sh.EMPTY]]}, '<Ranges>(A1)=[[0]]'),
        ('A1:C1', '=COUNTIF(A2:F2,{"60","29/02/1900","*0"})',
         {'A2:F2': [[60, "29/02/1900", sh.EMPTY, 0, "*", "AUG-98"]]},
         '<Ranges>(A1:C1)=[[2 2 1]]'),
        ('A1:G1', '=COUNTIF(A2:E2,{"<=FALSE",0,"",#VALUE!,"~*",FALSE})',
         {'A2:E2': [[sh.EMPTY, 0, Error.errors['#VALUE!'], "*", False]]},
         '<Ranges>(A1:G1)=[[1 1 1 1 1 1 #N/A]]'),
        ('A1', '=MAX("29/02/1900")', {}, '<Ranges>(A1)=[[60.0]]'),
        ('A1', '=COUNT(A2:E2,"26/08")',
         {'A2:E2': [[0, 345, True, Error.errors['#VALUE!'], "26/08"]]},
         '<Ranges>(A1)=[[3]]'),
        ('A1:G1', '=SUMIF(A2:E2,{"<=FALSE",0,"",#VALUE!,"~*",FALSE},A3:E3)',
         {'A2:E2': [[sh.EMPTY, 0, Error.errors['#VALUE!'], "*", False]],
          'A3:E3': [[11, 7, 5, 9, 2]]},
         '<Ranges>(A1:G1)=[[2.0 7.0 11.0 5.0 9.0 2.0 #N/A]]'),
        ('A1:C1', '=SUMIF(A2:F2,{"60","29/02/1900","*0"},A3:F3)',
         {'A2:F2': [[60, "29/02/1900", sh.EMPTY, 0, "*", "AUG-98"]],
          'A3:F3': [[1, 3, 11, 7, 9, 13]]},
         '<Ranges>(A1:C1)=[[4.0 4.0 3.0]]'),
        ('A1', '=YEARFRAC(0,345,TRUE)', {}, '<Ranges>(A1)=[[#VALUE!]]'),
        ('A1', '=YEARFRAC("26/8/1987 05:00 AM",345,4)', {},
         '<Ranges>(A1)=[[86.71111111111111]]'),
        ('A1', '=YEARFRAC("26/8/1987 05:00 AM",345,1)', {},
         '<Ranges>(A1)=[[86.71043215830248]]'),
        ('A1', '=YEARFRAC(2,1462,1)', {},
         '<Ranges>(A1)=[[3.9978094194961664]]'),
        ('A1', '=YEARFRAC(0,4382,1)', {}, '<Ranges>(A1)=[[12.0]]'),
        ('A1', '=YEARFRAC(1462,4382,1)', {},
         '<Ranges>(A1)=[[7.994524298425736]]'),
        ('A1', '=YEARFRAC(1462,4383,1)', {},
         '<Ranges>(A1)=[[7.997262149212868]]'),
        ('A1', '=YEARFRAC(3,368,1)', {}, '<Ranges>(A1)=[[1.0]]'),
        ('A1', '=YEARFRAC(366,2000,1)', {},
         '<Ranges>(A1)=[[4.4746691008671835]]'),
        ('A1', '=YEARFRAC(1,6000,1)', {}, '<Ranges>(A1)=[[16.4250281848929]]'),
        ('A1', '=YEARFRAC(1,2000,1)', {}, '<Ranges>(A1)=[[5.474212688270196]]'),
        ('A1', '=YEARFRAC(1,2000,0)', {}, '<Ranges>(A1)=[[5.475]]'),
        ('A1', '=YEARFRAC(1,2000,2)', {}, '<Ranges>(A1)=[[5.552777777777778]]'),
        ('A1', '=YEARFRAC(1,2000,3)', {}, '<Ranges>(A1)=[[5.476712328767123]]'),
        ('A1', '=YEARFRAC(1,2000,4)', {}, '<Ranges>(A1)=[[5.475]]'),
        ('A1', '=HOUR(-1)', {}, '<Ranges>(A1)=[[#NUM!]]'),
        ('A1', '=HOUR(0.4006770833)', {}, '<Ranges>(A1)=[[9]]'),
        ('A1', '=MINUTE(2.4)', {}, '<Ranges>(A1)=[[36]]'),
        ('A1', '=MINUTE(0.4006770833)', {}, '<Ranges>(A1)=[[36]]'),
        ('A1', '=SECOND(0.4006770833)', {}, '<Ranges>(A1)=[[58]]'),
        ('A1', '=SECOND(0.4006770834)', {}, '<Ranges>(A1)=[[59]]'),
        ('A1', '=SECOND(0.4)', {}, '<Ranges>(A1)=[[0]]'),
        ('A1', '=SECOND("22-Aug-2011 9:36 AM")', {}, '<Ranges>(A1)=[[0]]'),
        ('A1', '=TIMEVALUE("22-Aug-2011 9:36 AM")', {}, '<Ranges>(A1)=[[0.4]]'),
        ('A1', '=TIMEVALUE("9:36 AM")', {}, '<Ranges>(A1)=[[0.4]]'),
        ('A1', '=DAY(0)', {}, '<Ranges>(A1)=[[0]]'),
        ('A1', '=MONTH(0.7)', {}, '<Ranges>(A1)=[[1]]'),
        ('A1', '=TIME(24,0,0)', {}, '<Ranges>(A1)=[[0.0]]'),
        ('A1', '=TIME(36,12*60,6*60*60)', {}, '<Ranges>(A1)=[[0.25]]'),
        ('A1', '=TIME(36,0,6*60*60)', {}, '<Ranges>(A1)=[[0.75]]'),
        ('A1', '=TIME(12,0,6*60*60)', {}, '<Ranges>(A1)=[[0.75]]'),
        ('A1', '=TIME(0,0,6*60*60)', {}, '<Ranges>(A1)=[[0.25]]'),
        ('A1', '=DAY(2958466)', {}, '<Ranges>(A1)=[[#NUM!]]'),
        ('A1', '=DAY(60)', {}, '<Ranges>(A1)=[[29]]'),
        ('A1', '=DAY(50)', {}, '<Ranges>(A1)=[[19]]'),
        ('A1', '=DAY(100)', {}, '<Ranges>(A1)=[[9]]'),
        ('A1', '=DAY("29/2/1900")', {}, '<Ranges>(A1)=[[29]]'),
        ('A1', '=DAY("22 August 20")', {}, '<Ranges>(A1)=[[22]]'),
        ('A1', '=DATEVALUE("22 August 20")', {}, '<Ranges>(A1)=[[44065]]'),
        ('A1', '=DATEVALUE("01/01/00")', {}, '<Ranges>(A1)=[[36526]]'),
        ('A1', '=DATEVALUE("01/01/99")', {}, '<Ranges>(A1)=[[36161]]'),
        ('A1', '=DATEVALUE("01/01/29")', {}, '<Ranges>(A1)=[[47119]]'),
        ('A1', '=DATEVALUE("01/01/30")', {}, '<Ranges>(A1)=[[10959]]'),
        ('A1', '=DATEVALUE("8/22/2011")', {}, '<Ranges>(A1)=[[40777]]'),
        ('A1', '=DATEVALUE("22-MAY-2011")', {}, '<Ranges>(A1)=[[40685]]'),
        ('A1', '=DATEVALUE("2011/02/23")', {}, '<Ranges>(A1)=[[40597]]'),
        ('A1', '=DATEVALUE("5-JUL")', {}, '<Ranges>(A1)=[[43651]]'),
        ('A1', '=DATEVALUE("8/1987")', {}, '<Ranges>(A1)=[[31990]]'),
        ('A1', '=DATEVALUE("26/8/1987")', {}, '<Ranges>(A1)=[[32015]]'),
        ('A1', '=DATEVALUE("29/2/1900")', {}, '<Ranges>(A1)=[[60]]'),
        ('A1', '=DATE(1900,3,"")', {}, '<Ranges>(A1)=[[#VALUE!]]'),
        ('A1', '=DATE(1900,3,"-1")', {}, '<Ranges>(A1)=[[59]]'),
        ('A1', '=DATE(1900,3,-1)', {}, '<Ranges>(A1)=[[59]]'),
        ('A1', '=DATE(1900,3,0)', {}, '<Ranges>(A1)=[[60]]'),
        ('A1', '=DATE(9999,12,32)', {}, '<Ranges>(A1)=[[#NUM!]]'),
        ('A1', '=DATE(9999,12,31)', {}, '<Ranges>(A1)=[[2958465]]'),
        ('A1', '=DATE(-1,2,29)', {}, '<Ranges>(A1)=[[#NUM!]]'),
        ('A1', '=DATE(1899,2,29)', {}, '<Ranges>(A1)=[[693657]]'),
        ('A1', '=DATE(1900,1,0)', {}, '<Ranges>(A1)=[[0]]'),
        ('A1', '=DATE(1900,0,0)', {}, '<Ranges>(A1)=[[#NUM!]]'),
        ('A1', '=DATE(1900,2,28)', {}, '<Ranges>(A1)=[[59]]'),
        ('A1', '=DATE(1900,2,29)', {}, '<Ranges>(A1)=[[60]]'),
        ('A1', '=DATE(1904,2,29)', {}, '<Ranges>(A1)=[[1521]]'),
        ('A1', '=DATE(0,11.9,-40.1)', {}, '<Ranges>(A1)=[[264]]'),
        ('A1', '=DATE(0,11.4,1.9)', {}, '<Ranges>(A1)=[[306]]'),
        ('A1', '=DATE(0,11,0)', {}, '<Ranges>(A1)=[[305]]'),
        ('A1', '=DATE(1,-1.9,1.1)', {}, '<Ranges>(A1)=[[275]]'),
        ('A1', '=DATE(1,-1,0)', {}, '<Ranges>(A1)=[[305]]'),
        ('A1', '=DATE(0,0,0)', {}, '<Ranges>(A1)=[[#NUM!]]'),
        ('A1', '=DATE(2020,2,29)', {}, '<Ranges>(A1)=[[43890]]'),
        ('A1', '=OR({0,0,0},FALSE,"0")', {}, '<Ranges>(A1)=[[#VALUE!]]'),
        ('A1', '=OR(B1,FALSE)', {'B1': [['0']]}, '<Ranges>(A1)=[[False]]'),
        ('A1', '=OR("0",FALSE)', {'B1': [['0']]}, '<Ranges>(A1)=[[#VALUE!]]'),
        ('A1', '=XOR({0,0,0},FALSE,FALSE)', {}, '<Ranges>(A1)=[[False]]'),
        ('A1', '=XOR({0,0},FALSE,FALSE)', {}, '<Ranges>(A1)=[[False]]'),
        ('A1', '=XOR(TRUE,TRUE)', {}, '<Ranges>(A1)=[[False]]'),
        ('A1', '=XOR(TRUE(),TRUE())', {}, '<Ranges>(A1)=[[False]]'),
        ('A1', '=OR(TRUE,#REF!,"0")', {}, '<Ranges>(A1)=[[#REF!]]'),
        ('A1', '=OR(FALSE,"0",#REF!)', {}, '<Ranges>(A1)=[[#VALUE!]]'),
        ('A1', '=INDEX({2,3;4,5},FALSE,"0")', {}, '<Ranges>(A1)=[[2]]'),
        ('A1', '=INDEX({2,3;4,5}, -1)', {}, '<Ranges>(A1)=[[#VALUE!]]'),
        ('A1', '=INDEX(B1:C1, 1, 1)', {'B1:C1': [[sh.EMPTY, 2]]},
         '<Ranges>(A1)=[[0]]'),
        ('A1', '=INDEX(B1:C2, -1)', {'B1:C2': [[1, 2], [3, 4]]},
         '<Ranges>(A1)=[[#VALUE!]]'),
        ('A1', '=SUM(B1:D1 (B1:D1,B1:C1))',
         {'B1:D1': [[2, 3, 4]], 'B1:C1': [[2, 3]]}, '<Ranges>(A1)=[[14.0]]'),
        ('A1', '=INDEX(B1:D2 (B1:C1,B2:C2), 1, 1, 2)',
         {'B1:C1': [[2, 3]], 'B2:C2': [[4, 5]]}, '<Ranges>(A1)=[[4]]'),
        ('A1', '=INDEX((D1:D2:B1:C1, B2:C2), 1, 1, 2)',
         {'B1:D2': [[2, 3, 6], [4, 5, 7]], 'B2:C2': [[4, 5]]},
         '<Ranges>(A1)=[[4]]'),
        ('A1', '=INDEX({2,3;4,5},#NAME?)', {}, '<Ranges>(A1)=[[#NAME?]]'),
        ('A1:B2', '=INDEX({2,3;4,5},{1,2})', {},
         '<Ranges>(A1:B2)=[[2 4]\n [2 4]]'),
        ('A1', '=INDEX(C1:D2,1)', {'C1:D2': [[2, 3], [4, 5]]},
         '<Ranges>(A1)=[[#REF!]]'),
        ('A1:B1', '=INDEX(C1:D1,1)', {'C1:D1': [2, 3]},
         '<Ranges>(A1:B1)=[[2 2]]'),
        ('A1:B1', '=INDEX({2,3;4,5},1)', {}, '<Ranges>(A1:B1)=[[2 3]]'),
        ('A1', '=INDEX({2,3;4,5},1)', {}, '<Ranges>(A1)=[[2]]'),
        ('A1', '=INDEX({2,3,4},1,1)', {}, '<Ranges>(A1)=[[2]]'),
        ('A1', '=INDEX({2,3,4},2,1)', {}, '<Ranges>(A1)=[[#REF!]]'),
        ('A1', '=INDEX({2,3,4},2)', {}, '<Ranges>(A1)=[[3]]'),
        ('A1', '=LOOKUP(2,{-1.1,2.1,3.1,4.1})', {}, '<Ranges>(A1)=[[-1.1]]'),
        ('A1', '=LOOKUP(3,{-1.1,2.1,3.1,4.1})', {}, '<Ranges>(A1)=[[2.1]]'),
        ('A1', '=SWITCH(TRUE,1,0,,,TRUE,1,7)', {}, '<Ranges>(A1)=[[1]]'),
        ('A1:D1', '=SWITCH({0,1,TRUE},1,0,,,TRUE,1,7)', {},
         '<Ranges>(A1:D1)=[[0 0 1 #N/A]]'),
        ('A1', '=SWITCH(1,2,0,1,4,,4,5)', {}, '<Ranges>(A1)=[[4]]'),
        ('A1', '=GCD(5.2, -1, TRUE)', {}, '<Ranges>(A1)=[[#VALUE!]]'),
        ('A1', '=GCD(5.2, -1)', {}, '<Ranges>(A1)=[[#NUM!]]'),
        ('A1', '=GCD(5.2, 10)', {}, '<Ranges>(A1)=[[5]]'),
        ('A1', '=GCD(#NAME?, #VALUE!, #N/A)', {}, '<Ranges>(A1)=[[#NAME?]]'),
        ('A1', '=GCD(55, 15, 5)', {}, '<Ranges>(A1)=[[5]]'),
        ('A1', '=5%', {}, '<Ranges>(A1)=[[0.05]]'),
        ('A1', '=IF(#NAME?, #VALUE!, #N/A)', {}, '<Ranges>(A1)=[[#NAME?]]'),
        ('A1', '=IF(TRUE, #VALUE!, #N/A)', {}, '<Ranges>(A1)=[[#VALUE!]]'),
        ('A1', '=IF(FALSE, #VALUE!, #N/A)', {}, '<Ranges>(A1)=[[#N/A]]'),
        ('A1', '=IF(TRUE, "1a", "2b")', {}, '<Ranges>(A1)=[[\'1a\']]'),
        ('A1', '=IFS(TRUE, "FIRST")', {}, '<Ranges>(A1)=[[\'FIRST\']]'),
        ('A1', '=IFS(FALSE, "FIRST", TRUE, "SECOND")', {},
         '<Ranges>(A1)=[[\'SECOND\']]'),
        ('A1', '=IFS(FALSE, "FIRST", FALSE, "SECOND", TRUE, "THIRD")', {},
         '<Ranges>(A1)=[[\'THIRD\']]'),
        ('A1', '=IFS(FALSE, "FIRST", FALSE, "SECOND", TRUE,)', {},
         '<Ranges>(A1)=[[0]]'),
        ('A1', '=IFS(FALSE, "FIRST", FALSE, "SECOND")', {},
         '<Ranges>(A1)=[[#N/A]]'),
        ('A1', '=ROW(4:7)', inp_ranges('4:7'), '<Ranges>(A1)=[[4]]'),
        ('A1', '=ROW(B8:D8:F7:H8 D7:E8)',
         inp_ranges('B8:D8', 'F7:H8', 'D7:E8'), '<Ranges>(A1)=[[7]]'),
        ('A1', '=COLUMN(B8:D8:F7:H8 D7:E7)',
         inp_ranges('B8:D8', 'F7:H8', 'D7:E7'), '<Ranges>(A1)=[[4]]'),
        ('A1', '=COLUMN((B8:D8:F7:H8) D7:E7)',
         inp_ranges('B8:D8', 'F7:H8', 'D7:E7'), '<Ranges>(A1)=[[4]]'),
        ('A1:C3', '=ROW(D1:E1)', inp_ranges('D1:E1'),
         '<Ranges>(A1:C3)=[[1 1 1]\n [1 1 1]\n [1 1 1]]'),
        ('A1:C3', '=ROW(D1:D2)', inp_ranges('D1:D2'),
         '<Ranges>(A1:C3)=[[1 1 1]\n [2 2 2]\n [#N/A #N/A #N/A]]'),
        ('A1:C3', '=ROW(D1:E2)', inp_ranges('D1:E2'),
         '<Ranges>(A1:C3)=[[1 1 1]\n [2 2 2]\n [#N/A #N/A #N/A]]'),
        ('A11', '=ROW(B55:D55:F54:H55 D54:E54)',
         inp_ranges('B55:D55', 'F54:H55', 'D54:E54'), '<Ranges>(A11)=[[54]]'),
        ('A11', '=ROW(B53:D54 C54:E54)', inp_ranges('B53:D54', 'C54:E54'),
         '<Ranges>(A11)=[[54]]'),
        ('A11', '=ROW(L45)', inp_ranges('L45'), '<Ranges>(A11)=[[45]]'),
        ('A11', '=ROW()', {}, '<Ranges>(A11)=[[11]]'),
        ('A1', '=REF', {}, "<Ranges>(A1)=[[#REF!]]"),
        ('A1', '=(-INT(2))', {}, '<Ranges>(A1)=[[-2.0]]'),
        ('A1', '=(1+1)+(1+1)', {}, '<Ranges>(A1)=[[4.0]]'),
        ('A1', '=IFERROR(INDIRECT("aa") * 100,"")', {}, "<Ranges>(A1)=[['']]"),
        ('A1', '=( 1 + 2 + 3)*(4 + 5)^(1/5)', {},
         '<Ranges>(A1)=[[9.311073443492159]]'),
        ('A1', '={1,2;1,2}', {}, '<Ranges>(A1)=[[1]]'),
        ('A1:B2', '={1,2;1,2}', {}, '<Ranges>(A1:B2)=[[1 2]\n [1 2]]'),
        ('A1', '=PI()', {}, '<Ranges>(A1)=[[3.141592653589793]]'),
        ('A1', '=INT(1)%+3', {}, '<Ranges>(A1)=[[3.01]]'),
        ('A1', '=SUM({1, 3; 4, 2})', {}, '<Ranges>(A1)=[[10.0]]'),
        ('A1', '=" "" a"', {}, '<Ranges>(A1)=[[\' " a\']]'),
        ('A1', '=#NULL!', {}, "<Ranges>(A1)=[[#NULL!]]"),
        ('A1', '=1 + 2', {}, '<Ranges>(A1)=[[3.0]]'),
        ('A1', '=AVERAGE(((123 + 4 + AVERAGE({1,2}))))', {},
         '<Ranges>(A1)=[[128.5]]'),
        ('A1', '="a" & "b"""', {}, '<Ranges>(A1)=[[\'ab"\']]'),
        ('A1', '=SUM(B2:B4)',
         {'B2:B4': (sh.EMPTY, sh.EMPTY, sh.EMPTY)}, '<Ranges>(A1)=[[0]]'),
        ('A1', '=SUM(B2:B4)',
         {'B2:B4': (sh.EMPTY, 1, sh.EMPTY)}, '<Ranges>(A1)=[[1.0]]'),
        ('A1', '=MATCH("*b?u*",{"a",2.1,"ds  bau  dsd",4.1},0)', {},
         '<Ranges>(A1)=[[3]]'),
        ('A1', '=MATCH(4.1,{FALSE,2.1,TRUE,4.1},-1)', {},
         '<Ranges>(A1)=[[#N/A]]'),
        ('A1', '=HLOOKUP(-1.1,{-1.1,2.1,3.1,4.1;5,6,7,8},2,0)', {},
         '<Ranges>(A1)=[[5]]'),
        ('A1', '=HLOOKUP(-1.1,{-1.1,2.1,3.1,4.1;5,6,7,8},3,0)', {},
         '<Ranges>(A1)=[[#REF!]]'),
        ('A1', '=MATCH(1.1,{"b",4.1,"a",1.1})', {}, '<Ranges>(A1)=[[#N/A]]'),
        ('A1', '=MATCH(1.1,{4.1,2.1,3.1,1.1})', {}, '<Ranges>(A1)=[[#N/A]]'),
        ('A1', '=MATCH(4.1,{4.1,"b","a",1.1})', {}, '<Ranges>(A1)=[[4]]'),
        ('A1', '=MATCH(4.1,{"b",4.1,"a",1.1})', {}, '<Ranges>(A1)=[[2]]'),
        ('A1', '=MATCH(4.1,{4.1,"b","a",5.1},-1)', {}, '<Ranges>(A1)=[[1]]'),
        ('A1', '=MATCH(4.1,{"b",4.1,"a",5.1},-1)', {}, '<Ranges>(A1)=[[2]]'),
        ('A1', '=MATCH("b",{"b",4.1,"a",1.1})', {}, '<Ranges>(A1)=[[3]]'),
        ('A1', '=MATCH(3,{-1.1,2.1,3.1,4.1})', {}, '<Ranges>(A1)=[[2]]'),
        ('A1', '=MATCH(-1.1,{"b",4.1,"a",1.1})', {}, '<Ranges>(A1)=[[#N/A]]'),
        ('A1', '=MATCH(-1.1,{4.1,2.1,3.1,1.1},-1)', {}, '<Ranges>(A1)=[[4]]'),
        ('A1', '=MATCH(-1.1,{-1.1,2.1,3.1,4.1})', {}, '<Ranges>(A1)=[[1]]'),
        ('A1', '=MATCH(2.1,{4.1,2.1,3.1,1.1})', {}, '<Ranges>(A1)=[[2]]'),
        ('A1', '=MATCH(2.1,{4.1,2.1,3.1,1.1},-1)', {}, '<Ranges>(A1)=[[2]]'),
        ('A1', '=MATCH(2,{4.1,2.1,3.1,1.1},-1)', {}, '<Ranges>(A1)=[[3]]'),
        ('A1', '=LOOKUP(2.1,{4.1,2.1,3.1,1.1},{"L","ML","MR","R"})', {},
         '<Ranges>(A1)=[[\'ML\']]'),
        ('A1', '=LOOKUP("b",{"b",4.1,"a",1.1},{"L","ML","MR","R"})', {},
         '<Ranges>(A1)=[[\'MR\']]'),
        ('A1', '=LOOKUP(TRUE,{TRUE,4.1,FALSE,1.1},{"L","ML","MR","R"})', {},
         '<Ranges>(A1)=[[\'MR\']]'),
        ('A1', '=LOOKUP(4.1,{"b",4.1,"a",1.1},{"L","ML","MR","R"})', {},
         '<Ranges>(A1)=[[\'ML\']]'),
        ('A1', '=LOOKUP(2,{"b",4.1,"a",1.1},{"L","ML","MR","R"})', {},
         '<Ranges>(A1)=[[#N/A]]'),
        ('A1', '=LOOKUP(4.1,{4.1,2.1,3.1,1.1},{"L","ML","MR","R"})', {},
         '<Ranges>(A1)=[[\'R\']]'),
        ('A1', '=LOOKUP(4,{4.1,2.1,3.1,1.1},{"L","ML","MR","R"})', {},
         '<Ranges>(A1)=[[\'R\']]'),
        ('A1:D1', '=IF({0,-0.2,0},2,{1})', {},
         '<Ranges>(A1:D1)=[[1 2 1 #N/A]]'),
        ('A1', '=HEX2DEC(9999999999)', {}, '<Ranges>(A1)=[[-439804651111]]'),
        ('A1', '=HEX2BIN(9999999999)', {}, '<Ranges>(A1)=[[#NUM!]]'),
        ('A1', '=HEX2BIN("FFFFFFFE00")', {}, '<Ranges>(A1)=[[\'1000000000\']]'),
        ('A1', '=HEX2BIN("1ff")', {}, '<Ranges>(A1)=[[\'111111111\']]'),
        ('A1', '=HEX2OCT("FF0000000")', {}, '<Ranges>(A1)=[[#NUM!]]'),
        ('A1', '=HEX2OCT("FFE0000000")', {}, '<Ranges>(A1)=[[\'4000000000\']]'),
        ('A1', '=HEX2OCT("1FFFFFFF")', {}, '<Ranges>(A1)=[[\'3777777777\']]'),
        ('A1', '=DEC2HEX(-439804651111)', {},
         '<Ranges>(A1)=[[\'9999999999\']]'),
        ('A1', '=DEC2BIN(TRUE)', {}, '<Ranges>(A1)=[[#VALUE!]]'),
        ('A1', '=DEC2BIN(#DIV/0!)', {}, '<Ranges>(A1)=[[#DIV/0!]]'),
        ('A1', '=DEC2BIN("a")', {}, '<Ranges>(A1)=[[#VALUE!]]'),
        ('A1', '=DEC2BIN(4,6)', {}, '<Ranges>(A1)=[[\'000100\']]'),
        ('A1', '=DEC2BIN(4,-2)', {}, '<Ranges>(A1)=[[#NUM!]]'),
        ('A1', '=DEC2BIN(4,"a")', {}, '<Ranges>(A1)=[[#VALUE!]]'),
        ('A1', '=ROUND(2.5,0)', {}, '<Ranges>(A1)=[[3.0]]'),
        ('A1', '=ROUND(2.35,1)', {}, '<Ranges>(A1)=[[2.4]]'),
        ('A1', '=TRUE()', {}, '<Ranges>(A1)=[[True]]'),
        ('A1', '=FALSE()', {}, '<Ranges>(A1)=[[False]]'),
        ('A1', '=CONCAT("con", "cat", "enate")', {},
         '<Ranges>(A1)=[[\'concatenate\']]'),
        ('A1', '=CONCAT(A2:E2)', {
            'A2:E2': [["h", "e", "l", "l", 0.15]]
        }, '<Ranges>(A1)=[[\'hell0.15\']]'),
        ('A1', '=CONCAT(A2:E2, A3:E3, "curl")', {
            'A2:E2': [["h", "e", "l", "l", "o"]],
            'A3:E3': [["h", "e", "l", "l", "o"]]
        }, '<Ranges>(A1)=[[\'hellohellocurl\']]'),
        # ('A1:D1', '=IF({0,-0.2,0},{2,3},{1})', {},
        #  '<Ranges>(A1:D1)=[[1 2 1 #N/A]]'),
        # ('A1:D1', '=IF({0,-2,0},{2,3},{1,4})', {},
        #  '<Ranges>(A1:D1)=[[1 2 #N/A #N/A]]')
    ])
    def test_output(self, case):
        reference, formula, inputs, result = case
        dsp = sh.Dispatcher()
        cell = Cell(reference, formula).compile()
        assert cell.add(dsp)
        output = str(dsp(inputs)[cell.output])
        self.assertEqual(
            result, output,
            'Formula({}): {} != {}'.format(formula, result, output)
        )

    @ddt.idata([
        ('A1:D1', '=IF({0,-0.2,0},{2,3},{1})', {}),  # BroadcastError
        ('A1:D1', '=IF({0,-2,0},{2,3},{1,4})', {}),  # BroadcastError
    ])
    def test_invalid(self, case):
        reference, formula, inputs = case
        with self.assertRaises(sh.DispatcherError):
            dsp = sh.Dispatcher(raises=True)
            cell = Cell(reference, formula).compile()
            assert cell.add(dsp)
            dsp(inputs)

    @ddt.idata([
        ('A1', '=NOW()', 1),
        ('A1', '=RAND()', 0),
        # ('A1', '=TODAY()'),
    ])
    def test_impure(self, case):
        reference, formula, dt = case
        dsp = sh.Dispatcher()
        cell = Cell(reference, formula).compile()
        assert cell.add(dsp)
        out = str(dsp()[cell.output])
        time.sleep(dt)
        self.assertNotEqual(out, str(dsp()[cell.output]))
