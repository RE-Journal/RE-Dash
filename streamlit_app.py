import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from io import BytesIO

st.set_page_config(layout="wide")
from database_operations import (
    get_area_leased_by_sector, get_area_tenant_sector_share_data,
    get_security_deposit_data, get_leased_area_expiry_data, get_tenant_sector_share_data,
    get_area_leased_by_submarket, get_area_sold_by_quarter, get_sales_by_buyer_type,
    get_average_monthly_rental_trend, get_lease_start_rent_by_submarket,
    get_quarterly_leasing_trend,get_submarket_data,get_tenant_origin_data,
    get_area_sold_by_submarket, get_tenant_origin_share_data
)

def display_submarket_definition():
    st.markdown("""
    <div class="submarket-definition">
        <h4>Submarket Definition:</h4>
        <p><strong>Prime Axis</strong>: Fort, Nariman Point, Cuffe Parade, Churchgate <strong>|</strong>
        <strong>CentraZone</strong>: Worli, Mahalaxmi, Lower Parel, Prabhadevi, Parel, Dadar, Elphinstone, Byculla, Wadala <strong>|</strong>
        <strong>BKC Nexus</strong>: Bandra Kurla Complex <strong>|</strong>
        <strong>BKC Fringe</strong>: Bandra (E), Kalina, Santacruz, Kalanagar, Bandra (W), Kurla, CST Kalina Road <strong>|</strong>
        <strong>North Vista</strong>: Andheri, Chakala, Jogeshwari, Vile Parle, Saki Naka, JB Nagar, Marol, Saki Vihar Road, Mahakali Caves Road <strong>|</strong>
        <strong>West Haven</strong>: Goregaon, Dindoshi, Malad, Kandivali, Borivali, Oshiwara, Ram Mandir Road <strong>|</strong>
        <strong>East Enclave</strong>: Powai, Vikhroli, LBS Marg, Ghatkopar, Vidyavihar, Mulund, Kanjurmarg, Sion, Chembur, Bhandup <strong>|</strong>
        <strong>Thane Oasis</strong>: Thane, Wagle Estate, Ghodbunder Road, Kolshet, Hiranandani Estates, Panch Pakhadi, Dombivali <strong>|</strong>
        <strong>Harbor City</strong>: Airoli, Mahape, Ghansoli, Koparkhairane, Rabale, Vashi, Kharghar, Turbhe, Sanpada, Juinagar, Nerul, Seawoods, Panvel, CBD Belapur</p>
    </div>
    """, unsafe_allow_html=True)

def display_note(note):
    st.markdown(f"""
    <p style='font-size: 0.9em; color: #666; text-align: center;'>
        <strong>Note: {note}</></strong>
    </p>
    """, unsafe_allow_html=True)

def display_definition(title, definition):
    st.markdown(f"<h4>{title}</h4>", unsafe_allow_html=True)
    st.markdown(f"<p style='font-size: 0.9em;'>{definition}</p>", unsafe_allow_html=True)

# Main header styling
st.markdown("""
<style>
    .main .block-container { padding: 1rem 4rem; }
    .stApp { margin-top: -10px; }
    .stApp > header { background-color: transparent; }
    .main-header { 
        font-size: 3.5rem; 
        font-weight: bold; 
        text-align: center; 
        margin-bottom: 2rem;
        display: flex;
        justify-content: center;
        align-items: center;
    }
    .main-header-text {
        background-image: linear-gradient(to right, #38bdf8, #059669);
        -webkit-background-clip: text;
        background-clip: text;
        color: transparent;
        margin-left: 10px;
    }
</style>
""", unsafe_allow_html=True)

