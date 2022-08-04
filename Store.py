import mysql.connector
import sys



class Inventory:

   def __init__(self, title, author, publisher, stock, price, isbn):

      self.Title = title

      self.Author = author

      self.Publisher = publisher

      self.Stock = stock

      self.Price = price

      self.ISBN = isbn

   

   def getTitle(self):

      return self.Title

   def getAuthor(self):

      return self.Author

   def getPublisher(self):

      return self.Publisher

   def getStock(self):

      return self.Stock

   def getPrice(self):

      return self.Price

   def getISBN(self):

      return self.ISBN

   def Connect_inventory(self):
      try:
         connection = mysql.connector.connect(host="localhost" ,user="root", password="", database="MethodsProject")
         print("Successful connection.")
         cursor = connection.cursor()
         return connection, cursor
      except:
         print("Failed connection.")
         sys.exit()   
         
   def display_inventory(self):
      connection, cursor = self.Connect_inventory()
      selectInventoryQuery = "SELECT * FROM inventory" 
      
      cursor.execute(selectInventoryQuery)
      
      result = cursor.fetchall()
      connection.commit()
      
      for row in result:
         print("ISBN:", row[0], "||  Title:", row[1], "||  Author:", row[2])
         print("\tPublisher:", row[3], "||  In Stock:", row[4], "||  Price:$", row[5])
         print()
         
      
      cursor.close()
      connection.close()
      
   def lower_inventory(self, item):
    
      connection, cursor = self.Connect_inventory()
      selectQuantityQ = "SELECT Quantity FROM cart WHERE ISBN= %s"

      data = (item,)

      cursor.execute(selectQuantityQ, data)

      resultQuantity = cursor.fetchall()
    

      connection, cursor = self.Connect_inventory()

      selectStockQ = "SELECT Stock FROM inventory WHERE ISBN= %s"

      data2 = (item,)

      cursor.execute(selectStockQ, data2)

      resultStock = cursor.fetchall()
      
      newStock = resultStock[0][0] - resultQuantity[0][0]


      que = "UPDATE inventory SET Stock = %s WHERE ISBN = %s"

      data3 = (newStock, item)

      cursor.execute(que, data3)
      connection.commit()
      
      cursor.close()
      connection.close()

class Cart:

   def __init__(self, isbn, quantity, price):

      self.ISBN = isbn

      self.Quantity = quantity

      self.Total = price



   def getISBN(self):

      return self.ISBN

   def getQuantity(self):

      return self.Quantity

   def getTotal(self):

      return self.Total

   def Connect_cart(self):
      try:
         connection = mysql.connector.connect(host="localhost",user="root",password="",database="MethodsProject")
         print("Successful connection.")
         cursor = connection.cursor()
         return connection, cursor
      except:
         print("Failed connection.")
         sys.exit()
         
   def display_cart(self):
      connection, cursor = self.Connect_cart()
      selectCartQuery = "SELECT * FROM cart" 

      cursor.execute(selectCartQuery)

      result = cursor.fetchall()
      connection.commit()
      
      for row in result:
         print("ISBN:", row[0], "||  Quantity in Cart:", row[1], "||  Total price:$", row[2])
      
      cursor.close()
      connection.close()
         
   def Add_to_cart(self):
      connection, cursor = self.Connect_cart()
      
      item = input("Which item would you like to add to cart? (Enter ISBN): ")
      if len(item) != 13:
         item = input("That is not a valid ISBN number, please try again: ")
      quantity = int(input("How many copies would you like to add to cart? "))
        
      selectPriceQuery = "SELECT Price FROM inventory WHERE ISBN= %s" 
      data = (item,)
      cursor.execute(selectPriceQuery, data)
      resultPrice = cursor.fetchall()
      
      total = quantity * resultPrice[0][0]
        
      selectStockQuery = "SELECT Stock FROM inventory WHERE ISBN=%s"
      data2 = (item,)
      cursor.execute(selectStockQuery,data2)
      resultStock = cursor.fetchall()
        
      if quantity <= resultStock[0][0]:  
        
          query = "INSERT INTO cart (ISBN, Quantity, Price) VALUES (%s, %s, %s)"
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
         
   def Checkout(self,inventory):
   
      connection, cursor = self.Connect_cart()
      cursor.execute("SELECT * FROM cart")
      
      for row in cursor:
         inventory.lower_inventory(row[0])
         
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
      print("1. View Inventory\n2. View Cart\n3. Add to Cart\n4. Remove from Cart\n5. Checkout\n6. Exit")
      option = input("Make your selection: ")
      if option == "1":
         i.display_inventory()
      elif option == "2":
         c.display_cart()
      elif option == "3":
         c.Add_to_cart()
      elif option == "4":
         c.Remove_from_cart()
      elif option == "5":
         c.Checkout(i)
      elif option == "6":
         return
      else:
         print("You have entered an incorrect value, please try again:")


main()
  
