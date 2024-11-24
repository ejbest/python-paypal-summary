import pandas as pd

# load the csv file
data_file = "Download.csv"
data = pd.read_csv(data_file)

# insure ammount column is numeric
data["Amount"] = pd.to_numeric(data["Amount"], errors="coerce")

# general summary: grouping by name
summary_by_name = data.groupby("Name").agg(
    total_ammount = ("Amount","sum"),
    record_count = ("Amount","count")
).reset_index()

# specific summary for blank names
blank_data_summary = data[data["Name"].isnull() | (data["Name"].str.strip()=="")].groupby("Type").agg(
    total_ammount = ("Amount","sum"),
    record_count = ("Amount","count")
).reset_index()

# function to generate the reports
def generate_report(summary_by_name:pd.DataFrame, blank_data_summary:pd.DataFrame, output_file:str="report.txt"):
    with open(output_file,"w") as file:
        # general summary
        file.write("Summary by Name:\n")
        for _, row in summary_by_name.iterrows():
            file.write(f"{row['Name']:<40} ${row['total_ammount']:.2f}   records {row["record_count"]}\n")
        
        # blank summary 
        file.write("\nSummary for blank names:\n")
        for _, row in blank_data_summary.iterrows():
            file.write(f"{row['Type']:<40} ${row['total_ammount']:.2f}   records {row["record_count"]}\n")
    
# Generate the report
output_file = "summary_report.txt"
generate_report(summary_by_name,blank_data_summary,output_file)

print(f"Report generated successfully: {output_file}")