"""Basic usage example for the Signal Messenger Python API."""

import asyncio
import logging
import os

from dotenv import load_dotenv

from signal_messenger import SignalClient
from signal_messenger.exceptions import SignalAPIError

# Load environment variables from .env file
load_dotenv()


async def main():
    """Run the example."""
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    # Get API URL from environment variable or use default
    api_url = os.getenv("SIGNAL_API_URL", "http://localhost:9922")

    # Create a client
    async with SignalClient(api_url) as client:
        # Initialize modules
        await client._init_modules()

        # General Module Examples
        print("\n=== General Module Examples ===")

        # Get API information
        about = await client.get_about()
        print(f"API Version: {about.version}")
        print(f"API Build: {about.build}")
        print(f"API Mode: {about.mode}")
        print(f"API Versions: {', '.join(about.versions)}")
        print(f"API Capabilities: {about.capabilities}")

        # Get API configuration
        config = await client.get_configuration()
        print(f"Logging level: {config.logging.level}")

        # Perform a health check
        health = await client.health_check()
        print(f"Health check: {health}")

        # Get environment variables
        phone_number = os.getenv("SIGNAL_PHONE_NUMBER")
        device_name = os.getenv("SIGNAL_DEVICE_NAME", "My Device")
        verification_token = os.getenv("SIGNAL_VERIFICATION_TOKEN")

        # Ask the user which module to use
        print("\nWhich module would you like to use?")
        print("1. Devices")
        print("2. Accounts")
        print("3. Skip module operations")

        module_choice = input("\nEnter your choice (1-3): ")

        if module_choice == "1":
            # Devices Module Examples
            print("\n=== Devices Module Examples ===")

            # Ask the user which operation to perform
            print("\nWhich operation would you like to perform?")
            print("1. Get QR code link for device linking")
            print("2. Get linked devices")
            print("3. Link a new device")
            print("4. Register a device")
            print("5. Verify a device")
            print("6. Skip device operations")

            choice = input("\nEnter your choice (1-6): ")

            if choice == "1":
                # Get QR code link for device linking
                print("\nGetting QR code link for device linking...")
                try:
                    qr_code = await client.get_qr_code_link(device_name)
                    print(f"QR Code Link: {qr_code}")
                except Exception as e:
                    print(f"Error getting QR code link: {e}")

            elif choice == "2" and phone_number:
                # Get linked devices
                print("\nGetting linked devices...")
                try:
                    devices = await client.get_linked_devices(phone_number)
                    print(f"Linked Devices: {devices}")
                except Exception as e:
                    print(f"Error getting linked devices: {e}")

            elif choice == "3" and phone_number and device_name:
                # Link a new device
                print("\nLinking a new device...")
                try:
                    result = await client.link_device(phone_number, device_name)
                    print(f"Link Device Result: {result}")
                except Exception as e:
                    print(f"Error linking device: {e}")

            elif choice == "4" and phone_number:
                # Register a device
                print("\nRegistering a device...")
                try:
                    result = await client.register_device(phone_number)
                    print(f"Register Device Result: {result}")
                except Exception as e:
                    print(f"Error registering device: {e}")

            elif choice == "5" and phone_number and verification_token:
                # Verify a device
                print("\nVerifying a device...")
                try:
                    result = await client.verify_device(
                        phone_number, verification_token
                    )
                    print(f"Verify Device Result: {result}")
                except Exception as e:
                    print(f"Error verifying device: {e}")

            elif choice == "6":
                print("\nSkipping device operations.")

            else:
                print("\nInvalid choice or missing required environment variables.")

        elif module_choice == "2":
            # Accounts Module Examples
            print("\n=== Accounts Module Examples ===")

            # Ask the user which operation to perform
            print("\nWhich operation would you like to perform?")
            print("1. Register an account")
            print("2. Verify an account")
            print("3. Get account details")
            print("4. Update an account")
            print("5. Set account PIN")
            print("6. Remove account PIN")
            print("7. Delete an account")
            print("8. Skip account operations")

            choice = input("\nEnter your choice (1-8): ")

            if choice == "1" and phone_number:
                # Register an account
                print("\nRegistering an account...")
                try:
                    result = await client.register_account(phone_number)
                    print(f"Register Account Result: {result}")
                except Exception as e:
                    print(f"Error registering account: {e}")

            elif choice == "2" and phone_number and verification_token:
                # Verify an account
                print("\nVerifying an account...")
                try:
                    result = await client.verify_account(
                        phone_number, verification_token
                    )
                    print(f"Verify Account Result: {result}")
                except Exception as e:
                    print(f"Error verifying account: {e}")

            elif choice == "3" and phone_number:
                # Get account details
                print("\nGetting account details...")
                try:
                    result = await client.get_account_details(phone_number)
                    print(f"Account Details: {result}")
                except Exception as e:
                    print(f"Error getting account details: {e}")

            elif choice == "4" and phone_number:
                # Update an account
                print("\nUpdating an account...")
                try:
                    registration_id = input(
                        "Enter registration ID (leave empty to skip): "
                    )
                    pni_registration_id = input(
                        "Enter PNI registration ID (leave empty to skip): "
                    )

                    kwargs = {}
                    if registration_id:
                        kwargs["registration_id"] = int(registration_id)
                    if pni_registration_id:
                        kwargs["pni_registration_id"] = int(pni_registration_id)

                    result = await client.update_account(phone_number, **kwargs)
                    print(f"Update Account Result: {result}")
                except Exception as e:
                    print(f"Error updating account: {e}")

            elif choice == "5" and phone_number:
                # Set account PIN
                print("\nSetting account PIN...")
                try:
                    pin = input("Enter PIN: ")
                    result = await client.set_pin(phone_number, pin)
                    print(f"Set PIN Result: {result}")
                except Exception as e:
                    print(f"Error setting PIN: {e}")

            elif choice == "6" and phone_number:
                # Remove account PIN
                print("\nRemoving account PIN...")
                try:
                    result = await client.remove_pin(phone_number)
                    print(f"Remove PIN Result: {result}")
                except Exception as e:
                    print(f"Error removing PIN: {e}")

            elif choice == "7" and phone_number:
                # Delete an account
                print("\nDeleting an account...")
                try:
                    confirm = input(
                        "Are you sure you want to delete this account? (y/n): "
                    )
                    if confirm.lower() == "y":
                        result = await client.delete_account(phone_number)
                        print(f"Delete Account Result: {result}")
                    else:
                        print("Account deletion cancelled.")
                except Exception as e:
                    print(f"Error deleting account: {e}")

            elif choice == "8":
                print("\nSkipping account operations.")

            else:
                print("\nInvalid choice or missing required environment variables.")

        elif module_choice == "3":
            print("\nSkipping module operations.")

        else:
            print("\nInvalid choice.")


if __name__ == "__main__":
    asyncio.run(main())
