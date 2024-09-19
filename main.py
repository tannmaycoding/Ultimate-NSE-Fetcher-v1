from nselib import capital_market
import streamlit as st
import pandas as pd

st.title("Stock Market Historical Prices")
options = ["NSE Share", "Nifty 500", "Nifty 100", "Nifty 200", "Nifty 50", "Nifty Next 50", "Nifty Midcap 150", "Nifty Midcap 50",
           "Nifty Midcap Select", "Nifty Midcap 100", "Nifty Smallcap 250", "India Vix"]
name = st.selectbox("Broad Market Index Name", options=options)
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
def convert_df(dataframe: pd.DataFrame):
    return dataframe.to_csv().encode("utf-8")


plot_col1, plot_col2, plot_col3, plot_col4 = st.columns(4, vertical_alignment="top")

openPrice = plot_col1.checkbox("Open")
high = plot_col2.checkbox("High")
low = plot_col3.checkbox("Low")
close = plot_col4.checkbox("Close")
plot_options = []
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

            if not df.empty:
                st.line_chart(df)
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

            if not df.empty:
                st.line_chart(df)
            else:
                st.warning("None of the selected columns are available in the data.")

# Button to download data
if start_date != end_date:
    if st.button("Download Prices"):
        data = fetch_prices()

        if data is not None:
            csv_data = convert_df(data)
            st.success("Everything is done")
            st.download_button(
                label="Click here to download",
                data=csv_data,
                file_name=f"{name}.csv",
                mime="text/csv"
            )
