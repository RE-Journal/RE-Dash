import mysql.connector
from mysql.connector import Error
import pandas as pd



def get_lease_start_rent_by_submarket(selected_quarters):
    try:
        connection = mysql.connector.connect(
            host='193.203.184.1',
            user='u661384233_dbuser',
            password='Rejournal@123',
            database='u661384233_rejournal'
        )
        if connection.is_connected():
            # First, let's get the column names
            cursor = connection.cursor()
            cursor.execute("DESCRIBE leases")
            columns = [column[0] for column in cursor.fetchall()]
            cursor.close()

            # Find the column that likely represents the lease start rent
            rent_column = next((col for col in columns if 'rent' in col.lower() and 'start' in col.lower()), None)

            if not rent_column:
                print("Could not find a suitable column for lease start rent.")
                return []

            quarters_condition = "AND CONCAT(lease_start_year, ' Q', lease_start_qtr) IN ({})".format(
                ','.join(['%s'] * len(selected_quarters))
            ) if selected_quarters else ""
            
            query = f"""
            SELECT 
                CONCAT(lease_start_year, ' Q', lease_start_qtr) AS Quarter,
                COALESCE(submarket, 'Unknown') AS SUBMARKET,
                AVG({rent_column}) AS Average_Rent
            FROM leases
            WHERE {rent_column} IS NOT NULL
                AND lease_start_year IS NOT NULL
                AND lease_start_qtr IS NOT NULL
                AND submarket IS NOT NULL
                {quarters_condition}
            GROUP BY lease_start_year, lease_start_qtr, submarket
            ORDER BY lease_start_year, lease_start_qtr, SUBMARKET
            """
            
            df = pd.read_sql(query, connection, params=selected_quarters)
            
            if df.empty:
                print("No data returned from the query.")
                return []
            
            df['Average_Rent'] = df['Average_Rent'].round(2)
            
            return df.to_dict('records')
    except Error as e:
        print(f"Error: {e}")
        return []
    finally:
        if connection.is_connected():
            connection.close()

def get_average_monthly_rental_trend(selected_quarters):
    try:
        connection = mysql.connector.connect(
            host='193.203.184.1',
            user='u661384233_dbuser',
            password='Rejournal@123',
            database='u661384233_rejournal'
        )
        if connection.is_connected():
            # First, let's get the column names
            cursor = connection.cursor()
            cursor.execute("DESCRIBE leases")
            columns = [column[0] for column in cursor.fetchall()]
            cursor.close()

            # Find the column that likely represents the lease start rent
            rent_column = next((col for col in columns if 'rent' in col.lower() and 'start' in col.lower()), None)

            if not rent_column:
                print("Could not find a suitable column for lease start rent.")
                return []

            quarters_condition = "AND CONCAT(lease_start_year, ' Q', lease_start_qtr) IN ({})".format(
                ','.join(['%s'] * len(selected_quarters))
            ) if selected_quarters else ""
            
            query = f"""
            SELECT 
                CONCAT(lease_start_year, ' Q', lease_start_qtr) AS Quarter,
                AVG({rent_column}) AS Average_Rent
            FROM leases
            WHERE {rent_column} IS NOT NULL
                AND lease_start_year IS NOT NULL
                AND lease_start_qtr IS NOT NULL
                {quarters_condition}
            GROUP BY lease_start_year, lease_start_qtr
            ORDER BY lease_start_year, lease_start_qtr
            """
            
            df = pd.read_sql(query, connection, params=selected_quarters)
            
            if df.empty:
                print("No data returned from the query.")
                return []
            
            df['Average_Rent'] = df['Average_Rent'].round(2)
            
            return df.to_dict('records')
    except Error as e:
        print(f"Error: {e}")
        return []
    finally:
        if connection.is_connected():
            connection.close()


def get_available_quarters():
    try:
        connection = mysql.connector.connect(
            host='193.203.184.1',
            user='u661384233_dbuser',
            password='Rejournal@123',
            database='u661384233_rejournal'
        )
        if connection.is_connected():
            query = """
            SELECT DISTINCT CONCAT(lease_start_year, ' Q', lease_start_qtr) AS quarter
            FROM leases
            WHERE lease_start_year IS NOT NULL AND lease_start_qtr IS NOT NULL
            ORDER BY lease_start_year DESC, lease_start_qtr DESC
            LIMIT 8  -- Limit to the last 8 quarters for better usability
            """
            
            df = pd.read_sql(query, connection)
            
            if df.empty:
                print("No available quarters found.")
                return []
            
            return df['quarter'].tolist()
    except Error as e:
        print(f"Error: {e}")
        return []
    finally:
        if connection.is_connected():
            connection.close()

