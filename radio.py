__author__ = 'ctewani'

'''

>> Description of formulation the problem

1. The problem falls under the category of Constraint Satisfaction Problem, as the each state will be assigned one of the four frequency,
 such that the adjacent states should have a different frequency and few states will have legacy freq as constraints
2. Also, the problems hints to the problem of Map Coloring which is an classic Constraint Satisfaction Problem and is similar to it.
3. Instead of colors for the map, we assign a frequency to each state by following the constraints

>> Solution
1. Incremental model of the solution is implemented
2. The solution uses the following algorithms/features in the algorithms
 a. Backward chaining
      - As it tries to assign one freq to a state, it moves to the next state and tries to assign another freq and so one,
      If the next state cannot be assigned any freq it is backtracked to the previous state which assigns a different freq as
      it had previously assigned and then moves on to the next state and so on.. It runs in recursion and tries all combination
 b. Minimum Constrained Variable
      - To start the assignment, we have to pick a state (variable) which is the highest constrained of all states., i.e., state with the
      most number of adjacent states.
 c. Minimum Constraining Variable
      - The state which has the least domain, we have very few option to pick the frequency for the state.
      Minimum constraining variable and minimum constrained variable, are used together! i.e., state with the least freq to assign and within them,
      the one which has the highest adjacent states, i.e. constrained variable
 d. Least Constraining Value
      - Arc consistency is used to check, the constraining values. i.e. when a state is picked, we need to pick the freq in a particular order, or not all
      freq will satisfy teh constraints.
      So the constraints have to be propogated and further adn all arc are made consistent.


>> Approach for arc consistency
1. Store unqiue IDs for each state in PQ
2. Get from variable using MCV with normal get() in PQ,
   a. Check if the ID assigned to the state is a recent one
   b. If it is not the recent one, discard it
   c. Do a get() again to get the next best variable from MCV
   d. Sorted for life! :D
3. Do Maintaining Arc Consistency for the chosen variable
   a. Change domains of variables to make it arc consistent
   b. Add all the variables with modified domains back to the PQ with new updated unique IDs

>> method for arc consistency
1. form a queue all neighbouring nodes
2. while queue not empty:
a. pick a pair
b. call revise(pair)
      i. In revise, for every value in state domain, if there's a value in domain of the neighbor which is not consistent with any value in picked variable
      ii. delete the domain from the picked variable
      iii. Next domain in the picked variable
c. If revise true,

3. Data structure used
Priority queue is used, with each state has a unique ID and latest state with the most recent modified domain is picked. As arc consistency reduces teh domain  and there's no
way to edit teh PQ.

>> Poblems you faced,

The list is mutable and deepcopy had to be used.

>> Assumptions
There's no states in the legacy state file which has the same freq of the adjacent state
Or
One state given multiple values

>> brief analysis of how well your program works

It runs with ZERO backtracts and an average time of 0.018 sec or less. and able to assign all values properly


>> Improvement

Use cutlet and nearly tree CSP to improve


there are two approaches

2. Nearly tree CSP
 >> Cutset, find cutset
 >> make it into a tree CSP
 >> color the cutset, check RN tb

3. Local search
 >> randomization and local search

 Though it might take a lot of time to search, it might work well in some cases.

'''
from collections import defaultdict, Counter
import sys
from time import time,sleep
import Queue as queue
from copy import copy

class Node:
      def __init__(self, uniqueID, state, adjacentStates, freq):
            self.uniqueID = uniqueID
            self.state = state
            self.adjacentStates = adjacentStates
            #print state, len(adjacentStates)
            self.freq = freq

      def __cmp__(self,other):
            if len(self.freq) == len(other.freq) and len(self.adjacentStates) == len(other.adjacentStates):
                return 0
            elif len(self.freq) == len(other.freq) and len(self.adjacentStates) > len(other.adjacentStates):
                  return -1
            elif len(self.freq) == len(other.freq) and len(self.adjacentStates) < len(other.adjacentStates):
                  return 1
            elif len(self.freq) > len(other.freq):
                  return 1
            elif len(self.freq) < len(other.freq):
                  return -1