# Display the main title with icon
st.markdown('<h1 class="main-header">🏢<span class="main-header-text">RE Journal Sample Dashboards</span></h1>', unsafe_allow_html=True)
# Dashboard titles and section buttons styling
st.markdown("""
<style>
    .dashboard-title {
        font-size: 1.8rem;
        font-weight: bold;
        text-align: center;
        margin-top: 0.8rem;
        margin-bottom: 1rem;
        display: flex;
        justify-content: center;
        align-items: center;
    }
    .dashboard-title-text {
        color: #333;
        margin-left: 10px;
    }
            
    .stButton > button, .stButton > a {
        width: 100%;
        border-radius: 8px;
        background-color: white;
        color: black;
        border: 3px solid lightgrey;
        padding: 0.7rem 1rem;
        font-weight: bold;
        font-size: 1.3rem !important; 
        transition: all 0.3s ease;
        text-decoration: none;
        display: inline-block;
        text-align: center;
    }
    .stButton > button:hover, .stButton > a:hover {
        background-color: light grey !important;
    }
    .stButton > button:focus, .stButton > a:focus {
        box-shadow: none;
    }
    .chart-container { 
        border: 0.5px solid #e0e0e0; 
        border-radius: 10px; 
        padding: 0.1rem; 
        margin-bottom: 1rem; 
        background-color: light gray; 
        box-shadow: 0 2px 10px rgba(0,0,0,0.05); 
    }
    .chart-title { 
        font-size: 1.2rem; 
        font-weight: bold; 
        text-align: center; 
        margin-bottom: 1rem; 
        color: #333; 
    }
    .footer { 
        text-align: center; 
        color: gray; 
        margin-top: 2rem; 
        border-top: 1px solid #e0e0e0; 
        padding-top: 1rem; 
    }
    .custom-link-button {
        display: inline-block;
        width: 100%;
        border-radius: 8px;
        background-color: white;
        color: black;
        border: 3px solid lightgrey;
        padding: 0.5rem 1rem;
        font-weight: bold;
        font-size: 1.3rem;
        text-align: center;
        text-decoration: none;
        transition: all 0.3s ease;
    }
    .custom-link-button:hover {
        background-color: white;
    }
            
    button {
            font-size : 20px;
            }
    .submarket-definition {
        border: 1px solid #e0e0e0;
        border-radius: 5px;
        padding: 10px;
        margin-bottom: 20px;
        font-size: 0.9em;
        line-height: 1.4;
        background-color: #f9f9f9;
    }
    .submarket-definition h4 {
        margin-top: 0;
        margin-bottom: 10px;
        color: #333;
    }
</style>
""", unsafe_allow_html=True)

# Function to create dashboard titles
def create_dashboard_title(icon, title):
    st.markdown(f'<h2 class="dashboard-title">{icon}<span class="dashboard-title-text">{title}</span></h2>', unsafe_allow_html=True)

# Function to create section buttons
def create_section_button(icon, title):
    return st.button(f"{icon} {title}", key=f"btn_{title.lower().replace(' ', '_')}", use_container_width=True)

def create_centered_heading(title):
    st.markdown(f'<p class="chart-title">{title}</p>', unsafe_allow_html=True)

def chart_with_border(chart_function):
    with st.container():
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        chart_function()
        st.markdown('</div>', unsafe_allow_html=True)


def create_pie_chart(data, labels_col, values_col, percentage_col, title, height=400):
    df = pd.DataFrame(data)
    fig = go.Figure(data=[go.Pie(
        labels=df[labels_col],
        values=df[values_col],
        text=df[percentage_col],
        texttemplate='%{text:.1f}%',
        hovertext=[f"{label}<br>{value:.2f}M ({percent:.1f}%)" 
                   for label, value, percent in zip(df[labels_col], df[values_col], df[percentage_col])],
        textposition='inside',
        hoverinfo='text',
        textinfo='text'
    )])
    fig.update_traces(textfont_size=12, textfont_color='white')
    fig.update_layout(
        height=height,
        legend_title=labels_col.upper(),
        font=dict(family="Arial", size=12),
        legend=dict(
            orientation="v",
            yanchor="top",
            y=1,
            xanchor="left",
            x=1.02,
            itemwidth=30
        ),
        margin=dict(l=20, r=80, t=30, b=20),
        autosize=True
    )
    config = {
        'displayModeBar': False,
        'staticPlot': False,
        'responsive': True
    }
    create_centered_heading(title)
    st.plotly_chart(fig, use_container_width=True, config=config)

