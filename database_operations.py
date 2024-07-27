# database_operations.py

from db_manager import db_manager
import pandas as pd

def get_security_deposit_data():
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
    
    df = db_manager.execute_query_pandas(query)
    
    if df.empty:
        print("No data returned from the query.")
        return []
    
    df['SECURITY_DEPOSIT'] = df['SECURITY_DEPOSIT'].round(1)
    
    return df.to_dict('records')

def get_tenant_origin_share_data():
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
    
    df = db_manager.execute_query_pandas(query)
    
    if df.empty:
        print("No data returned from the query.")
        return []
    
    total_area = df['Area_Leased_Mln_Sqft'].sum()
    df['Percentage'] = (df['Area_Leased_Mln_Sqft'] / total_area * 100).round(2)
    
    return df.to_dict('records')

def get_area_tenant_sector_share_data():
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
    
    df = db_manager.execute_query_pandas(query)
    
    if df.empty:
        print("No data returned from the query.")
        return []
    
    total_area = df['Area_Leased_Mln_Sqft'].sum()
    df['Percentage'] = (df['Area_Leased_Mln_Sqft'] / total_area * 100).round(1)
    
    return df.to_dict('records')

def get_area_leased_by_submarket():
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
    
    df = db_manager.execute_query_pandas(query)
    
    if df.empty:
        print("No data returned from the query.")
        return []
    
    total_area = df['Area_Leased_Mln_Sqft'].sum()
    df['Percentage'] = (df['Area_Leased_Mln_Sqft'] / total_area * 100).round(1)
    
    return df.to_dict('records')

def get_tenant_sector_share_data():
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
    ORDER BY lease_start_qtr, Percentage ASC
    """
   
    df = db_manager.execute_query_pandas(query)
   
    if df.empty:
        print("No data returned from the query.")
        return []
   
    df['Order'] = df.groupby('Quarter').cumcount()
    return df.to_dict('records')

def get_quarterly_leasing_trend():
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
    
    df = db_manager.execute_query_pandas(query)
    
    if df.empty:
        print("No data returned from the query.")
        return []
    
    return df.to_dict('records')

def get_lease_start_rent_by_submarket():
    query = """
    SELECT 
        submarket AS SUBMARKET,
        CONCAT(lease_start_year, lease_start_qtr) AS Quarter,
        AVG(lease_start_rent_on_leasable_inr_psf) AS Average_Rent
    FROM leases
    WHERE submarket IS NOT NULL 
        AND lease_start_rent_on_leasable_inr_psf IS NOT NULL
        AND lease_start_year = 2024
        AND lease_start_qtr IN (1, 2)
    GROUP BY submarket, lease_start_year, lease_start_qtr
    ORDER BY submarket, lease_start_year, lease_start_qtr
    """
    
    df = db_manager.execute_query_pandas(query)
    
    if df.empty:
        print("No data returned from the query.")
        return []
    
    return df.to_dict('records')

def get_area_leased_by_sector():
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
    
    df = db_manager.execute_query_pandas(query)
    
    if df.empty:
        print("No data returned from the query.")
        return []
    
    total_area = df['Area_Leased_Mln_Sqft'].sum()
    df['Percentage'] = (df['Area_Leased_Mln_Sqft'] / total_area * 100).round(1)
    
    return df.to_dict('records')

def get_average_monthly_rental_trend():
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
    
    df = db_manager.execute_query_pandas(query)
    
    if df.empty:
        print("No data returned from the query.")
        return []
    
    return df.to_dict('records')

def get_available_quarters():
    query = """
    SELECT DISTINCT CONCAT(lease_start_year, ' Q', lease_start_qtr) AS quarter
    FROM leases
    WHERE lease_start_year IS NOT NULL AND lease_start_qtr IS NOT NULL
    ORDER BY lease_start_year DESC, lease_start_qtr DESC
    LIMIT 8
    """
    
    df = db_manager.execute_query_pandas(query)
    
    if df.empty:
        print("No available quarters found.")
        return []
    
    return df['quarter'].tolist()

def get_qoq_leasing_data():
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
    LIMIT 8
    """
   
    df = db_manager.execute_query_pandas(query)
   
    if df.empty:
        print("No data returned from the query.")
        return []
    
    df['Area_Leased_in_mln_sft'] = df['Area_Leased_in_mln_sft'].round(2)
    return df.to_dict('records')

