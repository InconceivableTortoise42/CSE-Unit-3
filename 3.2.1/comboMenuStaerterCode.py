#################################################################################
#    b3.1.3_TR_combo_menu_solution2.py
#    Example solution
################################################################################

order:list[str] = []

sandwhiches = ["beef", "chicken", "tofu"]
sizes = ["small", "medium", "large"]

# iteration 1 
sandwhich = input("Please pick a type of sandwhich, chicken for $5.25, beef for 6.25, or tofu for 5.75.")
if sandwhich not in sandwhiches:
  print("We don't sell that sandwich")
  sandwhich_bought = False 
else:
  sandwhich_bought = True
  print(sandwhich)
  order.append(sandwhich)

# iteration 2
beverage = input("Would you like a drink, yes or no?")
if (beverage == "yes"):
  beverage_bought = True
  beverage = input("would you like a small for $1.00, a medium for $1.75, or a large for $2.25?")
  if beverage not in sizes:
    print("We don't have that size")
    beverage_bought = False
  else:
    order.append(beverage + " beverage")
    print("You said", beverage, "drink.")
else:
  beverage_bought = False
  print("You did not want a drink.")
  
# iteration 2 cost
total = 0
if (sandwhich == "chicken"):
  total = total + 5.25
elif (sandwhich == "beef"):
  total = total + 6.25
elif (sandwhich == "tofu"):
  total = total + 5.75
  
if (beverage == "small"):
  total = total + 1
elif (beverage == "medium"):
  total = total + 1.75
elif (beverage == "large"):
  total = total + 2.25
  
  
# iteration 3
fries = input("Would you like french fries, yes or no? ")
if (fries == "yes"):
  fries_bought = True
  fries = input("Would you like a small for $1.00, a medium for $1.50, or a large for $2.00? ")
  if fries not in sizes:
    print("That size we do not sell!")
    fries_bought = False
  else:
    print("You said", fries, "fries.")
    order.append(fries +  " fries")
else: 
  fries_bought = False
  print("you did not want fries.")

if (fries == "small"):
  total = total + 1
elif (fries == "medium"):
  total = total + 1.50
elif (fries == "large"):
  total = total + 2
  

# iteration 4
ketchup_string = input("How many ketchup packets would you like? ")
ketchup = int(ketchup_string)
if ketchup < 0:
  print("We don't hand out negative matter")
else:
  ketchup_cost = ketchup * .25
  total += total + ketchup_cost
  order.append(ketchup_string +  " ketchup packets")

if (sandwhich_bought == True):
  if (beverage_bought == True):
    if (fries_bought == True):
      print("You bought:", sandwhich, "sandwhich,", beverage, "beverage,", fries, "fries, and", ketchup, "ketchup packets.")
      total = total - 1
    else:
      print("You bought:", sandwhich, "sandwhich", beverage, "beverage, no fries, and", ketchup, "ketchup packets.")
  elif (fries_bought == True):
    print("You bought:", sandwhich, "sandwhich, nothing to drink,", fries, "fries, and", ketchup, "ketchup packets.")
  else:
    print("You bought:", sandwhich, "sanwhich, nothing to drink, no fires, and", ketchup, "ketchup packets.")

print("Order Summary", [item + "\n" for item in order])
print(total)