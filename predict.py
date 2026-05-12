import pandas as pd

df = pd.read_csv(r"C:\Users\bingi\Desktop\horse_project_v9\race_sim\race_data.csv", encoding="cp949")
X=df[["speed","stamina"]]
Y=df["rank"]

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

X_train,X_test,Y_train,Y_test=train_test_split(X,Y,test_size=0.2)
model=RandomForestClassifier()
model.fit(X_train,Y_train)
print("학습완료")
print(model.predict([[12, 12]]))  # 디프 임팩트
print(model.predict([[8, 8]])) 