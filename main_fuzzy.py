#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 15 13:51:09 2021

@author: ipromo
"""


from FuzzySystem import FuzzySystem
from FuzzySystem import VariableInput
from FuzzySystem import FuzzyRule


# Fuzzy System configuration
SIn=[0.1, 1, 0.5]


## Fuzzy System CONFIGURATION  
FS = FuzzySystem()
FS.def_type('MISO')

########## add input variables
x1 = VariableInput(0, 'SI_varLow') 
x2 = VariableInput(1, 'SI_varXPTO')
x3 = VariableInput(3, 'SI_varMed') 

FS.add_input_variable( x1 )
FS.add_input_variable( x2 )
FS.add_input_variable( x3 )

print(FS)

# add values to input variables
x1.value = SIn[0]
x2.value = SIn[1]
x3.value = SIn[2]

print(FS)

rule = FuzzyRule()
rule.add_antecedent( x1 )
rule.add_antecedent( x2 )
rule.add_consequents( 0.0 )

#print(rule)

FS.add_rule( rule )

rule = FuzzyRule()
rule.add_antecedent( x1 )
rule.add_antecedent( x3 )
rule.add_consequents( 1.0 )

#print(rule)

FS.add_rule( rule )

print(FS)

out = FS.get_FS_simple_ouput()

######################################################
FS2 = FuzzySystem()
FS2.def_type('MIMO')
FS2.add_input_variable( x1 )
FS2.add_input_variable( x2 )
FS2.add_input_variable( x3 )


rule = FuzzyRule()
rule.add_antecedent( x1 )
rule.add_antecedent( x2 )
rule.add_consequents( 1.0 )
rule.add_consequents( 2.0 )
rule.add_consequents( 2.0 )

rule2 = FuzzyRule()
rule2.add_antecedent( x1 )
rule2.add_antecedent( x3 )
rule2.add_consequents( 3.0 )
rule2.add_consequents( 4.0 )
rule2.add_consequents( 4.0 )

#print(rule)

FS2.add_rule( rule )
FS2.add_rule( rule2 )

print(FS2)

#out2 = FS2.get_FS_multi_ouput()