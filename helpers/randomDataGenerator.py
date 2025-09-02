import pandas as pd
import random
from datetime import datetime, timedelta

shelter_count = 28
animal_count = 500
employee_count = 140

#--- ANIMAL INFO ---#

animal_names = [
    "Milo", "Luna", "Charlie", "Bella", "Max", "Lucy", "Rocky", "Daisy", "Buddy", "Lily",
    "Jack", "Molly", "Toby", "Coco", "Oscar", "Sadie", "Leo", "Maggie", "Simba", "Chloe",
    "Lucky", "Sophie", "Oliver", "Bailey", "Zeus", "Ruby", "Finn", "Nala", "Rex", "Lola",
    "Buster", "Mia", "Duke", "Zoe", "Bruno", "Rosie", "Teddy", "Ellie", "Sam", "Ginger",
    "Benji", "Roxy", "Murphy", "Penny", "Shadow", "Gracie", "Gizmo", "Pepper", "Bear", "Annie",
    "Hunter", "Abby", "Marley", "Hazel", "Diesel", "Olive", "Ace", "Mocha", "Oreo", "Lexi",
    "Ziggy", "Athena", "Jake", "Cleo", "Louie", "Minnie", "Harley", "Belle", "Thor", "Izzy",
    "Winston", "Nina", "Kobe", "Dixie", "Boomer", "Millie", "Archie", "Sasha", "Chester", "Fiona",
    "George", "Cookie", "Tank", "Trixie", "Jasper", "Princess", "Scout", "Kiki", "Benny", "Bonnie",
    "Cash", "Sky", "Moose", "Angel", "Zane", "Kira", "Remy", "Pixie", "Romeo", "Tina",
    "Rusty", "Rita", "Chance", "Poppy", "Hank", "Nikki", "Blue", "Tara", "Zorro", "Sandy",
    "Tyson", "Maya", "King", "Lacey", "Ranger", "Honey", "Apollo", "Muffin", "Axel", "Dora",
    "Baxter", "Pearl", "Arlo", "Fluffy", "Sammy", "Snowy", "Einstein", "Cupcake", "Rambo", "Demi",
    "Indy", "Juno", "Yogi", "Fifi", "Ronnie", "Toffee", "Smokey", "Queenie", "Joey", "Nessie",
    "Riley", "Mochi", "Vito", "Minnie", "Colt", "Candy", "Jett", "Gala", "Lou", "Peach",
    "Turbo", "Dudu", "Melo", "Cinnamon", "Bolt", "Kiwi", "Flash", "Sprinkles", "Coco", "Pika",
    "Jet", "Sushi", "Maxi", "Nemo", "Tango", "Minty", "Whiskey", "Waffle", "Draco", "Cherry",
    "Frodo", "Taffy", "Groot", "Dudu", "Spike", "Churro", "Storm", "Latte", "Vader", "S'mores",
    "Marsh", "Figaro", "Bugsy", "Bambi", "Casper", "Clover", "Nacho", "Maple", "Zuzu", "Bingo",
    "Tiger", "Bubbles", "Ringo", "Misty", "Smudge", "Kovu", "Sparky", "Snowball", "Cloud", "Otis",
    "Mamba", "Pumpkin", "Fang", "Cuddles", "Pickles", "Tofu", "Skittles", "Whiskers", "Kermit", "Beans",
    "Fudge", "Choco", "Snickers", "Wiggles", "Biscuit", "Echo", "Freckles", "Garfield", "Raisin", "Twix",
    "Mittens", "Snuggles", "Hiccup", "Nugget", "Snappy", "Olaf", "Marble", "Yoda", "Tater", "Spud",
    "Corky", "Boom", "Socks", "Basil", "Chippy", "Shaggy", "Cricket", "Jelly", "Zipper", "Blitz"
]
animals = [
    "cat",
    "dog",
    "bird",
    "hamster",
    "rabbit",
    "turtle",
    "fish",
    "iguana",
    "mouse",
    "squirrel"
]
cat_breeds = [
    "Abyssinian", "American Bobtail", "American Curl", "American Shorthair", "American Wirehair",
    "Balinese", "Bengal", "Birman", "Bombay", "British Longhair", "British Shorthair", "Burmese",
    "Burmilla", "Chartreux", "Chausie", "Colorpoint Shorthair", "Cornish Rex", "Cymric", "Devon Rex",
    "Egyptian Mau", "European Shorthair", "Exotic Shorthair", "Havana Brown", "Himalayan",
    "Japanese Bobtail", "Javanese", "Korat", "Kurilian Bobtail", "LaPerm", "Lykoi", "Maine Coon",
    "Manx", "Munchkin", "Nebelung", "Norwegian Forest", "Ocicat", "Oriental Longhair",
    "Oriental Shorthair", "Persian", "Peterbald", "Pixie-Bob", "Ragdoll", "Russian Blue",
    "Savannah", "Scottish Fold", "Selkirk Rex", "Siamese", "Siberian", "Singapura", "Snowshoe",
    "Somali", "Sphynx", "Tonkinese", "Toyger", "Turkish Angora", "Turkish Van"
]
dog_breeds = [
    "Affenpinscher", "Afghan Hound", "Airedale Terrier", "Akita", "Alaskan Malamute",
    "American Bulldog", "American Cocker Spaniel", "American Eskimo Dog", "American Foxhound",
    "American Pit Bull Terrier", "American Staffordshire Terrier", "Anatolian Shepherd Dog",
    "Australian Cattle Dog", "Australian Shepherd", "Australian Terrier", "Basenji", "Basset Hound",
    "Beagle", "Bearded Collie", "Beauceron", "Bedlington Terrier", "Belgian Malinois",
    "Belgian Sheepdog", "Belgian Tervuren", "Bernese Mountain Dog", "Bichon Frise", "Black Russian Terrier",
    "Bloodhound", "Border Collie", "Border Terrier", "Borzoi", "Boston Terrier", "Bouvier des Flandres",
    "Boxer", "Boykin Spaniel", "Briard", "Brittany Spaniel", "Brussels Griffon", "Bull Terrier",
    "Bulldog (English)", "Bullmastiff", "Cairn Terrier", "Cane Corso", "Cardigan Welsh Corgi",
    "Cavalier King Charles Spaniel", "Chesapeake Bay Retriever", "Chihuahua", "Chinese Crested",
    "Chinese Shar-Pei", "Chow Chow", "Clumber Spaniel", "Cocker Spaniel (English)",
    "Collie", "Coton de Tulear", "Curly-Coated Retriever", "Dachshund", "Dalmatian",
    "Dandie Dinmont Terrier", "Doberman Pinscher", "Dogo Argentino", "Dogue de Bordeaux",
    "English Foxhound", "English Setter", "English Springer Spaniel", "English Toy Spaniel",
    "Entlebucher Mountain Dog", "Field Spaniel", "Finnish Lapphund", "Finnish Spitz",
    "Flat-Coated Retriever", "French Bulldog", "German Pinscher", "German Shepherd Dog",
    "German Shorthaired Pointer", "German Wirehaired Pointer", "Giant Schnauzer",
    "Glen of Imaal Terrier", "Golden Retriever", "Gordon Setter", "Great Dane", "Great Pyrenees",
    "Greater Swiss Mountain Dog", "Greyhound", "Harrier", "Havanese", "Ibizan Hound", "Irish Setter",
    "Irish Terrier", "Irish Water Spaniel", "Irish Wolfhound", "Italian Greyhound", "Jack Russell Terrier"
]
bird_breeds = [
    "Budgerigar", "Canary", "Macaw (Blue-and-Gold)", "Macaw (Scarlet)", "African Grey Parrot",
    "Cockatoo", "Lovebird", "Zebra Finch", "European Goldfinch", "Gouldian Finch", "Cardinal",
    "Roller Canary", "Border Canary", "Norwich Canary", "Fife Canary", "Gloster Canary",
    "Spanish Timbrado Canary", "American Singer Canary", "Lancashire Canary", "Kakariki",
    "Monk Parakeet", "Rosella", "Ringneck Parakeet", "Bourke's Parrot", "Eclectus Parrot",
    "Sun Conure", "Green Cheek Conure", "Blue Crown Conure", "Dusky Conure", "Indian Ringneck",
    "Alexandrine Parakeet", "Cockatiel", "Quaker Parrot", "Senegal Parrot", "Pionus Parrot",
    "Caique", "Lorikeet", "Bee-eater", "Star Finch", "Crimson Rosella", "Eastern Rosella",
    "Scarlet Macaw", "Blue-and-Gold Macaw", "Hyacinth Macaw", "Military Macaw", "Golden Parakeet",
    "Splendid Parakeet", "Princess Parrot", "Plum-headed Parakeet", "Red-rumped Parrot"
]
rabbit_breeds = [
    "Holland Lop", "Mini Lop", "French Lop", "English Lop", "Lionhead", "Netherland Dwarf",
    "Mini Rex", "Standard Rex", "Flemish Giant", "New Zealand White", "New Zealand Red",
    "New Zealand Black", "Californian", "Checkered Giant", "Silver Marten", "Himalayan",
    "English Angora", "French Angora", "Satin Angora", "German Angora", "Jersey Wooly",
    "Polish", "Harlequin", "Belgian Hare", "Chinchilla", "American Chinchilla", "Giant Chinchilla",
    "Champagne d'Argent", "Crème d'Argent", "Silver Fox", "Thrianta", "Tan Rabbit",
    "English Spot", "Dutch", "Dwarf Hotot", "American Fuzzy Lop", "Mini Satin", "Satin",
    "Palomino", "Florida White", "Cinnamon", "English Rabbit", "Alaska", "Rhinelander",
    "Velveteen Lop", "American Sable", "Havana", "Britannia Petite", "Blanc de Hotot"
]
fish_breeds = [
    "Japon Balığı (Common Goldfish)", "Comet Goldfish", "Shubunkin", "Oranda", "Ranchu", "Lionhead",
    "Ryukin", "Black Moor", "Bubble Eye", "Celestial Eye", "Fantail", "Veiltail",
    "Telescope Goldfish", "Panda Moor", "Pearlscale", "Pompom Goldfish", "Guppy", "Endler Guppy",
    "Molly", "Black Molly", "Dalmatian Molly", "Sailfin Molly", "Platy", "Swordtail",
    "Angelfish", "Discus", "Oscar", "Convict Cichlid", "Jack Dempsey", "Firemouth Cichlid",
    "Parrotfish", "Ram Cichlid", "Kribensis", "Electric Blue Acara", "Green Terror", "Frontosa",
    "Neon Tetra", "Cardinal Tetra", "Glowlight Tetra", "Ember Tetra", "Black Skirt Tetra",
    "Zebra Danio", "Pearl Danio", "Giant Danio", "White Cloud Minnow", "Rainbowfish", "Killifish",
    "Clown Loach", "Kuhli Loach", "Corydoras Catfish", "Pleco", "Betta (Siamese Fighting Fish)"
]
hamster_breeds = [
    "Syrian Hamster", "Golden Hamster", "Teddy Bear Hamster", "Black Bear Hamster",
    "Albino Syrian", "Long-haired Syrian", "Short-haired Syrian", "Banded Syrian",
    "Satin Syrian", "Cream Syrian", "White Syrian", "Silver Grey Syrian", "Cinnamon Syrian",
    "Campbell's Dwarf", "Albino Campbell's", "Black Campbell's", "Blue Campbell's",
    "Fawn Campbell's", "Opal Campbell's", "Platinum Campbell's", "Winter White",
    "Pearl Winter White", "Sapphire Winter White", "Normal Winter White",
    "Roborovski Hamster (Agouti)", "Roborovski White Face", "Roborovski Husky",
    "Roborovski Platinum", "Roborovski Normal", "Chinese Hamster", "Chinese Hamster (Striped)",
    "Chinese Hamster (Dominant Spot)", "Chinese Hamster (White)", "Chinese Hamster (Black-eyed White)",
    "Chinese Hamster (Beige)", "Syrian (Umbrous)", "Syrian (Honey Cream)", "Syrian (Yellow)",
    "Syrian (Silver Grey)", "Syrian (Smoke Pearl)", "Syrian (Lilac)", "Syrian (Chocolate)",
    "Syrian (Black)", "Syrian (White)", "Syrian (Sable)", "Syrian (Calico)",
    "Syrian (Tortoiseshell)", "Syrian (Roan)", "Syrian (Dalmatian)"
]
turtle_breeds = [
    "Kırmızı Yanaklı Su Kaplumbağası", "Yellow-Bellied Slider", "Cumberland Slider",
    "Painted Turtle", "Diamondback Terrapin", "Mississippi Map Turtle", "Common Map Turtle",
    "False Map Turtle", "Spiny Softshell Turtle", "Smooth Softshell Turtle", "Common Musk Turtle",
    "Razorback Musk Turtle", "Eastern Mud Turtle", "Striped Mud Turtle", "Loggerhead Musk Turtle",
    "Eastern Box Turtle", "Three-Toed Box Turtle", "Gulf Coast Box Turtle", "Florida Box Turtle",
    "Ornate Box Turtle", "Desert Box Turtle", "Spotted Turtle", "Wood Turtle", "Blanding's Turtle",
    "Bog Turtle", "Western Painted Turtle", "Midland Painted Turtle", "Southern Painted Turtle",
    "Eastern Painted Turtle", "Leopard Tortoise", "Indian Star Tortoise", "Greek Tortoise",
    "Russian Tortoise", "Hermann's Tortoise", "Marginated Tortoise", "Egyptian Tortoise",
    "Aldabra Giant Tortoise", "Galápagos Giant Tortoise", "Sulcata Tortoise", "Red-footed Tortoise",
    "Yellow-footed Tortoise", "Elongated Tortoise", "Burmese Star Tortoise", "Asian Forest Tortoise",
    "Radiated Tortoise", "Spider Tortoise", "Pancake Tortoise", "Gopher Tortoise", "Snapping Turtle",
    "Alligator Snapping Turtle"
]
genders = ["male", "female"]
neutering_status_male = ["Neutered", "Intact"]
neutering_status_female = ["Spayed", "Intact"]
conditions = ["healthy", "sick", "under_treatment"]

