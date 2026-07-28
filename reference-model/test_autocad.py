import win32com.client


try:
    autocad = win32com.client.Dispatch("AutoCAD.Application")
    autocad.Visible = True

    print("AutoCAD connection successful")
    print("Version:", autocad.Version)

except Exception as error:
    print("AutoCAD connection failed")
    print(error)