def tenant_origin_share_chart():
    
    data = get_tenant_origin_share_data()
    if data:
        create_pie_chart(data, 'Tenant_Origin', 'Area_Leased_Mln_Sqft', 'Percentage', 
                         "🌍 Share of AREA LEASED by TENANT ORIGIN (H124)")
        display_note("APAC indicates all Asia pacific countries excluding India")
    else:
        st.write("No data available for Share of AREA LEASED by TENANT ORIGIN for 2024 H1")

def area_leased_by_submarket_chart():
    data = get_area_leased_by_submarket()
    if data:
        create_pie_chart(data, 'Submarket', 'Area_Leased_Mln_Sqft', 'Percentage', 
                         "🏙️ Share of AREA LEASED by SUBMARKET (H124)")
        display_note("Total or gross leasing included transactions in Grade A office properties only.")

    else:
        st.write("No data available for Share of AREA LEASED by SUBMARKET for 2024 H1")

def area_leased_tenant_sector_share_chart():
    data = get_area_tenant_sector_share_data()
    if data:
        create_pie_chart(data, 'Tenant_Sector', 'Area_Leased_Mln_Sqft', 'Percentage', 
                         "🏢 Share of AREA LEASED by TENANT SECTOR (H124)")
    else:
        st.write("No data available for Share of AREA LEASED by TENANT SECTOR for 2024 H1")

def tenant_sector_share_chart():
    create_centered_heading("🏢 Tenant Sector Share in LEASING (H124)")
    data = get_tenant_sector_share_data()
    if data:
        df = pd.DataFrame(data)
        
        # Ensure the order is maintained
        df = df.sort_values(['Quarter'],ascending=True)
        
        # Create a custom order for Tenant_Sector based on the sorted data
        custom_order = df['Tenant_Sector'].unique()
        
        fig = px.bar(df, x='Quarter', y='Percentage', color='Tenant_Sector',
                     labels={'Percentage': 'Share of Area Leased (%)'},
                     text='Percentage',
                     category_orders={"Tenant_Sector": custom_order})
        
        fig.update_traces(texttemplate='%{text:.1f}%', textposition='inside')
        fig.update_layout(
            xaxis_title="Quarter",
            yaxis_title="Share of Area Leased (%)",
            height=500,
            barmode='stack',
            legend_title="TENANT SECTOR",
            font=dict(family="Arial", size=12),
            yaxis=dict(
                tickformat='.1f',
                range=[0, 100],
                dtick=10,
                tickmode='linear'
            ),
            legend=dict(orientation="v", yanchor="top", y=1, xanchor="left", x=1.02),
            margin=dict(l=50, r=150, t=50, b=50)
        )
        
        fig.update_yaxes(range=[0, 100])
        
        fig.update_traces(hovertemplate='%{y:.2f}%<extra></extra>')
        
        config = {
            'displayModeBar': False,
            'staticPlot': False
        }
        st.plotly_chart(fig, use_container_width=True, config=config)
        
    else:
        st.write("No data available for Tenant Sector share in Leasing for 2024 Q1-Q2")