#--- SHELTER INFO ---#

shelter_names = [
    "Cankaya Karatas Gecici Hayvan Bakimevi",
    "Golbasi Gecici Hayvan Bakimevi ve Rehabilitasyon Merkezi",
    "Sincan Gecici Hayvan Bakimevi ve Rehabilitasyon Merkezi",
    "Patipark Hayvan Barinagi",
    "Etimesgut Hayvan Barinagi",
    "Cankaya Cemil Erkok Rehabilitasyon Merkezi",
    "Esenyurt Hayvan Bakimevi ve Rehabilitasyon Merkezi",
    "Altindag Belediyesi Hayvan Barinagi",
    "Esenyurt Hayvan Bakimevi ve Rehabilitasyon Merkezi",
    "Yedikule Hayvan Barinagi",
    "Tuzla Hayvan Barinagi",
    "Kadikoy Belediyesi Gecici Hayvan Bakim Merkezi",
    "Sile Hayvan Barinagi",
    "Buyukcekmece Sahipsiz Hayvanlar Bakim Merkezi",
    "Gumusdere Sahipsiz Hayvan Bakimevi",
    "Tepeoren Sahipsiz Hayvan Bakimevi",
    "Orhanli Sahipsiz Hayvan Bahceli Yasam Alani",
    "Kemerburgaz Sahipsiz Hayvan Bakimevi",
    "Beykoz Barinagi",
    "Mimarsinan Barinagi",
    "Seferihisar Hayvan Barinagi",
    "Selcuk Hayvan Barinagi",
    "Isikkent Gecici Kopek Bakimevi",
    "Pako Sokak Hayvanlari Sosyal Yasam Kampusu",
    "Buca Sokak Hayvanlari Rehabilitasyon Merkezi",
    "Foca Belediyesi Gecici Bakimevi",
    "Guzelbahce Gecici Kopek Bakimevi",
    "Patipark Hayvan Bakim ve Rehabilitasyon Merkezi"
]
shelter_locations = [
    "Cankaya, Ankara",
    "Gölbasi, Ankara",
    "Sincan, Ankara",
    "Ayas, Ankara",
    "Etimesgut, Ankara",
    "Cankaya, Ankara",
    "Mamak, Ankara",
    "Altindag, Ankara",
    "Esenyurt, Istanbul",
    "Fatih, Istanbul",
    "Tuzla, Istanbul",
    "Atasehir, Istanbul",
    "Sile, Istanbul",
    "Buyukcekmece, Istanbul",
    "Sariyer, Istanbul",
    "Pendik, Istanbul",
    "Tuzla, Istanbul",
    "Eyupsultan, Istanbul",
    "Beykoz, Istanbul",
    "Mimarsinan, Istanbul",
    "Seferihisar, Izmir",
    "Selcuk, Izmir",
    "Bornova, Izmir",
    "Bornova, Izmir",
    "Buca, Izmir",
    "Foca, Izmir",
    "Guzelbahce, Izmir",
    "Aliaga, Izmir"
]
shelter_capacity = [
    6000, 1500, 2200, 1000, 200, 470, 250, 150, 700, 2000,
    300, 350, 150, 2500, 1300, 1200, 500, 400, 1600, 150,
    250, 600, 550, 1500, 100, 200, 150, 250
]

