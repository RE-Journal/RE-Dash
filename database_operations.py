import mysql.connector
from mysql.connector import Error
import pandas as pd

def get_db_connection():
    return mysql.connector.connect(
        host='193.203.184.1',
        user='u661384233_dbuser',
        password='Rejournal@123',
        database='u661384233_rejournal'
    )

def get_security_deposit_data():
    try:
        connection = get_db_connection()
        if connection.is_connected():
            query = """
            SELECT 
                COALESCE(submarket, 'Unknown') AS SUBMARKET,
                AVG(security_deposit_months) AS SECURITY_DEPOSIT
            FROM leases
            WHERE security_deposit_months IS NOT NULL
                AND lease_start_year = 2024
                AND lease_start_qtr IN (1, 2)
            GROUP BY submarket
            ORDER BY SECURITY_DEPOSIT DESC
            """
            
            df = pd.read_sql(query, connection)
            
            if df.empty:
                print("No data returned from the query.")
                return []
            
            df['SECURITY_DEPOSIT'] = df['SECURITY_DEPOSIT'].round(1)
            
            return df.to_dict('records')
    except Error as e:
        print(f"Error: {e}")
        return []
    finally:
        if connection.is_connected():
            connection.close()

            
def get_tenant_origin_share_data():
    try:
        connection = get_db_connection()
        if connection.is_connected():
            query = """
            SELECT 
                tenant_origin_continent AS Tenant_Origin,
                SUM(leasable_area_sq_ft) / 1000000 AS Area_Leased_Mln_Sqft
            FROM leases
            WHERE lease_start_year = 2024
                AND lease_start_qtr IN (1, 2)
                AND tenant_origin_continent IS NOT NULL AND tenant_origin_continent != ''
            GROUP BY tenant_origin_continent
            ORDER BY Area_Leased_Mln_Sqft DESC
            """
            
            df = pd.read_sql(query, connection)
            
            if df.empty:
                print("No data returned from the query.")
                return []
            
            total_area = df['Area_Leased_Mln_Sqft'].sum()
            df['Percentage'] = (df['Area_Leased_Mln_Sqft'] / total_area * 100).round(2)
            
            return df.to_dict('records')
    except Error as e:
        print(f"Error: {e}")
        return []
    finally:
        if connection.is_connected():
            connection.close()
            
def get_area_tenant_sector_share_data():
    try:
        connection = get_db_connection()
        if connection.is_connected():
            query = """
            SELECT 
                tenant_sector AS Tenant_Sector,
                SUM(leasable_area_sq_ft) / 1000000 AS Area_Leased_Mln_Sqft
            FROM leases
            WHERE lease_start_year = 2024
                AND lease_start_qtr IN (1, 2)
                AND tenant_sector IS NOT NULL AND tenant_sector != ''
            GROUP BY tenant_sector
            ORDER BY Area_Leased_Mln_Sqft DESC
            """
            
            df = pd.read_sql(query, connection)
            
            if df.empty:
                print("No data returned from the query.")
                return []
            
            total_area = df['Area_Leased_Mln_Sqft'].sum()
            df['Percentage'] = (df['Area_Leased_Mln_Sqft'] / total_area * 100).round(1)
            
            return df.to_dict('records')
    except Error as e:
        print(f"Error: {e}")
        return []
    finally:
        if connection.is_connected():
            connection.close()

def get_area_leased_by_submarket():
    try:
        connection = get_db_connection()
        if connection.is_connected():
            query = """
            SELECT 
                submarket AS Submarket,
                SUM(leasable_area_sq_ft) / 1000000 AS Area_Leased_Mln_Sqft
            FROM leases
            WHERE lease_start_year = 2024
                AND lease_start_qtr IN (1, 2)
                AND submarket IS NOT NULL AND submarket != ''
            GROUP BY submarket
            ORDER BY Area_Leased_Mln_Sqft DESC
            """
            
            df = pd.read_sql(query, connection)
            
            if df.empty:
                print("No data returned from the query.")
                return []
            
            total_area = df['Area_Leased_Mln_Sqft'].sum()
            df['Percentage'] = (df['Area_Leased_Mln_Sqft'] / total_area * 100).round(1)
            
            return df.to_dict('records')
    except Error as e:
        print(f"Error: {e}")
        return []
    finally:
        if connection.is_connected():
            connection.close()


