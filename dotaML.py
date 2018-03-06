import dota2api,time,pickle
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score,confusion_matrix
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Flatten, Conv2D, MaxPooling2D
from keras.wrappers.scikit_learn import KerasClassifier
from keras import regularizers
from sklearn.model_selection import GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import KFold,StratifiedKFold

with open('matches','rb') as fp:
    matches=pickle.load(fp)
player_list=['player' + str(i) for i in range(0,10)]
X=pd.get_dummies(matches[player_list])
y=matches['radiant_win'].astype(int)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.30, random_state=7)

rfc = RandomForestClassifier(n_estimators=10)
rfc.fit(X_train, y_train)
rfc_pred = rfc.predict(X_test)
print(classification_report(y_test,rfc_pred))
no_features=X.shape[1]
no_features=10
def generate_model(no_features, l2_penalty=0.0,  type=1, dropout_rate=0.0):
        model = Sequential()
        if type==1:
            model.add(Dense(round(no_features), input_dim=X.shape[1], kernel_regularizer=regularizers.l2(l2_penalty), activation='relu')) # last layer should be linear so that we can have negative values as well
            model.add(Dropout(dropout_rate))
            model.add(Dense(round(no_features/2), kernel_regularizer=regularizers.l2(l2_penalty),  activation='relu')) # last layer should be linear so that we can have negative values as well
            model.add(Dropout(dropout_rate))   
            model.add(Dense(round(no_features/2), kernel_regularizer=regularizers.l2(l2_penalty),  activation='relu')) # last layer should be linear so that we can have negative values as well
            model.add(Dense(1, kernel_regularizer=regularizers.l2(l2_penalty),  activation='sigmoid')) # last layer should be linear so that we can have negative values as well

        model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy']) #mse for regression
        return model
n_folds=10
seed=7
kfold = StratifiedKFold(n_splits=n_folds, shuffle=True, random_state=seed).split(X_train,y_train)
estimator=KerasClassifier(build_fn=generate_model, epochs=10, batch_size=1000 , verbose=1)
l2_penalty=[0]#,  0.0001,  0.001,  0.01,  0.1] # usual parameters to check for EEG data
type=[1]#
dropout_rate = [0.0]#, 0.2, 0.4, 0.6]
param_grid = dict(no_features=[no_features],l2_penalty=l2_penalty, type=type, dropout_rate=dropout_rate)
grid = None;
grid = GridSearchCV( estimator=estimator, param_grid=param_grid, cv=kfold , scoring='accuracy')
grid_fit = grid.fit(X_train.values, y_train)
tr_result=grid_fit.predict(X_train.values)
tst_result=grid_fit.predict(X_test.values)

print(confusion_matrix(tst_result,y_test))
print(classification_report(y_test,tst_result))
        
#matches2=api.get_match_history(start_at_match_id=id-1)

#next((item for item in matches if item['lobby_type']==8))