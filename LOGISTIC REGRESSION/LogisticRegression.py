import numpy as np

#====== CLASS FOR IMPLEMENTING LOGISTIC REGRESSION ======#

class logReg:

    def set(self,Xin,Yin):
        self.X=Xin
        self.Y=Yin
        self.m=Yin.size # number of training examples
        self.slope=np.random.rand(Xin.shape[1])
        self.inter=np.random.rand(1)
        
    def Sigmoid(self,z):
        return 1/(1+np.exp(-z))

    def predict(self,X):
        return self.Sigmoid(np.dot(X,self.slope)+self.inter)>=0.5
    
    def Cost(self,LAMBDA=0):
        h=self.Sigmoid(np.dot(self.X,self.slope)+self.inter)
        reg=(LAMBDA/(2*self.m))*(np.sum(np.power(self.slope,2)))
        J=-(np.dot(self.Y.T,np.log(h))+np.dot(1-self.Y.T,np.log(1-h)))/self.m + reg # Cost after Regularisation
        return J
 
    def GradientDescent(self,LAMBDA=0,alpha=0.1,iter=2000):
        for i in range(1,iter):
            h=self.Sigmoid(np.dot(self.X,self.slope)+self.inter)
            P=np.dot(self.X.T,(h-self.Y))
            grad_slope=(alpha/self.m)*P+(LAMBDA/self.m)*self.slope
            grad_inter=(alpha/self.m)*np.sum(h-self.Y)
            self.slope=self.slope-grad_slope
            self.inter=self.inter-grad_inter
            #print("Cost in "+str(i)+"th iteration: "+str(self.Cost(LAMBDA)))

    def miniGradientDescent(self,batch_sz,shuffle=True,LAMBDA=0,alpha=0.1,iter=2000):
        if(shuffle):
            np.random.shuffle([self.X,self.Y])        
        for i in range(1,iter):
            for j in range(0,self.m,batch_sz):
                X_mini=self.X[j:j+batch_sz,:]
                Y_mini=self.Y[j:j+batch_sz]
                sz=Y_mini.size
                if(Y_mini.size==0):   
                    break       # to avoid division by zero error
                h=self.Sigmoid(np.dot(X_mini,self.slope)+self.inter)
                P=np.dot(X_mini.T,(h-Y_mini))
                grad_slope=(alpha/sz)*P+(LAMBDA/sz)*self.slope
                grad_inter=(alpha/sz)*np.sum(h-Y_mini)
                self.slope=self.slope-grad_slope
                self.inter=self.inter-grad_inter            
            #print("Cost in "+str(i)+"th iteration: "+str(self.Cost(LAMBDA)))
            
    def accuracy(self,test):
        prediction=self.predict(test.X)
        acc=(sum(prediction==test.Y)/test.m)*100
        return acc

    def params(self):
        return [self.inter,self.slope]