class Solution:
      def __init__(self):
            self.adjStateAndFreqDict = defaultdict(list)
            self.currStateFreqDict = defaultdict(str)
            self.domainFreq = ['A','B','C','D']
            self.legacyConstraintFile = sys.argv[1]
            self.backtrackCount = 0
            self.result = defaultdict(str)
            self.nodeCount = 0

      def addAdjStates(self):
            adjacentStatesFile = './adjacent-states'
            adjacentStatesList = open(adjacentStatesFile, 'r').read().split('\n')
            for adjStates in adjacentStatesList:
                  adjacentStates = adjStates.split()
                  self.adjStateAndFreqDict[adjacentStates[0]].extend([[],self.domainFreq,[]]) #1st list => adjacent states; 2nd list => Domain Freq; 3rd list => list of unique IDs for state
                  self.adjStateAndFreqDict[adjacentStates[0]][0].extend(adjacentStates[1:])

      def addConstraintFreq(self):
      # add the legacy constraint freq for states
            legacyConstraintList = open('./'+self.legacyConstraintFile, 'r').read().split('\n')
            if len(legacyConstraintList) != 1:
                  for legacyConstraint in legacyConstraintList:
                        legacyConstraint = legacyConstraint.split()
                        self.adjStateAndFreqDict[legacyConstraint[0]][1] = legacyConstraint[1]

      def createAdjStatesAndFreqDict(self):
            # read from adjacent-states file
            self.addAdjStates()
            # add legacy constraint domain
            self.addConstraintFreq()

      def getUniqueID(self):
            self.nodeCount += 1
            return self.nodeCount

      def updateStateFreqDict(self, ac3StateAndFreqDict):
            for state in ac3StateAndFreqDict:
                  self.currStateFreqDict[state] = copy(ac3StateAndFreqDict[state])
                  unqiueID = self.getUniqueID()
                  self.adjStateAndFreqDict[state][2].append(unqiueID)
                  self.statePQ.put(Node(unqiueID, state, self.adjStateAndFreqDict[state][0],copy(self.currStateFreqDict[state])))

      def restoreStateFreqDict(self, currState):
            # restore freq domains of unassigned and current node!
            for state in self.adjStateAndFreqDict:
                  if len(self.result[state]) == 0 and state != currState:
                        self.currStateFreqDict[state] = copy(self.adjStateAndFreqDict[state][1])

      def initStateFreqDict(self):
            for state in self.adjStateAndFreqDict:
                  self.currStateFreqDict[state] = copy(self.adjStateAndFreqDict[state][1])

      def populatePriorityQ(self):
            self.statePQ = queue.PriorityQueue()
            for state in self.adjStateAndFreqDict:
                  unqiueID = self.getUniqueID()
                  self.adjStateAndFreqDict[state][2].append(unqiueID)
                  self.statePQ.put(Node(unqiueID, state, self.adjStateAndFreqDict[state][0],self.adjStateAndFreqDict[state][1]))

      def getUnassignedState(self):
            unassignedStateList = [state for state in self.adjStateAndFreqDict if state not in self.result]
            return unassignedStateList

      def checkConstraint(self, state, freq):
            for adjState in self.adjStateAndFreqDict[state][0]:
                  if adjState in self.result and self.result[adjState] == freq:
                        #print "failConst", adjState, state, freq
                        return False
            return True

      def printResult(self):
            with open('result.txt','w') as f:
                  for state in self.result:
                        f.write(state+' '+self.result[state]+'\n')

      def checkCSP(self):
            for state in self.result:
                  for adjState in self.adjStateAndFreqDict[state][0]:
                        if self.result[state] not in self.adjStateAndFreqDict[state][1]:
                              print "failed valid domain", state, self.result[state],self.adjStateAndFreqDict[state][1]
                              return False
                        if self.result[state] == self.result[adjState]:
                              print "failed constraint", state, adjState, self.result[state]
                              return False
            return True

      def solve(self):
            self.createAdjStatesAndFreqDict()
            self.populatePriorityQ()
            self.initStateFreqDict()
            self.backwardChain()
            self.printResult()
            print "Number of backtrack",self.backtrackCount
            #print "CSP valid ", self.checkCSP()

      def revise(self, state, stateDomain, adjState, adjStateDomain):
            revise = False
            adjStateDomainIter = copy(adjStateDomain)
            for stateFreq in adjStateDomainIter:
                  if stateFreq in stateDomain and len(stateDomain) == 1:
                        adjStateDomain.remove(stateFreq)
                        revise = True
            return revise

      def ac_3(self, state):
            ac3StateAndFreqDict = {}
            stateDomain = [self.result[state]]
            # list all the pairs of neighbours of state, [(state,unassigned_neighbour1), (state,unassigned_neighbour2)..]
            StateAdjStatesDomainPair = [(state,stateDomain,adjState) for adjState in self.adjStateAndFreqDict[state][0] if len(self.result[adjState]) == 0]
            #print "curr",state,stateDomain
            while len(StateAdjStatesDomainPair) != 0:
                  currState, currStateDomain, adjState = StateAdjStatesDomainPair.pop(0)
                  adjStateDomain = self.currStateFreqDict[adjState]
                  if self.revise(currState, currStateDomain, adjState, adjStateDomain):
                        if len(adjStateDomain) == 0:
                              return False
                        ac3StateAndFreqDict[adjState] = adjStateDomain
                        self.updateStateFreqDict(ac3StateAndFreqDict)
                        StateAdjStatesDomainPair.extend([(adjState, adjStateDomain, adjStateX) for adjStateX in self.adjStateAndFreqDict[adjState][0] if len(self.result[adjStateX]) == 0 and adjStateX != adjState])
            return True

      def backwardChain(self):
            # check if all variables are assigned, if yes return True
            if len(self.result.keys()) == len(self.adjStateAndFreqDict.keys()):
                  return True
            # get un-assigned variable from priority queue; awesome?! Most constraining variable and Most constrained variable hueristic!
            stateNode = self.statePQ.get()
            #print stateNode.state
            while stateNode.uniqueID != self.adjStateAndFreqDict[stateNode.state][2][len(self.adjStateAndFreqDict[stateNode.state][2])-1]:
                  stateNode = self.statePQ.get()

            #get valid freq for state => Arc consistency or Forward checking?
            freqList = copy(stateNode.freq)
            for freq in freqList:
                  # check if the domain satisfies the constraint
                  if self.checkConstraint(stateNode.state, freq):
                        # assign freq to state
                        self.result[stateNode.state] = freq
                        if not self.ac_3(stateNode.state):
                              self.restoreStateFreqDict(stateNode.state)
                              continue
                              #return False
                        # call for next assignment
                        result = self.backwardChain()
                        # RESTORE ALL DOMAINS HERE! EXCLUDING CURRENT STATE, THOSE IN RESULTS!
                        self.restoreStateFreqDict(stateNode.state)

                        if result:
                              return True
                        else:
                              self.backtrackCount += 1

                        # un-assign the state from result
                        self.result.pop(stateNode.state)

            # put back state in PQ, as you removed from it at the start of for-loop
            self.statePQ.put(stateNode)
            return False

def main():
      solution = Solution()
      startTime = time()
      solution.solve()
      #print solution.result

if __name__ == '__main__':
    main()

