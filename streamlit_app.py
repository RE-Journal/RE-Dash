import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
from io import BytesIO

from database_operations import (
    get_tenant_sector_data, get_qoq_leasing_data, get_area_leased_by_sector,
    get_security_deposit_data, get_leased_area_expiry_data, get_tenant_sector_share_data,
    get_area_sold_by_submarket, get_area_sold_by_quarter, get_sales_by_buyer_type,
    get_completion_status_options, get_property_area_by_submarket, get_office_stock_by_completion_year,
    get_available_quarters, get_average_monthly_rental_trend, get_lease_start_rent_by_submarket
)

st.set_page_config(layout="wide", page_title="RE Journal Sample Dashboards")

# Updated Custom CSS for cleaner borders and spacing
st.markdown("""
<style>
    .chart-container {
        border: 1px solid #e0e0e0;
        border-radius: 5px;
        padding: 15px;
        margin-bottom: 30px;
        background-color: white;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    }
    .stPlotlyChart {
        margin-bottom: 20px;
    }
    h3 {
        margin-top: 0;
        margin-bottom: 20px;
        color: #333;
    }
    .st-emotion-cache-16idsys p {
        font-size: 14px;
    }
</style>
""", unsafe_allow_html=True)

def create_centered_heading(title):
    st.markdown(f"<h3 style='text-align: center;'>{title}</h3>", unsafe_allow_html=True)

def chart_with_border(chart_function):
    with st.container():
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        chart_function()
        st.markdown('</div>', unsafe_allow_html=True)

def tenant_sector_distribution_chart():
    create_centered_heading("Tenant Sector Distribution")
    tenant_sector_data = get_tenant_sector_data()
    if tenant_sector_data:
        colors = ['gold', 'mediumturquoise', 'darkorange', 'lightgreen']
        fig = go.Figure(data=[go.Pie(
            labels=[item['label'] for item in tenant_sector_data],
            values=[item['value'] for item in tenant_sector_data],
            textinfo='value',
            hoverinfo='label+percent',
            marker=dict(colors=colors, line=dict(color='#000000', width=2)),
            textfont_size=20
        )])
        fig.update_layout(
            height=300,
            margin=dict(t=0, b=0, l=0, r=0),
            showlegend=True,
            legend=dict(
                orientation="v",
                yanchor="middle",
                y=0.5,
                xanchor="left",
                x=1.05
            )
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.write("No data available for Tenant Sector Distribution")

def area_leased_by_sector_chart():
    create_centered_heading("Area Leased by Sector")
    area_leased_data, total_area = get_area_leased_by_sector()
    if area_leased_data:
        colors = ['gold', 'mediumturquoise', 'darkorange', 'lightgreen']
        fig = go.Figure(data=[go.Pie(
            labels=[item['label'] for item in area_leased_data],
            values=[item['value'] for item in area_leased_data],
            textinfo='percent',
            hoverinfo='label+value',
            hovertemplate='%{label}<br>Area: %{value:.2f}M sq ft<extra></extra>',
            marker=dict(colors=colors, line=dict(color='#000000', width=2)),
            textfont_size=16
        )])
        fig.update_layout(
            height=300,
            margin=dict(t=0, b=0, l=0, r=0),
            showlegend=True,
            legend=dict(
                orientation="v",
                yanchor="middle",
                y=0.5,
                xanchor="left",
                x=1.05
            )
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.write("No data available for Area Leased by Sector")

def security_deposit_by_submarket_chart():
    create_centered_heading("Average of SECURITY DEPOSIT (months) by SUBMARKET")
    security_deposit_data = get_security_deposit_data()
    if security_deposit_data:
        df = pd.DataFrame(security_deposit_data)
        df = df.sort_values('SECURITY_DEPOSIT', ascending=False)  # Sort data in descending order

        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=df['SUBMARKET'],
            y=df['SECURITY_DEPOSIT'],
            text=df['SECURITY_DEPOSIT'],
            textposition='outside',
            texttemplate='%{text:.1f}',
            marker_color='darkturquoise',
            marker=dict(
                line=dict(width=0),
            ),
            hoverinfo='x+y',
            hovertemplate='<b>%{x}</b><br>Security Deposit: %{y:.1f} months<extra></extra>'
        ))

        fig.update_layout(
            xaxis_title="SUBMARKET",
            yaxis_title="Average Security Deposit (months)",
            height=400,
            plot_bgcolor='white',
            yaxis=dict(
                gridcolor='lightgrey',
                zeroline=True,
                zerolinecolor='lightgrey',
                zerolinewidth=1
            ),
            xaxis=dict(
                tickangle=-45,  # Rotate x-axis labels for better readability
                title_standoff=25  # Increase space between x-axis and its title
            ),
            margin=dict(b=100),  # Increase bottom margin to accommodate rotated labels
            bargap=0.2,  # Adjust the gap between bars
            shapes=[dict(
                type='rect',
                xref='x',
                yref='y',
                x0=i - 0.45,
                y0=0,
                x1=i + 0.45,
                y1=val,
                fillcolor='darkturquoise',
                layer='below',
                line_width=0,
            ) for i, val in enumerate(df['SECURITY_DEPOSIT'])],
        )

        # Add rounded tops
        for i, val in enumerate(df['SECURITY_DEPOSIT']):
            fig.add_shape(
                type='circle',
                xref='x',
                yref='y',
                x0=i - 0.45,
                y0=val - 0.1,
                x1=i + 0.45,
                y1=val + 0.1,
                fillcolor='darkturquoise',
                layer='below',
                line_width=0,
            )

        st.plotly_chart(fig, use_container_width=True)
    else:
        st.write("No data available for Security Deposit by Submarket")

