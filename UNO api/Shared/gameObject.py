import playerObject

class gameObject:
    def __init__(self, adminPlayerId):
        self.playerIdList = [adminPlayerId]
        self.admin = [adminPlayerId]

    def addPlayer(self, playerIdList):
        returnList = []
        for playerId in playerIdList:
            if playerId in self.playerIdList:
                returnList.append(False)
            else:
                self.playerIdList.append(playerId)
                returnList.append(True)