#--- EMPLOYEE INFO ---#

employee_first_names = [
    "Ahmet", "Mehmet", "Fatma", "Ayse", "Emre", "Elif", "Can", "Deniz", "Mert", "Zeynep",
    "Hakan", "Hasan", "Huseyin", "Ismail", "Burak", "Ozge", "Cem", "Serkan", "Selin", "Ece",
    "Yusuf", "Sinem", "Irem", "Berke", "Omer", "Merve", "Esra", "Ali", "Sule", "Gokhan",
    "Murat", "Busra", "Eren", "Ilker", "Furkan", "Nazli", "Seda", "Volkan", "Gizem", "Okan",
    "Derya", "Selcuk", "Ceyda", "Ebru", "Suat", "Kadir", "Rabia", "Tugba", "Oguz", "Damla",
    "Baris", "Emine", "Sibel", "Cihan", "Ferhat", "Sirin", "Halil", "Asli", "Engin", "Nazan",
    "Volkan", "Ozlem", "Tuba", "Yasemin", "Fatih", "Hulya", "Kemal", "Elvan", "Murat", "Figen",
    "Tolga", "Sevgi", "Levent", "Gamze", "Ismail", "Hande", "Caglar", "Selma", "Onur", "Hatice",
    "Ali", "Nihat", "Serap", "Suleyman", "Nesrin", "Baran", "Leyla", "Kaan", "Nilay", "Deniz",
    "Arda", "Gulay", "Veli", "Pelin", "Suat", "Gul", "Ozan", "Nermin", "Fikret", "Bahar",
    "Ramazan", "Ozkan", "Naci", "Senay", "Efe", "Gulsah", "Berk", "Necla", "Fahri", "Selin",
    "Ugur", "Feride", "Ibrahim", "Sevil", "Serhat", "Yeliz", "Mevlut", "Fatma", "Halime", "Cansu",
    "Melek", "Deniz", "Seda", "Hakan", "Sibel", "Emir", "Bahar", "Alper", "Gulizar", "Koray",
    "Cemre", "Zeki", "Dilek", "Burcu", "Sinan", "Mine", "Baris", "Sebnem", "Ersin", "Sule",
    "Gokce", "Firat", "Duygu", "Tolga", "Sevim", "Ferit", "Pelin"
]

