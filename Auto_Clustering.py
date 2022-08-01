#this program auto clusters the Mären-networks with the help of kmeans
#author: Lisa Kiss
#start date: 15.06.22

import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix,classification_report
from sklearn import neighbors
from sklearn.model_selection import train_test_split
from sklearn.metrics import ConfusionMatrixDisplay
from sklearn.cluster import KMeans
from sklearn.utils import resample
from sklearn import decomposition

#supervised knn
#import data
data = pd.read_excel (r'C:\Users\lisak\Documents\Uni\Master\Masterarbeit\Metriken_Test.xlsx', sheet_name='Korpus')
korpus = pd.DataFrame(data, columns= ['Name','Degree Durchschnitt','Betweenness Durchschnitt','Closeness Durchschnitt','Eigenvector Durchschnitt','Label','Betrüger',
                                      'Betrogener','Liebender','Liebende','Gegenspieler'])
korpus.columns = ['Name','Degree Durchschnitt','Betweenness Durchschnitt','Closeness Durchschnitt','Eigenvector Durchschnitt','Label','Betrüger',
                                      'Betrogener','Liebender','Liebende','Gegenspieler']
X_prime = korpus.loc[0:83, 'Degree Durchschnitt':'Eigenvector Durchschnitt'].values
y = korpus.loc[0:83, 'Label'].values
#print(X_prime)

#upsampling to balance the corpus
#create dataframe for minor classes
df_minor_2 = korpus[korpus['Label'] == 2]
df_minor_3 = korpus[korpus['Label'] == 3]
df_minor_4 = korpus[korpus['Label'] == 4]
df_major_1 = korpus[korpus['Label'] == 1]
#upsample the minority class
df_2_upsampled = resample(df_minor_2,random_state=42,n_samples=20,replace=True)
df_3_upsampled = resample(df_minor_3,random_state=42,n_samples=20,replace=True)
df_4_upsampled = resample(df_minor_4,random_state=42,n_samples=20,replace=True)
#concatenate the upsampled dataframe
df_upsampled = pd.concat([df_2_upsampled,df_3_upsampled,df_4_upsampled,df_major_1])
df_upsampled_new = df_upsampled.reset_index(drop=True)
X_prime_up = df_upsampled_new.loc[0:234, 'Degree Durchschnitt':'Eigenvector Durchschnitt'].values
y_up = df_upsampled_new.loc[0:234, 'Label'].values

#without upsampling
X =X_prime
X_train, X_test, y_train, y_test = train_test_split(X,y, random_state=82, shuffle=True)
clf = neighbors.KNeighborsClassifier()
clf.fit(X_train,y_train)
y_expect = y_test
y_predict = clf.predict(X_test)

#confusion matrix
title ="CM_supervised"
disp = ConfusionMatrixDisplay.from_estimator(
    clf,
    X_test,
    y_test,
    display_labels=['1','2','3','4'],
    cmap=plt.cm.Blues)
disp.ax_.set_title(title)
plt.show()

#with upsampling
X_up = X_prime_up
X_train_up, X_test_up, y_train_up, y_test_up = train_test_split(X_up,y_up, random_state=82, shuffle=True)
clf = neighbors.KNeighborsClassifier()
clf.fit(X_train_up,y_train_up)
y_expect_up = y_test_up
y_predict_up = clf.predict(X_test_up)

#confusion matrix
title ="CM_supervised_with_upsampling"
disp = ConfusionMatrixDisplay.from_estimator(
    clf,
    X_test_up,
    y_test_up,
    display_labels=['1','2','3','4'],
    cmap=plt.cm.Blues)
disp.ax_.set_title(title)
plt.show()

#unsupervised kmeans
y_unsupervised = pd.DataFrame(data, columns=['Label'])
km= KMeans(n_clusters=4)
y_predicted = km.fit_predict(korpus[['Degree Durchschnitt','Betweenness Durchschnitt','Closeness Durchschnitt','Eigenvector Durchschnitt']])
#print(y_predicted)
korpus['pred_unsupervised'] = y_predicted

#PCA
pca = decomposition.PCA(n_components=2)
pca.fit(korpus[['Degree Durchschnitt','Betweenness Durchschnitt','Closeness Durchschnitt','Eigenvector Durchschnitt']])
new_korpus = pca.transform(korpus[['Degree Durchschnitt','Betweenness Durchschnitt','Closeness Durchschnitt','Eigenvector Durchschnitt']])
pca_df = pd.DataFrame(new_korpus, columns = ['Component_1', 'Component_2'])
label = korpus['Label']

#unsupervised kmeans with PCA
km= KMeans(n_clusters=4)
pca_y_predicted = km.fit_predict(pca_df[['Component_1','Component_2']])
pca_df['pred_pca'] = pca_y_predicted
pca_df['og_label'] = label
pca_df['Name'] = korpus['Name']
#print(pca_df)

#scatterplots
#Component 1 vs Component 2
pca_df1= pca_df[pca_df.pred_pca==0]
pca_df2= pca_df[pca_df.pred_pca==1]
pca_df3= pca_df[pca_df.pred_pca==2]
pca_df4= pca_df[pca_df.pred_pca==3]
plt.scatter(pca_df1['Component_1'],pca_df1['Component_2'], color = 'green')
plt.scatter(pca_df2['Component_1'],pca_df2['Component_2'], color = 'red')
plt.scatter(pca_df3['Component_1'],pca_df3['Component_2'], color = 'black')
plt.scatter(pca_df4['Component_1'],pca_df4['Component_2'], color = 'blue')
plt.xlim(-0.75, 1)
plt.ylim(-0.75, 1)
plt.xlabel('Component_1')
plt.ylabel('Component_2')
plt.title ("Plot_unsupervised_with_PCA_colors_new_labels")
plt.legend((0,1,2,3))
plt.show()
#export to excel
#pca_df.to_excel('pred_label.xlsx')