def quarterly_leasing_trend_chart():
    create_centered_heading("📊 Quarterly Trend in LEASING (H124)")
    data = get_quarterly_leasing_trend()
    if data:
        df = pd.DataFrame(data)
        fig = px.bar(df, x='Quarter', y='Area_Leased_in_mln_sft',
                     labels={'Area_Leased_in_mln_sft': 'Area Leased in mn sft'},
                     text='Area_Leased_in_mln_sft')
        fig.update_traces(texttemplate='%{text:.1f}M', textposition='outside')
        fig.update_layout(
            xaxis_title="Quarter",
            yaxis_title="Area Leased in mn sft",
            height=400,
            font=dict(family="Arial", size=12),
            yaxis=dict(range=[0, max(df['Area_Leased_in_mln_sft']) * 1.1], tickformat='.1f'),
            margin=dict(l=50, r=50, t=50, b=50)
        )
        config = {
            'displayModeBar': False,
            'staticPlot': True
        }
        st.plotly_chart(fig, use_container_width=True, config=config)
    else:
        st.write("No data available for Quarterly Leasing Trend for 2024 Q1-Q2")

def average_monthly_rental_trend_chart():
    create_centered_heading("📈 Average Monthly RENTAL TREND (H124)")
    data = get_average_monthly_rental_trend()
    if data:
        df = pd.DataFrame(data)
        fig = px.bar(df, x='Quarter', y='Average_Rent',
                     labels={'Average_Rent': 'Average Monthly Rent (INR psf)'},
                     text='Average_Rent')
        fig.update_traces(texttemplate='%{text:.0f}', textposition='outside')
        fig.update_layout(
            xaxis_title="Quarter",
            yaxis_title="Average Monthly Rental (INR psf)",
            height=400,
            font=dict(family="Arial", size=12),
            yaxis=dict(range=[0, max(df['Average_Rent']) * 1.1]),
            margin=dict(l=50, r=50, t=50, b=50)
        )
        config = {
            'displayModeBar': False,
            'staticPlot': True
        }
        st.plotly_chart(fig, use_container_width=True, config=config)
        display_note("Average monthly rental indicates city level simple average of rents for the transactions seen in the respective quarters")
    else:
        st.write("No data available for Average Monthly Rental Trend for 2024 Q1-Q2")

def lease_start_rent_by_submarket_chart():
    create_centered_heading("🏙️ Average LEASE START RENT ON LEASABLE by SUBMARKET and QUARTER")
    data = get_lease_start_rent_by_submarket()
    if data:
        df = pd.DataFrame(data)
        fig = px.bar(df, x='SUBMARKET', y='Average_Rent', color='Quarter',
                     labels={'Average_Rent': 'Average Lease Start Rent (INR psf)', 'SUBMARKET': 'Submarket'},
                     text='Average_Rent', barmode='group')
        fig.update_traces(texttemplate='%{text:.0f}', textposition='outside')
        fig.update_layout(
            xaxis_title="Submarket", yaxis_title="Average Lease Start Rent (INR psf)",
            height=500, legend_title="Quarter", xaxis_tickangle=-45,
            font=dict(family="Arial", size=12),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            margin=dict(l=50, r=50, t=80, b=100)
        )
        config = {'displayModeBar': False, 'staticPlot': True}
        st.plotly_chart(fig, use_container_width=True, config=config)
        display_note("Lease start rent at submarket indicates monthly simple average of rents for the transactions seen in the respective quarters.")
    else:
        st.write("No data available for Lease Start Rent by Submarket for 2024 Q1-Q2")

def area_leased_by_sector_chart():
    create_centered_heading("🏢 Area Leased by PROPERTY SECTOR (H124)")
    data = get_area_leased_by_sector()
    if data:
        df = pd.DataFrame(data)
        fig = go.Figure(data=[go.Pie(
            labels=df['Project_Category'],
            values=df['Area_Leased_Mln_Sqft'],
            text=[f"{percent:.1f}%" for percent in df['Percentage']],
            textposition='outside',
            hoverinfo='label+percent',
            textinfo='text'
        )])
        fig.update_traces(textfont_size=12, pull=[0.05] * len(df))
        fig.update_layout(
            height=450,
            legend_title="PROJECT CATEGORY",
            font=dict(family="Arial", size=12),
            legend=dict(orientation="v", yanchor="middle", y=0.9, xanchor="left", x=1),
            margin=dict(l=50, r=150, t=50, b=50)
        )
        config = {
            'displayModeBar': False,
            'staticPlot': False
        }
        st.plotly_chart(fig, use_container_width=True, config=config)
    else:
        st.write("No data available for Area Leased by Property Sector for 2024 H1")


