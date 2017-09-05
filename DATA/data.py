from DATA import datasql


sql = datasql.GetDataFromPc()
data = sql.read()
print(data)