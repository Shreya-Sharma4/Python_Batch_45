from login.admin_login import admin_login
from menus.user_menu import menu as user_menu
from menus.admin_menu import admin_menu

def main():
    while True:
        print("\n" + "="*40)
        print("   🍿 MOVIE TICKET BOOKING SYSTEM 🍿   ")
        print("="*40)
        print("1. User Panel")
        print("2. Admin Panel")
        print("3. Exit")
        
        choice = input("\nEnter your choice: ").strip()
        
        if choice == "1":
            user_menu()
        elif choice == "2":
            # If login is successful, open admin menu
            if admin_login():
                admin_menu()
        elif choice == "3":
            print("\nThank you for using the system. Goodbye!\n")
            break
        else:
            print("\n❌ Invalid choice. Please try again.")

if __name__ == "__main__":
    main()