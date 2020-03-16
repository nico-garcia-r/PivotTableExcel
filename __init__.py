# coding: utf-8
"""
Base para desarrollo de modulos externos.
Para obtener el modulo/Funcion que se esta llamando:
     GetParams("module")

Para obtener las variables enviadas desde formulario/comando Rocketbot:
    var = GetParams(variable)
    Las "variable" se define en forms del archivo package.json

Para modificar la variable de Rocketbot:
    SetVar(Variable_Rocketbot, "dato")

Para obtener una variable de Rocketbot:
    var = GetVar(Variable_Rocketbot)

Para obtener la Opcion seleccionada:
    opcion = GetParams("option")


Para instalar librerias se debe ingresar por terminal a la carpeta "libs"

    pip install <package> -t .

"""
# Changing the data types of all strings in the module at once
from __future__ import unicode_literals
import os
import sys

base_path = tmp_global_obj["basepath"]
cur_path = base_path + 'modules' + os.sep + 'AdvancedExcel' + os.sep + 'libs' + os.sep
sys.path.append(cur_path)

global constants
global abc

constants = {"xlRowField": 1, "xlColumnField": 2, "xlPageField": 3}
abc = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
           'w', 'x', 'y', 'z']

module = GetParams("module")

if module == "createPivotTable":
    data = GetParams("data")
    destination = GetParams("destination")
    table_name = GetParams("tableName")
    excel = GetGlobals("excel")

    try:
        xls = excel.file_[excel.actual_id]
        wb = xls['workbook']

        data = data.split("!")
        destination = destination.split("!")
        sheet_1, sheet_2 = None, None
        if len(data) > 1:
            sheet = data[0]
            range_ = data[1].split(":")
        else:
            sheet = 1
            range_ = data[0].split(":")
        sheet_1 = wb.api.Worksheets(sheet)
        if len(destination) > 1:
            pivot_sheet = destination[0]
            cell = destination[1]
            if sheet != pivot_sheet:
                sheet_2 = wb.api.Worksheets(destination[0])
        else:
            cell = destination[0]

        # range_ = [C1, D2]
        cell_1 = abc.index(range_[0][0].lower()) + 1, int(range_[0][1])
        cell_2 = abc.index(range_[1][0].lower()) + 1, int(range_[1][1])
        cell_3 = abc.index(cell[0].lower()) + 1, int(cell[1])

        print(cell_1, cell_2)
        cell_1 = sheet_1.Cells(cell_1[1], cell_1[0])
        cell_2 = sheet_1.Cells(cell_2[1], cell_2[0])


        source_range = sheet_1.Range(cell_1, cell_2)

        if sheet_2:
            cell_3 = sheet_2.Cells(cell_3[1],cell_3[0])
            pivotTargetRange = sheet_2.Range(cell_3, cell_3)
        else:
            cell_3 = sheet_1.Cells(cell_3[1],cell_3[0])
            pivotTargetRange = sheet_1.Range(cell_3, cell_3)

        pivot_table = wb.api.PivotCaches().Create(SourceType=1, SourceData=source_range, Version=4)
        pivot_table.CreatePivotTable(TableDestination=pivotTargetRange, TableName=table_name, DefaultVersion=4)

    except Exception as e:
        PrintException()
        raise e

if module == "refreshPivot":
    sheet = GetParams("sheet")
    pivotTableName = GetParams("table")
    excel = GetGlobals("excel")

    xls = excel.file_[excel.actual_id]
    wb = xls['workbook']
    wb.sheets[sheet].select()
    print(dir(wb.api.ActiveSheet.PivotTables(pivotTableName)))
    wb.api.ActiveSheet.PivotTables(pivotTableName).PivotCache().refresh()

if module == "addField":

    sheet = GetParams("sheet")
    pivotTableName = GetParams("table")
    data = GetParams("data")
    option = GetParams("option_")

    excel = GetGlobals("excel")
    xls = excel.file_[excel.actual_id]

    try:
        wb = xls['workbook']
        sht = wb.sheets[sheet].select()

        pivot_table = wb.api.ActiveSheet.PivotTables(pivotTableName)
        for d in data.split(","):
            print(d)
            cubeField = pivot_table.PivotFields(d)
            if option != "data":
                cubeField.Orientation = constants[option]
                cubeField.Position = 1

            else:
                field = pivot_table.PivotFields(d)
                pivot_table.AddDataField(field, "Suma de {value}".format(value=d))

    except Exception as e:
        PrintException()
        raise e



if module == "filter":

    sheet = GetParams("sheet")
    pivotTableName = GetParams("table")
    data = GetParams("filter")
    value = GetParams("value")

    excel = GetGlobals("excel")
    xls = excel.file_[excel.actual_id]
    try:
        wb = xls['workbook']
        sht = wb.sheets[sheet].select()

        pivotTable = wb.api.ActiveSheet.PivotTables(pivotTableName)
        filter_ = pivotTable.PivotFields(data)
        filter_.CurrentPage = "(All)"

        print(value.split(","))
        for f in filter_.PivotItems():
            print(f.Name in value.split(","), f.Name)
            f.Visible = f.Name in value.split(",")


    except Exception as e:
        PrintException()
        raise e

if module == "listFields":
    sheet = GetParams("sheet")
    pivotTableName = GetParams("table")
    result = GetParams("result")

    excel = GetGlobals("excel")
    xls = excel.file_[excel.actual_id]
    try:
        wb = xls['workbook']
        sht = wb.sheets[sheet].select()

        pivotTable = wb.api.ActiveSheet.PivotTables(pivotTableName)

        cubeFields = pivotTable.PivotFields()

        fields = [field.Name for field in cubeFields]

        SetVar(result, fields)

    except Exception as e:
        PrintException()
        raise e
