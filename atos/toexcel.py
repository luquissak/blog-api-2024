import pandas as pd

filename = "./atos/PROJ_CENSO_AWL-Prod.xlsx"
xls = pd.ExcelFile(filename)

sheet_to_df_map = {}
with open("./atos/prod.txt", "w") as arquivo:
    arquivo.write(f"sheet_name|value\n")
    for sheet_name in xls.sheet_names:
        sheet_to_df_map[sheet_name] = xls.parse(sheet_name)
        df = pd.read_excel(filename, sheet_name=sheet_name)
        try:
            values = sheet_to_df_map[sheet_name]["FOTOS"].values
            for value in values:
                if isinstance(value, str):
                    print(sheet_name, value)
                    arquivo.write(f"{sheet_name}|{value}\n")
        except KeyError:
            print(sheet_name)
