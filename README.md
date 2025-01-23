# fetch-takehome

1. Data Exploration

There are many Data Quality issues present in these three datasets.

Starting with the Users table:
1. There is a lot of missing data:
    BIRTH_DATE - 3675 values
    STATE - 4812 values
    LANGUAGE - 30508 values
    GENDER - 5892

2. There are a number of dates that are clearly fake/test dates.
    2 instances of a BIRTH_DATE being 1900-01-01
    A few other dates that are clearly outliers between 1900 and 1940

3. There are many overlapping values for GENDER:
    There is a 'Non-Binary' and a 'non_binary' option that needed to be combined
    These options: nan, prefer_not_to_say, not_listed, unknown, not_specified, My gender isn't listed, and Prefer not to say. All say effectively the same thing.
4. The STATE column had a number of 'NaN' values

The Products table:
1. There is even more missing data. Some of the columns don't need data, like columns CATEGORY_4 and CATEGORY_3. However there were 226474 instances of MANUFACTURER missing, and 226472 instances of BRAND missing. These make up ~25% of the total number of rows. Finally, there were 4025 instances of a missing BARCODE, which I assume to be the primary key of the table. This makes no sense and needs to be handled.
2. There are 215 duplicate rows.
3. There were ~27 duplicate BARCODES.
4. There were 86,900 instances of the value: 'PLACEHOLDER_MANUFACTURER' ~10% of all the products. This would make querying products by manufacturer challenging.
5. Returning back to point 1. above, the 226474 missing manufacturers and the 226472 missing brands actually overlapped perfectly, with only two barcodes having a brand without having a manufacturer.

The Transactions Table:
1. There are 5762 transactions that are missing a BARCODE. This feels like it should be impossible and must be some sort of error.
2. There are 171 duplicate rows
3. FINAL_QUANTITY column has about 25% of the rows where the value is the string 'zero'. This needs to be changed to a float
4. FINAL_SALE has a similar issue where instead of a number or a value at all, about 25% of the rows have an eempty string: '' as the value. Important to note that only a few of the rows had both FINAL_QUANTITY and FINAL_SALE as 0.0 (after cleaning). Most of the rows were either or.

Now for the fixes.

The data cleaning across the three tables was fairly straight forward. I stripped whitespace from string columns, dropped duplicate rows in each table, I filled in missing data when I thought it made sense, and I combined certain values (Non-Binary and non_binary) when it made sense. I didn't feel like it was for me to clean up the rest of the gender column values because it was not important for the ask in part two of this take-home. Normally I would ask someone else for what they thing I should do. I would normally combine all of the values listed above into a 'not_specified' value, so as to protect user privacy and not make decisions for them, while making it easier for us to work with. For columns that had missing data, if it was non-essential to the tasks in part two, I replaced the missing data with a string 'NaN'.

For the Birth_dates in the users table, I graphed the dates on a histogram and felt that the outlier dates that I left in were so small in percentage, that it was okay to leave in.

Several times, I felt compelled to remove data from the tables because the missing data prevented it from being useful. I did so, by making the error data it's own dataframe. I did this with the missing barcode data in the products table, the 'PLACEHOLDER_MANUFACTURER' rows in the products table, the missing brand or manuafacturer rows in the products table, and missing barcode data in the transactions table. For all of these new dataframes, many were so numerous in rows (as much as 11.5% of the total for some) that I felt I could be missing some sort of understanding. I exported all of them as csv's and I would ask for clarity on them before deciding to toss the data.

The last problem that I have, and didn't know how to resolve, was the discrepency between transaction rows where the FINAL_QUANTITY was 0.0 and the transaction rows where the FINAL_SALE was 0.0. I can envision a world in which a transaction was made resulting in a final sale of 0, and I can even see a way where quantity was 0 (like a return of some sort), but because these rows made up such a large part of the dataset, I didn't feel comfortable removing them. If I were to remove both sets of weird 0 values, I would be eliminating 25% of the data, and then 50% of the data. That doesn;t feel acceptable given my level of confusion. I had no other method for replacing the missing data (in the case of FINAL_SALE). I learned a lot about this issue though, specifically that in the case where final quantity was 0, there was always a corresponding row in the table with the same receipt_id, dates, barcode, everything, but with the FINAL_QUANTITY equal to 1.0. This made me think maybe one row is an error and the second, the fix, but why would it be on the same receipt_id? It also could be one, the purchase, and two the return, but thats also quite the assumption. 25% of all the rows were returns? That doesn't make sense.

