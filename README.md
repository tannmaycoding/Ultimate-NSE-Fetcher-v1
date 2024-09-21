# Ultimate-NSE-Fetcher-v1
This is a website for getting NSE share market data and data of broad market indices of NSE, graph of data from given start date to given end date. It is different from Ultimate-NSE-Fetcher-v2 as:
- It is not multipage
- Less Functionalities
- Is on Streamlit Community Cloud
  -This is because I wasn't able to upload Ultimate-NSE-Fetcher-v1 on Stremlit Community Cloud :disappointed:

[The Link For Website](https://ultimate-nse-fetcher.streamlit.app/)

The working:
1. Has input fields for share name, start date, start month, start year, end date, end month, end year

2. When you press `Get Graph`:
   - Takes data of the share
   - Removing some columns to not plot
   - Using streamlits `st.line_chart` to plot the dataframe
     - Takes the data
     - Make another buttons `Download as CSV` and `Download as Excel will come` after doing all the fetching
     - Clicking that button downloads the data
