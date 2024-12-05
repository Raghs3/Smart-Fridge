import tkinter as tk
from tkinter import messagebox
from contents import pantry, recipes
from meal_planner import add_shopping_item


class SmartFridgeGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Smart Fridge")
        self.root.geometry("600x400")

        self.shopping_list = {}

        # Recipe selection
        tk.Label(root, text="Available Recipes", font=("Arial", 14)).pack(pady=10)
        self.recipe_listbox = tk.Listbox(root, height=8, width=40)
        for recipe in recipes.keys():
            self.recipe_listbox.insert(tk.END, recipe)
        self.recipe_listbox.pack(pady=5)

        # Buttons
        tk.Button(root, text="Check Ingredients", command=self.check_ingredients).pack(pady=10)

        # Results
        self.result_label = tk.Label(root, text="", font=("Arial", 12), justify=tk.LEFT)
        self.result_label.pack(pady=5)

        self.shopping_list_label = tk.Label(root, text="", font=("Arial", 12), justify=tk.LEFT, fg="blue")
        self.shopping_list_label.pack(pady=5)

    def check_ingredients(self):
        # Get the selected recipe
        selected_index = self.recipe_listbox.curselection()
        if not selected_index:
            messagebox.showwarning("No Selection", "Please select a recipe!")
            return

        selected_recipe = self.recipe_listbox.get(selected_index)
        ingredients = recipes[selected_recipe]

        # Check pantry and generate a shopping list
        missing_items = []
        result_text = f"Ingredients for {selected_recipe}:\n"
        for item, required_qty in ingredients.items():
            available_qty = pantry.get(item, 0)
            if required_qty <= available_qty:
                result_text += f"  - {item}: OK\n"
            else:
                qty_to_buy = required_qty - available_qty
                result_text += f"  - {item}: Missing {qty_to_buy}\n"
                add_shopping_item(self.shopping_list, item, qty_to_buy)

        self.result_label.config(text=result_text)

        # Display the shopping list if any items are missing
        if self.shopping_list:
            shopping_text = "Shopping List:\n" + "\n".join(f"{item}: {qty}" for item, qty in self.shopping_list.items())
            self.shopping_list_label.config(text=shopping_text)
        else:
            self.shopping_list_label.config(text="")


# Main program
if __name__ == "__main__":
    root = tk.Tk()
    app = SmartFridgeGUI(root)
    root.mainloop()