2. SQL Queries.

1. What are the top 5 Brands by receipts scanned among users 21 and over?
Query:     
    SELECT p.BRAND,
           COUNT(t.receipt_ID) AS receipt_count
    FROM users u
    JOIN transactions t ON u.ID = t.USER_ID
    JOIN products p ON t.BARCODE = p.BARCODE
    WHERE DATE('now') >= DATE(u.BIRTH_DATE, '+21 years')
    GROUP BY p.Brand
    ORDER BY receipt_count DESC
    LIMIT 5

Answer:              BRAND  receipt_count
        0      NERDS CANDY              6
        1             DOVE              6
        2          TRIDENT              4
        3  SOUR PATCH KIDS              4
        4           MEIJER              4

2. What are the top 5 brands by sales among users that have had their account for at least six months?

Query:
    SELECT p.BRAND,
           SUM(t.FINAL_SALE) as total_sales
    FROM users u
    JOIN transactions t ON u.ID = t.USER_ID
    JOIN products p ON t.BARCODE = p.BARCODE
    WHERE DATE('now') >= DATE(u.CREATED_DATE, '+6 months')
    GROUP BY p.BRAND
    ORDER BY total_sales DESC
    LIMIT 5

Answer:
             BRAND  total_sales
    0          CVS        72.00
    1      TRIDENT        46.72
    2         DOVE        42.88
    3  COORS LIGHT        34.96
    4       QUAKER        16.60

3. Which is the leanding brand in the Dips and Salsa category?

I am assuming here that the sum of FINAL_SALE is an accurate representation of money generated, and is therefore fair to compare across other brands.

Query: 
    SELECT p.BRAND,
           SUM(t.FINAL_SALE) as total_sales
    FROM products p
    JOIN transactions t ON p.BARCODE = t.BARCODE
    WHERE p.CATEGORY_2 = 'Dips & Salsa' -- Category 2 is the only on that has Chips and Salsa
    GROUP BY p.BRAND
    ORDER BY total_sales DESC
    LIMIT 1


Answer:
              BRAND  total_sales
        0  TOSTITOS       260.99

There may be some anomalies due to leaving the FINAL_QUANTITY and FINAL_SALE issues alone. 

3. Communicate with stakeholders

    Stakeholders,

    After going through the data provided, I have identified a number of interesting insights as well as a few data quality issues.
    
    Insights:
        1. Our longer-term users tend to spend on CVS products/at CVS.
        Amongst users that have had their accounts for more than 6 months, the most popular brands are CVS, by a landslide, and then Trident, Dove, and Coors Light, followed not so closely by Quaker Oats.

        2. Users 21 and over are spending their money on Candy and wellness products. Nerds Candy and Dove are the most popular, with Trident, Sour Patch, and Meijer close behind. It seems like our users are making small, edible purchases more than large purchases.

        3. Unsuprisingly, Tostitos is leading in the Chips and Salsa category when analyzed through the lens of total sales ($).

    Issues:
        The dataset had a lot of data that needed to be cleaned, but only a couple of large outstanding issues.

        1. I have a number of datasets that have errors in the data. Mostly missing, but a few placeholder values. Would love to get another pair of eyes on it to see if we can clean it up so we can use it.

        2. I am confused as to what the columns FINAL_QUANTITY and FINAL_SALE mean asa result of seeing the data that occupies those columns. Many of the FINAL_SALE values were empty before I assumed them to be 0, and many of the FINAL_QUANTITY values were 'zero'. I definitely need some help parsing what is happening there, as the combination of those two issues comprise 50% of our data.

    Thanks,
        Ryan Hoffman
