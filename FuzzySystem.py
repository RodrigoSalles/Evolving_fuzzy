#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 15 09:10:19 2021

@author: ipromo
"""
import numpy as np

class VariableInput:
    def __init__(self, var, name):
        self.var = var # database column
        self.name = name # variable name
        self.value = -1.0
        
            # prints the column and threshold of the variable
    def __str__(self): 
        print("I am variable ", self.var, "and my name is ", self.name)
     
    def get_variable_input_value(self):

        return self.value   
        
class FuzzyRule():

    def __init__(self):
        self._antecedents = []
        self._consequents = []
        self._rule_strength = 0.0
        
    def __str__(self):

        ret_str = 'Rule: \n  IF '
        
        for p in range(0,len(self._antecedents)):
            s = self._antecedents[p].name
            ret_str = ret_str + f'{s}'
            if len(self._antecedents) -1 > p :
                ret_str = ret_str + ' AND '
            
        ret_str = ret_str + ' THEN output is '
            
        for p in range(0,len(self._consequents)):
            v = self._consequents[p]
            ret_str = ret_str + f'{v}\n'

        return ret_str

    def add_antecedent(self, input_var):
        self._antecedents.append(input_var)

    def add_consequents(self, value):
        self._consequents = np.append(self._consequents,value)

    def get_rule_antecedent_value(self):

        aux = 1.0

        for ant in self._antecedents:
            aux *= ant.value

        self._rule_strength = aux
        
        return self._rule_strength
    
    
    def get_rule_consequent_value(self):

        return self._consequents
        
class FuzzySystem:

    def __init__(self):
        '''
        Initializes the Fuzzy System:
            input variables -- dict, having format {variable_name: FuzzyVariable, ...}
            output variables -- dict, having format {variable_name: FuzzyVariable, ...}
            rules -- list of FuzzyRule
        '''
        self._input_variables = []
        self._type = {} # SISO; MISO, MIMO
        self._rules = []
        self._phi = []
        self._ouput = 0.0

    def __str__(self):
        ret_str = 'Inputs: \n'
        
        for j in range(0,len(self._input_variables)):
            s = self._input_variables[j].name
            v = self._input_variables[j].value
            ret_str = ret_str + f'var {j}: {s} [{v}]\n'
            
        ret_str = ret_str + '\n'   

        for i in range(0,len(self._rules)):
            
            ret_str = ret_str + f'Rule {i+1}: IF '
           
            for p in range(0,len(self._rules[i]._antecedents)):
                s = self._rules[i]._antecedents[p].name
                ret_str = ret_str + f'{s}'
                
                if len(self._rules[i]._antecedents) -1 > p :
                    ret_str = ret_str + ' AND '
            
            ret_str = ret_str + ' THEN output is '
            
            for p in range(0,len(self._rules[i]._consequents)):
                v = self._rules[i]._consequents[p]
                ret_str = ret_str + f'{v}\n'

        return ret_str

    def def_type(self, FS_type):
        
        while True:
            if FS_type.lower() not in ('siso','miso','mimo'):
                try:    
                    FS_type = str(input("Enter Fuzzy type (SISO, MISO, MIMO):  "))
                except ValueError:
                        print("Really!! must be SISO, MISO, or MIMO")  
                        continue
                if FS_type.lower() not in ('siso','miso','mimo'):
                    print("Really!! must be SISO, MISO, or MIMO")  
                    continue
                else:
                  
                    break
            else:
                  
                break

        self._type = FS_type.lower() 
        
    def get_type(self):
        return self._type
        
        
    def add_input_variable(self, variable):
        self._input_variables.append(variable)
        
    def add_input_variable_value(self, var, data_value):
        self._input_variables[var].value = data_value
        
    def get_number_inputs(self):
        return len(self._input_variables)

    def get_input_variables_name(self, var):
        return self._input_variables[var].name
    
    def get_input_variables_value(self, var):
        return self._input_variables[var].value
    
    def get_Phi(self):
        return self._phi
    
    def add_rule(self, new_rule):
        self._rules.append(new_rule)
 
    def get_FS_simple_ouput(self):
        
        if self._type not in ('siso','miso'):
             
            print('The method get_FS_simple_ouput() is just for SISO or MISO Fuzzy Systems!!')
        else:
            aux = 0.0
            phi_aux = [];
            theta = []
            
            for i in range(0,len(self._rules)):
                phi_aux.append(self._rules[i].get_rule_antecedent_value())
                aux = aux +  phi_aux[i]
                theta = np.append(theta,self._rules[i].get_rule_consequent_value()) 
                
            self._phi = [i / aux for i in phi_aux]
            
            omega = np.array(self._phi)
            
            theta_t = np.array([theta])
            
            
            return omega @ theta_t.T

    def get_FS_multi_ouput(self):
        
        if self._type not in ('mimo'):
             
            print('The method get_FS_multi_ouput() is just for MIMO Fuzzy Systems!!')
        else:
            aux = 0.0
            phi_aux = [];
            theta = []
            
            
            for i in range(0,len(self._rules)):
                phi_aux.append(self._rules[i].get_rule_antecedent_value())
                aux = aux +  phi_aux[i]
                theta = np.append(theta,self._rules[i].get_rule_consequent_value()) 
               
                aux_cons = theta[0] #b0
                for j in range(0,len(theta)-1):
                    
                    aux_cons += theta[j+1] * self._rules[i]._antecedents[j].value
                
                
                theta_t = np.array([aux_cons])
                
            self._phi = [i / aux for i in phi_aux]
            
            omega = np.array(self._phi)
            
            theta_t = np.array([theta])
            
            print(omega)
            
            print(theta_t)
            
            
            return omega @ theta_t.T