employee_last_names = [
    "Yilmaz", "Kaya", "Demir", "Celik", "Sahin", "Yildiz", "Ozturk", "Aydin", "Arslan", "Dogan",
    "Kurt", "Koc", "Ozdemir", "Polat", "Gunes", "Acar", "Erdogan", "Aksoy", "Cetin", "Kaplan",
    "Yalcin", "Bulut", "Ozkan", "Aslan", "Tas", "Kilinc", "Bozkurt", "Erdem", "Kara", "Ozer",
    "Cakir", "Duran", "Tekin", "Gur", "Yucel", "Yavuz", "Sever", "Ozkan", "Kalkan", "Ozkan",
    "Arikan", "Yilmazer", "Demirtas", "Sonmez", "Altun", "Cinar", "Gul", "Ozturk", "Eren", "Erkan",
    "Karaaslan", "Kalkan", "Sari", "Uslu", "Ozkan", "Aktas", "Polat", "Celik", "Kurtulus", "Ucar",
    "Yildirim", "Gok", "Aydin", "Kara", "Cakmak", "Ozer", "Basaran", "Savas", "Guler", "Kurt",
    "Erdem", "Kara", "Ozdemir", "Yalcin", "Koc", "Gunduz", "Cetin", "Kaplan", "Demirci", "Akdogan",
    "Ozkan", "Arslan", "Sahin", "Yilmaz", "Kaya", "Demir", "Celik", "Sahin", "Yildiz", "Ozturk",
    "Aydin", "Arslan", "Dogan", "Kurt", "Koc", "Ozdemir", "Polat", "Gunes", "Acar", "Erdogan",
    "Aksoy", "Cetin", "Kaplan", "Yalcin", "Bulut", "Ozkan", "Aslan", "Tas", "Kilinc", "Bozkurt",
    "Erdem", "Kara", "Ozer", "Cakir", "Duran", "Tekin", "Gur", "Yucel", "Yavuz", "Sever",
    "Ozkan", "Kalkan", "Ozkan", "Arikan", "Yilmazer", "Demirtas", "Sonmez", "Altun", "Cinar",
    "Gul", "Ozturk", "Eren", "Erkan", "Karaaslan", "Kalkan", "Sari", "Uslu", "Ozkan", "Aktas",
    "Polat", "Celik", "Kurtulus", "Ucar", "Yildirim", "Gok", "Aydin", "Kara", "Cakmak"
]

