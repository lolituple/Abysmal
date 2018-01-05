import numpy as np
path='mnist.npz'
f = np.load(path)
x_train = f['x_train']
y_train = f['y_train']
x_test = f['x_test']
y_test = f['y_test']
f.close()
#(x_train, y_train), (x_test, y_test) =mnist.l("mnist.npz");
print (y_train.shape)
print (x_train.shape)
id=np.array(np.where(y_train==0))
id=np.reshape(id,-1)
print id.shape
id=np.random.permutation(id)
id=id[0:50]
idy=y_train[id]
idx=x_train[id,:]
print idx[0]

#for i in range(y_train.shape[0]):
    
