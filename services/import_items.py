from db import init_db
from services.bootstrap_service import bootstrap_reference_data


def main():
    init_db()
    stats = bootstrap_reference_data(
        verbose=True
    )
    print(f"Drugs Imported: {stats['drugs']}")
    print(f"Medical Supplies Imported: {stats['medical_items']}")
    print(f"Total Imported: {stats['drugs'] + stats['medical_items']}")


if __name__ == "__main__":
    main()