roles = ["Veterinarian", "Caretaker", "Cleaning Staff", "Manager", "Volunteer"]


#--- VET INFO ---#

vet_specialties = [
    "Internal Medicine",
    "Surgery",
    "Obstetrics and Gynecology",
    "Parasitology",
    "Microbiology",
    "Animal Nutrition",
    "Epidemiology",
    "Pathology",
    "Pharmacology",
    "Radiology",
    "Rehabilitation",
    "Anesthesiology",
    "Animal Science",
    "Intensive Care",
    "Emergency",
]

#--- MEDICAL INFO ---#

diagnoses = [
    "Parvovirus infection",
    "Distemper",
    "Kennel cough",
    "Lyme disease",
    "Dermatitis",
    "Ear infection",
    "Parasitic infection",
    "Gastritis",
    "Diabetes",
    "Heart disease",
    "Kidney failure",
    "Hypothyroidism",
    "Patellar luxation",
    "Cancer"
]
treatments = [
    "Fluid therapy, antiviral drugs, supportive care",
    "Antiviral and antibiotic therapy, vaccination",
    "Antibiotics, cough suppressants, rest",
    "Antibiotics, tick preventive medications",
    "Topical corticosteroids, antihistamines",
    "Antibiotic ear drops, ear cleaning",
    "Parasitic preventive medications, regular care",
    "Antacids, diet modification, proton pump inhibitors",
    "Insulin therapy, diet and exercise",
    "Medication, diet, exercise, and regular check-ups",
    "Diet modification, dialysis, supportive care",
    "Thyroid hormone replacement therapy",
    "Surgical intervention, physical therapy, pain relief",
    "Chemotherapy, radiotherapy, surgical intervention"
]

