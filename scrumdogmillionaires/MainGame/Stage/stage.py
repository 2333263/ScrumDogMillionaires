class Stage:
    def __init__(self, goalItems, acquisitionRewards, complete, failure, reward, penalty, misc):
        self.goalItems = goalItems
        self.acquisitionRewards = acquisitionRewards
        
        self.complete = complete
        self.failure = failure
        self.reward = reward
        self.penalty = penalty
        self.misc = misc

    def getGoalItems(self):
        return self.goalItems
    
    def getAcquisitionRewards(self):
        return self.acquisitionRewards
    
    def getComplete(self):
        return self.complete

    def getFailure(self):
        return self.failure

    def getReward(self):
        return self.reward

    def getPenalty(self):
        return self.penalty

    def getMisc(self):
        return self.misc
