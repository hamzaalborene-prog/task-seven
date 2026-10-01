import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

الاتصال = sqlite3.connect("store.db")

# ربط المبيعات بالمنتجات، ثم ترتيب إيراد كل منتج داخل كل مدينة
استعلام = """
WITH إيراد_المنتج_في_المدينة AS (
    SELECT s.city, p.product_id, p.product_name,
           SUM(s.quantity * p.price) AS total_revenue
    FROM sales AS s
    INNER JOIN products AS p
        ON s.product_id = p.product_id
    GROUP BY s.city, p.product_id, p.product_name
)
SELECT city, product_name, total_revenue,
       RANK() OVER (
           PARTITION BY city
           ORDER BY total_revenue DESC
       ) AS revenue_rank
FROM إيراد_المنتج_في_المدينة
ORDER BY city, revenue_rank, product_name
"""

النتيجة = pd.read_sql_query(استعلام, الاتصال)
print("ترتيب المنتجات حسب الإيراد داخل كل مدينة:")
print(النتيجة.to_string(index=False))

# رسم الإيراد لكل منتج في كل مدينة
بيانات_الرسم = النتيجة.pivot(
    index="city",
    columns="product_name",
    values="total_revenue"
).fillna(0)

بيانات_الرسم.plot(kind="bar", figsize=(10, 6))
plt.title("Product Revenue by City")
plt.xlabel("City")
plt.ylabel("Total Revenue")
plt.xticks(rotation=0)
plt.legend(title="Product", bbox_to_anchor=(1.02, 1), loc="upper left")
plt.tight_layout()
plt.savefig("city_product_revenue.png", dpi=150)
plt.show()

الاتصال.close()
print("الرؤية: يمكن مقارنة إيراد المنتجات بين المدن، ومعرفة المنتج الأعلى إيراداً في كل مدينة من خلال عمود الترتيب.")