#FOR ANIMALS SHEET

shelter_ids = list(range(1, shelter_count+1))

animal_id = list(range(1, animal_count + 1))

shelter_id_animal = [random.choice(shelter_ids) for _ in range(animal_count)]
shelter_id_animal.sort()

name = [random.choice(animal_names) for _ in range(animal_count)]
animal_type = [random.choice(animals) for _ in range(animal_count)]

breed = []
for a_type in animal_type:
    if a_type == "cat":
        breed.append(random.choice(cat_breeds))
    elif a_type == "dog":
        breed.append(random.choice(dog_breeds))
    elif a_type == "bird":
        breed.append(random.choice(bird_breeds))
    elif a_type == "rabbit":
        breed.append(random.choice(rabbit_breeds))
    elif a_type == "fish":
        breed.append(random.choice(fish_breeds))
    elif a_type == "hamster":
        breed.append(random.choice(hamster_breeds))
    elif a_type == "turtle":
        breed.append(random.choice(turtle_breeds))
    else:
        breed.append("Mixed/Unknown")

weight = []
for a_type in animal_type:
    if a_type == "cat":
        weight.append(round(random.uniform(2.0, 7.0), 1))
    elif a_type == "dog":
        weight.append(round(random.uniform(3.0, 40.0), 1))
    elif a_type == "bird":
        weight.append(round(random.uniform(0.05, 2.0), 2))
    elif a_type == "rabbit":
        weight.append(round(random.uniform(1.0, 6.0), 1))
    elif a_type == "fish":
        weight.append(round(random.uniform(0.01, 1.0), 2))
    elif a_type == "hamster":
        weight.append(round(random.uniform(0.03, 0.2), 2))
    elif a_type == "turtle":
        weight.append(round(random.uniform(0.5, 20.0), 1))
    else: 
        weight.append(round(random.uniform(0.1, 5.0), 1))