def security_deposit_chart():
    create_centered_heading("🔐 Average SECURITY DEPOSIT (months) by SUBMARKET (H124)")
    data = get_security_deposit_data()
    if data:
        df = pd.DataFrame(data)
        # Round the SECURITY_DEPOSIT to the nearest integer
        df['SECURITY_DEPOSIT'] = df['SECURITY_DEPOSIT'].round().astype(int)
        
        fig = px.bar(df, x='SUBMARKET', y='SECURITY_DEPOSIT',
                     labels={'SECURITY_DEPOSIT': 'Average Security Deposit (months)'},
                     text='SECURITY_DEPOSIT')
        fig.update_traces(texttemplate='%{text}', textposition='outside')
        fig.update_layout(
            xaxis_title="Submarket",
            yaxis_title="Average Security Deposit (months)",
            height=500,
            xaxis_tickangle=-45,
            font=dict(family="Arial", size=12),
            yaxis=dict(range=[0, max(df['SECURITY_DEPOSIT']) * 1.1]),
            margin=dict(l=50, r=50, t=50, b=100)
        )
        config = {'displayModeBar': False, 'staticPlot': True}
        st.plotly_chart(fig, use_container_width=True, config=config)
    else:
        st.write("No data available for Security Deposit by Submarket for 2024 H1")

def leases_page():
    create_dashboard_title("📋", "Leases Dashboard (Mumbai Office)")

    col1, col2 = st.columns(2)
    with col1:
        chart_with_border(area_leased_by_submarket_chart)
    with col2:
        chart_with_border(lambda: area_leased_tenant_sector_share_chart())

    display_submarket_definition()

    col1, col2 = st.columns(2)
    with col1:
        chart_with_border(security_deposit_chart)
    with col2:
        chart_with_border(lambda: tenant_origin_share_chart())

    


    col1, col2 = st.columns(2)
    with col1:
        chart_with_border(area_leased_by_sector_chart)
    with col2:
        chart_with_border(tenant_sector_share_chart)

    col1, col2 = st.columns(2)
    with col1:
        chart_with_border(average_monthly_rental_trend_chart)
    with col2:
        chart_with_border(quarterly_leasing_trend_chart)

    chart_with_border(lease_start_rent_by_submarket_chart)

def area_sold_by_submarket_chart():
    create_centered_heading("📈 Share of AREA SOLD by SUBMARKET (H124)")
    data = get_area_sold_by_submarket()
    if data:
        df = pd.DataFrame(data).sort_values('percentage', ascending=True)
        fig = px.bar(df, y='submarket', x='percentage', orientation='h',
                     text=[f"{val:.2f}%" for val in df['percentage']],
                     labels={'percentage': 'AREA SOLD', 'submarket': 'SUBMARKET'},
                     color_discrete_sequence=['#1E90FF'])
        fig.update_layout(
            xaxis_title="AREA SOLD", yaxis_title="SUBMARKET", height=400,
            xaxis=dict(tickformat='.1f', ticksuffix='%'),
            font=dict(family="Arial", size=12),
        )
        fig.update_traces(textposition='outside', texttemplate='%{text}')
        config = {'displayModeBar': False, 'staticPlot': True}
        st.plotly_chart(fig, use_container_width=True, config=config)
    else:
        st.write("No data available for Area Sold by Submarket")