def get_tenant_sector_data():
    try:
        connection = mysql.connector.connect(
            host='193.203.184.1',
            user='u661384233_dbuser',
            password='Rejournal@123',
            database='u661384233_rejournal'
        )

        if connection.is_connected():
            query = """
            SELECT tenant_sector, SUM(area_transcatedsq_ft) as total_area 
            FROM leases 
            WHERE tenant_sector IS NOT NULL AND tenant_sector != '' 
            GROUP BY tenant_sector 
            ORDER BY total_area DESC

            """
            
            df = pd.read_sql(query, connection)
            
            # Check if the dataframe is empty
            if df.empty:
                print("No data returned from the query.")
                return []
            
            # Calculate the total area
            total_area = df['total_area'].sum()
            
            # Check if total_area is zero
            if total_area == 0:
                print("Total area is zero. Cannot calculate percentages.")
                return []
            
            # Calculate the percentage and format the data for the pie chart
            chart_data = df.apply(lambda row: {
                "id": row['tenant_sector'],
                "label": row['tenant_sector'],
                "value": round(row['total_area'] / total_area * 100, 2),
                "color": f"hsl({hash(row['tenant_sector']) % 360}, 70%, 50%)"
            }, axis=1).tolist()
            
            return chart_data

    except Error as e:
        print(f"Error: {e}")
        return []

    finally:
        if connection.is_connected():
            connection.close()


def get_qoq_leasing_data():
    try:
        connection = mysql.connector.connect(
            host='193.203.184.1',
            user='u661384233_dbuser',
            password='Rejournal@123',
            database='u661384233_rejournal'
        )
        if connection.is_connected():
            query = """
            SELECT 
                CONCAT(lease_start_year, ' Q', lease_start_qtr) AS Quarter,
                SUM(area_transcatedsq_ft) / 1000000 AS Area_Leased_in_mln_sft
            FROM 
                leases
            WHERE 
                lease_start_year IS NOT NULL 
                AND lease_start_qtr IS NOT NULL
                AND area_transcatedsq_ft IS NOT NULL
            GROUP BY 
                lease_start_year, lease_start_qtr
            ORDER BY 
                lease_start_year, lease_start_qtr
            LIMIT 8  -- Limit to the last 8 quarters for better visualization
            """
           
            df = pd.read_sql(query, connection)
           
            # Check if the dataframe is empty
            if df.empty:
                print("No data returned from the query.")
                return []
            df['Area_Leased_in_mln_sft'] = df['Area_Leased_in_mln_sft'].round(2)
    
            # Format the data for the chart
            chart_data = df.to_dict('records')
           
            return chart_data
    except Error as e:
        print(f"Error: {e}")
        return []
    finally:
        if connection.is_connected():
            connection.close()
            
def get_area_leased_by_sector():
    try:
        connection = mysql.connector.connect(
            host='193.203.184.1',
            user='u661384233_dbuser',
            password='Rejournal@123',
            database='u661384233_rejournal'
        )
        if connection.is_connected():
            query = """
            SELECT 
                COALESCE(project_category, 'Unknown') AS sector,
                SUM(area_transcatedsq_ft) / 1000000 AS area_leased_mln
            FROM leases
            GROUP BY project_category
            ORDER BY area_leased_mln DESC
            LIMIT 10  -- Limiting to top 10 sectors for better visualization
            """
            
            df = pd.read_sql(query, connection)
            
            if df.empty:
                print("No data returned from the query.")
                return [], 0
            
            total_area = df['area_leased_mln'].sum()
            
            chart_data = df.apply(lambda row: {
                "id": row['sector'],
                "label": row['sector'],
                "value": row['area_leased_mln'],
                "formattedValue": f"{row['area_leased_mln']:.2f}M ({row['area_leased_mln']/total_area*100:.2f}%)"
            }, axis=1).tolist()
            
            return chart_data, total_area
    except Error as e:
        print(f"Error: {e}")
        return [], 0
    finally:
        if connection.is_connected():
            connection.close()
            
            
