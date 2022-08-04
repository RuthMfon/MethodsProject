

class Inventory:

   def __init__(self, title, author, publisher, stock, price, isbn):

      self.Title = title

      self.Author = author

      self.Publisher = publisher

      self.Stock = stock

      self.Price = price

      self.ISBN = isbn



   def Connect_inventory(self):
      try:
         connection = mysql.connector.connect(host="localhost" ,user="root", password="", database="MethodsProject")
         print("Successful connection.")
         cursor = connection.cursor()
         return connection, cursor
      except:
         print("Failed connection.")
         sys.exit()   
         
    def Display_inventory(self):
      connection, cursor = self.Connect_cart()
      selectInventoryQuery = "SELECT * FROM inventory" 
      
      cursor.execute(selectInventoryQuery)
      connection.commit()
      
      result = cursor.fetchall()
      for row in result:
         print(row)
      
      cursor.close()
      connection.close()

class Cart:

   def __init__(self, isbn, quantity, price):

      self.ISBN = isbn

      self.Quantity = quantity

      self.Total = price

   def Connect_cart(self):
      try:
         connection = mysql.connector.connect(host="localhost",user="root",password="",database="MethodsProject")
         print("Successful connection.")
         cursor = connection.cursor()
         return connection, cursor
      except:
         print("Failed connection.")
         sys.exit()
         
    def Display_cart(self):
      connection, cursor = self.Connect_cart()
      selectCartQuery = "SELECT * FROM cart" 
      
      cursor.execute(selectCartQuery)
      connection.commit()
      
      result = cursor.fetchall()
      for row in result:
         print(row)
      
      cursor.close()
      connection.close()
         
    def Add_to_cart(self):
      connection, cursor = self.Connect_cart()
      
      item = input("Which item would you like to add to cart? (Enter ISBN): ")
      quantity = int(input("How many copies would you like to add to cart? "))
        
      selectPriceQuery = "SELECT Price FROM Inventory WHERE ISBN=%s" 
      data = (item)
      cursor.execute(selectPriceQuery,data)
      resultPrice = cursor.fetchall()
      
      total = quantity * resultPrice
        
      selectStockQuery = "SELECT Stock FROM Inventory WHERE ISBN=%s"
      data2 = (item)
      cursor.execute(selectStockQuery,data2)
      resultStock = cursor.fetchall()
        
      if quantity <= resultStock:  
        
          query = "INSERT INTO cart (ISBN, Quantity, Total) VALUES (%s, %s, %s)"
          data3 = (item, quantity, total)
            
          cursor.execute(query,data3)
          connection.commit() 
          print(cursor.rowcount, "record inserted, item is added to cart.")   
          cursor.close()
          connection.close()
      else:
          print("Error. There are not enough items in stock to add to cart.")
      
      cursor.close()
      connection.close()
     
   def Remove_from_cart(self):
      connection, cursor = self.Connect_cart()
        
      item = input("Which item would you like to remove from cart? (Enter ISBN): ")
        
      query = "DELETE FROM cart WHERE ISBN=%s"
      data = (item,)
      cursor.execute(query,data)
      connection.commit()
      print(cursor.rowcount, "record deleted, item is removed from cart.")
      cursor.close()
      connection.close()      
         
   def Checkout():
      connection, cursor = Cart.Connect_cart()
      #rows = cursor.execute("SELECT COUNT(ISBN) FROM cart")
      #for r in rows:
         #Inventory.lowerstock()
      cursor.execute("DELETE FROM cart")
      connection.commit()
      print(cursor.rowcount, "records deleted, cart cleared")
      cursor.close()
      connection.close()
      print("Connection closed")

      
def main():
   while True:
      i = Inventory("Test Title", "Test Author", "Test Publisher", 0, 0.00, "000-0000000000")
      c = Cart("000-0000000000", 0, 0.00)
      print("Welcome to the online book store!")
      print("Here are your options:")
      print("1. View Inventory\n2. Add to Inventory\n3. View Cart\n4. Add to Cart\n5. Remove from Cart\n6. Checkout\n7. Exit")
      option = int(input("Make your selection: "))
      if option == 1:
         i.Display_inventory()
      elif option == 2:
         i.Add_inventory()
      elif option == 3:
         c.Display_cart()
      elif option == 4:
         c.Add_to_cart()
      elif option == 5:
         c.Remove_from_cart()
      elif option == 6:
         c.Checkout()
      elif option == 7:
         return
      else:
         print("You have entered an incorrect value, please try again:")


main()


