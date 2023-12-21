def get_stock():
    import pandas as pd
    from sqlalchemy import create_engine
    from sqlalchemy.engine.url import URL
    #from plyer import notification
    con_str = "DRIVER={ODBC Driver 17 for SQL Server};SERVER=192.168.1.20\\MKSSQL2017;DATABASE=SUNSCO_HN;UID=sa;PWD=sa1234"
    con_url = URL.create("mssql+pyodbc",query={"odbc_connect":con_str})
    engine = create_engine(con_url)
    SQL = "exec sp_VIE060_LoadData '1','%','%','%' ,'20231201','20231231','20231101','20231130' ,'E','%','%','%','%'"
    SQL1 = "SELECT CUSTOMER_CODE,E_NAME FROM CUSTOMMF"
    df = pd.read_sql(SQL,engine)
    df.to_csv("Database/StockEF.csv" ,index = False)
    dk = pd.read_sql(SQL1,engine)
    dk.to_csv("Database/Customer.csv",index = False)
    #notification.notify(title = "Thông Báo!!!",message = f"Load Dữ Liệu Thành Công!!",
        #timeout = 10 )

def get_BOM():
    import pandas as pd
    from sqlalchemy import create_engine
    from sqlalchemy.engine.url import URL
    #from plyer import notification
    con_str = "DRIVER={ODBC Driver 17 for SQL Server};SERVER=192.168.1.20\\MKSSQL2017;DATABASE=SUNSCO_HN;UID=sa;PWD=sa1234"
    con_url = URL.create("mssql+pyodbc",query={"odbc_connect":con_str})
    engine = create_engine(con_url)
    # Stock
    SQL2 = "SELECT ParentItemCode,ParentThickness2,ParentLength,ChildItemCode,ChildThickness2,ChildLength,ParentQty,ProcessCode,Main_Material From SPREADMF"
    SQL = "SELECT ITEM_CODE,ITEM_NAME_V,ITEM_GROUP1,ITEM_GROUP2,ITEM_GROUP3,ITEM_GROUP4,ITEM_GROUP5,GROUP15,DIAMETER1,DIAMETER2,THICKNESS,WIDTH,INV_DV FROM PRODUCTMF"
    SQL3 ="SELECT GROUP_CLASSIFY,GROUP_CODE_1,GROUP_CODE_2,GROUP_CODE_3,GROUP_CODE_4,GROUP_CODE_5,SHORT_NAME,GROUP_NAME_E,INV_DV FROM GROUPMF"
    BOM = pd.read_sql(SQL2,engine)
    Item = pd.read_sql(SQL,engine)
    Name = pd.read_sql(SQL3,engine)
    BOM.to_csv("Database/BOM.csv",index = False)
    Item.to_csv("Database/Itemcode.csv",index = False)
    Name_f = Name[(Name['INV_DV'] != "*")]
    Name_f.to_csv("Database/Code_Name.csv",index = False)

def read_stock():
    import pandas as pd
    stock_read = pd.read_csv('Database/StockEF.csv')
    cus = pd.read_csv('Database/Customer.csv')
    dk = pd.read_excel('Report/Report.xlsx',index_col=0)
    # Chinh sua du lieu stock
    stock_filter = stock_read[(stock_read["DIAMETER1"] !=0) & (stock_read["future_Stock"] >0)]
    stock = stock_filter.drop(['ITEM_CODE','GROUP_CODE','TotalLast_StockOut','TotalStockOut','HisStockOut','StockOut','TotalCurrentStock','TotalPln','PlnQty','ikey'],axis=1)
    cus1 = cus.dropna()
    cusname = pd.merge(stock,cus1,how="left",on=["CUSTOMER_CODE"])
    new_stock = cusname.drop(['CUSTOMER_CODE'],axis=1)
    # Chinh sua du lieu Mr.Cuong
    dk_s = dk.loc[1:,['CUSTOMER_NAME','Material_LP','DIAMETER1','DIAMETER2','THICKNESS','Group_LP','BeatCut']]
    long = dk_s.dropna()
    short_p = dk.loc[1:,['CUSTOMER_NAME','GROUP_NAME','DIAMETER1','DIAMETER2','THICKNESS','LENGTH','BeatCut']]
    long_p = long.rename(columns={'Material_LP':'GROUP_NAME','Group_LP':'LENGTH'})
    #stock = pd.DataFrame(dk)
    #longp = pd.DataFrame(df3)
    #result = pd.merge(left,right,how="left",on=["GROUP_NAME","DIAMETER1","DIAMETER2","THICKNESS","LENGTH","BeatCut"])
 