def area_sold_by_quarter():
    create_centered_heading("📊 Share of Area Sold by Quarter (H124)")
    data = get_area_sold_by_quarter()
    if data:
        df = pd.DataFrame(data)
        total_area = df['total_area_sold'].sum()
        df['percentage'] = (df['total_area_sold'] / total_area * 100).round(2)
        fig = go.Figure(data=[go.Bar(
            x=df['QTR'],
            y=df['percentage'],
            text=[f"{p:.2f}%" for p in df['percentage']],
            textposition='outside',
            marker_color='#0078D4'
        )])
        fig.update_layout(
            xaxis_title="Quarter", yaxis_title="Share of Area Sold (%)", height=400,
            margin=dict(t=50, b=50, l=50, r=50), plot_bgcolor='white',
            yaxis=dict(tickformat='.2f', range=[0, max(df['percentage']) * 1.1],
                       tickfont=dict(size=12), showgrid=True, gridcolor='lightgrey'),
            xaxis=dict(tickfont=dict(size=12), showgrid=False),
            showlegend=False, font=dict(family="Arial", size=12),
        )
        fig.update_traces(hoverinfo='text', hovertemplate='%{x}<br>Share: %{text}<extra></extra>')
        config = {'displayModeBar': False, 'staticPlot': True}

        st.plotly_chart(fig, use_container_width=True, config=config)
    else:
        st.write("No data available for Area Sold by Quarter")

def sales_by_buyer_type():
    create_centered_heading("👥 Share of Area Sold by Buyer Type")
    data = get_sales_by_buyer_type()
    if data:
        df = pd.DataFrame(data)
        fig = go.Figure(data=[go.Pie(
            labels=df['buyer_type'],
            values=df['total_area_sold'],
            textposition='auto',
            textinfo='percent',
            hoverinfo='label+percent+value',
            hovertemplate='<b>%{label}</b><br>%{percent}<br>Area: %{value:,.0f} sq ft<extra></extra>'
        )])
        fig.update_traces(textfont_size=12, pull=[0.05] * len(df))
        fig.update_layout(
            legend=dict(orientation="v", yanchor="middle", y=0.5, xanchor="left", x=1.05, font=dict(size=12)),
            height=350, margin=dict(t=0, b=20, l=20, r=120), font=dict(family="Arial", size=12),
        )
        config = {'displayModeBar': False, 'staticPlot': True}
        st.plotly_chart(fig, use_container_width=True, config=config)
    else:
        st.write("No data available for Sales by Buyer Type")

def sales_page():
    create_dashboard_title("💰", "Sales Dashboard (Mumbai Office)")
    
    col1, col2 = st.columns(2)
    with col1:
        chart_with_border(area_sold_by_quarter)
    with col2:
        chart_with_border(area_sold_by_submarket_chart)

    col1, col2, col3 = st.columns(3)
    with col2:
        chart_with_border(sales_by_buyer_type)

def clean_dataframe(df):
    # Function to remove commas and convert to integer
    def clean_year(x):
        if pd.isna(x):
            return None
        return int(str(x).replace(',', ''))
    
    # Clean Lease Start Year and Lease Expiry Year
    year_columns = ['LEASE START YEAR', 'LEASE EXPIRY YEAR']
    for col in year_columns:
        if col in df.columns:
            df[col] = df[col].apply(clean_year)
    
    # List of columns to convert to whole numbers
    numeric_columns = [
        'STAMP DUTY (INR)', 'REGSTN FEES (INR)', 'LEASE TENURE (MONTHS)',
        'AREA TRANSCATED(sq ft)', 'AVERAGE MONTHLY RENT (INR Lumsum)',
        'AVERAGE MONTHLY RENT (INR psf)', 'LEASABLE AREA (sq ft)',
        'AVERAGE MONTHLY RENT ON LEASABLE (INR psf)',
        'LEASE START RENT ON LEASABLE (INR psf)',
        'LEASE END RENT ON LEASABLE (INR psf)', 'ANNUAL ESCALATION (%)',
        'SECURITY DEPOSIT (INR)', 'SECURITY DEPOSIT (months)',
        'CAM CHARGES (INR)', 'NO CAR PARKS'
    ]
    
    # Convert numeric columns to integers
    for col in numeric_columns:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col].astype(str).str.replace(',', ''), errors='coerce').fillna(0).astype(int)
    
    return df