def get_security_deposit_data():
    try:
        connection = mysql.connector.connect(
            host='193.203.184.1',
            user='u661384233_dbuser',
            password='Rejournal@123',
            database='u661384233_rejournal'
        )
        if connection.is_connected():
            query = """
            SELECT 
                COALESCE(submarket, 'Unknown') AS SUBMARKET,
                AVG(security_deposit_months) AS SECURITY_DEPOSIT
            FROM leases
            WHERE security_deposit_months IS NOT NULL
            GROUP BY submarket
            ORDER BY SECURITY_DEPOSIT DESC
            """
            
            df = pd.read_sql(query, connection)
            
            if df.empty:
                print("No data returned from the query.")
                return []
            
            # Round the security deposit to 1 decimal place
            df['SECURITY_DEPOSIT'] = df['SECURITY_DEPOSIT'].round(1)
            
            # Convert DataFrame to list of dictionaries
            chart_data = df.to_dict('records')
            
            return chart_data
    except Error as e:
        print(f"Error: {e}")
        return []
    finally:
        if connection.is_connected():
            connection.close()
            
def get_leased_area_expiry_data():
    try:
        connection = mysql.connector.connect(
            host='193.203.184.1',
            user='u661384233_dbuser',
            password='Rejournal@123',
            database='u661384233_rejournal'
        )
        if connection.is_connected():
            query = """
            SELECT 
                lease_expiry_year AS expiry_year,
                SUM(area_transcatedsq_ft) / 1000000 AS area_mln_sqft
            FROM leases
            WHERE lease_expiry_year IS NOT NULL
                AND lease_expiry_year BETWEEN YEAR(CURDATE()) AND 2039
            GROUP BY lease_expiry_year
            ORDER BY expiry_year
            """
            
            df = pd.read_sql(query, connection)
            
            if df.empty:
                print("No data returned from the query.")
                return []
            
            chart_data = df.to_dict('records')
            return chart_data
    except Error as e:
        print(f"Error: {e}")
        return []
    finally:
        if connection.is_connected():
            connection.close()
            
            
            
def get_tenant_sector_share_data():
    try:
        connection = mysql.connector.connect(
            host='193.203.184.1',
            user='u661384233_dbuser',
            password='Rejournal@123',
            database='u661384233_rejournal'
        )
        if connection.is_connected():
            query = """
            SELECT 
                CONCAT(lease_start_year, ' Q', lease_start_qtr) AS quarter,
                tenant_sector,
                SUM(area_transcatedsq_ft) AS area_leased_sqft
            FROM leases
            WHERE lease_start_year IS NOT NULL 
                AND lease_start_qtr IS NOT NULL
                AND tenant_sector IS NOT NULL
                AND tenant_sector != ''
            GROUP BY lease_start_year, lease_start_qtr, tenant_sector
            ORDER BY lease_start_year DESC, lease_start_qtr DESC
            LIMIT 16  -- This will give us data for the last 2 quarters
            """
            
            df = pd.read_sql(query, connection)
            
            if df.empty:
                print("No data returned from the query.")
                return []
            
            # Calculate percentage for each sector within each quarter
            df['percentage'] = df.groupby('quarter')['area_leased_sqft'].transform(lambda x: x / x.sum() * 100)
            
            chart_data = df.to_dict('records')
            return chart_data
    except Error as e:
        print(f"Error: {e}")
        return []
    finally:
        if connection.is_connected():
            connection.close()
            
            
def get_area_sold_by_submarket():
    try:
        connection = mysql.connector.connect(
            host='193.203.184.1',
            user='u661384233_dbuser',
            password='Rejournal@123',
            database='u661384233_rejournal'
        )
        if connection.is_connected():
            query = """
            SELECT 
                submarket,
                SUM(area_sold_sq_ft) as total_area_sold
            FROM sales
            WHERE submarket IS NOT NULL AND submarket != ''
            GROUP BY submarket
            ORDER BY total_area_sold DESC
            """
            
            df = pd.read_sql(query, connection)
            
            if df.empty:
                print("No data returned from the query.")
                return []
            
            total_area = df['total_area_sold'].sum()
            df['percentage'] = df['total_area_sold'] / total_area * 100
            
            chart_data = df.to_dict('records')
            return chart_data
    except Error as e:
        print(f"Error: {e}")
        return []
    finally:
        if connection.is_connected():
            connection.close()

