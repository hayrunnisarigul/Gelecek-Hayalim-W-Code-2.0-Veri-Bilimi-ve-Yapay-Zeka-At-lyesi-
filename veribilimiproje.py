import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

#Dosyayı okuma
df = pd.read_csv("C:\\Users\\Acer\\Downloads\\merged_water_data.csv")

df.head()

#Önce sütunları kontrol edelim
#print(df.columns)

threshold = 0.95
missing_per_column = df.isnull().mean()
cols_to_drop = missing_per_column[missing_per_column > threshold].index.tolist()
df_cleaned = df.drop(columns=cols_to_drop)
print(f"Tamamen ya da neredeyse tamamen boş sütunlar: {cols_to_drop}")

missing_rows = df_cleaned[df_cleaned.isnull().any(axis=1)]
print(f"Toplam eksik/hatalı değer içeren satır sayısı: {len(missing_rows)}")

# Eksik veya hatalı değerleri doldurma (sayısal alanlar için ortalama)
df_filled = df_cleaned.fillna(df_cleaned.mean(numeric_only=True))

"""
#Ülke Sayısı
country_count = df['Country'].value_counts()
print(country_count)

#Görselleştirme
plt.figure(figsize=(6, 4))
sns.countplot(x='Country', data=df, palette='viridis')
plt.title('Distribution by Country')
plt.xlabel('Country')
plt.ylabel('Count')
plt.show()

#Yıl Sayısı
year_count = df['Year'].value_counts()
print(year_count)

#Görselleştirme
plt.figure(figsize=(6, 4))
sns.countplot(x='Year', data=df, palette='viridis')
plt.title('Distribution by Year')
plt.xlabel('Year')
plt.ylabel('Count')
plt.show()

# Gruplu özet
print(df.groupby('Country')['Total Water Consumption (Billion Cubic Meters)'].mean())

# Türkiye'nin su tüketimi trend analizi
plt.figure(figsize=(12,6))
sns.lineplot(x='Year', y='Total Water Consumption (Billion Cubic Meters)', data=df[df['Country']=='Turkey'])
plt.title('Türkiye’nin Su Tüketimi Trend Analizi')
plt.show()

# En yüksek su tüketimine sahip ülke
highest_consumption_country = df.groupby('Country')['Total Water Consumption (Billion Cubic Meters)'].sum().sort_values(ascending=False).head(1)
print("En yüksek su tüketimine sahip ülke:")
print(highest_consumption_country)

# 2000 yılında kişi başına en yüksek su tüketimi
highest_per_capita_consumption_2000 = df[df['Year']==2000].sort_values('Per Capita Water Use (Liters per Day)', ascending=False).head(1)
print("2000 yılında kişi başına en yüksek su tüketimi:")
print(highest_per_capita_consumption_2000)

# Türkiye'nin yıllara göre su tüketimi
plt.figure(figsize=(10,5))
turkey = df[df['Country']=='Turkey']
sns.lineplot(x='Year', y='Total Water Consumption (Billion Cubic Meters)', data=turkey)
plt.title('Türkiye Su Tüketimi Yıllara Göre')
plt.show()

# Su tüketimi ve kişi başına su kullanımı arasındaki ilişki
plt.figure(figsize=(10,6))
sns.scatterplot(x='Per Capita Water Use (Liters per Day)', y='Total Water Consumption (Billion Cubic Meters)', hue='Country', data=df)
plt.title('Su Tüketimi ve Kişi Başı Su Kullanımı Arasındaki İlişki')
plt.show()

# Korelasyon matrisi
numeric_columns = df.select_dtypes(include=['float64', 'int64']).columns
correlation_matrix = df[numeric_columns].corr()
plt.figure(figsize=(10,8))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm')
plt.title('Korelasyon Matrisi')
plt.show()

# Zaman serisi analizi: Türkiye'nin su tüketimi
plt.figure(figsize=(12,6))
sns.lineplot(x='Year', y='Total Water Consumption (Billion Cubic Meters)', data=df[df['Country']=='Turkey'])
plt.title('Türkiye’nin Su Tüketimi Zaman Serisi Analizi')
plt.show()

# Tarımsal su kullanımı trendleri
plt.figure(figsize=(12,6))
sns.lineplot(x='Year', y='Agricultural Water Use (%)', hue='Country', data=df)
plt.title('Yıllara Göre Tarımsal Su Kullanım Trendleri')
plt.show()

# Su tüketimindeki yıllık büyüme oranı
df['Growth_Rate'] = df.groupby('Country')['Total Water Consumption (Billion Cubic Meters)'].pct_change()
print(df[['Country', 'Year', 'Growth_Rate']].dropna().sort_values(by='Growth_Rate', ascending=False).head())

# Yüksek su kıtlığı seviyesine sahip ülkeler ve yıllar
scarce = df[df['Water Scarcity Level']=='High']
print(scarce[['Country', 'Year']].drop_duplicates())

# Eksik veri analizi
print(df.isnull().sum())

# Aykırı değer analizi: Kişi başına su kullanımı
q1 = df['Per Capita Water Use (Liters per Day)'].quantile(0.25)
q3 = df['Per Capita Water Use (Liters per Day)'].quantile(0.75)
iqr = q3 - q1
outliers = df[(df['Per Capita Water Use (Liters per Day)'] < q1 - 1.5*iqr) | (df['Per Capita Water Use (Liters per Day)'] > q3 + 1.5*iqr)]
print(outliers[['Country','Year','Per Capita Water Use (Liters per Day)']])

# Türkiye'nin su tüketimi istatistikleri
turkey_stats = df[df['Country']=='Turkey'].describe().T
print(turkey_stats)

# Bölgesel su kıtlığı analizi
regional_scarcity = df.groupby('region')['Water Scarcity Level'].value_counts().unstack().fillna(0)
print(regional_scarcity)
regional_scarcity.plot(kind='bar', stacked=True, figsize=(10,6))
plt.title('Bölgelere Göre Su Kıtlığı Seviyesi Dağılımı')
plt.xlabel('Bölge')
plt.ylabel('Yıl Sayısı')
plt.legend(title='Su Kıtlığı Seviyesi')
plt.show()

# Yeraltı suyu tükenme oranı analizi
plt.figure(figsize=(12,6))
sns.lineplot(x='Year', y='Groundwater Depletion Rate (%)', hue='Country', data=df)
plt.title('Yeraltı Suyu Tükenme Oranının Zaman İçindeki Değişimi')
plt.show()

# Hane halkı su kullanımı analizi
top_household = df.groupby('Country')['Household Water Use (%)'].mean().sort_values(ascending=False).head(5)
print(top_household)

# Yağış miktarı ve su tüketimi arasındaki ilişki
plt.figure(figsize=(8,5))
sns.scatterplot(x='Rainfall Impact (Annual Precipitation in mm)', y='Total Water Consumption (Billion Cubic Meters)', hue='Country', data=df)
plt.title('Yağış Miktarı ve Toplam Su Tüketimi Arasındaki İlişki')
plt.show()

# Şehir bazında su dağıtımı analizi
city_dist = df.groupby('City')['Water_Distribution_m3'].mean().sort_values(ascending=False)
print(city_dist.head())

# Endüstriyel su kullanımı trendleri
plt.figure(figsize=(12,6))
sns.lineplot(x='Year', y='Industrial Water Use (%)', hue='Country', data=df)
plt.title('Endüstriyel Su Kullanımı Trendleri')
plt.show()

# Şehir bazında su tüketimi analizi
city_consumption = df.groupby('City')['consumption_liters'].mean().sort_values(ascending=False)
print("En yüksek su tüketen şehirler:\n", city_consumption.head())
print("En düşük su tüketen şehirler:\n", city_consumption.tail())

# Pivot tablo oluşturma
pivot = df.pivot_table(index='Country', columns='Year', values='Water Scarcity Level', aggfunc=lambda x: x.mode()[0] if not x.mode().empty else None)
print(pivot)

# Her Bölgedeki en yüksek su tüketen ülke
last_year = df['Year'].max()
most_consuming_per_region = df[df['Year']==last_year].groupby('region').apply(lambda x: x.loc[x['Total Water Consumption (Billion Cubic Meters)'].idxmax()][['Country','Total Water Consumption (Billion Cubic Meters)']])
print(most_consuming_per_region)

# Su kullanım türlerinin yıllara göre dağılımı
su_turu_pivot = df.groupby('Year')[['Agricultural Water Use (%)','Industrial Water Use (%)','Household Water Use (%)']].mean()
su_turu_pivot.plot(kind='bar', stacked=True, figsize=(12,6))
plt.title('Yıllara Göre Su Kullanım Türlerinin Payı')
plt.ylabel('Oran (%)')
plt.show()

# Bölge bazında kişi başına su kullanımı analizi
region_consumption = df.groupby('region')['Per Capita Water Use (Liters per Day)'].mean().sort_values(ascending=False)
print(region_consumption)

# Veri doğrulama: Su kullanım türlerinin toplamı %100 olmalı
df['check'] = df['Agricultural Water Use (%)'] + df['Industrial Water Use (%)'] + df['Household Water Use (%)']
print(df[['Country','Year','check']].head())
"""