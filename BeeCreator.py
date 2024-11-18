import json
import os

def generate_json():
    # Set default values
    default_color = "#c9c7c2"
    default_size = 1.0

    # Get user input for color, flowerItem, and mod ID
    primary_color = input(f"Enter primary color (hex format, or press Enter to use default '{default_color}'): ") or default_color

    # Get user input for secondary color or leave it empty if nothing is provided
    secondary_color = input(f"Enter secondary color (hex format, or press Enter to leave empty): ")

    particle_color = input(f"Enter particle color (hex format, or press Enter to use default '{default_color}'): ") or default_color
    size = float(input("Enter size (float format, e.g., 1.0): ") or default_size)
    flower_item = input("Enter flower item (e.g., 'gtceu:titanium_block' or If you leave it empty it will default to '#minecraft:flowers'")
    self_breed = input("Does it self-breed? (True/False) (Default: false): ").lower() or False

    # Get user input for mod ID or use default value "gtceu" if nothing is provided
    mod_id = input("Enter mod ID (or press Enter to use default 'gtceu'): ") or "gtceu"

    # Create JSON structure for the first file (bee)
    data = {
        "primaryColor": primary_color,
        "secondaryColor": secondary_color,
        "particleColor": particle_color,
        "size": size,
        "flowerItem": flower_item,
        "selfbreed": self_breed,
        "conditions": [
            {
                "type": "forge:mod_loaded",
                "modid": mod_id
            }
        ]
    }

    # Include secondaryColor in the JSON if the user provided input
    if not secondary_color:
        del data["secondaryColor"]

    # Get user input for file name
    bee_name = input("Enter the name of the file (without extension): ").lower()

    # Check if the input is empty
    while not bee_name:
        print("Please enter a non-empty name.")
        bee_name = input("Enter the name of the file (without extension): ").lower()

    # Get user input for save path or use desktop if no input
    save_path = input("Enter the save path (or press Enter to save on the desktop): ") or os.path.join(os.path.expanduser("~"), "Desktop")

    # Write JSON to file
    file_path = os.path.join(save_path, f"{bee_name}.json")
    with open(file_path, "w") as json_file:
        json.dump(data, json_file, indent=2)

    print(f"File '{file_path}' generated successfully.")

    # Ask the user if they want breeding or feeding conversion
    conversion_choice = input("Enter '1' for breeding, '2' for feeding, 'breeding', or 'feeding': \n ")


    while conversion_choice not in ['1', '2', 'breeding', 'feeding']:
        print("Invalid choice. Please enter '1' for breeding, '2' for feeding, 'breeding', or 'feeding'.")
        conversion_choice = input("Enter '1' for breeding, '2' for feeding, 'breeding', or 'feeding': \n")

    if conversion_choice in ['1', 'breeding']:
        print("Breeding: There is no need to type the mod if you type in bees just type the name")
        # Ask additional questions for breeding

        parent1_bee = input("Enter parent1 bee (e.g., crystalline): ")
        parent2_bee = input("Enter parent2 bee (e.g., ashy_mining_bee): ")

       
        # Create JSON structure for breeding
        breeding_data = {
            "type": "productivebees:bee_breeding",
            "parent1": f"productivebees:{parent1_bee}",
            "parent2": f"productivebees:{parent2_bee}",
            "offspring": [f"productivebees:{bee_name}"],
            "conditions": [
                {
                    "type": "productivebees:bee_exists",
                    "bee": f"productivebees:{bee_name}"
                },
                {
                    "type": "productivebees:bee_exists",
                    "bee": f"productivebees:{parent1_bee}"
                },
                {
                    "type": "productivebees:bee_exists",
                    "bee": f"productivebees:{parent2_bee}"
                }
            ]
        }

       # breeding_item_choice = input("Do you want Custom breeding Items (If you want to use tags instead change the code to 'tag' or change it manually) (True/False): ").lower() or False


        #if breeding_item_choice:
            #item1 = input("Enter breeding item1  (e.g., 'minecraft:dirt'): ")
            #item2 = input("Enter breeding item2  (e.g., 'minecraft:iron'): ")
            #breeding_data["breeding_items"] = [
                #{"item": item1},
                #{"item": item2}
            #]

        # Write breeding JSON to file
        breeding_file_path = os.path.join(save_path, f"{bee_name}_breeding.json")
        with open(breeding_file_path, "w") as json_file:
            json.dump(breeding_data, json_file, indent=2)

        print(f"Breeding file '{breeding_file_path}' generated successfully.")

    elif conversion_choice in ['2', 'feeding']:
        print("You selected feeding.")
        # Ask additional questions for feeding conversion
        source_bee = input("Enter the name of the source bee(e.g. iron)")
        feeding_item = input("Enter the feeding item (e.g., 'gtceu:nan_certificate'): ")
        
        # Create JSON structure for feeding conversion
        feeding_data = {
            "type": "productivebees:bee_conversion",
            "source": f"productivebees:{source_bee}",
            "result": f"productivebees:{bee_name}",
            "item": {
                "item": feeding_item
            },
            "conditions": [
                {
                    "type": "productivebees:bee_exists",
                    "bee": f"productivebees:{bee_name}"
                },
                {
                    "type": "productivebees:bee_exists",
                    "bee": f"productivebees:{source_bee}"
                }
            ]
        }

        # Write feeding JSON to file
        feeding_file_path = os.path.join(save_path, f"{bee_name}_bee.json")
        with open(feeding_file_path, "w") as json_file:
            json.dump(feeding_data, json_file, indent=2)

        print(f"Feeding conversion file '{feeding_file_path}' generated successfully.")
    

    produce_data = {
        "type": "productivebees:advanced_beehive",
        "ingredient": f"productivebees:{bee_name}",
        "results": [
            {
                "item": {
                    "type": "forge:nbt",
                    "item": "productivebees:configurable_honeycomb",
                    "nbt": {
                        "EntityTag": {
                            "type": f"productivebees:{bee_name}"
                        }
                    }
                }
            }
        ],
        "conditions": [
            {
                "type": "productivebees:bee_exists",
                "bee": f"productivebees:{bee_name}"
            }
        ]
    }

    produce_file_path = os.path.join(save_path, f"{bee_name}_produce.json")
    with open(produce_file_path, "w") as json_file:
        json.dump(produce_data, json_file, indent=2)

    print(f"Produce file '{produce_file_path}' generated successfully.\n\n")


    print("Put this inside the en_us file to give it the right name: " f"\"entity.productivebees.{bee_name}_bee\"" ": " f"\"{bee_name} Bee\"")


    print("You can change the name if you edit the string after the ':' :D")


# Call the function to generate JSON
generate_json()