#Component 1 vs Component 2 with colors of the original labels
pca_df1= pca_df[pca_df.og_label==1]
pca_df2= pca_df[pca_df.og_label==2]
pca_df3= pca_df[pca_df.og_label==3]
pca_df4= pca_df[pca_df.og_label==4]
plt.scatter(pca_df1['Component_1'],pca_df1['Component_2'], color = 'green')
plt.scatter(pca_df2['Component_1'],pca_df2['Component_2'], color = 'red')
plt.scatter(pca_df3['Component_1'],pca_df3['Component_2'], color = 'black')
plt.scatter(pca_df4['Component_1'],pca_df4['Component_2'], color = 'blue')
plt.xlim(-0.75, 1)
plt.ylim(-0.75, 1)
plt.xlabel('Component_1')
plt.ylabel('Component_2')
plt.title ("Plot_unsupervised_with_PCA_colors_og_labels")
plt.legend((1,2,3,4))
plt.show()
#Confusion Matrix
conf_m = confusion_matrix(pca_df['og_label'], pca_y_predicted)
disp = ConfusionMatrixDisplay(conf_m)
disp.plot()
disp.ax_.set_title("CM_unsupervised_with_PCA")
plt.show()

#print("Scores for unsupervised with PCA \n")
#print(classification_report(label, pca_y_predicted))
#print("Overall F1-Score")
#print(f1_score(label, pca_y_predicted, average='micro'))

#unsupervised kmeans with PCA and 'Bezeichnung' as features
#PCA
pca = decomposition.PCA(n_components=2)
pca.fit(korpus[['Degree Durchschnitt','Betweenness Durchschnitt','Closeness Durchschnitt','Eigenvector Durchschnitt','Betrüger',
                                      'Betrogener','Liebender','Liebende','Gegenspieler']])
pca_korpus_bez = pca.transform(korpus[['Degree Durchschnitt','Betweenness Durchschnitt','Closeness Durchschnitt','Eigenvector Durchschnitt','Betrüger',
                                      'Betrogener','Liebender','Liebende','Gegenspieler']])
pca_df_bez = pd.DataFrame(pca_korpus_bez, columns = ['Component_1', 'Component_2'])

#unsupervised kmeans with PCA
km= KMeans(n_clusters=4)
pca_y_bez_pred = km.fit_predict(pca_df_bez[['Component_1','Component_2']])
pca_df_bez['pred'] = pca_y_bez_pred
pca_df_bez['og_label'] = korpus['Label']
pca_df_bez['Name'] = korpus['Name']

#Component 1 vs Component 2
pca_bez_df1= pca_df_bez[pca_df_bez.pred==0]
pca_bez_df2= pca_df_bez[pca_df_bez.pred==1]
pca_bez_df3= pca_df_bez[pca_df_bez.pred==2]
pca_bez_df4= pca_df_bez[pca_df_bez.pred==3]
plt.scatter(pca_bez_df1['Component_1'],pca_bez_df1['Component_2'], color = 'green')
plt.scatter(pca_bez_df2['Component_1'],pca_bez_df2['Component_2'], color = 'red')
plt.scatter(pca_bez_df3['Component_1'],pca_bez_df3['Component_2'], color = 'black')
plt.scatter(pca_bez_df4['Component_1'],pca_bez_df4['Component_2'], color = 'blue')
plt.xlabel('Component_1')
plt.ylabel('Component_2')
plt.title ("Plot_unsupervised_with_PCA_with_Bez_colors_new_labels")
plt.legend((0,1,2,3))
plt.show()
#export to excel
#pca_df_bez.to_excel('pred_label_bez.xlsx')

#Component 1 vs Component 2 with colors of the original labels
pca_bez_df1= pca_df_bez[pca_df_bez.og_label==1]
pca_bez_df2= pca_df_bez[pca_df_bez.og_label==2]
pca_bez_df3= pca_df_bez[pca_df_bez.og_label==3]
pca_bez_df4= pca_df_bez[pca_df_bez.og_label==4]
plt.scatter(pca_bez_df1['Component_1'],pca_bez_df1['Component_2'], color = 'green')
plt.scatter(pca_bez_df2['Component_1'],pca_bez_df2['Component_2'], color = 'red')
plt.scatter(pca_bez_df3['Component_1'],pca_bez_df3['Component_2'], color = 'black')
plt.scatter(pca_bez_df4['Component_1'],pca_bez_df4['Component_2'], color = 'blue')
plt.xlabel('Component_1')
plt.ylabel('Component_2')
plt.title ("Plot_unsupervised_with_PCA_with_Bez_colors_og_labels")
plt.legend((1,2,3,4))
plt.show()

#print("Scores for unsupervised with PCA with Bezeichnung \n")
#print(classification_report(korpus['Label'], pca_y_bez_pred))
#print("Overall F1-Score")
#print(f1_score(korpus['Label'], pca_y_bez_pred, average='micro'))

og_label = pca_df_bez['og_label']
conf_bez = confusion_matrix(og_label,pca_y_bez_pred)
disp = ConfusionMatrixDisplay(conf_bez)
disp.plot()
disp.ax_.set_title("CM_unsupervised_with_PCA_with_Bez")
plt.show()

cf_matrix = confusion_matrix(og_label,pca_y_bez_pred )