import numpy as np

def sample_data():
    create_dashboard_title("📁", "Sample Data (Mumbai Office)")

    def safe_int_convert(x):
        if pd.isna(x) or np.isinf(x):
            return 0  # or any other value you prefer for NaN/inf
        return int(round(x))

    def display_sample_data(df, title):
        st.subheader(title)
        
        # Create a copy of the dataframe for display
        display_df = df.copy()
        
        # Convert float and decimal columns to whole numbers, handling NaN and inf
        float_columns = display_df.select_dtypes(include=['float64', 'float32']).columns
        for col in float_columns:
            display_df[col] = display_df[col].apply(safe_int_convert)
        
        # Format integer columns to display without commas
        int_columns = display_df.select_dtypes(include=['int64', 'int32']).columns
        for col in int_columns:
            display_df[col] = display_df[col].apply(lambda x: f"{x:d}")
        
        # Format datetime columns to display only the date part
        date_columns = display_df.select_dtypes(include=['datetime64']).columns
        for col in date_columns:
            display_df[col] = display_df[col].dt.strftime('%Y-%m-%d')
        
        st.dataframe(
            display_df.head(10),
            use_container_width=True,
            hide_index=True,
        )
        st.markdown(f"*Showing 10 out of {len(df)} rows*")

    # Read and display Leases data
    df_leases = pd.read_excel('Leases Sample Data Sheet.xlsx', parse_dates=['LEASE EXPIRY DATE', 'REGSTN DATE', 'LEASE START DATE'])
    display_sample_data(df_leases, '📋 Leases Sample Data')

    # Read and display Projects data
    df_projects = pd.read_excel('Projects Sample Data Sheet.xlsx')
    display_sample_data(df_projects, '🏗️ Projects Sample Data')

    # Read and display Sales data
    df_sales = pd.read_excel('Sales Sample Data Sheet.xlsx')
    display_sample_data(df_sales, '💰 Sales Sample Data')

    def prepare_excel(df):
        # Convert float columns to integers for download, handling NaN and inf
        for col in df.select_dtypes(include=['float64', 'float32']).columns:
            df[col] = df[col].apply(safe_int_convert)
        
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Sheet1')
        return output.getvalue()

    st.subheader("📥 Download Sample Datasets")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.download_button(
            label="📋 Download Leases Data",
            data=prepare_excel(df_leases),
            file_name="leases_sample_data.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
    with col2:
        st.download_button(
            label="🏗️ Download Projects Data",
            data=prepare_excel(df_projects),
            file_name="projects_sample_data.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
    with col3:
        st.download_button(
            label="💰 Download Sales Data",
            data=prepare_excel(df_sales),
            file_name="sales_sample_data.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
def main():
    
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("📄 Leases", key="btn_leases", use_container_width=True):
            st.session_state.page = "leases"
    with col2:
        if st.button("💰 Sales", key="btn_sales", use_container_width=True):
            st.session_state.page = "sales"
    with col3:
        if st.button("📁 Sample Data", key="btn_sample_data", use_container_width=True):
            st.session_state.page = "sample_data"
    
    if 'page' not in st.session_state:
        st.session_state.page = "leases"
    
    if st.session_state.page == "leases":
        leases_page()
    elif st.session_state.page == "sales":
        sales_page()
    elif st.session_state.page == "sample_data":
        sample_data()
    
    st.markdown('<p class="footer">© 2024 RE Journal. All rights reserved.</p>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col2:
        st.markdown('<a href="https://www.rejournal.in/" target="_blank" class="custom-link-button">RE Journal Website</a>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
