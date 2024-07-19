import tkinter as tk
from tkinter import ttk, messagebox
from plyer import notification


# Sample user credentials (for demonstration purposes)
user_credentials = {"username": "shubham@123", "password": "password123"}

# Initialize user details dictionary
user_details = {
    "shubham@123": {
        "name": "ShubhamH Mangal",
        "email": "Abcdefg123@gmail.com",
        "phone": "75XXXXXXX",
    }
}


# Sample product catalog
products = [
    {"name": "Piano", "price": 500},
    {"name": "Guitar", "price": 300},
    {"name": "Drums", "price": 800},
    {"name": "Flute", "price": 600},
    {"name": "Clarinet", "price": 400},
    {"name": "Saxophone", "price": 450},
    {"name": "Violin", "price": 835},
    {"name": "Harp", "price": 522},
    {"name": "Sitar", "price": 799},
    {"name": "Harmonium", "price": 423},
    {"name": "Tabla", "price": 450},
    {"name": "xylophone", "price": 500},
    {"name": "Bagpipes", "price": 599},
    {"name": "Recorder", "price": 399},
]

# Initialize shopping cart
cart = []

# Create a list to store feedback
feedback_list = []


user_profile_window = None
name_entry = None
email_entry = None
phone_entry = None
signup_window = None
name_label = None
email_label = None
phone_label = None
feedback_window = None
feedback_text = None


# Function to open the "Feedback" window
def open_feedback_window():
    global feedback_window, feedback_text

    feedback_window = tk.Toplevel(root)
    feedback_window.title("Feedback")
    feedback_window.configure(bg="#1E3D59")  # Set background color to dark blue

    explanation_label = ttk.Label(
        feedback_window,
        text="We value your feedback! Please share your thoughts about your experience with our store below:",
        foreground="white",
        background="#1E3D59",
    )
    explanation_label.pack()

    feedback_label = ttk.Label(
        feedback_window, text="Your Feedback:", foreground="white", background="#1E3D59"
    )
    feedback_label.pack()

    feedback_text = tk.Text(feedback_window, height=5, width=40, font=("Helvetica", 12))
    feedback_text.pack()

    submit_button = ttk.Button(
        feedback_window,
        text="Submit Feedback",
        command=submit_feedback,
        style="Submit.TButton",
    )
    submit_button.pack()


def submit_feedback():
    feedback = feedback_text.get(
        "1.0", "end-1c"
    )  # Get the feedback text from the Text widget
    if feedback:
        feedback_list.append(feedback)  # Store the feedback in the list
        feedback_window.destroy()
        show_notification("Feedback Submitted", "Thank you for your feedback!")
        update_feedback_display()


def update_feedback_display():
    feedback_display_window = tk.Toplevel(root)
    feedback_display_window.title("Feedback Display")
    feedback_display_window.configure(bg="#1E3D59")  # Set background color to dark blue

    feedback_label = ttk.Label(
        feedback_display_window,
        text="Feedback Received:",
        foreground="white",
        background="#1E3D59",
    )
    feedback_label.pack()

    feedback_textbox = tk.Text(
        feedback_display_window, height=10, width=40, font=("Helvetica", 12)
    )
    feedback_textbox.pack()

    for feedback in feedback_list:
        feedback_textbox.insert("end", feedback + "\n")


# Function to authenticate user
def authenticate():
    entered_username = username_entry.get()
    entered_password = password_entry.get()
    if (
        entered_username == user_credentials["username"]
        and entered_password == user_credentials["password"]
    ):
        login_frame.grid_remove()
        product_catalog_frame.grid()
    else:
        login_status_label.config(text="Invalid credentials")


# Function to show product details
def show_product_details():
    selected_item = product_listbox.curselection()
    if selected_item:
        index = selected_item[0]
        product = next(
            (p for p in products if p["name"] == product_listbox.get(index)), None
        )
        if product:
            product_details_label.config(
                text=f"Name: {product['name']}\nPrice: ${product['price']}"
            )
        else:
            product_details_label.config(text="")


# Function to add product to the cart
def add_to_cart():
    selected_item = product_listbox.curselection()
    if selected_item:
        index = selected_item[0]
        product = next(
            (p for p in products if p["name"] == product_listbox.get(index)), None
        )
        if product:
            cart.append(product)
            update_cart_display()


# Function to remove selected item from the cart
def remove_from_cart():
    selected_item = cart_listbox.curselection()
    if selected_item:
        index = selected_item[0]
        del cart[index]
        update_cart_display()


# Function to update the cart display
def update_cart_display():
    cart_listbox.delete(0, "end")
    total_price = 0
    for item in cart:
        cart_listbox.insert("end", f"{item['name']} - ${item['price']}")
        total_price += item["price"]
    cart_total_label.config(text=f"Total: ${total_price}")


