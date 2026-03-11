# SUSPICIOUS TRANSACTION
import pandas as pd
import streamlit as st
import pymysql
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score,precision_score,recall_score,confusion_matrix


# Preprocessing of DATA
df=pd.read_csv(r"C:\Users\Deepa Rathore\OneDrive\Desktop\python libraries\scikit_learn\synthetic_fraud_dataset.csv")
print(df.head(),"\n")    
df.drop(columns=['Transaction_ID','Timestamp','Location','Device_Type','Previous_Fraudulent_Activity','Daily_Transaction_Count','Card_Type','Card_Age',
 'Transaction_Distance','Risk_Score','Is_Weekend'],inplace=True)

print(df.info())    
print("\n",df.describe())    
print("\nNo. of duplicate row =",df.duplicated().sum())   



# MYSQL CONNECTION
mydb=pymysql.connect(host='localhost',user='root',password='sakdee@2005',database='fraud',ssl={"disabled":True})
cur=mydb.cursor()

# s="CREATE TABLE bank_fraud (User_ID varchar(10),Transaction_Amount float(8,4), Account_Balance float(12,2)" \
# ", IP_Address_Flag varchar(3), Avg_Transaction_Amount_7d float(10,4), Failed_Transaction_Count_7d int(3), Authentication_Method varchar(13), Fraud_Label int(2) )"



# Label Encoding
le=LabelEncoder()
def label_encod(df):
     col=['User_ID','IP_Address_Flag','Authentication_Method']
     for i in col:
          df[i]=le.fit_transform(df[i])
     return df
df=label_encod(df)



# split the data for Training & Testing
X=df[['User_ID','Transaction_Amount','Account_Balance','IP_Address_Flag','Avg_Transaction_Amount_7d','Failed_Transaction_Count_7d','Authentication_Method']]
y=df['Fraud_Label']

X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.2,random_state=42)



# training and testing of model
model=RandomForestClassifier(n_estimators=200,random_state=42)
model.fit(X_train,y_train)

# testing
def pred(df):
    y_pred=model.predict(df[:len(df)])
    return y_pred

y_pred=pd.DataFrame(pred(X_test))
y_test=pd.DataFrame(y_test)



# Evaluate Performance
ac=(accuracy_score(y_test,y_pred))*100
print("Accuracy of model : ",ac,"%")     
print("\nPrecision of model : ",precision_score(y_test,y_pred))    
print("\nRecall_Score of model : ",recall_score(y_test,y_pred))        
print("\nconfusion_metrics of model : \n",confusion_matrix(y_test,y_pred)) 



# USER INPUT

st.title("Bank Fraud Detection Model")
st.text("To check Suspicious transaction enter some Informations")
with st.form("my_form"):
     data={
                         
     'User_ID' : [st.text_input("Enter your user id : ")],
     'Transaction_Amount' : [st.number_input("Enter Transaction Amount : ")],
     'Account_Balance' : [st.number_input("Enter Acount Balance before transaction : ")],
     
     'IP_Address_Flag' : [st.selectbox("Is IP Address Suspicious  ",["Yes","No"])],
     'Avg_Transaction_Amount_7d' : [st.number_input("Enter Average Transaction Amount in a Week : ")],
     'Failed_Transaction_Count_7d' : [st.number_input("Enter Failed Transaction in a Week : ")],
     'Authentication_Method' :  [st.selectbox("Choose Authentication Method  ",["Biometric","PIN","Password","OTP"])]
          }
     submit=st.form_submit_button("Submit")



if submit:
     df1=pd.DataFrame(data)
     df1=label_encod(df1)
     y_p=pred(df1) 

     # Insert data into database
     query="INSERT INTO bank_fraud values (%s,%s,%s,%s,%s,%s,%s,%s)"
     values= (data['User_ID'][0],data['Transaction_Amount'][0],data[ 'Account_Balance'][0],data['IP_Address_Flag'][0],data['Avg_Transaction_Amount_7d'][0],data['Failed_Transaction_Count_7d'][0],data['Authentication_Method'][0],y_p[0])
     cur.execute(query,values)
     mydb.commit()
     if y_p==0:
         st.success("Transaction is Normal")
     else:
          st.warning("This Transaction is Suspicious")


     s="select user_id from bank_fraud where fraud_label=1  " \
     "group by user_id having count(fraud_label)>2"
     cur.execute(s)
     result=cur.fetchall()


     if result==():
          st.write("There is no suspicious User_ID")
     else:
          st.error(f"User ID {result} done more than 2 suspicious transaction that's why this ID has to BLOCK")

