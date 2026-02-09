# Libraries Used
import pandas as pd


def main():
    # Load data
    df = pd.read_csv("universities.csv", encoding="latin-1")

    print("Initial Data Info:")
    print(df.info())
    print("\nPreview:")
    print(df.head())

    # -------- Clean Founded column --------
    df["Founded"] = df["Founded"].astype(str).str.extract(r"(\d{4})")
    df["Founded"] = df["Founded"].astype(int)

    print("\nFounded column cleaned.")

    # -------- Check missing links --------
    missing_links = df[df["Link"].isnull()]
    if not missing_links.empty:
        print("\nRows with missing links:")
        print(missing_links)

    # -------- Clean Enrollment column --------
    df["Enrollment"] = df["Enrollment"].astype(str)

    # Replace spaces with commas (for consistency)
    df["Enrollment"] = df["Enrollment"].str.replace(" ", ",", regex=False)

    # Extract numeric values with commas
    df["Enrollment"] = df["Enrollment"].str.extract(r"(\d{1,3}(?:,\d{1,3})*)")

    # Remove commas and convert to int
    df["Enrollment"] = df["Enrollment"].str.replace(",", "", regex=False)
    df["Enrollment"] = df["Enrollment"].astype(int)

    print("\nEnrollment column cleaned.")
    print("\nFinal Data Info:")
    print(df.info())

    # Save cleaned data
    df.to_csv("universities-clean.csv", index=False)
    print("\nCleaned file saved as universities-clean.csv")


if __name__ == "__main__":
    main()
