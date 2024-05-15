import streamlit as st
import lxml.etree as ET
import pandas as pd

def parse_tcx(file):
    tree = ET.parse(file)
    root = tree.getroot()
    ns = {'ns': 'http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2'}

    coordinates = []

    for trackpoint in root.findall('.//ns:Trackpoint', ns):
        lat = trackpoint.find('.//ns:LatitudeDegrees', ns)
        lon = trackpoint.find('.//ns:LongitudeDegrees', ns)
        if lat is not None and lon is not None:
            coordinates.append((float(lat.text), float(lon.text)))

    return coordinates

def parse_gpx(file):
    tree = ET.parse(file)
    root = tree.getroot()
    ns = {'ns': 'http://www.topografix.com/GPX/1/1'}

    coordinates = []

    for trkpt in root.findall('.//ns:trkpt', ns):
        lat = trkpt.get('lat')
        lon = trkpt.get('lon')
        if lat is not None and lon is not None:
            coordinates.append((float(lat), float(lon)))

    return coordinates

def main():
    st.title("GPS Coordinates Extractor")
    st.write("Upload a TCX or GPX file to extract the coordinates.")

    uploaded_file = st.file_uploader("Choose a TCX or GPX file", type=["tcx", "gpx"])

    if uploaded_file is not None:
        if uploaded_file.name.endswith(".tcx"):
            coordinates = parse_tcx(uploaded_file)
        elif uploaded_file.name.endswith(".gpx"):
            coordinates = parse_gpx(uploaded_file)
        else:
            st.error("Unsupported file type. Please upload a TCX or GPX file.")
            return

        # Convert to DataFrame
        df = pd.DataFrame(coordinates, columns=["Latitude", "Longitude"])

        # Display DataFrame
        st.write("Extracted Coordinates:")
        st.dataframe(df)

        # Convert DataFrame to CSV
        csv = df.to_csv(index=False).encode('utf-8')

        # Create a download button for the CSV file
        st.download_button(
            label="Download Coordinates as CSV",
            data=csv,
            file_name="coordinates.csv",
            mime="text/csv"
        )

if __name__ == "__main__":
    main()