# Function to place an order
def place_order():
    if not cart:
        order_status_label.config(text="Cart is empty. Add items to cart.")
    else:
        open_placing_order_window()


# Function to process the order and payment
def process_order_and_payment(selected_product, shipping_address, payment_method):
    global placing_order_window

    payment_successful = tk.messagebox.askyesno(
        "Payment Confirmation",
        f"Total Amount: ${selected_product['price']}\nPayment Method: {payment_method}\n\nProceed with payment?",
    )
    if payment_successful:
        order_status_label.config(
            text="Order placed successfully. Notification will be sent."
        )

        # Send a notification to the user
        notification_title = "Order Placed"
        notification_message = (
            f"Your order for {selected_product['name']} has been placed successfully."
        )

        notification.notify(
            title=notification_title,
            message=notification_message,
            app_name="Online Music Store",
        )

        # Handle order processing (e.g., store order details in a database).
        cart.clear()
        update_cart_display()
        placing_order_window.destroy()
    else:
        order_status_label.config(text="Payment processing failed. Please try again.")


def show_notification(title, message):
    messagebox.showinfo(title, message)


# Function to open the "Placing Order" window
def open_placing_order_window():
    global placing_order_window  # Define placing_order_window as a global variable
    placing_order_window = tk.Toplevel(root)
    placing_order_window.title("Placing Order")

    product_label = ttk.Label(placing_order_window, text="Select Product:")
    product_label.pack()

    product_var = tk.StringVar()
    product_dropdown = ttk.Combobox(
        placing_order_window,
        textvariable=product_var,
        values=[product["name"] for product in products],
    )
    product_dropdown.pack()

    shipping_label = ttk.Label(placing_order_window, text="Shipping Address:")
    shipping_label.pack()

    shipping_entry = ttk.Entry(placing_order_window)
    shipping_entry.pack()

    payment_label = ttk.Label(placing_order_window, text="Select Payment Method:")
    payment_label.pack()

    payment_var = tk.StringVar()
    payment_options = ["Credit Card", "PayPal", "Cash on Delivery"]
    payment_dropdown = ttk.Combobox(
        placing_order_window, textvariable=payment_var, values=payment_options
    )
    payment_dropdown.pack()

    def process_placing_order():
        selected_product_name = product_var.get()
        shipping_address = shipping_entry.get()
        payment_method = payment_var.get()

        if not selected_product_name or not shipping_address or not payment_method:
            messagebox.showerror(
                "Error",
                "Please select a product, enter a shipping address, and choose a payment method.",
            )
        else:
            selected_product = next(
                (
                    product
                    for product in products
                    if product["name"] == selected_product_name
                ),
                None,
            )
            if selected_product:
                process_order_and_payment(
                    selected_product, shipping_address, payment_method
                )

    place_order_button = ttk.Button(
        placing_order_window, text="Place Order", command=process_placing_order
    )
    place_order_button.pack()


# Function to open the "User Profile" window
def open_user_profile_window():
    global user_profile_window, name_label, email_label, phone_label
    user_profile_window = tk.Toplevel(root)
    user_profile_window.title("User Profile")

    # Add user profile content here
    user_profile_label = ttk.Label(user_profile_window, text="User Profile")
    user_profile_label.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

    username = username_entry.get()

    # Check if the username exists in user_details
    if username in user_details:
        # Display user details
        ttk.Label(user_profile_window, text="Username:").grid(
            row=1, column=0, padx=10, pady=5
        )
        ttk.Label(user_profile_window, text=username).grid(
            row=1, column=1, padx=10, pady=5
        )

        ttk.Label(user_profile_window, text="Name:").grid(
            row=2, column=0, padx=10, pady=5
        )
        ttk.Label(user_profile_window, text=user_details[username]["name"]).grid(
            row=2, column=1, padx=10, pady=5
        )

        ttk.Label(user_profile_window, text="Email:").grid(
            row=3, column=0, padx=10, pady=5
        )
        ttk.Label(user_profile_window, text=user_details[username]["email"]).grid(
            row=3, column=1, padx=10, pady=5
        )

        ttk.Label(user_profile_window, text="Phone:").grid(
            row=4, column=0, padx=10, pady=5
        )
        ttk.Label(user_profile_window, text=user_details[username]["phone"]).grid(
            row=4, column=1, padx=10, pady=5
        )
    else:
        messagebox.showerror("Error", "User not found.")

    def close_user_profile_window():
        user_profile_window.destroy()

    close_button = ttk.Button(
        user_profile_window, text="Close", command=close_user_profile_window
    )
    close_button.grid(row=5, column=0, columnspan=2, padx=10, pady=10)