def get_leased_area_expiry_data():
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
    
    df = db_manager.execute_query_pandas(query)
    
    if df.empty:
        print("No data returned from the query.")
        return []
    
    return df.to_dict('records')

def get_area_sold_by_submarket():
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
   
    df = db_manager.execute_query_pandas(query)
   
    if df.empty:
        print("No data returned from the query.")
        return []
   
    total_area = df['total_area_sold'].sum()
    df['percentage'] = (df['total_area_sold'] / total_area * 100).round(2)
   
    return df.to_dict('records')

def get_area_sold_by_quarter():
    query = """
    SELECT
        CONCAT('', sale_qtr) as QTR,
        SUM(area_sold_sqft) as total_area_sold
    FROM sales
    WHERE sale_year = 2024 AND sale_qtr IN (1, 2)
    GROUP BY sale_qtr
    ORDER BY sale_qtr
    """
   
    df = db_manager.execute_query_pandas(query)
   
    if df.empty:
        print("No data returned from the query.")
        return None
   
    total_area = df['total_area_sold'].sum()
    df['percentage'] = (df['total_area_sold'] / total_area * 100).round(1)
   
    return df.to_dict('records')

def get_sales_by_buyer_type():
    query = """
    SELECT 
        buyer_type,
        SUM(area_sold_sqft) as total_area_sold,
        SUM(total_value_inr) as total_value
    FROM sales
    WHERE buyer_type IS NOT NULL AND buyer_type != ''
    GROUP BY buyer_type
    """
    
    df = db_manager.execute_query_pandas(query)
    
    if df.empty:
        print("No data returned from the query.")
        return []
    
    return df.to_dict('records')

# database_operations.py (continued)

def get_completion_status_options():
    query = """
    SELECT DISTINCT completion_status
    FROM projects
    WHERE completion_status IS NOT NULL AND completion_status != ''
    """
    
    df = db_manager.execute_query_pandas(query)
    
    if df.empty:
        print("No completion status options found.")
        return []
    
    return df['completion_status'].tolist()

def get_property_area_by_submarket(selected_statuses):
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
    
    df = db_manager.execute_query_pandas(query, params=selected_statuses if selected_statuses else None)
    
    if df.empty:
        print("No data returned from the query.")
        return []
    
    return df.to_dict('records')

def get_office_stock_by_completion_year(selected_statuses):
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
    
    df = db_manager.execute_query_pandas(query, params=selected_statuses if selected_statuses else None)
    
    if df.empty:
        print("No data returned from the query.")
        return []
    
    df['CUMULATIVE_OFFICE_STOCK'] = df['OFFICE_STOCK'].cumsum()
    
    return df.to_dict('records')

def get_submarket_data():
    query = """
    SELECT 
        submarket as label,
        SUM(area_transcatedsq_ft) as total_area
    FROM leases
    WHERE lease_start_year = 2024 AND lease_start_qtr IN (1, 2)
    GROUP BY submarket
    """
    df = db_manager.execute_query_pandas(query)
    if df is not None and not df.empty:
        df['percentage'] = (df['total_area'] / df['total_area'].sum() * 100).round(2)
        return df.to_dict('records')
    return None

def get_tenant_origin_data():
    query = """
    SELECT 
        tenant_origin_continent as label,
        SUM(area_transcatedsq_ft) as total_area
    FROM leases
    WHERE lease_start_year = 2024 AND lease_start_qtr IN (1, 2)
    GROUP BY tenant_origin_continent
    """
    df = db_manager.execute_query_pandas(query)
    if df is not None and not df.empty:
        df['percentage'] = (df['total_area'] / df['total_area'].sum() * 100).round(2)
        return df.to_dict('records')
    return None