import matplotlib.pyplot as plt
import numpy as np
from matplotlib import image as img
from django.core.files.base import ContentFile
from django.core.files.images import ImageFile
from django.core.files import File
from io import BytesIO
import io
import base64
import pandas as pd
from scipy import stats

#-----------------------------------------------------------------------------------------------------------
#this functions are used for creating any kind of graph graph
def get_graph():
    buffer = BytesIO()
    plt.savefig(buffer , format="png")
    buffer.seek(0)
    image_png = buffer.getvalue()
    graph = base64.b64encode(image_png)
    graph = graph.decode('utf-8')
    buffer.close()
    return graph

#-----------------------------------------------------------------------------------------------------------
#plot pi chart
def plotPi(results):
    plt.switch_backend('AGG')
    plotCustomePiChart(results)
    graph = get_graph()
    return graph

#-----------------------------------------------------------------------------------------------------------
#plot pi bar graph
def plotBar(results):
    plt.switch_backend('AGG')
    plotCustomeBarGraph(results)
    graph = get_graph()
    return graph

#-----------------------------------------------------------------------------------------------------------
#plot the trending graph

def plotTrend(results):
    plt.switch_backend('AGG')
    status=getTrendResult(results)
    graph = get_graph()
    return [graph,status]

#-----------------------------------------------------------------------------------------------------------
#Modify the properties of bar graph
def plotCustomeBarGraph(results):
    rightQue =[]
    wrongQue = []
    for result in results:
      rightQue.append(result.right)
      wrongQue.append(result.wrong)

    total_res = len(results)
    x = np.arange(total_res)
    rightQueArr = np.array(rightQue)
    wrongQueArr = np.array(wrongQue)
   
    plt.bar(x,rightQueArr ,color='g' )
    plt.bar(x,wrongQueArr , bottom=rightQueArr,color='r' )
    plt.xlabel('Test')
    plt.ylabel('Total Question')
    plt.title("Performance in each test")
    if total_res<20:
        plt.xticks(x,[int(i+1) for i in x])
    
    plt.legend(['Right' ,'Wrong'] ,loc="upper right")



#-----------------------------------------------------------------------------------------------------------
#Modify the properties of bar graph
def plotCustomePiChart(results):
    rightQue = 0
    wrongQue =0
    totalQue =0
    totalTest =0
    for result in results:
        rightQue +=result.right
        totalQue +=result.attempt
        wrongQue +=result.wrong
        totalTest+=1

    totalNotAttemptQue = (rightQue+wrongQue) - totalQue
    y = np.array([rightQue,wrongQue,totalQue,totalTest])
    labels = ["Right","Wrong","Attempted" ,"Test Given" ]
    color =['green' ,'red' ,'orange','pink']
    # plt.figure(figsize =(10,10))
    plt.figure(figsize=(9, 7.5))
    plt.title('Overall Performance',fontsize=25)
    textprops = {'fontsize':20}
    plt.pie(y,labels=labels,shadow=True,colors=color,autopct=make_autopact(y),textprops=textprops)
    plt.legend(loc ="lower left",fontsize=15)
#used to represent the actual value and total percentage on the pi chart
def make_autopact(values):
    def my_autopct(pct):
        total = sum(values)
        val = int(round(pct*total/100.0))
        return '{p:.2f}% ({v:d})'.format(p=pct,v=val)
    return my_autopct

#-----------------------------------------------------------------------------------------------------------
# Analyse the data and predict the performance of all the exams
def getTrendResult(results):
    test = []
    wrong = []
    right = []
    totalAttempted = []
    i = 1
    for res in results:
        test.append(i)
        right.append(res.right)
        wrong.append(res.wrong)
        totalAttempted.append(res.attempt)
        i+=1
    test = np.array(test)
    right = np.array(right)
    wrong = np.array(wrong)
    totalAttempted = np.array(totalAttempted)

    data = {
    'Test': test,
    'Correct Marks': right,
    'Wrong Marks': wrong,
    'Total Attempted Questions': totalAttempted
    }
    df = pd.DataFrame(data)

    # Calculate the performance
    df['Performance'] = (df['Correct Marks'] / df['Total Attempted Questions']) * 100

    # Perform linear regression
    slope, intercept, r_value, p_value, std_err = stats.linregress(df['Test'], df['Performance'])

    # Calculate the trend line data points
    # trend_line = [slope * x + intercept for x in df['Test']]

    # Plot the data and trend line
    plt.figure(figsize=(8, 6))
    plt.scatter(df['Test'], df['Performance'], label='Performance')
    
    # To give label to each points
    #  
    # for (t,per) in zip(df['Test'],df['Performance']):
    #     plt.text(t,per,t,va='bottom',ha='right')

    # plt.plot(df['Test'], trend_line, color='red', label='Trend Line')

    x = np.array(df['Performance'])
    y = np.array(range(1,len(x)+1))
    plt.plot(y,x)

    plt.xlabel('Test')
    plt.ylabel('Performance (%)')
    plt.title('Performance Trend')
    plt.legend()
    plt.grid(True)
    plt.show()

    if slope <= 0:
        return 1 #Decreasing
    else:
        return  2 #Increasing

#-----------------------------------------------------------------------------------------------------------