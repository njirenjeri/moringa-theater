from models import Role, Audition, session
# from sqlalchemy.orm import sessionmaker
# from sqlalchemy import create_engine

# Connect to the database
# engine = create_engine("sqlite:///moringa_theater.db")  
# Session = sessionmaker(bind=engine)
# session = Session()

def add_role():
    """Function to add a new role"""
    character_name = input("Enter the character name for the role: ")
    if character_name:
        new_role = Role(character_name=character_name)
        session.add(new_role)
        session.commit()
        print(f"✅ Role '{character_name}' added successfully!")
    else:
        print('Could not add character')
    # return new_role.id

def add_audition():
    """Function to add an audition for a given role"""
    actor = input("Enter actor's name: ")
    location = input("Enter audition location: ")
    phone_no = input("Enter actor's phone number: ")
    # hired = input("Was the actor hired? (yes/no): ").strip().lower() == "yes"

    roles = session.query(Role).all()
    if not roles:
        print('No available roles')

    print('\nAvailble roles for hire')
    for role in roles:
        print(f"{role.id}. {role.character_name}")
    
    role_id = input('Enter role ID to audition for: ').strip()
    if not role_id.isdigit() or not session.get(Role, (int(role_id))):
        print('Invalid Role ID')
        return
    
    new_audition = Audition(actor=actor, location=location, phone_no=int(phone_no), hired=False, role_id=role_id)
    session.add(new_audition)
    session.commit()
    print(f"Audition for {actor} at {location} added successfully!")

def view_roles():
    """Function to list all available roles"""
    roles = session.query(Role).all()
    if roles:
        print("\nAvailable Roles:")
        for role in roles:
            print(f"{role.id} | Character: {role.character_name}")
    else:
        print("No roles found!")

def view_auditions():
    """Function to list all auditions"""
    auditions = session.query(Audition).all()
    if auditions:
        print("\nAvailable Auditions:")
        for audition in auditions:
            role = session.query(Role).filter_by(id=audition.role_id).first()
            role_name = role.character_name if role else "Unknown Role"
            status = "Hired" if audition.hired else "Not Hired"
            print(f"{audition.id} | Actor: {audition.actor} | Location: {audition.location} | Role: {role_name} | {status}")
    else:
        print("No auditions found!")

def hire_actor():
    """Function to hire an actor for a role"""
    view_auditions()
    audition_id = input("\nEnter the ID of the audition to hire the actor: ")
    audition = session.query(Audition).filter_by(id=int(audition_id)).first()

    if audition:
        audition.hired = True
        session.commit()
        print(f"{audition.actor} has been hired for their role!")
    else:
        print("Audition ID not found!")

def main():
    """Main CLI function"""
    while True:
        print("\nChoose an Option:")
        print("1. Add Role")
        print("2. Add Audition")
        print("3. View Roles")
        print("4. View Auditions")
        print("5.  Hire an Actor")
        print("6. Exit")
        
        choice = input("\nEnter your choice: ")

        if choice == "1":
            add_role()

            # while True:
            #     add_audition(role_id)
            #     more_auditions = input("Add another audition for this role? (yes/no): ").strip().lower()
            #     if more_auditions != "yes":
            #         break

        elif choice == "2":
            add_audition()
            # roles = session.query(Role).all()
            # if not roles:
            #     print("❌ No roles found! Add a role first.")
            #     continue
            
            # view_roles()
            # role_id = input("\nEnter the role ID for the audition: ")
            # add_audition(int(role_id))

        elif choice == "3":
            view_roles()

        elif choice == "4":
            view_auditions()

        elif choice == "5":
            hire_actor()

        elif choice == "6":
            print("Exiting program. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
