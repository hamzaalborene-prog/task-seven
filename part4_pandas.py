import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

الاتصال = sqlite3.connect("store.db")

# جلب إجمالي الإيراد لكل منتج مباشرة إلى DataFrame
استعلام_الإيراد = """
SELECT p.product_name,
       SUM(s.quantity * p.price) AS total_revenue
FROM sales AS s
INNER JOIN products AS p
    ON s.product_id = p.product_id
GROUP BY p.product_id, p.product_name
ORDER BY total_revenue DESC
"""
الإيرادات = pd.read_sql_query(استعلام_الإيراد, الاتصال)
print("إجمالي الإيراد لكل منتج:")
print(الإيرادات.to_string(index=False))

# رسم أعلى خمسة منتجات من ناحية الإيراد
أعلى_خمسة = الإيرادات.head(5)
أعلى_خمسة.plot(
    kind="bar",
    x="product_name",
    y="total_revenue",
    legend=False,
    title="Top 5 Products by Revenue"
)
plt.xlabel("Product")
plt.ylabel("Total Revenue")
plt.xticks(rotation=30, ha="right")
plt.tight_layout()
plt.savefig("top_5_revenue.png", dpi=150)
plt.show()

# حساب المجموع اليومي ثم المجموع التراكمي
استعلام_التراكمي = """
SELECT sale_date,
       SUM(quantity) AS daily_quantity,
       SUM(SUM(quantity)) OVER (
           ORDER BY sale_date
           ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
       ) AS running_total
FROM sales
GROUP BY sale_date
ORDER BY sale_date
"""
التراكمي = pd.read_sql_query(استعلام_التراكمي, الاتصال)
print("\nالمجموع التراكمي حسب التاريخ:")
print(التراكمي.to_string(index=False))

# رسم المجموع التراكمي عبر الوقت
plt.figure(figsize=(9, 5))
plt.plot(التراكمي["sale_date"], التراكمي["running_total"], marker="o")
plt.title("Cumulative Sales Over Time")
plt.xlabel("Sale Date")
plt.ylabel("Running Total")
plt.xticks(rotation=30, ha="right")
plt.grid(True)
plt.tight_layout()
plt.savefig("cumulative_sales.png", dpi=150)
plt.show()

الاتصال.close()
print("الاتجاه التراكمي تصاعدي أو ثابت؛ لأنه يجمع كميات المبيعات مع مرور الوقت.")