def get_tenant_sector_share_data():
    try:
        connection = get_db_connection()
        if connection.is_connected():
            query = """
            SELECT 
                CONCAT('2024 ', lease_start_qtr) AS Quarter,
                tenant_sector AS Tenant_Sector,
                SUM(leasable_area_sq_ft) AS Total_Area,
                (SUM(leasable_area_sq_ft) / SUM(SUM(leasable_area_sq_ft)) OVER (PARTITION BY lease_start_qtr)) * 100 AS Percentage
            FROM leases
            WHERE lease_start_year = 2024
                AND lease_start_qtr IN (1, 2)
                AND tenant_sector IS NOT NULL AND tenant_sector != ''
            GROUP BY lease_start_qtr, tenant_sector
            ORDER BY lease_start_qtr, Percentage DESC
            """
            
            df = pd.read_sql(query, connection)
            
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

def get_quarterly_leasing_trend():
    try:
        connection = get_db_connection()
        if connection.is_connected():
            query = """
            SELECT 
                CONCAT('2024 ', lease_start_qtr) AS Quarter,
                SUM(leasable_area_sq_ft) / 1000000 AS Area_Leased_in_mln_sft
            FROM leases
            WHERE lease_start_year = 2024
                AND lease_start_qtr IN (1, 2)
            GROUP BY lease_start_qtr
            ORDER BY lease_start_qtr
            """
            
            df = pd.read_sql(query, connection)
            
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



def get_lease_start_rent_by_submarket():
    try:
        connection = get_db_connection()
        if connection.is_connected():
            query = """
            SELECT 
                submarket AS SUBMARKET,
                CONCAT(lease_start_year, ' Q', lease_start_qtr) AS Quarter,
                AVG(lease_start_rent_on_leasable_inr_psf) AS Average_Rent
            FROM leases
            WHERE submarket IS NOT NULL 
                AND lease_start_rent_on_leasable_inr_psf IS NOT NULL
                AND lease_start_year = 2024
                AND lease_start_qtr IN (1, 2)
            GROUP BY submarket, lease_start_year, lease_start_qtr
            ORDER BY submarket, lease_start_year, lease_start_qtr
            """
            
            df = pd.read_sql(query, connection)
            
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


def get_area_leased_by_sector():
    try:
        connection = get_db_connection()
        if connection.is_connected():
            query = """
            SELECT 
                project_category AS Project_Category,
                SUM(leasable_area_sq_ft) / 1000000 AS Area_Leased_Mln_Sqft
            FROM leases
            WHERE lease_start_year = 2024
                AND lease_start_qtr IN (1, 2)
                AND project_category IS NOT NULL AND project_category != ''
            GROUP BY project_category
            ORDER BY Area_Leased_Mln_Sqft DESC
            """
            
            df = pd.read_sql(query, connection)
            
            if df.empty:
                print("No data returned from the query.")
                return []
            
            total_area = df['Area_Leased_Mln_Sqft'].sum()
            df['Percentage'] = (df['Area_Leased_Mln_Sqft'] / total_area * 100).round(1)
            
            return df.to_dict('records')
    except Error as e:
        print(f"Error: {e}")
        return []
    finally:
        if connection.is_connected():
            connection.close()




