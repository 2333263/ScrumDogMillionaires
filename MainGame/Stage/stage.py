class Stage:
    def __init__(self, goalItems, acquisitionRewards, complete, failure, reward, penalty, misc):
        #initialize variables to values of arguments
        self.goalItems = goalItems
        self.acquisitionRewards = acquisitionRewards
        
        self.complete = complete
        self.failure = failure
        self.reward = reward
        self.penalty = penalty
        self.misc = misc
    #methods used to obtain stage information form a stage::

    # getting the items that we need to break if we need to collect
    def getGoalItems(self):
        return self.goalItems
    
    # get rewards for actions that lead you to the next stage if you need to break/collect items
    def getAcquisitionRewards(self):
        return self.acquisitionRewards
    
    # get a big reward for advancing to the next stage
    def getComplete(self):
        return self.complete

    # return a negative reward, that will lead you to going back a stage
    # for example, to craft a stone pickaxe we need 5 stones and 2 wooden planks
    # placing wooden planks would be bad
    def getFailure(self):
        return self.failure

    # get rewards for actions that lead you to the next stage if you need to craft an item
    def getReward(self):
        return self.reward

    # return a negative reward, ie penalty, for making an action that will set you back a stage 
    def getPenalty(self):
        return self.penalty

    # miscalenous reward return, for eg, reward for moving as an action (doesn't really affect whether a stage is passed or not)
    def getMisc(self):
        return self.misc