def get_area_sold_by_quarter():
    try:
        connection = mysql.connector.connect(
            host='193.203.184.1',
            user='u661384233_dbuser',
            password='Rejournal@123',
            database='u661384233_rejournal'
        )
        if connection.is_connected():
            query = """
            SELECT 
                CONCAT(sale_year, ' Q', sale_qtr) as sale_quarter,
                SUM(area_sold_sq_ft) / 1000000 as area_sold_mln_sqft
            FROM sales
            GROUP BY sale_year, sale_qtr
            ORDER BY sale_year DESC, sale_qtr DESC
            LIMIT 2
            """
            
            df = pd.read_sql(query, connection)
            
            if df.empty:
                print("No data returned from the query.")
                return []
            
            chart_data = df.to_dict('records')
            return chart_data
    except Error as e:
        print(f"Error: {e}")
        return []
    finally:
        if connection.is_connected():
            connection.close()

def get_sales_by_buyer_type():
    try:
        connection = mysql.connector.connect(
            host='193.203.184.1',
            user='u661384233_dbuser',
            password='Rejournal@123',
            database='u661384233_rejournal'
        )
        if connection.is_connected():
            query = """
            SELECT 
                buyer_type,
                SUM(area_sold_sq_ft) as total_area_sold,
                SUM(total_value_inr) as total_value
            FROM sales
            WHERE buyer_type IS NOT NULL AND buyer_type != ''
            GROUP BY buyer_type
            """
            
            df = pd.read_sql(query, connection)
            
            if df.empty:
                print("No data returned from the query.")
                return []
            
            chart_data = df.to_dict('records')
            return chart_data
    except Error as e:
        print(f"Error: {e}")
        return []
    finally:
        if connection.is_connected():
            connection.close()

def get_completion_status_options():
    try:
        connection = mysql.connector.connect(
            host='193.203.184.1',
            user='u661384233_dbuser',
            password='Rejournal@123',
            database='u661384233_rejournal'
        )
        if connection.is_connected():
            query = """
            SELECT DISTINCT completion_status
            FROM projects
            WHERE completion_status IS NOT NULL AND completion_status != ''
            """
            
            df = pd.read_sql(query, connection)
            
            if df.empty:
                print("No completion status options found.")
                return []
            
            return df['completion_status'].tolist()
    except Error as e:
        print(f"Error: {e}")
        return []
    finally:
        if connection.is_connected():
            connection.close()

def get_property_area_by_submarket(selected_statuses):
    try:
        connection = mysql.connector.connect(
            host='193.203.184.1',
            user='u661384233_dbuser',
            password='Rejournal@123',
            database='u661384233_rejournal'
        )
        if connection.is_connected():
            status_condition = "AND completion_status IN ({})".format(
                ','.join(['%s'] * len(selected_statuses))
            ) if selected_statuses else ""
            
            query = f"""
            SELECT 
                submarket AS SUBMARKET,
                SUM(property_area_in_sqft) / 1000000 AS PROPERTY_AREA
            FROM projects
            WHERE submarket IS NOT NULL AND submarket != ''
                AND property_area_in_sqft IS NOT NULL
                {status_condition}
            GROUP BY submarket
            ORDER BY PROPERTY_AREA DESC
            LIMIT 10
            """
            
            df = pd.read_sql(query, connection, params=selected_statuses)
            
            if df.empty:
                print("No data returned from the query.")
                return []
            
            return df.to_dict('records')
    except Error as e:
        print(f"Error: {e}")
        return []
    finally:
        if connection.is_connected():
            connection.close()

def get_office_stock_by_completion_year(selected_statuses):
    try:
        connection = mysql.connector.connect(
            host='193.203.184.1',
            user='u661384233_dbuser',
            password='Rejournal@123',
            database='u661384233_rejournal'
        )
        if connection.is_connected():
            status_condition = "AND completion_status IN ({})".format(
                ','.join(['%s'] * len(selected_statuses))
            ) if selected_statuses else ""
            
            query = f"""
            SELECT 
                completion_year AS COMPLETION_YEAR,
                SUM(property_area_in_sqft) / 1000000 AS OFFICE_STOCK
            FROM projects
            WHERE completion_year IS NOT NULL
                AND property_area_in_sqft IS NOT NULL
                AND completion_year >= 2008
                {status_condition}
            GROUP BY completion_year
            ORDER BY completion_year
            """
            
            df = pd.read_sql(query, connection, params=selected_statuses)
            
            if df.empty:
                print("No data returned from the query.")
                return []
            
            # Calculate cumulative sum of office stock
            df['CUMULATIVE_OFFICE_STOCK'] = df['OFFICE_STOCK'].cumsum()
            
            return df.to_dict('records')
    except Error as e:
        print(f"Error: {e}")
        return []
    finally:
        if connection.is_connected():
            connection.close()
            

