import json
from MainGame.Stage.stage import Stage

def populateStages():
    stages = {}
    file = open("MainGame/Rewards/rewards.json")
    data = json.load(file)
    for i in data:
        tempStage = Stage(data[i]['GoalItems'],
                          data[i]['AcquisitionRewards'],
                          
                          data[i]['Complete'],
                          data[i]['Failure'],
                          data[i]['Reward'],
                          data[i]['Penalty'],
                          data[i]['Misc'])
        stages[i] = tempStage
    file.close()
    return stages
