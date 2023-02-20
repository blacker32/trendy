# Gerekli kütüphaneleri içe aktarın
from sklearn.tree import DecisionTreeClassifier
from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# Veri setini yükleyin
iris = datasets.load_iris()

# Özellik ve hedef değişkenleri ayrı değişkenlere aktarın
X = iris.data
y = iris.target

# Veriyi eğitim ve test setleri olarak bölün
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=1)

# Decision Tree sınıflandırıcısını tanımlayın
dt = DecisionTreeClassifier()

# Decision Tree modelini eğitin
dt.fit(X_train, y_train)

# Test verilerini kullanarak modelin doğruluğunu değerlendirin
y_pred = dt.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print("Accuracy:", accuracy)