# Function to update and save user profile details
def update_user_profile():
    updated_name = name_entry.get()
    updated_email = email_entry.get()
    updated_phone = phone_entry.get()

    # Update user_details dictionary
    user_details[username_entry.get()]["name"] = updated_name
    user_details[username_entry.get()]["email"] = updated_email
    user_details[username_entry.get()]["phone"] = updated_phone

    # Close the user profile window
    user_profile_window.destroy()


def search_products():
    search_query = (
        search_entry.get().lower()
    )  # Get the search query and convert it to lowercase
    filtered_products = []

    # Filter products based on the search query
    for product in products:
        if search_query in product["name"].lower():
            filtered_products.append(product)

    # Clear and update the product listbox with the filtered products
    product_listbox.delete(0, "end")
    for product in filtered_products:
        product_listbox.insert("end", product["name"])


# Create the main window
root = tk.Tk()
root.title("Online Music Instrument Store")
root.configure(bg="#1E3D59")


# Create login frame
login_frame = ttk.Frame(root)
login_frame.grid(row=0, column=0, padx=20, pady=20)

username_label = ttk.Label(
    login_frame, text="Username:", foreground="black", font=("Helvetica", 12, "bold")
)
password_label = ttk.Label(
    login_frame, text="Password:", foreground="black", font=("Helvetica", 12, "bold")
)

username_entry = ttk.Entry(login_frame)
password_entry = ttk.Entry(login_frame, show="*")
login_button = ttk.Button(login_frame, text="Login", command=authenticate)
login_status_label = ttk.Label(login_frame, text="", foreground="red")

username_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
password_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")
username_entry.grid(row=0, column=1, padx=5, pady=5)
password_entry.grid(row=1, column=1, padx=5, pady=5)
login_button.grid(row=2, column=1, padx=5, pady=5)
login_status_label.grid(row=3, column=1, padx=5, pady=5)

# Create product catalog frame
product_catalog_frame = ttk.Frame(root)
product_catalog_frame.grid(row=0, column=0, padx=20, pady=20)

product_listbox = tk.Listbox(
    product_catalog_frame,
    bg="lightgrey",
    selectbackground="white",
    selectforeground="#1E3D59",
)
product_listbox.pack(side="left", fill="both", expand=True)

product_details_label = tk.Label(
    product_catalog_frame, text="", bg="#1E3D59", fg="white"
)
product_details_label.pack(side="right", padx=20)

product_listbox.bind("<<ListboxSelect>>", lambda event: show_product_details())

# Create shopping cart frame
cart_frame = ttk.Frame(root)
cart_frame.grid(row=0, column=1, padx=20, pady=20)

cart_label = ttk.Label(
    cart_frame, text="Shopping Cart", foreground="white", background="#1E3D59"
)
cart_label.pack()

cart_listbox = tk.Listbox(
    cart_frame, bg="lightgray", selectbackground="white", selectforeground="#1E3D59"
)
cart_listbox.pack(side="left", fill="both", expand=True)

cart_total_label = ttk.Label(
    cart_frame, text="", foreground="white", background="#1E3D59"
)
cart_total_label.pack()

add_to_cart_button = ttk.Button(
    product_catalog_frame, text="Add to Cart", command=add_to_cart
)
add_to_cart_button.pack()

remove_from_cart_button = ttk.Button(
    cart_frame, text="Remove from Cart", command=remove_from_cart
)
remove_from_cart_button.pack()

place_order_button = ttk.Button(cart_frame, text="Place Order", command=place_order)
place_order_button.pack()

user_profile_button = ttk.Button(
    cart_frame, text="User Profile", command=open_user_profile_window
)
user_profile_button.pack()

order_status_label = ttk.Label(
    cart_frame, text="", foreground="red", background="#1E3D59"
)
order_status_label.pack()

search_frame = ttk.Frame(product_catalog_frame)
search_frame.pack(fill="x", padx=10, pady=10)

search_label = ttk.Label(
    search_frame, text=" Search : ", foreground="white", background="red"
)
search_label.pack(side="left")

search_entry = ttk.Entry(search_frame)
search_entry.pack(side="left", fill="x", expand=True)

search_button = ttk.Button(search_frame, text="Search", command=search_products)
search_button.pack(side="left")

feedback_button = ttk.Button(cart_frame, text="Feedback", command=open_feedback_window)
feedback_button.pack()

# Styling for "Submit Feedback" button
style = ttk.Style()
style.configure(
    "Submit.TButton",
    foreground="black",
    background="#2980B9",
    font=("Helvetica", 10, "bold"),
)


# Populate product listbox with product names
for product in products:
    product_listbox.insert("end", product["name"])

# Hide the product catalog frame initially
product_catalog_frame.grid_remove()

root.mainloop()
