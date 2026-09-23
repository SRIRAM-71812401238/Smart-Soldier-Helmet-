# RFID Authentication Module

# Authorized RFID cards
AUTHORIZED_RFID = {
    "A1B2C3D4": "Soldier_001",
    "B2C3D4E5": "Soldier_002",
    "C3D4E5F6": "Soldier_003"
}


def authenticate_rfid(rfid_id):

    if rfid_id in AUTHORIZED_RFID:
        soldier = AUTHORIZED_RFID[rfid_id]

        print("\n✓ AUTHENTICATION SUCCESSFUL")
        print("✓ Soldier:", soldier)
        print("✓ Helmet Activated")

        return True, soldier

    else:
        print("\n✗ AUTHENTICATION FAILED")
        print("✗ Unauthorized RFID")
        print("✗ Helmet Locked")

        return False, None


# Test RFID
rfid_id = input("Scan RFID card: ")

authenticate_rfid(rfid_id)