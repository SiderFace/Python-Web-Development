def travel_app():
   destination = input("Where do you want to travel? ")

   if destination == 'Paris':
      print("Enjoy your stay in Paris! ")
   elif destination == 'London':
      print("Enjoy your stay in London! ")
   elif destination == 'New York':
      print("Enjoy your stay in New York! ")
   else:
      print("Oops, that destination is not currently available. ")

travel_app()