import sys
import os

import numpy as np
from mpl_toolkits.mplot3d import Axes3D  # registers 3D projection, not used directly
import matplotlib.pyplot as plt
#from sklearn import linear_model
#from sklearn.metrics import mean_squared_error
#from tqdm.notebook import tqdm
from random import sample


filename = sys.argv[1] #'data/sample0.csv'
data = np.genfromtxt(filename, dtype=float, delimiter=' ', skip_header=1, usecols=(0, 1, 2))
N=data.shape[0]
eps=10**(-5)
B=np.ones(3)
ma=data.T.max(axis=1)
mi=data.T.min(axis=1)

print('Cube has 6 planes. Finding 6 planes equations: A*x+B*y+C*z=1. This can take time...')

planes={}
plane_ind=0

while plane_ind<6:
    ind_0, ind_1, ind_2=sample(range(0,N),3)
    A=np.stack([data[ind_0], data[ind_1], data[ind_2]])
    if np.linalg.det(A)!=0.0:
        Plane_params=np.linalg.solve(A, B)
        #Number inliers for each plane =N*(1/3)/6/2 
        if sum(abs(data@Plane_params-np.ones(N))<eps)>N*(1/3)/6/2 and \
        sum([np.allclose(Plane_params, planes[x]) for x in planes])==0:
            planes[plane_ind]=Plane_params
            plane_ind+=1
            #print((ind_0, ind_1, ind_2), str(Plane_params), sum(abs(data@Plane_params-np.ones(N))<eps))
print('planes found!')
print(planes)

planes_np=np.array([x for x in planes.values()])

#Lets find vertices: each is intesection of 3 differect planes
num_vertices=0
possible_vertices=[]
for ind_0 in range(0,6):
    for ind_1 in range(0,6):
        for ind_2 in range(0,6):
            if ind_0>ind_1>ind_2:
                #We will have 20 combinations of different 3 planes from 6
                A=planes_np[[ind_0, ind_1, ind_2]]
                #A[:,2]=np.ones(3)*(-1)
                #B=coeffs[[ind_0, ind_1, ind_2],2]*(-1)
                B=np.ones(3)
                possible_vert=np.linalg.solve(A[:3],B[:3])
                #Planes intersection should be inside point_cloud. Their number 20 decreased to 6
                if sum(np.greater_equal(possible_vert, mi))==3 and sum(np.greater_equal(ma, possible_vert))==3:
                    possible_vertices.append(possible_vert)
                    num_vertices+=1
print('number of found vertices: ', num_vertices)    

solution=np.array(possible_vertices)
print(solution)

np.savetxt("answer.txt", solution, delimiter=" ")
    
#Optional: compare to answer
filename_ans = filename.replace('sample', 'answer')#'data/answer0.csv'#sys.argv[1]
if os.path.isfile(filename_ans):
    data_ans = np.genfromtxt(filename_ans, dtype=float, delimiter=' ', skip_header=1, usecols=(0, 1, 2))
    #xs_GT, ys_GT, zs_GT = data_ans.T
    correct=0
    for i in possible_vertices:
        for j in data_ans:
            if np.allclose(i,j):
                correct+=1
    print('Found {} correct vertices'.format(correct))