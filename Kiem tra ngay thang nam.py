day = int(input("Nhap ngay: "))
month = int(input("Nhap thang: "))
year = int(input("Nhap nam: "))

if 1 <= month <=12:
    if month in [4,6,9,11]:
        max_day = 30
    elif month == 2:
        if(year %4 == 0 and year % 100!= 0) or (year % 400 == 0):
            max_day = 29
        else:
            max_day = 28
    else:
        max_day = 31
    if 1 <= day <= max_day:
        print("Ngay hop le")
    else:
        print("Ngay khong hop le")
else:
    print("Thang khong hop le")