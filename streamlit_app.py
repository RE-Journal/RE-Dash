import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from io import BytesIO

from database_operations import (
    get_area_leased_by_sector,get_area_tenant_sector_share_data,
    get_security_deposit_data, get_leased_area_expiry_data, get_tenant_sector_share_data,
    get_area_leased_by_submarket, get_area_sold_by_quarter, get_sales_by_buyer_type,
    get_average_monthly_rental_trend, get_lease_start_rent_by_submarket,
    get_submarket_data, get_tenant_origin_data, get_quarterly_leasing_trend, 
    get_area_sold_by_submarket,get_tenant_origin_share_data
)

st.set_page_config(layout="wide", page_title="RE Journal Sample Dashboards", page_icon="📊")

# Custom CSS for styling
st.markdown("""
<style>
    .main .block-container { padding: 1rem 5rem; }
    .stApp { margin-top: -10px; }
    .stApp > header { background-color: transparent; }
    .main-header { font-size: 2.5rem; font-weight: bold; text-align: center; margin-bottom: 2rem; }
    .chart-container { border: 0.5px solid #e0e0e0; border-radius: 10px; padding: 1rem; margin-bottom: 1rem; background-color: white; box-shadow: 0 2px 10px rgba(0,0,0,0.05); }
    .chart-title { font-size: 1.2rem; font-weight: bold; text-align: center; margin-bottom: 1rem; color: #333; }
    .stButton > button { width: 100%; border-radius: 5px; background-color: white; color: #3AC0B0; border: 1px solid #3AC0B0; padding: 0.5rem 1rem; font-weight: bold; transition: all 0.3s ease; }
    .stButton > button:hover { background-color: #f0f0f0; border-color: #2E9A8C; }
    .footer { text-align: center; color: gray; margin-top: 2rem; border-top: 1px solid #e0e0e0; padding-top: 1rem; }
</style>
""", unsafe_allow_html=True)

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
    else:
        st.write("No data available for Share of AREA LEASED by TENANT ORIGIN for 2024 H1")

def area_leased_by_submarket_chart():
    data = get_area_leased_by_submarket()
    if data:
        create_pie_chart(data, 'Submarket', 'Area_Leased_Mln_Sqft', 'Percentage', 
                         "🏙️ Share of AREA LEASED by SUBMARKET (H124)")
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
    create_centered_heading("🏢 Tenant Sector share in Leasing (H124)")
    data = get_tenant_sector_share_data()
    if data:
        df = pd.DataFrame(data)
        fig = px.bar(df, x='Quarter', y='Percentage', color='Tenant_Sector',
                     labels={'Percentage': 'Share of Area Leased (%)'},
                     text='Percentage')
        fig.update_traces(texttemplate='%{text:.2f}%', textposition='inside')
        fig.update_layout(
            xaxis_title="Year",
            yaxis_title="Share of Area Leased (%)",
            height=500,
            barmode='stack',
            legend_title="TENANT SECTOR",
            font=dict(family="Arial", size=12),
            yaxis=dict(tickformat='.0%', range=[0, 100],dtick=10,tickmode='linear'),
            legend=dict(orientation="v", yanchor="top", y=1, xanchor="left", x=1.02),
            margin=dict(l=50, r=150, t=50, b=50)
        )
        config = {
            'displayModeBar': False,
            'staticPlot': True
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
    create_centered_heading("📈 Average Monthly Rental (INR psf) Trend")
    data = get_average_monthly_rental_trend()
    if data:
        df = pd.DataFrame(data)
        fig = px.bar(df, x='Quarter', y='Average_Rent',
                     labels={'Average_Rent': 'Average Monthly Rental (INR psf)'},
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
    else:
        st.write("No data available for Average Monthly Rental Trend for 2024 Q1-Q2")

def lease_start_rent_by_submarket_chart():
    create_centered_heading("🏙️ Average of LEASE START RENT ON LEASABLE (INR psf) by SUBMARKET and Quarter")
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
    else:
        st.write("No data available for Lease Start Rent by Submarket for 2024 Q1-Q2")

def area_leased_by_sector_chart():
    create_centered_heading("🏢 Area Leased by Property Sector (H124)")
    data = get_area_leased_by_sector()
    if data:
        df = pd.DataFrame(data)
        fig = go.Figure(data=[go.Pie(
            labels=df['Project_Category'],
            values=df['Area_Leased_Mln_Sqft'],
            text=[f"{value:.2f}M ({percent:.1f}%)" for value, percent in zip(df['Area_Leased_Mln_Sqft'], df['Percentage'])],
            textposition='outside',
            hoverinfo='label+percent+text',
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

def leases_page():
    st.markdown('<h2 class="main-header">📋 Leases Dashboard</h2>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        chart_with_border(area_leased_by_submarket_chart)
    with col2:
        chart_with_border(lambda: area_leased_tenant_sector_share_chart())
    with col3:
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
    st.markdown('<h2 class="main-header">💰 Sales Dashboard</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        chart_with_border(area_sold_by_quarter)
    with col2:
        chart_with_border(area_sold_by_submarket_chart)

    col1, col2, col3 = st.columns(3)
    with col2:
        chart_with_border(sales_by_buyer_type)

def sample_data():
    st.markdown('<h2 class="main-header">📁 Sample Data</h2>', unsafe_allow_html=True)

    def format_date_columns(df):
        date_columns = df.select_dtypes(include=['datetime64']).columns
        for col in date_columns:
            df[col] = pd.to_datetime(df[col]).dt.strftime('%Y-%m-%d')
        return df

    def display_sample_data(df, title):
        st.subheader(title)
        df_formatted = format_date_columns(df)
        st.dataframe(
            df_formatted.head(10),
            use_container_width=True,
            hide_index=True,
        )
        st.markdown(f"*Showing 10 out of {len(df)} rows*")

    df_leases = pd.read_excel('Leases Sample Data Sheet.xlsx', parse_dates=True)
    display_sample_data(df_leases, '📋 Leases Sample Data')

    df_projects = pd.read_excel('Projects Sample Data Sheet.xlsx', parse_dates=True)
    display_sample_data(df_projects, '🏗️ Projects Sample Data')

    df_sales = pd.read_excel('Sales Sample Data Sheet.xlsx', parse_dates=True)
    display_sample_data(df_sales, '💰 Sales Sample Data')

    def prepare_excel(df):
        df_formatted = format_date_columns(df)
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df_formatted.to_excel(writer, index=False, sheet_name='Sheet1')
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
    st.markdown('<h1 class="main-header">🏢 RE Journal Sample Dashboard</h1>', unsafe_allow_html=True)
       
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("📋 Leases", use_container_width=True):
            st.session_state.page = "leases"
    with col2:
        if st.button("💰 Sales", use_container_width=True):
            st.session_state.page = "sales"
    with col3:
        if st.button("📁 Sample Data", use_container_width=True):
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
        st.link_button("RE Journal Website", "https://www.rejournal.in/", use_container_width=True)  

if __name__ == "__main__":
    main()
