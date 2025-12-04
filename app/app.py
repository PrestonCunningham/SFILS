from db import get_connection

MENU = """
=========================================================
 SFILS Database Application
=========================================================
1. Show total patrons by type
2. Show total checkouts by library branch
3. Show patron distribution inside vs outside SF County
4. Show checkouts by age range
5. Exit
=========================================================
Choose an option: """


def query_patron_type_stats(cur):
    sql = """
    SELECT
        pt.patron_type_definition,
        COUNT(*) AS num_patrons
    FROM usage_fact u
    JOIN patron_type pt USING (patron_type_code)
    GROUP BY pt.patron_type_definition
    ORDER BY num_patrons DESC;
    """
    cur.execute(sql)
    rows = cur.fetchall()
    print("\nPatrons by Type:")
    print("====================")
    for r in rows:
        print(f"{r[0]:25} : {r[1]}")
    print()


def query_branch_checkouts(cur):
    sql = """
    SELECT
        lb.home_library_definition,
        SUM(u.checkout_total) AS total_checkouts
    FROM usage_fact u
    JOIN library_branch lb USING (home_library_code)
    GROUP BY lb.home_library_definition
    ORDER BY total_checkouts DESC;
    """
    cur.execute(sql)
    rows = cur.fetchall()
    print("\nCheckouts by Library Branch:")
    print("==================")
    for r in rows:
        branch = r[0] if r[0] else "(Unknown Branch)"
        print(f"{branch:30} : {r[1]}")
    print()


def query_county_distribution(cur):
    sql = """
    SELECT
        CASE
            WHEN within_sf_county = 1 THEN 'Within SF County'
            ELSE 'Outside SF County'
        END AS county_status,
        COUNT(*) AS num_patrons,
        SUM(checkout_total) AS total_checkouts
    FROM usage_fact
    GROUP BY within_sf_county;
    """
    cur.execute(sql)
    rows = cur.fetchall()
    print("\nSF County Distribution:")
    print("====================")
    for r in rows:
        print(f"{r[0]:22} | Patrons: {r[1]:6} | Checkouts: {r[2]}")
    print()


def query_age_range_stats(cur):
    sql = """
    SELECT
        ar.age_range_label,
        SUM(u.checkout_total) AS total_checkouts
    FROM usage_fact u
    JOIN age_range ar USING (age_range_id)
    GROUP BY ar.age_range_label
    ORDER BY total_checkouts DESC;
    """
    cur.execute(sql)
    rows = cur.fetchall()
    print("\nCheckouts by Age Range:")
    print("====================")
    for r in rows:
        label = r[0] if r[0] else "(Unknown)"
        print(f"{label:20} : {r[1]}")
    print()


def main():
    conn = get_connection()
    cur = conn.cursor()

    while True:
        choice = input(MENU).strip()

        if choice == "1":
            query_patron_type_stats(cur)
        elif choice == "2":
            query_branch_checkouts(cur)
        elif choice == "3":
            query_county_distribution(cur)
        elif choice == "4":
            query_age_range_stats(cur)
        elif choice == "5":
            print("Exiting app...\n")
            break
        else:
            print("Invalid option. Try again.\n")

    cur.close()
    conn.close()


if __name__ == "__main__":
    main()
