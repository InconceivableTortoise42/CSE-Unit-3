food = ["Burger", "Shake", "Fries"]

for i, item in enumerate(food):
  print(f"Food: {item}, Index: {i}")

if ("Sundae" in food):
   print("One sundae, coming up!")
else:
   print("Sorry, we don't carry sundaes")

if ("Shake" in food):
   print("One Shake, coming up!")
else:
   print("Sorry, we don't carry shakes")

if ("Fries" in food):
   print("Fries, coming right up!")
else:
   print("Sorry, we don't carry fries")

if ("Burger" in food):
   print("One burger, coming up!")
else:
   print("Sorry, we don't carry burgers")

if ("Pizza" not in food):
   print("Pizza is not in the food list.")
else:
   print("Pizza is in the list.")