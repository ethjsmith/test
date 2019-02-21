from test2 import takeme
takke = takeme.take()
print takke.test2()
method = getattr(takke,"test2","failed")
print method()