def get_average_monthly_rental_trend():
    try:
        connection = get_db_connection()
        if connection.is_connected():
            query = """
            SELECT 
                CONCAT('2024 ', lease_start_qtr) AS Quarter,
                AVG(average_monthly_rent_on_leasable_inr_psf) AS Average_Rent
            FROM leases
            WHERE lease_start_year = 2024
                AND lease_start_qtr IN (1, 2)
                AND average_monthly_rent_on_leasable_inr_psf IS NOT NULL
            GROUP BY lease_start_qtr
            ORDER BY lease_start_qtr
            """
            
            df = pd.read_sql(query, connection)
            
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
            
            
            

            
            
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_area_sold_by_submarket():
    try:
        connection = get_db_connection()
        if connection.is_connected():
            query = """
            SELECT
                submarket,
                SUM(area_sold_sqft) as total_area_sold
            FROM sales
            WHERE submarket IS NOT NULL AND submarket != ''
                AND sale_year = 2024
                AND sale_qtr IN (1, 2)
            GROUP BY submarket
            ORDER BY total_area_sold DESC
            """
           
            df = pd.read_sql(query, connection)
           
            if df.empty:
                logger.warning("No data returned from the query.")
                return []
           
            total_area = df['total_area_sold'].sum()
            if total_area > 0:
                df['percentage'] = (df['total_area_sold'] / total_area * 100).round(2)
            else:
                logger.warning("Total area sold is zero. Setting all percentages to 0.")
                df['percentage'] = 0
           
            result = df.to_dict('records')
            logger.info(f"Successfully retrieved data for {len(result)} submarkets.")
            return result
    except Error as e:
        logger.error(f"Database error: {e}")
        return []
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return []
    finally:
        if connection and connection.is_connected():
            connection.close()
            logger.debug("Database connection closed.")
import mysql.connector
import pandas as pd

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
                CONCAT('', sale_qtr) as QTR,
                SUM(area_sold_sqft) as total_area_sold
            FROM sales
            WHERE sale_year = 2024 AND sale_qtr IN (1, 2)
            GROUP BY sale_qtr
            ORDER BY sale_qtr
            """
           
            df = pd.read_sql(query, connection)
           
            if df.empty:
                print("No data returned from the query.")
                return None
           
            total_area = df['total_area_sold'].sum()
            df['percentage'] = (df['total_area_sold'] / total_area * 100).round(1)
           
            result = df.to_dict('records')
            return result
   
    except mysql.connector.Error as e:
        print(f"Error: {e}")
        return None
   
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
                SUM(area_sold_sqft) as total_area_sold,
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
            

import pandas as pd
import mysql.connector

def get_db_connection():
    return mysql.connector.connect(
        host='193.203.184.1',
        user='u661384233_dbuser',
        password='Rejournal@123',
        database='u661384233_rejournal'
    )

def execute_query(query):
    try:
        connection = get_db_connection()
        if connection.is_connected():
            df = pd.read_sql(query, connection)
            if df.empty:
                print("No data returned from the query.")
                return None
            return df
    except mysql.connector.Error as e:
        print(f"Error: {e}")
        return None
    finally:
        if connection.is_connected():
            connection.close()

def get_submarket_data():
    query = """
    SELECT 
        submarket as label,
        SUM(area_transcatedsq_ft) as total_area
    FROM leases
    WHERE lease_start_year = 2024 AND lease_start_qtr IN (1, 2)
    GROUP BY submarket
    """
    df = execute_query(query)
    if df is not None:
        df['percentage'] = (df['total_area'] / df['total_area'].sum() * 100).round(2)
    return df


def get_tenant_origin_data():
    query = """
    SELECT 
        tenant_origin_continent as label,
        SUM(area_transcatedsq_ft) as total_area
    FROM leases
    WHERE lease_start_year = 2024 AND lease_start_qtr IN (1, 2)
    GROUP BY tenant_origin_continent
    """
    df = execute_query(query)
    if df is not None:
        df['percentage'] = (df['total_area'] / df['total_area'].sum() * 100).round(2)
    return df