gender = [random.choice(genders) for _ in range(animal_count)]

neutering_status = []
for g in gender:
    if g == "male":
        neutering_status.append(random.choice(neutering_status_male))
    else:
        neutering_status.append(random.choice(neutering_status_female))

arrival_date = [datetime.strptime(f"{random.randint(2020,2026)}-{random.randint(1,12)}-{random.randint(1,28)}", "%Y-%m-%d").date() for _ in range(animal_count)]

current_year = datetime.now().year
age = [random.randint(0, 15) if (current_year - d.year) > 15 else random.randint(current_year - d.year, 15) for d in arrival_date]

health_condition = [random.choice(conditions) for _ in range(animal_count)]

#FOR EMPLOYEES SHEET

employee_id = list(range(1, employee_count + 1))
first_name = [random.choice(employee_first_names) for _ in range(employee_count)]
last_name = [random.choice(employee_last_names) for _ in range(employee_count)]
start_date = [datetime.strptime(f"{random.randint(2018,2026)}-{random.randint(1,12)}-{random.randint(1,28)}", "%Y-%m-%d").date() for _ in range(employee_count)]

role_column = []

for s_id in range(1, shelter_count+1):
    for role in roles:
        role_column.append(role)

shelter_id_employee = [random.choice(shelter_ids) for _ in range(employee_count)]
shelter_id_employee.sort()


df_employee = pd.DataFrame({
    "employee_id": employee_id,
    "name": first_name,
    "last_name": last_name,
    "role": role_column,
    "start_date": start_date,
    "shelter_id": shelter_id_employee
})

#FOR VETS SHEET

df_vets = df_employee[df_employee["role"] == "Veterinarian"]
df_vets["specialties"] = [random.choice(vet_specialties) for _ in range(len(df_vets))]

df_animal = pd.DataFrame({
    "animal_id": animal_id,
    "name": name,
    "animal_type": animal_type,
    "breed": breed,
    "gender": gender,
    "age": age,
    "weight": weight,
    "neutering_status": neutering_status,
    "health_condition": health_condition,
    "arrival_date": arrival_date,
    "shelter_id": shelter_id_animal
})

#FOR SHELTERS SHEET

df_shelter = pd.DataFrame({
    "shelter_id": shelter_ids,
    "shelter_name": shelter_names,
    "location": shelter_locations,
    "capacity": shelter_capacity,
    "password": shelter_ids
})

#FOR EXAMINATIONS SHEET

animals_under_treatment = df_animal[df_animal["health_condition"] == "under_treatment"]

examination_records = []

exam_id = 1
for _, row in animals_under_treatment.iterrows():
    animal_id = row["animal_id"]
    shelter_id = row["shelter_id"]

    vets_in_shelter = df_vets[df_vets["shelter_id"] == shelter_id]
    if len(vets_in_shelter) == 0:
        continue  
    vet_id = random.choice(vets_in_shelter["employee_id"].tolist())

    diag_index = random.randint(0, len(diagnoses)-1)
    diagnosis = diagnoses[diag_index]
    treatment = treatments[diag_index]
    
    examination_records.append({
        "examination_id": exam_id,
        "animal_id": animal_id,
        "veterinarian_id": vet_id,
        "date": row["arrival_date"],
        "diagnosis": diagnosis,
        "treatment": treatment
    })
    exam_id += 1

df_examinations = pd.DataFrame(examination_records)

with pd.ExcelWriter("./data/animal_shelter.xlsx") as writer:
    df_animal.to_excel(writer, sheet_name="animals", index=False)
    df_shelter.to_excel(writer, sheet_name="shelters", index=False)
    df_employee.to_excel(writer, sheet_name="employees", index=False)
    df_vets.to_excel(writer, sheet_name="vets", index=False)
    df_examinations.to_excel(writer, sheet_name="examinations", index=False)
    


print("Excel file successfully created: data/animal_shelter.xlsx")
