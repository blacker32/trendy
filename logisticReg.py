# Gerekli kütüphaneleri içe aktarın
from sklearn.linear_model import LogisticRegression
from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt           
# Veri setini yükleyin
iris = datasets.load_iris()

# Özellik ve hedef değişkenleri ayrı değişkenlere aktarın
X = iris.data
y = iris.target

# Veriyi eğitim ve test setleri olarak bölün
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=1)

# Lojistik Regresyon modelini tanımlayın
lr = LogisticRegression()

# Lojistik Regresyon modelini eğitin
lr.fit(X_train,y_train)
y_pred=lr.predict(X_test)
sc=accuracy_score(y_test,y_pred)
plt.scatter(y_test,y_pred)
plt.show()