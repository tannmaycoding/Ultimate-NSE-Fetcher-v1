from nselib import capital_market
import streamlit as st
import pandas as pd
from io import BytesIO

st.title("Stock Market Historical Prices")
options = ["NSE Share", "Nifty 500", "Nifty 100", "Nifty 200", "Nifty 50", "Nifty Next 50", "Nifty Midcap 150", "Nifty Midcap 50",
           "Nifty Midcap Select", "Nifty Midcap 100", "Nifty Smallcap 250", "India Vix"]
name = st.selectbox("NSE Type Name", options=options)
if name == "NSE Share":
    name2 = st.text_input("NSE Share: ")

start, end = st.columns(2, vertical_alignment="top")

sdate = start.selectbox("Start Date", options=["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12",
                                               "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24",
                                               "25", "26", "27", "28", "29", "30", "31"])

smonth = start.selectbox("Start Month", options=["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"])

syear = start.selectbox("Start Year", options=["2024", "2023", "2022", "2021", "2020", "2019", "2018", "2017", "2016",
                                               "2015", "2014", "2013", "2012", "2011", "2010", "2009", "2008", "2007",
                                               "2006", "2005", "2004", "2003", "2002", "2001", "2000", "1999", "1998",
                                               "1997", "1996", "1995", "1994", "1993", "1992", "1991", "1990"])

edate = end.selectbox("End Date", options=["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12",
                                           "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24",
                                           "25", "26", "27", "28", "29", "30", "31"], index=1)

emonth = end.selectbox("End Month", options=["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"])

eyear = end.selectbox("End Year", options=["2024", "2023", "2022", "2021", "2020", "2019", "2018", "2017", "2016",
                                           "2015", "2014", "2013", "2012", "2011", "2010", "2009", "2008", "2007",
                                           "2006", "2005", "2004", "2003", "2002", "2001", "2000", "1999", "1998",
                                           "1997", "1996", "1995", "1994", "1993", "1992", "1991", "1990"])

start_date = f"{sdate}-{smonth}-{syear}"
end_date = f"{edate}-{emonth}-{eyear}"


def fetch_prices():
    try:
        # Fetch data from the library
        if name == "India Vix":
            vix_data = capital_market.india_vix_data(start_date, end_date)
            return vix_data

        elif name != "NSE Share":
            indexData = capital_market.index_data(name, start_date, end_date)
            return indexData

        else:
            nseData = capital_market.price_volume_and_deliverable_position_data(name2, start_date, end_date)
            return nseData

    except Exception as e:
        st.error(f"Error fetching data: {e}")
        return None


# Function to convert DataFrame to CSV
def convert_df_to_csv(dataframe: pd.DataFrame):
    return dataframe.to_csv().encode("utf-8")


def convert_df_to_excel(dataframe: pd.DataFrame):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        dataframe.to_excel(writer, index=False, sheet_name='Sheet1')

    processed_data = output.getvalue()
    return processed_data


plot_col1, plot_col2, plot_col3, plot_col4, plot_col5 = st.columns(5, vertical_alignment="top")

openPrice = plot_col1.checkbox("Open")
high = plot_col2.checkbox("High")
low = plot_col3.checkbox("Low")
close = plot_col4.checkbox("Close")

if name == "NSE Share":
    volume = plot_col5.checkbox("Volume")

plot_options = []


# Button to download data
if start_date != end_date:
    # Button to fetch graph data
    if st.button("Get Graph"):
        data = fetch_prices()
    
        if data is not None:
            if name != "NSE Share":
    
                if openPrice:
                    plot_options.append("OPEN_INDEX_VAL")
    
                if high:
                    plot_options.append("HIGH_INDEX_VAL")
    
                if low:
                    plot_options.append("LOW_INDEX_VAL")
    
                if close:
                    plot_options.append("CLOSE_INDEX_VAL")
    
                # Ensure that the selected columns exist in the data
                df = data[[col for col in plot_options if col in data.columns]]
                df2 = data["TIMESTAMP"]
                res = pd.concat([df2, df], axis="columns")
    
                if not df.empty:
                    st.line_chart(res, x="TIMESTAMP")
    
                else:
                    st.warning("None of the selected columns are available in the data.")
    
            else:
                if openPrice:
                    plot_options.append("OpenPrice")
    
                if high:
                    plot_options.append("HighPrice")
    
                if low:
                    plot_options.append("LowPrice")
    
                if close:
                    plot_options.append("ClosePrice")
    
                df = data[[col for col in plot_options if col in data.columns]]
                df2 = data["Date"]
                res = pd.concat([df2, df], axis="columns")
    
                if not df.empty:
                    st.line_chart(res, x="Date")
    
                else:
                    st.warning("None of the selected columns are available in the data.")

    if st.button("Download Prices"):
        data = fetch_prices()
        data["No.ofTrades"] = pd.to_numeric(data["No.ofTrades"].str.replace(",", ""))
        col1, col2 = st.columns(2, vertical_alignment="top")

        if data is not None:
            # Download as CSV
            csv_data = convert_df_to_csv(data)
            col1.download_button(
                label="Download as CSV",
                data=csv_data,
                file_name=f"{name if name != 'NSE Share' else name2}.csv",
                mime="text/csv",
                use_container_width=True
            )

            # Download as Excel
            excel_data = convert_df_to_excel(data)
            col2.download_button(
                label="Download as Excel",
                data=excel_data,
                file_name=f"{name if name != 'NSE Share' else name2}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )

    if st.button("View Data"):
        data = fetch_prices()
        if name == "NSE Share":
            data["No.ofTrades"] = pd.to_numeric(data["No.ofTrades"].str.replace(",", ""))

        if data is not None:
            if name != "NSE Share":
                plot_options.append("TIMESTAMP")
                if openPrice:
                    plot_options.append("OPEN_INDEX_VAL")

                if high:
                    plot_options.append("HIGH_INDEX_VAL")

                if low:
                    plot_options.append("LOW_INDEX_VAL")

                if close:
                    plot_options.append("CLOSE_INDEX_VAL")

                # Ensure that the selected columns exist in the data
                df = data[[col for col in plot_options if col in data.columns]]

                if not df.empty:
                    st.dataframe(df, hide_index=True)

                else:
                    st.warning("None of the selected columns are available in the data.")

            else:
                plot_options.append("Date")
                if openPrice:
                    plot_options.append("OpenPrice")

                if high:
                    plot_options.append("HighPrice")

                if low:
                    plot_options.append("LowPrice")

                if close:
                    plot_options.append("ClosePrice")

                if volume:
                    plot_options.append("No.ofTrades")

                df = data[[col for col in plot_options if col in data.columns]]

                if not df.empty:
                    st.dataframe(df, hide_index=True)

                else:
                    st.warning("None of the selected columns are available in the data.")
