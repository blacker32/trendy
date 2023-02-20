# Gerekli kütüphaneleri içe aktarın
from sklearn.cluster import KMeans
import pandas as pd
import numpy as np
import warnings
# Veri setini yükleyin
data = pd.read_excel('Sonveri3.xlsx')

# Özellikleri seçin ve veri kümesini numpy dizisine dönüştürün
X = np.array(data[['satis_fiyat', 'urun_favori_sayisi', 'urun_Toplam_yorum_sayisi']])

# K-Means kümeleme modelini tanımlayın
kmeans = KMeans(n_clusters=3)

# K-Means modelini eğitin
kmeans.fit(X)

# Her bir veri noktasının küme numarasını tahmin edin
y_pred = kmeans.predict(X)

# Tahminleri bir sütun olarak veri kümesine ekleyin
data['cluster'] = y_pred
data.to_excel("sonveri.xlsx")
import matplotlib.pyplot as plt           
data.plot()
plt.show()