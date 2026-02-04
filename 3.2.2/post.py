from datetime import datetime

class Post:
    postId = 0
    
    def __init__(self, userName, message):
        self.message = message
        self.userName = userName
        self.timestamp = datetime.now()
        self.postId= Post.postId
        Post.postId += 1
    
    def __str__(self):
        return self.userName + " " + self.timestamp.__str__() + ": " + self.message
    
    def setMessage(self, message):
        self.message = message
    
    def getUserName(self):
        return self.userName
    
    def getPostId(self):
        return self.postId