import matplotlib.pyplot as plt

##### Finding Y form Y=mx+b #######
def compute_y(x,m,b):
    y=m*x+b
    return y
######## Finding all Y's in a list of Y=mx+b######
def compute_all_y(x_list,m,b):
    y_lst=[]
    for num in x_list:
        y=num*m+b
        y_lst.append(y)
    return y_lst
##### Computing MSE ######
def compute_mse(y_actual_list, y_predicted_list):
    sum_num=0
    for i in range(len(y_actual_list)):
        er=(y_actual_list[i]-y_predicted_list[i])**2
        sum_num+=er
    MSE= sum_num/len(y_actual_list)
    return MSE
##### Minimizing MSE ######
def minimize_mse(x_list, y_actual_list, m_start, b_start, m_step, b_step, iterations):     
    m = m_start
    b = b_start
    predicted_y = compute_all_y(x_list, m, b)
    lowest_MSE = compute_mse(y_actual_list, predicted_y)
    
    for _ in range(iterations):
        # Try increasing m
        m_larger = m + m_step
        predicted_y_larger_m = compute_all_y(x_list, m_larger, b)
        mse_larger_m = compute_mse(y_actual_list, predicted_y_larger_m)
        
        if mse_larger_m < lowest_MSE:
            m = m_larger
            lowest_MSE = mse_larger_m
        else:
            # Try decreasing m
            m_smaller = m - m_step
            predicted_y_smaller_m = compute_all_y(x_list, m_smaller, b)
            mse_smaller_m = compute_mse(y_actual_list, predicted_y_smaller_m)
            
            if mse_smaller_m < lowest_MSE:
                m = m_smaller
                lowest_MSE = mse_smaller_m
        
        # Try increasing b
        b_larger = b + b_step
        predicted_y_larger_b = compute_all_y(x_list, m, b_larger)
        mse_larger_b = compute_mse(y_actual_list, predicted_y_larger_b)
        
        if mse_larger_b < lowest_MSE:
            b = b_larger
            lowest_MSE = mse_larger_b
        else:
            # Try decreasing b
            b_smaller = b - b_step
            predicted_y_smaller_b = compute_all_y(x_list, m, b_smaller)
            mse_smaller_b = compute_mse(y_actual_list, predicted_y_smaller_b)
            
            if mse_smaller_b < lowest_MSE:
                b = b_smaller
                lowest_MSE = mse_smaller_b
    
    return m, b
def calc_sum(lst):
    tot=0
    for num in lst:
        tot+=num
    return tot
def calc_mean(lst):
    mean=calc_sum(lst)/len(lst)
    return mean
def square(x):
    y=x**2
    return y
def calc_variance(data):
    if len(data) == 0:
        return 0  # Avoid division by zero if the list is empty
    
    mean = calc_mean(data)
    squared_diffs = [(x - mean) ** 2 for x in data]
    variance = sum(squared_diffs) / len(data)
    
    return variance
def calc_covariance(x_list,y_actual_list):
    cov=0
    xmean=calc_mean(x_list)
    ymean=calc_mean(y_actual_list)
    for i in range (len(x_list)):
        cov+=(x_list[i]-xmean)*(y_actual_list[i]-ymean)
    cov=cov/len(x_list)
    return cov
#### Testing ####

## reading data 1###
temps_train=[]
chirps_train=[]
with open("crickets_train.csv","r") as file:
    for aline in file:
        aline=aline.strip().split(",")
        chirps_train.append(aline[0])
        temps_train.append(aline[1])
            
file.close()
temps_train=temps_train[1:]
chirps_train=chirps_train[1:]
for i in range(len(temps_train)):
    temps_train[i]=float(temps_train[i])
    chirps_train[i]=float(chirps_train[i])
## reading data 2 ###
temps_test=[]
chirps_test=[]
with open("crickets_test.csv","r") as file:
    for aline in file:
        aline=aline.strip().split(",")
        chirps_test.append(aline[0])
        temps_test.append(aline[1])
            
file.close()
temps_test=temps_test[1:]
chirps_test=chirps_test[1:]
for i in range(len(temps_test)):
    temps_test[i]=float(temps_test[i])
    chirps_test[i]=float(chirps_test[i])

m_crickets,b_crickets=minimize_mse(chirps_train,temps_train, 105, 105, 0.01,0.01, 100000)
## plotting ##
x_vals = chirps_train
y_vals=temps_train
y_vals_p = compute_all_y(x_vals,m_crickets,b_crickets)
plt.plot(x_vals, y_vals,"x",label= "Actual Data")
plt.plot(x_vals, y_vals_p,color="red", label="Lowest MSE, m=4.42 b=6.84")
plt.title('Temps by Chirps/Min')
plt.xlabel('chirps/min')
plt.grid(True)
plt.legend()
plt.ylabel('Temp')
plt.show()
# Error
y_test=compute_all_y(chirps_test,m_crickets,b_crickets)
error=[]
for i in range (len(y_test)):
    er=abs(y_test[i]-temps_test[i])
    error.append(er)