def read_delivery_Item():
    import pandas as pd
    from sqlalchemy import create_engine
    from sqlalchemy.engine.url import URL
    #from plyer import notification
    con_str = "DRIVER={ODBC Driver 17 for SQL Server};SERVER=192.168.1.20\\MKSSQL2017;DATABASE=SUNSCO_HN;UID=sa;PWD=sa1234"
    con_url = URL.create("mssql+pyodbc",query={"odbc_connect":con_str})
    engine = create_engine(con_url)
    # Stock
    SQL = "exec sp_Load_CUS025 '%','%','%','4','E'"
    Delivery_item = pd.read_sql(SQL,engine)
    Delivery_item.to_csv("Database/Delivery_item.csv",index = False)

def BOM_Compare():
    import pandas as pd
    r_bom = pd.read_csv('Database/BOM.csv')
    r_delivery = pd.read_csv('Database/Delivery_item.csv')
    r_item = pd.read_csv('Database/Itemcode.csv')
    r_name = pd.read_csv('Database/Code_Name.csv')
    #item_name = pd.merge(r_item,r_name,how="left",on=["GROUP_CODE_1","GROUP_CODE_2","GROUP_CODE_3","GROUP_CODE_4","GROUP_CODE_5"])
    #name1 = r_name.loc[0:,['GROUP_CODE_1','GROUP_CODE_2','GROUP_CODE_3','GROUP_CODE_4','GROUP_CODE_5','SHORT_NAME']]
    #xoa item user deleted.
    item_fix = r_item[(r_item['INV_DV'] != "*")&(r_item['WIDTH'] >0 )]
    #sua index de mapping
    r_name_fix = r_name.rename(columns={'GROUP_CODE_1':'ITEM_GROUP1','GROUP_CODE_2':'ITEM_GROUP2','GROUP_CODE_3':'ITEM_GROUP3','GROUP_CODE_4':'ITEM_GROUP4','GROUP_CODE_5':'ITEM_GROUP5'})
    item_name = pd.merge(item_fix,r_name_fix,how="left",on=["ITEM_GROUP1","ITEM_GROUP2","ITEM_GROUP3","ITEM_GROUP4"])
    item = item_name.loc[0:,['ITEM_CODE','DIAMETER1','DIAMETER2','THICKNESS','WIDTH','SHORT_NAME']]
    item_filter = item[(item['SHORT_NAME'] != "0")&(item['SHORT_NAME'] != "00")]
    item_filter.to_csv('Report/Coil_Name.csv')
    # Bien doi Delivery_Item
    Delivery = r_delivery.loc[0:,['CUSTOMER_CODE','CUSTOMER_GROUP','ITEM_CODE','Model','MaterialName','DIAMETER1','DIAMETER2','THICKNESS','LENGTH','ColorName','ProcessName','SurfaceName','INV_DV','HideInCUS030']]
    Delivery_filter = Delivery[(Delivery['INV_DV'] != "*")&(Delivery['HideInCUS030'] != 1)]
    Delivery_filter.to_csv('Report/Pipe_Name.csv')

    
get_stock()
get_BOM()
read_stock()
read_delivery_Item()
BOM_Compare()