#!/usr/bin/env python

'''
Topic   :: Help with PDDL stuff
Project :: Explanations for Multi-Model Planning
Author  :: Tathagata Chakraborti
Date    :: 09/29/2016
'''

import re, os


'''
Global :: global variables
'''

__DOMAIN_SOURCE__ = '../../domain/domain_template.pddl'

__GROUND_CMD__    = "./ground.sh {} {} > stdout.txt"
__GROUND1_CMD__    = "./ground1.sh {} {} > stdout.txt"
__FD_PLAN_CMD__   = "./fdplan.sh {} {}"
__FD_PLAN_COST_CMD__   = "./get_plan_cost.sh"
__VAL_PLAN_CMD__  = "./valplan.sh {} {} {}"


'''
Method :: write domain file from given state
'''

def write_domain_file_from_state(state, domain_source):

    predicateList = set()
    actionList    = {}

    for item in state:

        regex_probe   = re.compile("(.*)-has-(parameters|precondition|add-effect|delete-effect)-(.*)$").search(item)
        actionName    = regex_probe.group(1)
        _condition    = regex_probe.group(2)
        predicateName = regex_probe.group(3)

        predicateList.add(predicateName)

        if actionName not in actionList: actionList[actionName] = {'parameters':"", 'precondition' : [], 'add-effect' : [], 'delete-effect' : []}
        if _condition == 'parameters':
            actionList[actionName][_condition] = predicateName
        else:
            actionList[actionName][_condition].append(predicateName) 

    temp_domainFileName = 'temp.pddl'
    with open(domain_source, 'r') as template_domain_file:
        template_domain = template_domain_file.read()


    with open(temp_domainFileName, 'w') as temp_domain_file:

        predicateString = '\n'.join(['( {} )'.format(item) for item in predicateList])
        actionString    = '\n'.join(['(:action {}\n:parameters ({})\n:precondition\n(and\n{}\n)\n:effect\n(and\n{}\n)\n)\n'\
                                     .format(key, actionList[key]['parameters'],'\n'.join(['( {} )'.format(p) for p in actionList[key]['precondition']]), \
                                             '{}\n{}'.format('\n'.join(['( {} )'.format(p) for p in actionList[key]['add-effect']]), \
                                                             '\n'.join(['(not ( {} ))'.format(p) for p in actionList[key]['delete-effect']]))) for key in actionList.keys()])
        
        temp_domain_file.write(template_domain.format(actionString))

    return temp_domainFileName
        

'''
Method :: read state from given domain file
'''

def read_state_from_domain_file(domainFileName):

    def PDDLaction(description):
        action_name            = re.search('\(:action(.*?)[\s+]*:', description).group(1).strip()

        try:    parameters     = re.search(':parameters[\s+]*\((.*?)\)[\s+]*:', description).group(1)
        except: parameters     = ""
        try:    preconditions  = {re.search('\(((?!not).*?)\)', item).group(1).strip() : not 'not ' in item \
                                  for item in re.findall('(\(not[\s+]*\(.*?\)[\s+]*\)|\(.*?\))', re.search(':precondition[\s+]*\(and(.*?)\)[\s+]*:', description).group(1))}

        except: preconditions  = {}

        try:
            all_effects = [item for item in re.findall('(\(not[\s+]*\(.*?\)[\s+]*\)|\(increase[\s+]*\(.*?\)[\s+]*\(.*?\)[\s+]*\)|\(.*?\))', re.search(':effect[\s+]*\(and(.*?)\)$', description).group(1))]
            effects = {}
            for eff in all_effects:
                if 'increase' in eff:
                    effects[re.search('\((increase.*)\)',eff).group(1)] = True
                else:
                    effects[re.search('\(((?!not\s).*?)\)', eff).group(1).strip()] = bool(not 'not ' in eff)

        except: effects        = {}
            
        return [action_name, parameters, preconditions, effects]

    
    ''''''

    with open(domainFileName, 'r') as domain_file:
        action_dict = {item.split(' ')[1] : PDDLaction(item) for item in re.findall('\(:action.*?\)[\s+]*\)[\s+]*\)', re.sub('[\s+]', ' ', domain_file.read()))}

    ''''''

    state = []
    for key in action_dict.keys():
        actionName        = action_dict[key][0]
        state.append('{}-has-parameters-{}'.format(actionName, action_dict[key][1]))
        for precondition in action_dict[key][2].items():
            state.append('{}-has-precondition-{}'.format(actionName, precondition[0]))
            
        for effect in action_dict[key][3].items():
            if effect[1]: state.append('{}-has-add-effect-{}'.format(actionName, effect[0]))
            else:         state.append('{}-has-delete-effect-{}'.format(actionName, effect[0]))
            
    return state


'''
Method :: compute plan from domain and problem files
'''

def get_plan(domainFileName, problemFileName):
    #print "command",__FD_PLAN_CMD__.format(domainFileName, problemFileName)
    output = os.popen(__FD_PLAN_CMD__.format(domainFileName, problemFileName)).read().strip()
        
    #plan   = [item.strip().replace('_', ' ') for item in output.split('\n')] if output != '' else []
    plan   = [item.strip() for item in output.split('\n')] if output != '' else []
    if len(plan) > 0:
        output = os.popen(__FD_PLAN_COST_CMD__).read().strip()
        cost   = int(output)
    else:
        cost = 0
    #print "plan","\n".join(plan)
    #print "cost",cost

    return [plan, cost]


''' 
Method :: ground PDDL domain and problem files
'''

def ground(domainFileName, problemFileName):

    output = os.system('./clean.sh')
    output = os.system(__GROUND_CMD__.format(domainFileName, problemFileName))


def ground1(domainFileName, problemFileName):

    output = os.system('./clean.sh')
    output = os.system(__GROUND1_CMD__.format(domainFileName, problemFileName))



''' 
Method :: validate plan given PDDL domain and problem files
'''

#def validate_plan(domainFileName, problemFileName, planFileName):

#    output = os.system(__VAL_PLAN_CMD__.format(domainFileName, problemFileName, planFileName))
#    return eval(output)

def validate_plan(domainFileName, problemFileName, planFileName):
    print(__VAL_PLAN_CMD__.format(domainFileName, problemFileName, planFileName))
    output = os.popen(__VAL_PLAN_CMD__.format(domainFileName, problemFileName, planFileName)).read().strip()
    print( output )
    return eval(output)



if __name__ == '__main__':
    pass

    ''' debug list '''
    #print validate_plan('../domain/fetchworld-base-m.pddl', '../domain/problem1.pddl', 'sas_plan')
    #state = read_state_from_domain_file('../domain/fetchworld-base-m.pddl')
    #write_domain_file_from_state(state)
