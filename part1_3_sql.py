import sqlite3

# الاتصال بقاعدة البيانات التي أُنشئت في المهمة السابقة
الاتصال = sqlite3.connect("store.db")
الاتصال.row_factory = sqlite3.Row
مؤشر = الاتصال.cursor()

def عرض_النتيجة(العنوان, الاستعلام):
    print("\n" + "=" * 65)
    print(العنوان)
    print("=" * 65)
    مؤشر.execute(الاستعلام)
    النتائج = مؤشر.fetchall()
    if not النتائج:
        print("لا توجد نتائج.")
    for صف in النتائج:
        print(dict(صف))

# الجزء الأول: JOIN

عرض_النتيجة("1. INNER JOIN: اسم المنتج والكمية وتاريخ البيع", """
SELECT p.product_name, s.quantity, s.sale_date
FROM sales AS s
INNER JOIN products AS p
    ON s.product_id = p.product_id
ORDER BY s.sale_date, s.sale_id
""")

عرض_النتيجة("2. إجمالي الإيراد لكل منتج", """
SELECT p.product_name,
       SUM(s.quantity * p.price) AS total_revenue
FROM sales AS s
INNER JOIN products AS p
    ON s.product_id = p.product_id
GROUP BY p.product_id, p.product_name
ORDER BY total_revenue DESC
""")

عرض_النتيجة("3. LEFT JOIN: جميع المنتجات وحالة مبيعاتها", """
SELECT p.product_name, s.quantity, s.sale_date
FROM products AS p
LEFT JOIN sales AS s
    ON p.product_id = s.product_id
ORDER BY p.product_name, s.sale_date
""")

عرض_النتيجة("المنتجات التي لم تُبع", """
SELECT p.product_name
FROM products AS p
LEFT JOIN sales AS s
    ON p.product_id = s.product_id
WHERE s.sale_id IS NULL
ORDER BY p.product_name
""")

print("\nالفرق بين INNER JOIN وLEFT JOIN:")
print("INNER JOIN يعرض الصفوف التي لها تطابق في الجدولين فقط.")
print("LEFT JOIN يعرض كل صفوف الجدول الأيسر، وتكون أعمدة الجدول الآخر NULL عند عدم وجود تطابق.")

# الجزء الثاني: Subqueries

عرض_النتيجة("4. المنتجات التي أسعارها أعلى من متوسط أسعار المنتجات", """
SELECT product_name, price
FROM products
WHERE price > (SELECT AVG(price) FROM products)
ORDER BY price DESC
""")

عرض_النتيجة("5. عمليات البيع التي كميتها أعلى من متوسط كميات المبيعات", """
SELECT sale_id, product_id, quantity, sale_date, city
FROM sales
WHERE quantity > (SELECT AVG(quantity) FROM sales)
ORDER BY quantity DESC, sale_id
""")

عرض_النتيجة("6. المنتج أو المنتجات الأعلى سعراً باستخدام Subquery", """
SELECT product_name, price
FROM products
WHERE price = (SELECT MAX(price) FROM products)
""")

print("\nيمكن أيضاً استخدام ORDER BY price DESC LIMIT 1.")
print("الـ Subquery توضح أن السعر يساوي أعلى سعر في جدول المنتجات.")

# الجزء الثالث: Window Functions

عرض_النتيجة("7. ترتيب المنتجات حسب إجمالي الإيراد", """
WITH إيراد_المنتجات AS (
    SELECT p.product_id, p.product_name,
           SUM(s.quantity * p.price) AS total_revenue
    FROM products AS p
    INNER JOIN sales AS s
        ON p.product_id = s.product_id
    GROUP BY p.product_id, p.product_name
)
SELECT product_name, total_revenue,
       RANK() OVER (ORDER BY total_revenue DESC) AS revenue_rank
FROM إيراد_المنتجات
ORDER BY revenue_rank, product_name
""")

عرض_النتيجة("8. أكبر عملية بيع في كل مدينة", """
WITH ترتيب_المبيعات AS (
    SELECT sale_id, product_id, quantity, sale_date, city,
           ROW_NUMBER() OVER (
               PARTITION BY city
               ORDER BY quantity DESC, sale_date, sale_id
           ) AS رقم_الصف
    FROM sales
)
SELECT t.city, p.product_name, t.quantity, t.sale_date
FROM ترتيب_المبيعات AS t
INNER JOIN products AS p
    ON t.product_id = p.product_id
WHERE t.رقم_الصف = 1
ORDER BY t.city
""")

عرض_النتيجة("9. المجموع التراكمي لكميات المبيعات حسب التاريخ", """
SELECT sale_date, quantity,
       SUM(quantity) OVER (
           ORDER BY sale_date, sale_id
           ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
       ) AS running_total
FROM sales
ORDER BY sale_date, sale_id
""")

print("\nالفرق بين GROUP BY وWindow Functions:")
print("GROUP BY يلخص الصفوف ويُنتج صفاً لكل مجموعة.")
print("Window Functions تحسب الترتيب أو المجموع مع الاحتفاظ بتفاصيل الصفوف.")

الاتصال.close()