def tenant_sector_share_chart():
    create_centered_heading("Tenant Sector share in Leasing")
    tenant_sector_share_data = get_tenant_sector_share_data()
    if tenant_sector_share_data:
        df = pd.DataFrame(tenant_sector_share_data)
        fig = px.bar(df, x='quarter', y='percentage', color='tenant_sector', 
                     labels={'percentage': 'Share of Area Leased (%)', 'quarter': 'Quarter'},
                     text='percentage')
        fig.update_traces(texttemplate='%{text:.1f}%', textposition='inside')
        fig.update_layout(
            xaxis_title="Quarter",
            yaxis_title="Share of Area Leased (%)",
            height=400,
            barmode='stack',
            yaxis_range=[0, 100]
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.write("No data available for Tenant Sector share in Leasing")

def qoq_leasing_trend_chart():
    create_centered_heading("Quarter-over-Quarter Leasing Trend")
    qoq_data = get_qoq_leasing_data()
    if qoq_data:
        fig = go.Figure(data=[go.Bar(
            x=[item['Quarter'] for item in qoq_data],
            y=[item['Area_Leased_in_mln_sft'] for item in qoq_data],
            text=[f"{item['Area_Leased_in_mln_sft']:.2f}" for item in qoq_data],
            textposition='auto',
        )])
        fig.update_layout(
            xaxis_title="Quarter",
            yaxis_title="Area Leased (mln sft)",
            height=500
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.write("No data available for Quarter-over-Quarter Leasing Trend")

def leased_area_expiry_chart():
    create_centered_heading("Leased Area (sq ft) due for Expiry by Year")
    expiry_data = get_leased_area_expiry_data()
    if expiry_data:
        df = pd.DataFrame(expiry_data)
        if not df.empty:
            fig = px.bar(df, x='expiry_year', y='area_mln_sqft',
                         labels={'expiry_year': 'Year', 'area_mln_sqft': 'Leased Area (million sq ft)'},
                         text='area_mln_sqft')
            fig.update_traces(texttemplate='%{text:.2f}M', textposition='outside')
            fig.update_layout(
                xaxis_title="Year",
                yaxis_title="Leased Area (million sq ft)",
                height=500,
                yaxis=dict(tickformat='.2f'),
                xaxis=dict(dtick=1, tickangle=45, tickmode='linear'),
                margin=dict(b=100)
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.write("No data available for Leased Area due for Expiry")
    else:
        st.write("Error fetching data for Leased Area due for Expiry")

def average_monthly_rental_trend_chart(selected_quarters):
    create_centered_heading("Average Monthly Rental (INR psf) Trend")
    rental_trend_data = get_average_monthly_rental_trend(selected_quarters)
    if rental_trend_data:
        df = pd.DataFrame(rental_trend_data)
        fig = px.bar(df, x='Quarter', y='Average_Rent',
                     labels={'Average_Rent': 'Average Monthly Rental (INR psf)'},
                     text='Average_Rent')
        fig.update_traces(texttemplate='%{text:.0f}', textposition='outside')
        fig.update_layout(
            xaxis_title="Quarter",
            yaxis_title="Average Monthly Rental (INR psf)",
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.write("No data available for Average Monthly Rental Trend")

def lease_start_rent_by_submarket_chart(selected_quarters):
    create_centered_heading("Average of LEASE START RENT ON LEASABLE (INR psf) by SUBMARKET and Quarter")
    lease_start_rent_data = get_lease_start_rent_by_submarket(selected_quarters)
    if lease_start_rent_data:
        df = pd.DataFrame(lease_start_rent_data)
        fig = px.bar(df, x='SUBMARKET', y='Average_Rent', color='Quarter',
                     labels={'Average_Rent': 'Average Lease Start Rent (INR psf)'},
                     text='Average_Rent',
                     barmode='group')
        fig.update_traces(texttemplate='%{text:.0f}', textposition='outside')
        fig.update_layout(
            xaxis_title="SUBMARKET",
            yaxis_title="Average Lease Start Rent (INR psf)",
            height=400,
            legend_title="Quarter"
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.write("No data available for Lease Start Rent by Submarket")

def leases_page():
    st.header("Leases Dashboard")
    
    col1, col2 = st.columns(2)
    
    with col1:
        chart_with_border(tenant_sector_distribution_chart)

    with col2:
        chart_with_border(area_leased_by_sector_chart)

    col3, col4 = st.columns(2)

    with col3:
        chart_with_border(security_deposit_by_submarket_chart)

    with col4:
        chart_with_border(tenant_sector_share_chart)

    chart_with_border(qoq_leasing_trend_chart)
    chart_with_border(leased_area_expiry_chart)
    
    available_quarters = get_available_quarters()
    selected_quarters = st.multiselect(
        "Select Quarters",
        options=available_quarters,
        default=available_quarters[:2]
    )

    col5, col6 = st.columns(2)

    with col5:
        chart_with_border(lambda: average_monthly_rental_trend_chart(selected_quarters))

    with col6:
        chart_with_border(lambda: lease_start_rent_by_submarket_chart(selected_quarters))

def area_sold_by_submarket(color_scale):
    create_centered_heading("Share of AREA SOLD (sq ft) by SUBMARKET")
    area_sold_data = get_area_sold_by_submarket()
    if area_sold_data:
        df = pd.DataFrame(area_sold_data)
        df = df.sort_values('percentage', ascending=True)
        fig = px.bar(df, y='submarket', x='percentage', orientation='h',
                     text=[f"{val:.2f}%" for val in df['percentage']],
                     color='percentage',
                     color_continuous_scale=color_scale)
        fig.update_layout(
            xaxis_title="% of Total Area Sold (log scale)",
            yaxis_title="Submarket",
            height=400,
            xaxis=dict(type="log", tickformat='.1f'),
            coloraxis_showscale=False
        )
        fig.update_traces(textposition='outside', texttemplate='%{y} %{text}')
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.write("No data available for Area Sold by Submarket")

def area_sold_by_quarter(color_scale):
    create_centered_heading("Share of AREA SOLD by QTR (H124)")
    area_sold_qtr_data = get_area_sold_by_quarter()
    if area_sold_qtr_data:
        df = pd.DataFrame(area_sold_qtr_data)
        total_area = df['area_sold_mln_sqft'].sum()
        df['percentage'] = df['area_sold_mln_sqft'] / total_area * 100
        df = df.sort_values('sale_quarter')
        
        fig = go.Figure(data=[go.Bar(
            x=df['sale_quarter'].str[-2:],
            y=df['percentage'],
            text=[f"{p:.1f}%" for p in df['percentage']],
            textposition='outside',
            marker_color='#1E90FF',
            marker_line_color='#1E90FF',
            marker_line_width=1.5,
            opacity=0.8
        )])
        
        fig.update_layout(
            xaxis_title="QTR",
            yaxis_title="",
            height=400,
            margin=dict(t=0, b=50, l=50, r=50),
            plot_bgcolor='white',
            yaxis=dict(
                tickformat='%',
                range=[0, 100],
                dtick=20,
                tickfont=dict(size=12),
                showgrid=True,
                gridcolor='lightgrey',
                zeroline=True,
                zerolinecolor='lightgrey',
                zerolinewidth=1
            ),
            xaxis=dict(
                tickfont=dict(size=12),
                showgrid=False
            ),
            showlegend=False
        )
        
        
        fig.update_traces(
            hoverinfo='text',
            hovertemplate='%{x}<br>Share: %{text}<extra></extra>'
        )
        
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.write("No data available for Area Sold by Quarter")


def area_sold_by_quarter(color_scale):
    create_centered_heading("Share of AREA SOLD by QTR (H124)")
    area_sold_qtr_data = get_area_sold_by_quarter()
    if area_sold_qtr_data:
        df = pd.DataFrame(area_sold_qtr_data)
        total_area = df['area_sold_mln_sqft'].sum()
        df['percentage'] = df['area_sold_mln_sqft'] / total_area * 100
        df = df.sort_values('sale_quarter')
        
        fig = go.Figure(data=[go.Bar(
            x=df['sale_quarter'].str[-2:],
            y=df['percentage'],
            text=[f"{p:.1f}%" for p in df['percentage']],
            textposition='outside',
            marker_color='#1E90FF',
            marker_line_color='#1E90FF',
            marker_line_width=1.5,
            opacity=0.8
        )])
        
        fig.update_layout(
            xaxis_title="QTR",
            yaxis_title="",
            height=400,
            margin=dict(t=0, b=50, l=50, r=50),
            plot_bgcolor='white',
            yaxis=dict(
                tickformat='%',
                range=[0, 100],
                dtick=20,
                tickfont=dict(size=12),
                showgrid=True,
                gridcolor='lightgrey',
                zeroline=True,
                zerolinecolor='lightgrey',
                zerolinewidth=1
            ),
            xaxis=dict(
                tickfont=dict(size=12),
                showgrid=False
            ),
            showlegend=False
        )
        
        fig.update_traces(
            hoverinfo='text',
            hovertemplate='%{x}<br>Share: %{text}<extra></extra>'
        )
        
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.write("No data available for Area Sold by Quarter")

def sales_by_buyer_type(color_sequence):
    create_centered_heading("Share of AREA SOLD by BUYER TYPE (H124)")
    sales_buyer_type_data = get_sales_by_buyer_type()
    if sales_buyer_type_data:
        df = pd.DataFrame(sales_buyer_type_data)
        
        colors = ['#FFD700', '#48D1CC', '#FFA500', '#90EE90']
        
        fig = go.Figure(data=[go.Pie(
            labels=df['buyer_type'],
            values=df['total_area_sold'],
            marker=dict(colors=colors, line=dict(color='#000000', width=2)),
            textposition='auto',
            textinfo='percent',
            hoverinfo='label+percent+value',
            hovertemplate='<b>%{label}</b><br>%{percent}<br>Area: %{value:,.0f} sq ft<extra></extra>'
        )])
        
        fig.update_traces(
            textfont_size=12,
            pull=[0.05] * len(df),
        )
        
        fig.update_layout(
            legend=dict(
                orientation="v",
                yanchor="middle",
                y=0.5,
                xanchor="left",
                x=1.05,
                font=dict(size=12)
            ),
            height=300,
            margin=dict(t=0, b=20, l=20, r=120)
        )
        
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.write("No data available for Sales by Buyer Type")

def sales_page():
    st.header("Sales Dashboard")

    continuous_color_scale = [
        (0, "#36BCF3"), (0.17424242198467255, "#36BCF3"),
        (0.3484848439693451, "#24AEC1"), (0.6742424219846725, "#24AEC1"),
        (1, "#0C9B7C")
    ]
    discrete_colors = ["#36BCF3", "#24AEC1", "#0C9B7C"]

    col1, col2 = st.columns(2)

    with col1:
        chart_with_border(lambda: area_sold_by_submarket(continuous_color_scale))

    with col2:
        chart_with_border(lambda: area_sold_by_quarter(continuous_color_scale))

    col1, col2, col3 = st.columns(3)
    with col2:
        chart_with_border(lambda: sales_by_buyer_type(discrete_colors))

def sample_data():
    st.header('Sample Data')

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
    display_sample_data(df_leases, 'Leases Sample Data')

    df_projects = pd.read_excel('Projects Sample Data Sheet.xlsx', parse_dates=True)
    display_sample_data(df_projects, 'Projects Sample Data')

    df_sales = pd.read_excel('Sales Sample Data Sheet.xlsx', parse_dates=True)
    display_sample_data(df_sales, 'Sales Sample Data')

    def prepare_excel(df):
        df_formatted = format_date_columns(df)
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df_formatted.to_excel(writer, index=False, sheet_name='Sheet1')
        return output.getvalue()

    st.subheader("Download Sample Datasets")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.download_button(
            label="Download Leases Data",
            data=prepare_excel(df_leases),
            file_name="leases_sample_data.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )

    with col2:
        st.download_button(
            label="Download Projects Data",
            data=prepare_excel(df_projects),
            file_name="projects_sample_data.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )

    with col3:
        st.download_button(
            label="Download Sales Data",
            data=prepare_excel(df_sales),
            file_name="sales_sample_data.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )

def main():
    st.markdown("<h1 style='text-align: center;'>RE Journal Sample Dashboard</h1>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1,2,1])
    with col1:
        st.link_button("RE Journal Website", "https://www.rejournal.in/")
        
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Leases", use_container_width=True):
            st.session_state.page = "leases"
    with col2:
        if st.button("Sales", use_container_width=True):
            st.session_state.page = "sales"
    with col3:
        if st.button("Sample Data", use_container_width=True):
            st.session_state.page = "sample_data"
    
    if 'page' not in st.session_state:
        st.session_state.page = "leases"
    
    if st.session_state.page == "leases":
        leases_page()
    elif st.session_state.page == "sales":
        sales_page()
    elif st.session_state.page == "sample_data":
        sample_data()
    
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: gray;'>© 2024 RE Journal. All rights reserved.</p>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
